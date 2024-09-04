from afex_logger.http_agent import HttpAgent


class AppLogService:

    def __init__(self):
        from afex_logger.util import LogTypes, LogUtil

        self.path_mappings = {
            LogTypes.activities: "activities",
            LogTypes.errors: "errors",
            LogTypes.process: "process",
            LogTypes.requests: "requests",
        }

        util = LogUtil()
        config_provider = util.get_config_provider()

        api_key = config_provider.get_api_key()
        base_url = config_provider.get_base_url()

        self.https_agent = HttpAgent(
            api_key, base_url + "/api/v1/logs/"
        )

    def fetch_logs(self, log_type, filter_params):
        return self.https_agent.make_get_request(self.path_mappings[log_type], filter_params)

    def send_logs(self, log_type, payload):
        return self.https_agent.make_post_request(self.path_mappings[log_type], payload)
