import json

import boto3

from afex_logger.util import LogUtil


class SsmService:

    __secrets_bucket = {}

    def __init__(self, region_name, access_key=None, secret_key=None, session_token=None):
        self.log_util = LogUtil()
        config_provider = self.log_util.get_config_provider()

        credentials = dict(
            service_name='secretsmanager',
            region_name=region_name,
        )

        if config_provider.is_test_mode():
            credentials['aws_access_key_id'] = access_key
            credentials['aws_secret_access_key'] = secret_key
            credentials['aws_session_token'] = session_token

        session = boto3.session.Session()
        self.client = session.client(**credentials)

    def __retrieve_ssm_secrets(self, secret_name, uses_cache=True):
        if uses_cache:
            secrets = self.__secrets_bucket.get(secret_name)
            if secrets:
                return secrets, None

        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )
        except Exception as e:
            self.log_util.debug_print("Exception", str(e))
            return None, str(e)

        secrets_str = get_secret_value_response.get('SecretString')
        secrets = json.loads(secrets_str)
        self.__secrets_bucket[secret_name] = secrets

        return secrets, None

    def get_secret_value(self, secret_name, key_name, uses_cache=True):
        secrets, error = self.__retrieve_ssm_secrets(secret_name, uses_cache=uses_cache)
        if error:
            return None, error

        return secrets.get(key_name), None
