from datetime import date
import json
import os

from ssb_altinn3_util.models.skjemadata.skjemadata_request_models import (
    SkjemaRequestModel,
)

from dapla_suv_tools._internals.integration.api_client import SuvApiClient
from dapla_suv_tools._internals.integration import user_tools
from dapla_suv_tools._internals.util.operation_result import OperationResult
from dapla_suv_tools._internals.util.suv_operation_context import SuvOperationContext
from dapla_suv_tools._internals.util import constants
from dapla_suv_tools._internals.util.validators import (
    skjema_id_validator,
    ra_nummer_validator,
)
from dapla_suv_tools._internals.util.decorators import result_to_dict
from dapla_suv_tools.pagination import PaginationInfo


END_USER_API_BASE_URL = os.getenv("SUV_END_USER_API_URL")

client = SuvApiClient(base_url=END_USER_API_BASE_URL)


@result_to_dict
@SuvOperationContext(validator=skjema_id_validator)
def get_skjema_by_id(
    self, *, skjema_id: int, context: SuvOperationContext = None
) -> OperationResult:
    """
    Gets a 'skjema' based on it's skjema_id.
    :param skjema_id: The skjema's id
    :param context: Operation context.  This is injected by the underlying pipeline.  Adding a custom context will result in an error.
    :return: a json object containing skjema data.
    """
    try:
        content: str = client.get(
            path=f"{constants.SKJEMA_PATH}/{skjema_id}", context=context
        )
        content_json = json.loads(content)
        # context.log(constants.LOG_INFO, "get_skjema_by_id", f"Fetched 'skjema' with id '{skjema_id}'")
        context.log(message="Fetched 'skjema' with id '{skjema_id}'")
        return OperationResult(value=content_json, log=context.logs())

    except Exception as e:
        context.set_error(f"Failed to fetch for id {skjema_id}", e)
        return OperationResult(
            success=False, value=context.errors(), log=context.logs()
        )


def _get_non_paged_result(
    path: str, max_results: int, filters: str, context: SuvOperationContext
) -> str:
    if max_results > 0:
        return client.post(
            path=f"{path}?size={max_results}&order_by=versjon&asc=false",
            body_json=filters,
            context=context,
        )

    items = []
    total = 1
    page = 1

    while len(items) < total:
        response = client.post(
            path=f"{path}?page={page}&size=100&order_by=versjon&asc=false",
            body_json=filters,
            context=context,
        )

        response_json = json.loads(response)
        total = int(response_json["total"])
        items.extend(response_json["results"])
        page += 1

    return json.dumps({"results": items})


def _get_paged_result(
    path: str, paging: PaginationInfo, filters: str, context: SuvOperationContext
) -> str:
    return client.post(
        path=f"{path}?page={paging.page}&size={paging.size}&order_by=versjon&asc=false",
        body_json=filters,
        context=context,
    )


@result_to_dict
@SuvOperationContext(validator=ra_nummer_validator)
def get_skjema_by_ra_nummer(
    self,
    *,
    ra_nummer: str,
    max_results: int = 0,
    latest_only: bool = False,
    pagination_info: PaginationInfo = None,
    context: SuvOperationContext = None,
) -> OperationResult:
    """
    Attempts to get all skjema with the supplied RA-number.

    :param ra_nummer: Skjema's RA-number
    :param max_results: Maximum number of results int the result set.  A value of 0 will get ALL results.
    :param latest_only: Only return the newest entry
    :param pagination_info: An object holding pagination metadata
    :param context: Operation context.  This is injected by the underlying pipeline.  Adding a custom context will result in an error.

    :return: A list of skjema json objects matching the RA-number
    """
    try:
        filters = json.dumps({"ra_nummer": ra_nummer})
        content: str
        if pagination_info is None:
            content = _get_non_paged_result(
                path="/skjemadata/skjema-paged",
                max_results=max_results,
                filters=filters,
                context=context,
            )
        else:
            content = _get_paged_result(
                path="/skjemadata/skjema-paged",
                paging=pagination_info,
                filters=filters,
                context=context,
            )

        result: dict = json.loads(content)

        if latest_only:
            # context.log(constants.LOG_INFO, "get_skjema_by_ra_number", f"Fetched latest version of 'skjema' with RA-number '{ra_nummer}'")
            context.log(
                message=f"Fetched latest version of 'skjema' with RA-number '{ra_nummer}'"
            )
            return OperationResult(value=result["results"][0], log=context.logs())

        # context.log(constants.LOG_INFO, "get_skjema_by_ra_number", f"Fetched all 'skjema' with RA-number '{ra_nummer}'")
        context.log(message="Fetched all 'skjema' with RA-number '{ra_nummer}'")
        return OperationResult(value=result["results"], log=context.logs())

    except Exception as e:
        context.set_error(f"Failed to fetch for ra_nummer '{ra_nummer}'.", e)
        return OperationResult(
            success=False, value=context.errors(), log=context.logs()
        )


@result_to_dict
@SuvOperationContext(validator=ra_nummer_validator)
def create_skjema(
    self,
    *,
    ra_nummer: str,
    versjon: int,
    undersokelse_nr: str,
    gyldig_fra: date,
    datamodell: str | None = None,
    beskrivelse: str | None = None,
    navn_nb: str | None = None,
    navn_nn: str | None = None,
    navn_en: str | None = None,
    infoside: str | None = None,
    eier: str | None = None,
    kun_sky: bool = False,
    gyldig_til: date | None = None,
    context: SuvOperationContext = None,
) -> OperationResult:
    """
    Creates a new version of metadata for the given skjema, based upon the supplied metadata.
    :param self:
    :param ra_nummer:
    :param versjon:
    :param undersokelse_nr:
    :param gyldig_fra:
    :param datamodell:
    :param beskrivelse:
    :param navn_nb:
    :param navn_nn:
    :param navn_en:
    :param infoside:
    :param eier:
    :param kun_sky:
    :param gyldig_til:
    :param context: Operation context.  This is injected by the underlying pipeline.  Adding a custom context will result in an error.
    :return:
    """

    user: str = user_tools.get_current_user(context)

    model = SkjemaRequestModel(
        ra_nummer=ra_nummer,
        versjon=versjon,
        undersokelse_nr=undersokelse_nr,
        gyldig_fra=gyldig_fra,
        gyldig_til=gyldig_til,
        endret_av=user,
        datamodell=datamodell,
        beskrivelse=beskrivelse,
        navn_nb=navn_nb,
        navn_nn=navn_nn,
        navn_en=navn_en,
        infoside=infoside,
        eier=eier,
        kun_sky="J" if kun_sky else "N",
    )

    try:
        body = model.model_dump_json()
        content: str = client.post(
            path=constants.SKJEMA_PATH, body_json=body, context=context
        )
        new_id = json.loads(content)["id"]
        # context.log(constants.LOG_INFO, "create_skjema", f"Created 'skjema' with id '{new_id}'")
        context.log(message="Created 'skjema' with id '{new_id}'")
        return OperationResult(value={"id": new_id}, log=context.logs())
    except Exception as e:
        context.set_error(
            f"Failed to create for ra_number '{ra_nummer}' - version '{versjon}'", e
        )
        return OperationResult(
            success=False, value=context.errors(), log=context.logs()
        )


@result_to_dict
@SuvOperationContext(validator=skjema_id_validator)
def delete_skjema(
    self, *, skjema_id: int, context: SuvOperationContext = None
) -> OperationResult:
    """
    Attempts to delete the skjema with the supplied id.

    :param skjema_id:
    :param context: Operation context.  This is injected by the underlying pipeline.  Adding a custom context will result in an error.

    :return: A json object containing the operation result.
    """
    try:
        content: str = client.delete(
            path=f"{constants.SKJEMA_PATH}/{skjema_id}", context=context
        )
        # context.log(constants.LOG_INFO, "delete_skjema", f"Deleted 'skjema' with id '{skjema_id}'")
        context.log(message="Deleted 'skjema' with id '{skjema_id}'")
        return OperationResult(value=content, log=context.logs())
    except Exception as e:
        context.set_error(f"Failed to delete skjema with id '{skjema_id}'.", e)
        return OperationResult(
            success=False, value=context.errors(), log=context.logs()
        )
