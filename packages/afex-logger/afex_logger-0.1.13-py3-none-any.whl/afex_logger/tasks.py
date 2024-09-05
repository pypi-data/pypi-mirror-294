import json

from celery import shared_task

from afex_logger.log_service import AppLogService


@shared_task
def submit_log_data(log_type, log_data: str):
    from afex_logger.util import LogUtil

    log_util = LogUtil()
    config_provider = log_util.get_config_provider()

    if config_provider.is_test_mode():
        log_util.debug_print(log_type, "|", log_data)

    try:
        data = json.loads(log_data)
        AppLogService().send_logs(log_type, data)
    except Exception as e:
        log_util.debug_print(e)

