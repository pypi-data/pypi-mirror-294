from functools import cached_property
from typing import Union

from ._api import (
    CatalogAPI,
    CustomAPI,
    LicenseManagerAPI,
    LogisticsAPI,
    MasterDataAPI,
    OrdersAPI,
    PaymentsGatewayAPI,
)
from ._config import Config  # type: ignore[attr-defined]
from ._logging import get_logger
from ._sentinels import UNDEFINED, UndefinedSentinel
from ._types import IterableType


class VTEX:
    """
    Entrypoint for the VTEX SDK.
    From this class you can access all the APIs on VTEX
    """

    def __init__(
        self,
        account_name: Union[str, UndefinedSentinel] = UNDEFINED,
        app_key: Union[str, UndefinedSentinel] = UNDEFINED,
        app_token: Union[str, UndefinedSentinel] = UNDEFINED,
        timeout: Union[float, None, UndefinedSentinel] = UNDEFINED,
        retry_attempts: Union[int, UndefinedSentinel] = UNDEFINED,
        retry_backoff_min: Union[float, UndefinedSentinel] = UNDEFINED,
        retry_backoff_max: Union[float, UndefinedSentinel] = UNDEFINED,
        retry_backoff_exponential: Union[bool, float, UndefinedSentinel] = UNDEFINED,
        retry_statuses: Union[IterableType[int], UndefinedSentinel] = UNDEFINED,
        retry_logs: Union[bool, UndefinedSentinel] = UNDEFINED,
        raise_for_status: Union[bool, UndefinedSentinel] = UNDEFINED,
    ) -> None:
        self._logger = get_logger("client")
        self._config = Config(
            account_name=account_name,
            app_key=app_key,
            app_token=app_token,
            timeout=timeout,
            retry_attempts=retry_attempts,
            retry_backoff_min=retry_backoff_min,
            retry_backoff_max=retry_backoff_max,
            retry_backoff_exponential=retry_backoff_exponential,
            retry_statuses=retry_statuses,
            retry_logs=retry_logs,
            raise_for_status=raise_for_status,
        )

    @cached_property
    def custom(self) -> CustomAPI:
        return CustomAPI(config=self._config, logger=self._logger)

    @cached_property
    def catalog(self) -> CatalogAPI:
        return CatalogAPI(config=self._config, logger=self._logger)

    @cached_property
    def license_manager(self) -> LicenseManagerAPI:
        return LicenseManagerAPI(config=self._config, logger=self._logger)

    @cached_property
    def logistics(self) -> LogisticsAPI:
        return LogisticsAPI(config=self._config, logger=self._logger)

    @cached_property
    def master_data(self) -> MasterDataAPI:
        return MasterDataAPI(config=self._config, logger=self._logger)

    @cached_property
    def orders(self) -> OrdersAPI:
        return OrdersAPI(config=self._config, logger=self._logger)

    @cached_property
    def payments_gateway(self) -> PaymentsGatewayAPI:
        return PaymentsGatewayAPI(config=self._config, logger=self._logger)
