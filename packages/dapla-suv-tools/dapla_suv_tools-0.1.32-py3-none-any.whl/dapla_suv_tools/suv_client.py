from typing import Callable, Optional
from dapla_suv_tools._internals.util.help_helper import HelpAssistant
from dapla_suv_tools._internals.util import constants


class SuvClient:
    suppress_exceptions: bool
    operations_log: list
    help_assistant: HelpAssistant

    from dapla_suv_tools._internals.client_apis.skjema_api import (
        get_skjema_by_id,
        get_skjema_by_ra_nummer,
        create_skjema,
        delete_skjema,
    )

    from dapla_suv_tools._internals.client_apis.periode_api import (
        get_periode_by_id,
        get_perioder_by_skjema_id,
        create_periode,
        delete_periode,
    )

    from dapla_suv_tools._internals.client_apis.instans_api import (
        get_instance,
    )

    from dapla_suv_tools._internals.client_apis.instantiator_api import (
        resend_instances,
    )

    from dapla_suv_tools._internals.client_apis.innkvittering_api import (
        resend_receipts,
    )

    def __init__(self, suppress_exceptions: bool = False):
        self.suppress_exceptions = suppress_exceptions
        self.operations_log = []
        self._build_help_cache()

    def logs(self, threshold: str | None = None, results: int = 0) -> list:
        if not threshold or threshold not in constants.LOG_LEVELS:
            threshold = constants.LOG_INFO

        log = self._filter_logs(threshold=threshold)

        if results > 0:
            return log[-results:]

        return log

    def help(self, function: Optional[Callable] = None):
        if function is None:
            return self.__doc__
        doc = self.help_assistant.get_function_help_entry(function.__name__)

        if doc is not None:
            print(doc)

        print(f"No help entry for '{function.__name__}' exists.")

    def _build_help_cache(self):
        self.help_assistant = HelpAssistant()
        self.help_assistant.register_functions(
            [
                self.get_skjema_by_id,
                self.get_skjema_by_ra_nummer,
                self.create_skjema,
                self.delete_skjema,
                self.get_periode_by_id,
                self.get_perioder_by_skjema_id,
                self.create_periode,
                self.delete_periode,
            ]
        )

    def flush_logs(self):
        self.operations_log = []

    def _filter_logs(self, threshold: str) -> list:
        limit = constants.LOG_LEVELS.index(threshold)

        filtered = []

        for log_entry in self.operations_log:
            logs = log_entry["logs"]
            if len(logs) == 0:
                continue
            for entry in logs:
                if constants.LOG_LEVELS.index(entry["level"]) < limit:
                    continue
                filtered.append(entry)

        return sorted(filtered, key=lambda x: x["time"])
