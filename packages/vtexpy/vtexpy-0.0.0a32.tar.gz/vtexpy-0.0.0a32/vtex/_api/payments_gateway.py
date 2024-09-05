from typing import Any

from .._dto import VTEXListResponse, VTEXResponse
from .base import BaseAPI


class PaymentsGatewayAPI(BaseAPI):
    """
    Client for the Transactions API.
    This is not in the VTEX API documentation.
    """

    ENVIRONMENT = "vtexpayments"

    def get_transaction(self, transaction_id: str, **kwargs: Any) -> VTEXResponse:
        return self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint=f"/api/pvt/transactions/{transaction_id}",
            config=self._config.with_overrides(**kwargs),
            response_class=VTEXResponse,
        )

    def list_transaction_interactions(
        self,
        transaction_id: str,
        **kwargs: Any,
    ) -> VTEXListResponse:
        return self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint=f"/api/pvt/transactions/{transaction_id}/interactions",
            config=self._config.with_overrides(**kwargs),
            response_class=VTEXListResponse,
        )

    def list_transaction_payments(
        self,
        transaction_id: str,
        **kwargs: Any,
    ) -> VTEXListResponse:
        return self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint=f"/api/pvt/transactions/{transaction_id}/payments",
            config=self._config.with_overrides(**kwargs),
            response_class=VTEXListResponse,
        )

    def get_transaction_payment(
        self,
        transaction_id: str,
        payment_id: str,
        **kwargs: Any,
    ) -> VTEXResponse:
        return self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint=f"/api/pvt/transactions/{transaction_id}/payments/{payment_id}",
            config=self._config.with_overrides(**kwargs),
            response_class=VTEXResponse,
        )

    def get_transaction_capabilities(
        self,
        transaction_id: str,
        **kwargs: Any,
    ) -> VTEXResponse:
        return self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint=f"/api/pvt/transactions/{transaction_id}/capabilities",
            config=self._config.with_overrides(**kwargs),
            response_class=VTEXResponse,
        )

    def get_transaction_cancellations(
        self,
        transaction_id: str,
        **kwargs: Any,
    ) -> VTEXResponse:
        return self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint=f"/api/pvt/transactions/{transaction_id}/cancellations",
            config=self._config.with_overrides(**kwargs),
            response_class=VTEXResponse,
        )

    def get_transaction_refunds(
        self,
        transaction_id: str,
        **kwargs: Any,
    ) -> VTEXResponse:
        return self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint=f"/api/pvt/transactions/{transaction_id}/refunds",
            config=self._config.with_overrides(**kwargs),
            response_class=VTEXResponse,
        )

    def get_transaction_settlements(
        self,
        transaction_id: str,
        **kwargs: Any,
    ) -> VTEXResponse:
        return self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint=f"/api/pvt/transactions/{transaction_id}/settlements",
            config=self._config.with_overrides(**kwargs),
            response_class=VTEXResponse,
        )
