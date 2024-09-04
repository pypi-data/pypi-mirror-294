import decimal
import json
from abc import abstractmethod
from datetime import datetime, date
from pydoc import locate
from typing import List
from uuid import UUID

from django.conf import settings
from django.db.models import TextChoices
from django.utils import timezone

from afex_logger.log_service import AppLogService
from afex_logger.tasks import submit_log_data


class LogTypes(TextChoices):
    requests = "requests"
    process = "process"
    errors = "errors"
    activities = "activities"


class Environment(TextChoices):
    test = "Test"
    prod = "Prod"


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, UUID):
            return str(o)
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, date):
            return o.isoformat()
        elif hasattr(o, '__dict__'):
            return o.__dict__.get('name', '')
        return super(DecimalEncoder, self).default(o)


class ConfigProvider:
    """
    Configuration Provider for logger
    """

    __log_base_urls = {
        Environment.test: "https://log-server.afex.dev",
        Environment.prod: "https://log-server.africaexchange.com",
    }

    __defaults = {
        "body_data": ['password', 'csrfmiddlewaretoken'],
        "content_types": [],
        "request_methods": ['HEAD', 'OPTIONS', 'TRACE'],
        "path_prefixes": ["/logs/", 'media/', "static/"],
        "api_prefixes": "/api/",
    }

    def __init__(self, env: Environment):
        self.env = env

    @abstractmethod
    def get_api_key(self):
        raise NotImplementedError(
            "Please implement this method, return the API Key as provided by SSM for Log Server"
        )

    def get_base_url(self):
        raise self.__log_base_urls[self.env]

    def is_test_mode(self) -> bool:
        return self.env == Environment.test

    def get_excluded_path_patterns(self):
        return self.__defaults["path_prefixes"]

    def get_excluded_request_method(self) -> List[str]:
        return self.__defaults["request_methods"]

    def get_rest_content_types(self) -> List[str]:
        return self.__defaults['content_types']

    def get_excluded_data_fields(self):
        return self.__defaults['body_data']

    def get_api_path_prefix(self):
        return self.__defaults['api_prefixes']


class LogUtil:

    @classmethod
    def submit_error_log(cls, data):
        cls.__submit_log(LogTypes.errors, data)

    @classmethod
    def submit_activity_log(cls, data):
        cls.__submit_log(LogTypes.activities, data)

    @classmethod
    def submit_process_log(cls, data):
        cls.__submit_log(LogTypes.process, data)

    @classmethod
    def submit_requests_log(cls, data):
        cls.__submit_log(LogTypes.requests, data)

    @classmethod
    def __submit_log(cls, log_type, data):
        task_id = submit_log_data.delay(log_type, json.dumps(data, cls=DecimalEncoder))
        config_util = cls.get_config_provider()
        if config_util.is_test_mode():
            cls.debug_print("Task:", task_id, log_type, data)

    @classmethod
    def fetch_error_logs(cls, params):
        return AppLogService().fetch_logs(LogTypes.errors, params)

    @classmethod
    def fetch_activity_logs(cls, params):
        return AppLogService().fetch_logs(LogTypes.activities, params)

    @classmethod
    def fetch_process_logs(cls, params):
        return AppLogService().fetch_logs(LogTypes.process, params)

    @classmethod
    def fetch_request_logs(cls, params):
        return AppLogService().fetch_logs(LogTypes.requests, params)

    @classmethod
    def debug_print(cls, *args):
        print("Log Service::[{}]".format(timezone.now()), *args)

    @staticmethod
    def get_config_provider() -> ConfigProvider:
        try:
            app_config_provider_loc = getattr(settings, "LOG_CONFIG_PROVIDER")
            env = getattr(settings, "LOG_CONFIG_ENV") or Environment.test
            if isinstance(app_config_provider_loc, str):
                app_config_provider = locate(app_config_provider_loc)
            else:
                app_config_provider = app_config_provider_loc

            return app_config_provider(env)
        except Exception as _:
            raise NotImplementedError(
                "Ensure you add 'LOG_CONFIG_PROVIDER' to your django settings. "
                "This class must  extend ConfigProvider"
            )
