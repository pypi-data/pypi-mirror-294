from dapla_suv_tools._internals.util import constants


class OperationResult:
    result_json: dict
    result: str
    operation_log: dict

    def __init__(self, value: dict | str, success: bool = True,  log: dict = None):
        if success and isinstance(value, str):
            value = {"result": value}
        self.result = constants.OPERATION_OK if success else constants.OPERATION_ERROR
        self.result_json = value
        self.operation_log = {} if log is None else log

    def process(self, caller) -> dict:
        if hasattr(caller, "operations_log"):
            caller.operations_log.append(self.operation_log)
        if self.result == constants.OPERATION_OK:
            return self.result_json

        if self.result == constants.OPERATION_ERROR:
            if hasattr(caller, "suppress_exceptions") and caller.suppress_exceptions:
                return self.result_json
            errors = self.result_json["errors"]
            raise errors[len(errors) - 1]["exception"]

        return {"result": "Undefined result.  This shouldn't happen."}
