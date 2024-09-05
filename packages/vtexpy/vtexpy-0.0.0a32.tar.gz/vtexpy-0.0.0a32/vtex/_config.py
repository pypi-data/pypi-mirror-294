# type: ignore
from os import getenv
from typing import Union

from ._constants import (
    ACCOUNT_NAME_ENV_VAR,
    APP_KEY_ENV_VAR,
    APP_TOKEN_ENV_VAR,
    DEFAULT_RAISE_FOR_STATUS,
    DEFAULT_RETRY_ATTEMPTS,
    DEFAULT_RETRY_BACKOFF_EXPONENTIAL,
    DEFAULT_RETRY_BACKOFF_MAX,
    DEFAULT_RETRY_BACKOFF_MIN,
    DEFAULT_RETRY_LOGS,
    DEFAULT_RETRY_STATUSES,
    DEFAULT_TIMEOUT,
    RAISE_FOR_STATUS_ENV_VAR,
    RETRY_ATTEMPTS_ENV_VAR,
    RETRY_BACKOFF_EXPONENTIAL_ENV_VAR,
    RETRY_BACKOFF_MAX_ENV_VAR,
    RETRY_BACKOFF_MIN_ENV_VAR,
    RETRY_LOGS_ENV_VAR,
    RETRY_STATUSES_ENV_VAR,
    TIMEOUT_ENV_VAR,
)
from ._sentinels import UNDEFINED, UndefinedSentinel
from ._types import IterableType
from ._utils import is_nullish_str, str_to_bool


class Config:
    def __init__(
        self,
        account_name: Union[str, UndefinedSentinel] = UNDEFINED,
        app_key: Union[str, UndefinedSentinel] = UNDEFINED,
        app_token: Union[str, UndefinedSentinel] = UNDEFINED,
        timeout: Union[float, int, None, UndefinedSentinel] = UNDEFINED,
        retry_attempts: Union[int, UndefinedSentinel] = UNDEFINED,
        retry_backoff_min: Union[float, int, UndefinedSentinel] = UNDEFINED,
        retry_backoff_max: Union[float, int, UndefinedSentinel] = UNDEFINED,
        retry_backoff_exponential: Union[
            bool, float, int, UndefinedSentinel
        ] = UNDEFINED,
        retry_statuses: Union[IterableType[int], UndefinedSentinel] = UNDEFINED,
        retry_logs: Union[bool, UndefinedSentinel] = UNDEFINED,
        raise_for_status: Union[bool, UndefinedSentinel] = UNDEFINED,
    ) -> None:
        self._account_name = self._parse_account_name(account_name)
        self._app_key = self._parse_app_key(app_key)
        self._app_token = self._parse_app_token(app_token)
        self._timeout = self._parse_timeout(timeout)
        self._retry_attempts = self._parse_retry_attempts(retry_attempts)
        self._retry_backoff_min = self._parse_retry_backoff_min(retry_backoff_min)
        self._retry_backoff_max = self._parse_retry_backoff_max(retry_backoff_max)
        self._retry_backoff_exponential = self._parse_retry_backoff_exponential(
            retry_backoff_exponential,
        )
        self._retry_statuses = self._parse_retry_statuses(retry_statuses)
        self._retry_logs = self._parse_retry_logs(retry_logs)
        self._raise_for_status = self._parse_raise_for_status(raise_for_status)

        if self.get_retry_backoff_min() > self.get_retry_backoff_max():
            raise ValueError("Minimum backoff has to be lower than maximum backoff")

    def with_overrides(
        self,
        account_name: Union[str, UndefinedSentinel] = UNDEFINED,
        app_key: Union[str, UndefinedSentinel] = UNDEFINED,
        app_token: Union[str, UndefinedSentinel] = UNDEFINED,
        timeout: Union[float, int, None, UndefinedSentinel] = UNDEFINED,
        retry_attempts: Union[int, UndefinedSentinel] = UNDEFINED,
        retry_backoff_min: Union[float, int, UndefinedSentinel] = UNDEFINED,
        retry_backoff_max: Union[float, int, UndefinedSentinel] = UNDEFINED,
        retry_backoff_exponential: Union[
            bool, int, float, UndefinedSentinel
        ] = UNDEFINED,
        retry_statuses: Union[IterableType[int], UndefinedSentinel] = UNDEFINED,
        retry_logs: Union[bool, UndefinedSentinel] = UNDEFINED,
        raise_for_status: Union[bool, UndefinedSentinel] = UNDEFINED,
    ) -> "Config":
        return Config(
            account_name=(
                self._account_name if account_name is UNDEFINED else account_name
            ),
            app_key=self._app_key if app_key is UNDEFINED else app_key,
            app_token=self._app_token if app_token is UNDEFINED else app_token,
            timeout=self._timeout if timeout is UNDEFINED else timeout,
            retry_attempts=(
                self._retry_attempts if retry_attempts is UNDEFINED else retry_attempts
            ),
            retry_backoff_min=(
                self._retry_backoff_min
                if retry_backoff_min is UNDEFINED
                else retry_backoff_min
            ),
            retry_backoff_max=(
                self._retry_backoff_max
                if retry_backoff_max is UNDEFINED
                else retry_backoff_max
            ),
            retry_backoff_exponential=(
                self._retry_backoff_exponential
                if retry_backoff_exponential is UNDEFINED
                else retry_backoff_exponential
            ),
            retry_statuses=(
                self._retry_statuses if retry_statuses is UNDEFINED else retry_statuses
            ),
            retry_logs=(self._retry_logs if retry_logs is UNDEFINED else retry_logs),
            raise_for_status=(
                self._raise_for_status
                if raise_for_status is UNDEFINED
                else raise_for_status
            ),
        )

    def get_account_name(self) -> str:
        if self._account_name is UNDEFINED:
            raise ValueError("Missing VTEX Account Name")

        return self._account_name

    def get_app_key(self) -> str:
        if self._app_key is UNDEFINED:
            raise ValueError("Missing VTEX APP Key")

        return self._app_key

    def get_app_token(self) -> str:
        if self._app_token is UNDEFINED:
            raise ValueError("Missing VTEX APP Token")

        return self._app_token

    def get_timeout(self) -> Union[float, None]:
        if self._timeout is UNDEFINED:
            return DEFAULT_TIMEOUT

        return self._timeout

    def get_retry_attempts(self) -> int:
        if self._retry_attempts is UNDEFINED:
            return DEFAULT_RETRY_ATTEMPTS

        return self._retry_attempts

    def get_retry_backoff_min(self) -> float:
        if self._retry_backoff_min is UNDEFINED:
            return DEFAULT_RETRY_BACKOFF_MIN

        return self._retry_backoff_min

    def get_retry_backoff_max(self) -> float:
        if self._retry_backoff_max is UNDEFINED:
            return DEFAULT_RETRY_BACKOFF_MAX

        return self._retry_backoff_max

    def get_retry_backoff_exponential(self) -> float:
        if self._retry_backoff_exponential is UNDEFINED:
            return DEFAULT_RETRY_BACKOFF_EXPONENTIAL

        return self._retry_backoff_exponential

    def get_retry_statuses(self) -> IterableType[int]:
        if self._retry_statuses is UNDEFINED:
            return DEFAULT_RETRY_STATUSES

        return self._retry_statuses

    def get_retry_logs(self) -> bool:
        if self._retry_logs is UNDEFINED:
            return DEFAULT_RETRY_LOGS

        return self._retry_logs

    def get_raise_for_status(self) -> bool:
        if self._raise_for_status is UNDEFINED:
            return DEFAULT_RAISE_FOR_STATUS

        return self._raise_for_status

    def _parse_account_name(
        self,
        account_name: Union[str, UndefinedSentinel] = UNDEFINED,
    ) -> Union[str, UndefinedSentinel]:
        if isinstance(account_name, str) and account_name:
            return account_name

        if account_name is UNDEFINED:
            env_account_name = getenv(ACCOUNT_NAME_ENV_VAR, UNDEFINED)

            if env_account_name is UNDEFINED or env_account_name:
                return env_account_name

            raise ValueError(
                f"Invalid value for {ACCOUNT_NAME_ENV_VAR}: {env_account_name}",
            )

        raise ValueError(f"Invalid value for account_name: {account_name}")

    def _parse_app_key(
        self,
        app_key: Union[str, UndefinedSentinel] = UNDEFINED,
    ) -> Union[str, UndefinedSentinel]:
        if isinstance(app_key, str) and app_key:
            return app_key

        if app_key is UNDEFINED:
            env_app_key = getenv(APP_KEY_ENV_VAR, UNDEFINED)

            if env_app_key is UNDEFINED or env_app_key:
                return env_app_key

            raise ValueError(f"Invalid value for {APP_KEY_ENV_VAR}: {env_app_key}")

        raise ValueError(f"Invalid value for app_key: {app_key}")

    def _parse_app_token(
        self,
        app_token: Union[str, UndefinedSentinel] = UNDEFINED,
    ) -> Union[str, UndefinedSentinel]:
        if isinstance(app_token, str) and app_token:
            return app_token

        if app_token is UNDEFINED:
            env_app_token = getenv(APP_TOKEN_ENV_VAR, UNDEFINED)

            if env_app_token is UNDEFINED or env_app_token:
                return env_app_token

            raise ValueError(f"Invalid value for {APP_TOKEN_ENV_VAR}: {env_app_token}")

        raise ValueError(f"Invalid value for app_token: {app_token}")

    def _parse_timeout(
        self,
        timeout: Union[float, int, None, UndefinedSentinel] = UNDEFINED,
    ) -> Union[float, None, UndefinedSentinel]:
        if isinstance(timeout, (float, int)) and timeout > 0:
            return float(timeout)

        if timeout is None:
            return timeout

        if timeout is UNDEFINED:
            env_timeout = getenv(TIMEOUT_ENV_VAR, UNDEFINED)

            if env_timeout is UNDEFINED:
                return env_timeout

            if is_nullish_str(env_timeout):
                return None

            try:
                converted_value = float(env_timeout)

                if converted_value > 0:
                    return converted_value
            except ValueError:
                pass

            raise ValueError(f"Invalid value for {TIMEOUT_ENV_VAR}: {env_timeout}")

        raise ValueError(f"Invalid value for timeout: {timeout}")

    def _parse_retry_attempts(
        self,
        retry_attempts: Union[int, UndefinedSentinel] = UNDEFINED,
    ) -> Union[int, UndefinedSentinel]:
        if isinstance(retry_attempts, int) and retry_attempts >= 0:
            return retry_attempts

        if retry_attempts is UNDEFINED:
            env_retry_attempts = getenv(RETRY_ATTEMPTS_ENV_VAR, UNDEFINED)

            if env_retry_attempts is UNDEFINED:
                return env_retry_attempts

            try:
                converted_value = int(env_retry_attempts)

                if converted_value >= 0:
                    return converted_value
            except ValueError:
                pass

            raise ValueError(
                f"Invalid value for {RETRY_ATTEMPTS_ENV_VAR}: {env_retry_attempts}",
            )

        raise ValueError(f"Invalid value for retry_attempts: {retry_attempts}")

    def _parse_retry_backoff_min(
        self,
        retry_backoff_min: Union[float, int, UndefinedSentinel] = UNDEFINED,
    ) -> Union[float, UndefinedSentinel]:
        if isinstance(retry_backoff_min, (float, int)) and retry_backoff_min > 0:
            return float(retry_backoff_min)

        if retry_backoff_min is UNDEFINED:
            env_retry_backoff_min = getenv(RETRY_BACKOFF_MIN_ENV_VAR, UNDEFINED)

            if env_retry_backoff_min is UNDEFINED:
                return env_retry_backoff_min

            try:
                converted_value = float(env_retry_backoff_min)

                if converted_value > 0:
                    return converted_value
            except ValueError:
                pass

            raise ValueError(
                f"Invalid value for {RETRY_BACKOFF_MIN_ENV_VAR}: "
                f"{env_retry_backoff_min}",
            )

        raise ValueError(f"Invalid value for retry_backoff_min: {retry_backoff_min}")

    def _parse_retry_backoff_max(
        self,
        retry_backoff_max: Union[float, UndefinedSentinel] = UNDEFINED,
    ) -> Union[float, UndefinedSentinel]:
        if isinstance(retry_backoff_max, (float, int)) and retry_backoff_max > 0:
            return float(retry_backoff_max)

        if retry_backoff_max is UNDEFINED:
            env_retry_backoff_max = getenv(RETRY_BACKOFF_MAX_ENV_VAR, UNDEFINED)

            if env_retry_backoff_max is UNDEFINED:
                return env_retry_backoff_max

            try:
                converted_value = float(env_retry_backoff_max)

                if converted_value > 0:
                    return converted_value
            except ValueError:
                pass

            raise ValueError(
                f"Invalid value for {RETRY_BACKOFF_MAX_ENV_VAR}: "
                f"{env_retry_backoff_max}",
            )

        raise ValueError(f"Invalid value for retry_backoff_max: {retry_backoff_max}")

    def _parse_retry_backoff_exponential(
        self,
        retry_backoff_exponential: Union[
            bool, float, int, UndefinedSentinel
        ] = UNDEFINED,
    ) -> Union[float, UndefinedSentinel]:
        if (
            not isinstance(retry_backoff_exponential, bool)
            and isinstance(retry_backoff_exponential, (float, int))
            and retry_backoff_exponential >= 1
        ):
            return float(retry_backoff_exponential)
        elif isinstance(retry_backoff_exponential, bool):
            return (
                DEFAULT_RETRY_BACKOFF_EXPONENTIAL if retry_backoff_exponential else 1.0
            )

        if retry_backoff_exponential is UNDEFINED:
            env_retry_backoff_exponential = getenv(
                RETRY_BACKOFF_EXPONENTIAL_ENV_VAR,
                UNDEFINED,
            )

            if env_retry_backoff_exponential is UNDEFINED:
                return env_retry_backoff_exponential

            try:
                converted_value = float(env_retry_backoff_exponential)

                if converted_value >= 1:
                    return converted_value
            except ValueError:
                pass

            try:
                converted_value = str_to_bool(env_retry_backoff_exponential)
                return DEFAULT_RETRY_BACKOFF_EXPONENTIAL if converted_value else 1.0
            except ValueError:
                pass

            raise ValueError(
                f"Invalid value for {RETRY_BACKOFF_EXPONENTIAL_ENV_VAR}: "
                f"{env_retry_backoff_exponential}",
            ) from None

        raise ValueError(
            f"Invalid value for retry_backoff_exponential: {retry_backoff_exponential}",
        )

    def _parse_retry_statuses(
        self,
        retry_statuses: Union[IterableType[int], UndefinedSentinel] = UNDEFINED,
    ) -> Union[IterableType[int], UndefinedSentinel]:
        if isinstance(retry_statuses, (list, set, tuple)) and all(
            isinstance(status, int) and 100 <= status <= 599
            for status in retry_statuses
        ):
            return retry_statuses

        if retry_statuses is UNDEFINED:
            env_retry_statuses = getenv(RETRY_STATUSES_ENV_VAR, UNDEFINED)

            if env_retry_statuses is UNDEFINED:
                return env_retry_statuses

            try:
                converted_values = [
                    int(status.strip())
                    for status in env_retry_statuses.split(",")
                    if status.strip()
                ]

                if all(100 <= value <= 599 for value in converted_values):
                    return converted_values
            except ValueError:
                pass

            raise ValueError(
                f"Invalid value for {RETRY_STATUSES_ENV_VAR}: {env_retry_statuses}",
            ) from None

        raise ValueError(f"Invalid value for retry_statuses: {retry_statuses}")

    def _parse_retry_logs(
        self,
        retry_logs: Union[bool, UndefinedSentinel] = UNDEFINED,
    ) -> Union[bool, UndefinedSentinel]:
        if isinstance(retry_logs, bool):
            return retry_logs

        if retry_logs is UNDEFINED:
            env_retry_logs = getenv(RETRY_LOGS_ENV_VAR, UNDEFINED)

            if env_retry_logs is UNDEFINED:
                return env_retry_logs

            try:
                return str_to_bool(env_retry_logs)
            except ValueError:
                raise ValueError(
                    f"Invalid value for {RETRY_LOGS_ENV_VAR}: {env_retry_logs}"
                ) from None

        raise ValueError(f"Invalid value for retry_logs: {retry_logs}")

    def _parse_raise_for_status(
        self,
        raise_for_status: Union[bool, UndefinedSentinel] = UNDEFINED,
    ) -> Union[bool, UndefinedSentinel]:
        if isinstance(raise_for_status, bool):
            return raise_for_status

        if raise_for_status is UNDEFINED:
            env_raise_for_status = getenv(RAISE_FOR_STATUS_ENV_VAR, UNDEFINED)

            if env_raise_for_status is UNDEFINED:
                return env_raise_for_status

            try:
                return str_to_bool(env_raise_for_status)
            except ValueError:
                raise ValueError(
                    f"Invalid value for {RAISE_FOR_STATUS_ENV_VAR}: "
                    f"{env_raise_for_status}"
                ) from None

        raise ValueError(f"Invalid value for raise_for_status: {raise_for_status}")
