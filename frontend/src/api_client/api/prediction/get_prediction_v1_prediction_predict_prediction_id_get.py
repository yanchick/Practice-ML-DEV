from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.prediction_scheme import PredictionScheme
from ...types import Response


def _get_kwargs(
    prediction_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/prediction/predict/{prediction_id}",
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | PredictionScheme | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = PredictionScheme.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = cast(Any, None)
        return response_422
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | PredictionScheme]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    prediction_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Any | PredictionScheme]:
    """Get Prediction

    Args:
        prediction_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and
        Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PredictionScheme]]
    """

    kwargs = _get_kwargs(
        prediction_id=prediction_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    prediction_id: int,
    *,
    client: AuthenticatedClient,
) -> Any | PredictionScheme | None:
    """Get Prediction

    Args:
        prediction_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and
        Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PredictionScheme]
    """

    return sync_detailed(
        prediction_id=prediction_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    prediction_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Any | PredictionScheme]:
    """Get Prediction

    Args:
        prediction_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and
        Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PredictionScheme]]
    """

    kwargs = _get_kwargs(
        prediction_id=prediction_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    prediction_id: int,
    *,
    client: AuthenticatedClient,
) -> Any | PredictionScheme | None:
    """Get Prediction

    Args:
        prediction_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and
        Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PredictionScheme]
    """

    return (
        await asyncio_detailed(
            prediction_id=prediction_id,
            client=client,
        )
    ).parsed
