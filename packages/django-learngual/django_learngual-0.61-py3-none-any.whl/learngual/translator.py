import importlib
import json
import os
from collections import defaultdict
from logging import getLogger

import gspread
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from google.oauth2.service_account import Credentials
from rest_framework.serializers import ValidationError

from .enums import LanguageCodeType

logger = getLogger(__file__)


def load_callable(path: str) -> object | None:
    paths = path.split(".")
    modules = importlib.import_module(".".join(paths[:-1]))
    result = getattr(modules, paths[-1], None)
    if not result:
        logger.warning("Module does no exists. path: %s", path)
    return result


class Translator:
    key = "Translator-data"
    use_cache_key = "Translator-user-cache"

    refresh_duration = timezone.timedelta(minutes=1).total_seconds()

    def __init__(
        self,
        sheet_id=None,
        sheet_name=None,
        celery_app_path: str | None = None,
        target_language: str = "EN",
    ):
        self.sheet_id = (
            sheet_id
            or getattr(settings, "LEARNGUAL_TRANSLATE_SHEET_ID", None)
            or os.getenv("LEARNGUAL_TRANSLATE_SHEET_ID")
        )
        self.sheet_name = (
            sheet_name
            or getattr(settings, "LEARNGUAL_TRANSLATE_SHEET_NAME", None)
            or os.getenv("LEARNGUAL_TRANSLATE_SHEET_NAME")
        )

        self.celery_app_path = (
            celery_app_path
            or getattr(settings, "LEARNGUAL_CELERY_APP_PATH", None)
            or os.getenv("LEARNGUAL_CELERY_APP_PATH")
        )

        assert (
            self.sheet_id
        ), "`LEARNGUAL_TRANSLATE_SHEET_ID` must be set in enviroment variable or Django setting"
        assert (
            self.sheet_name
        ), "`LEARNGUAL_TRANSLATE_SHEET_NAME` must be set in enviroment variable or Django setting"

        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = json.loads(
            getattr(settings, "LEARNGUAL_GOOGLE_BOT_GRED", None)
            or os.getenv("LEARNGUAL_GOOGLE_BOT_GRED")
            or "{}"
        )
        credentials = Credentials.from_service_account_info(creds, scopes=scopes)
        self.gc = gspread.authorize(credentials)

        self.target_language = target_language

    @property
    def translations(self):
        return self.load_translations()

    @property
    def headers(self):
        if data := cache.get(self.key):
            return [x.upper() for x in data.get("headers", [])]

        return []

    @property
    def celery_app(self):
        return load_callable(self.celery_app_path)

    def remove_duplicate_rows(self, column_name="en"):
        # Authenticate and open the Google Sheet

        sheet = self.gc.open_by_key(self.sheet_id)
        worksheet = sheet.worksheet(self.sheet_name)

        # Get all data from the sheet
        data = worksheet.get_all_values()

        # Extract header and data rows
        header = data[0]
        rows = data[1:]

        # Find the index of the target column
        try:
            if column_name.lower() in header:
                column_index = header.index(column_name.lower())
            elif column_name.upper() in header:
                column_index = header.index(column_name.upper())
            else:
                column_index = header.index(column_name)
        except ValueError:
            raise ValueError(f"Column '{column_name}' not found in the sheet.")

        # Use a dictionary to track the last occurrence of each value in the target column
        last_occurrence = defaultdict(int)

        # Iterate through the rows to find the last occurrence of each value
        for i, row in enumerate(rows):
            value = row[column_index]
            last_occurrence[value] = i + 1  # +1 because of header

        # Build a list of row indices to keep
        rows_to_keep = set(last_occurrence.values())

        # Delete rows that are not in the rows_to_keep set
        rows_to_delete = [
            i + 2 for i in range(len(rows)) if (i + 1) not in rows_to_keep
        ]
        rows_to_delete.reverse()  # Delete from bottom to top to avoid shifting issues

        for row_index in rows_to_delete:
            worksheet.delete_rows(row_index)

        logger.info(
            f"Removed {len(rows_to_delete)} duplicate rows from column '{column_name}'."
        )

    def force_load_translations(self):
        logger.info("Initiate refresh tranlsations")
        sheet = self.gc.open_by_key(self.sheet_id)
        worksheet = sheet.worksheet(self.sheet_name)
        data = worksheet.get_all_values()

        headers = [x.upper() for x in data[0]]
        translations = {}

        for row in data[1:]:
            en_value = row[0].strip()
            translations[en_value] = {
                headers[i]: row[i] for i in range(1, len(headers))
            }
        cache.set(self.key, {"headers": headers, "translations": translations})

        cache.set(self.use_cache_key, True, timeout=int(self.refresh_duration))
        return translations

    def load_translations(self):
        if not cache.get(self.use_cache_key):
            logger.info("Trgger load refresh translations")
            self.celery_app.send_task(
                "iam.accounts.translate_load_translations",
                routing_key="iam.accounts.translate_load_translations",
            )

        if data := cache.get(self.key):
            return data.get("translations")
        try:
            return self.force_load_translations()
        except gspread.exceptions.APIError:
            return {}

    def get_language_code(self, language: str) -> str:
        languages = {
            key.strip().upper(): value.strip().upper()
            for key, value in LanguageCodeType.dict_name_key().items()
        }
        if not language:
            language = "EN"
        language = language.strip().upper()
        return languages.get(language, language)

    def log_microcopy(self, text: str):
        if text not in self.translations:
            translations = self.translations
            headers = self.headers
            translations[text] = {headers[i]: "" for i in range(1, len(headers))}
            cache.set(
                self.key,
                {"headers": headers, "translations": translations},
            )
            self.celery_app.send_task(
                "iam.accounts.translate_log_microcopy",
                routing_key="iam.accounts.translate_log_microcopy",
                args=(text,),
            )
            logger.info(f"Logged missing microcopy: {text}")

    def force_log_microcopy(self, text: str):
        if text in self.translations:
            return
        logger.info(f"Log microcopy: {text}")

        sheet = self.gc.open_by_key(self.sheet_id)
        worksheet = sheet.worksheet(self.sheet_name)
        data = worksheet.get_all_values()

        translations = {}
        headers = [x.upper() for x in data[0]]

        for row in data[1:]:
            en_value = row[0].strip()
            translations[en_value] = {
                headers[i]: row[i] for i in range(1, len(headers))
            }

        if not translations.get(text):
            # Find the first empty row in the English column
            worksheet.insert_row([text.strip()], index=2)

    def force_add_language_column(self, language: str):
        if self.headers and language not in self.headers:
            sheet = self.gc.open_by_key(self.sheet_id)
            worksheet = sheet.worksheet(self.sheet_name)
            # Add new column with target language header
            col_count = len(worksheet.row_values(1))
            worksheet.update_cell(1, col_count + 1, language.upper())
            logger.info(f"Added new language column: {language}")

    def add_language_column(self, language: str):
        if self.headers and language not in self.headers:
            self.headers.append(language.upper())
            cache.set(
                self.key, {"headers": self.headers, "translations": self.translations}
            )
            self.celery_app.send_task(
                "iam.accounts.translate_add_language_column",
                routing_key="iam.accounts.translate_add_language_column",
                args=(language,),
            )

    def translate(self, text: str, target_language: str):
        target_language = self.get_language_code(target_language)

        if target_language.upper() not in self.headers:
            if not self.headers:
                self.load_translations()
            else:
                self.add_language_column(target_language.upper())
            return text
        stripped_text = text.strip()
        translated_dict = self.translations.get(stripped_text)
        if not translated_dict:
            if translated_dict is None:
                self.log_microcopy(text)
            return stripped_text

        translated_text = translated_dict.get(target_language, text)
        if not translated_text:
            return stripped_text

        return translated_text

    def get_translation(
        self, text, target_language: str | None = None, **kwargs
    ) -> str:
        target_language = target_language or self.target_language
        assert target_language, "target_language is required."
        result = self.translate(text, target_language)
        if kwargs:
            result = self.render(result, **kwargs)

        return result

    def render(self, text: str, **kwargs):
        if not text:
            return text
        try:
            return text.format(**kwargs)
        except KeyError as e:
            raise ValidationError(
                {"detail": f"Imcomplete kwargs for {kwargs} for text {text}"}
            ) from e
