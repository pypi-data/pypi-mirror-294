from datetime import date
import json
import os

from ssb_altinn3_util.models.skjemadata.skjemadata_request_models import (
    PeriodeRequestModel,
)

from dapla_suv_tools._internals.integration.api_client import SuvApiClient
from dapla_suv_tools._internals.integration import user_tools
from dapla_suv_tools._internals.util import constants
from dapla_suv_tools._internals.util.decorators import result_to_dict
from dapla_suv_tools._internals.util.operation_result import OperationResult
from dapla_suv_tools._internals.util.suv_operation_context import SuvOperationContext
from dapla_suv_tools._internals.util.validators import (
    periode_id_validator,
    skjema_id_validator,
)


END_USER_API_BASE_URL = os.getenv("SUV_END_USER_API_URL")

client = SuvApiClient(base_url=END_USER_API_BASE_URL)


@result_to_dict
@SuvOperationContext(validator=periode_id_validator)
def get_periode_by_id(
    self, *, periode_id: int, context: SuvOperationContext = None
) -> OperationResult:
    """

    :param self:
    :param periode_id:
    :param context:
    :return:
    """
    try:
        content: str = client.get(
            path=f"{constants.PERIODE_PATH}/{periode_id}", context=context
        )
        content_json = json.loads(content)
        context.log(message=f"Fetched periode with periode_id '{periode_id}'")

        return OperationResult(value=content_json, log=context.logs())
    except Exception as e:
        context.set_error(f"Failed to fetch for id {periode_id}", e)

        return OperationResult(
            success=False, value=context.errors(), log=context.logs()
        )


@result_to_dict
@SuvOperationContext(validator=skjema_id_validator)
def get_perioder_by_skjema_id(
    self, *, skjema_id: int, context: SuvOperationContext = None
) -> OperationResult:
    try:
        content: str = client.get(
            path=f"{constants.PERIODE_PATH}/skjema/{skjema_id}", context=context
        )

        content_json = json.loads(content)

        context.log(message=f"Fetched perioder for skjema_id '{skjema_id}'")

        return OperationResult(value=content_json, log=context.logs())
    except Exception as e:
        context.set_error(f"Failed to fetch for skjema_id {skjema_id}", e)

        return OperationResult(
            success=False, value=context.errors(), log=context.logs()
        )


@result_to_dict
@SuvOperationContext(validator=skjema_id_validator)
def create_periode(
    self,
    *,
    skjema_id: int,
    periode_type: str | None = None,
    periode_nr: int | None = None,
    periode_aar: int | None = None,
    periode_dato: date | None = None,
    delreg_nr: int | None = None,
    enhet_type: str | None = None,
    vis_oppgavebyrde: str | None = "N",
    vis_brukeropplevelse: str | None = "N",
    har_skjemadata: str | None = "N",
    journalnummer: str | None = None,
    context: SuvOperationContext = None,
) -> OperationResult:
    user = user_tools.get_current_user(context)

    model = PeriodeRequestModel(
        skjema_id=skjema_id,
        endret_av=user,
        periode_type=periode_type,
        periode_nr=periode_nr,
        periode_aar=periode_aar,
        periode_dato=periode_dato,
        delreg_nr=delreg_nr,
        enhet_type=enhet_type,
        vis_oppgavebyrde=vis_oppgavebyrde,
        vis_brukeropplevelse=vis_brukeropplevelse,
        har_skjemadata=har_skjemadata,
        journalnummer=journalnummer,
    )

    try:
        body = model.model_dump_json()
        content: str = client.post(
            path=constants.PERIODE_PATH, body_json=body, context=context
        )
        new_id = json.loads(content)["id"]
        context.log(message="Created 'periode' with id '{new_id}'")
        return OperationResult(value={"id": new_id}, log=context.logs())
    except Exception as e:
        context.set_error(
            f"Failed to create for skjema_id '{skjema_id}' - periode {periode_nr} {periode_type} {periode_nr}",
            e,
        )
        return OperationResult(
            success=False, value=context.errors(), log=context.logs()
        )


@result_to_dict
@SuvOperationContext(validator=periode_id_validator)
def delete_periode(
    self, *, periode_id: int, context: SuvOperationContext = None
) -> OperationResult:
    try:
        content: str = client.delete(
            path=f"{constants.PERIODE_PATH}/{periode_id}", context=context
        )
        context.log(message="Deleted 'periode' with id '{periode_id}'")
        return OperationResult(value=content, log=context.logs())
    except Exception as e:
        context.set_error(f"Failed to delete Periode with id '{periode_id}'.", e)
        return OperationResult(
            success=False, value=context.errors(), log=context.logs()
        )
