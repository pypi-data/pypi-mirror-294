# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable
from typing_extensions import Literal

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...types.qbd import invoice_list_params, invoice_create_params
from ...pagination import SyncMyCursorPage, AsyncMyCursorPage
from ..._base_client import AsyncPaginator, make_request_options
from ...types.qbd.qbd_invoice import QbdInvoice

__all__ = ["InvoicesResource", "AsyncInvoicesResource"]


class InvoicesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> InvoicesResourceWithRawResponse:
        return InvoicesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> InvoicesResourceWithStreamingResponse:
        return InvoicesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        customer_id: str,
        conductor_end_user_id: str,
        accounts_receivable_account_id: str | NotGiven = NOT_GIVEN,
        billing_address: invoice_create_params.BillingAddress | NotGiven = NOT_GIVEN,
        class_id: str | NotGiven = NOT_GIVEN,
        customer_message_id: str | NotGiven = NOT_GIVEN,
        customer_sales_tax_code_id: str | NotGiven = NOT_GIVEN,
        due_date: str | NotGiven = NOT_GIVEN,
        exchange_rate: float | NotGiven = NOT_GIVEN,
        external_id: str | NotGiven = NOT_GIVEN,
        invoice_line_groups: Iterable[invoice_create_params.InvoiceLineGroup] | NotGiven = NOT_GIVEN,
        invoice_lines: Iterable[invoice_create_params.InvoiceLine] | NotGiven = NOT_GIVEN,
        is_finance_charge: bool | NotGiven = NOT_GIVEN,
        is_pending: bool | NotGiven = NOT_GIVEN,
        is_tax_included: bool | NotGiven = NOT_GIVEN,
        is_to_be_emailed: bool | NotGiven = NOT_GIVEN,
        is_to_be_printed: bool | NotGiven = NOT_GIVEN,
        item_sales_tax_id: str | NotGiven = NOT_GIVEN,
        link_to_transaction_ids: List[str] | NotGiven = NOT_GIVEN,
        memo: str | NotGiven = NOT_GIVEN,
        other_field: str | NotGiven = NOT_GIVEN,
        purchase_order_number: str | NotGiven = NOT_GIVEN,
        ref_number: str | NotGiven = NOT_GIVEN,
        sales_representative_id: str | NotGiven = NOT_GIVEN,
        set_credit: Iterable[invoice_create_params.SetCredit] | NotGiven = NOT_GIVEN,
        shipping_address: invoice_create_params.ShippingAddress | NotGiven = NOT_GIVEN,
        shipping_date: str | NotGiven = NOT_GIVEN,
        shipping_method_id: str | NotGiven = NOT_GIVEN,
        shipping_origin: str | NotGiven = NOT_GIVEN,
        template_id: str | NotGiven = NOT_GIVEN,
        terms_id: str | NotGiven = NOT_GIVEN,
        transaction_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> QbdInvoice:
        """
        Creates an invoice.

        Args:
          conductor_end_user_id: The ID of the EndUser to receive this request (e.g.,
              `"Conductor-End-User-Id: {{END_USER_ID}}"`).

          class_id: The class associated with this object. Classes can be used to categorize objects
              or transactions by department, location, or other meaningful segments.

          external_id: An arbitrary globally unique identifier (GUID) the developer can provide to
              track this object in their own system. This value must be formatted as a GUID;
              otherwise, QuickBooks will return an error.

          ref_number: The user-defined identifier for the transaction. It is not required to be unique
              and can be arbitrarily changed by the QuickBooks user. Case sensitive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Conductor-End-User-Id": conductor_end_user_id, **(extra_headers or {})}
        return self._post(
            "/quickbooks-desktop/invoices",
            body=maybe_transform(
                {
                    "customer_id": customer_id,
                    "accounts_receivable_account_id": accounts_receivable_account_id,
                    "billing_address": billing_address,
                    "class_id": class_id,
                    "customer_message_id": customer_message_id,
                    "customer_sales_tax_code_id": customer_sales_tax_code_id,
                    "due_date": due_date,
                    "exchange_rate": exchange_rate,
                    "external_id": external_id,
                    "invoice_line_groups": invoice_line_groups,
                    "invoice_lines": invoice_lines,
                    "is_finance_charge": is_finance_charge,
                    "is_pending": is_pending,
                    "is_tax_included": is_tax_included,
                    "is_to_be_emailed": is_to_be_emailed,
                    "is_to_be_printed": is_to_be_printed,
                    "item_sales_tax_id": item_sales_tax_id,
                    "link_to_transaction_ids": link_to_transaction_ids,
                    "memo": memo,
                    "other_field": other_field,
                    "purchase_order_number": purchase_order_number,
                    "ref_number": ref_number,
                    "sales_representative_id": sales_representative_id,
                    "set_credit": set_credit,
                    "shipping_address": shipping_address,
                    "shipping_date": shipping_date,
                    "shipping_method_id": shipping_method_id,
                    "shipping_origin": shipping_origin,
                    "template_id": template_id,
                    "terms_id": terms_id,
                    "transaction_date": transaction_date,
                },
                invoice_create_params.InvoiceCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=QbdInvoice,
        )

    def list(
        self,
        *,
        conductor_end_user_id: str,
        id: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        account_id: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        cursor: str | NotGiven = NOT_GIVEN,
        customer_id: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        include_line_items: bool | NotGiven = NOT_GIVEN,
        include_linked_transactions: bool | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        paid_status: Literal["all", "paid", "not_paid"] | NotGiven = NOT_GIVEN,
        ref_number: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        ref_number_contains: str | NotGiven = NOT_GIVEN,
        ref_number_ends_with: str | NotGiven = NOT_GIVEN,
        ref_number_from: str | NotGiven = NOT_GIVEN,
        ref_number_starts_with: str | NotGiven = NOT_GIVEN,
        ref_number_to: str | NotGiven = NOT_GIVEN,
        transaction_date_from: str | NotGiven = NOT_GIVEN,
        transaction_date_to: str | NotGiven = NOT_GIVEN,
        updated_after: str | NotGiven = NOT_GIVEN,
        updated_before: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncMyCursorPage[QbdInvoice]:
        """
        Returns a list of invoices.

        Args:
          conductor_end_user_id: The ID of the EndUser to receive this request (e.g.,
              `"Conductor-End-User-Id: {{END_USER_ID}}"`).

          id: The QuickBooks-assigned unique identifier of the transaction to return. You can
              provide one or multiple instances of this parameter to fetch specific
              transactions.

          account_id: Filter for invoices from this account (e.g., accounts receivable, accounts
              payable).

          cursor: The pagination token to use with the `cursor` request parameter to fetch the
              next set of results. This value was returned in the `nextCursor` field of the
              previous response when using the `limit` parameter.

          customer_id: Filter for invoices from this customer.

          include_line_items: Whether to include line items in the response.

          include_linked_transactions: Whether to include linked transactions in the response. For example, a payment
              linked to an invoice.

          limit: The maximum number of objects to return, ranging from 1 to 500. Defaults to 500.
              Include this parameter to paginate through the results. The `nextCursor` field
              in the response will contain the value to use with the `cursor` request
              parameter to fetch the next set of results.

          paid_status: Filter for transactions that are paid, not paid, or both.

          ref_number: The user-defined identifier for the transaction. It is not required to be unique
              and can be arbitrarily changed by the QuickBooks user. Case sensitive. You can
              provide one or multiple instances of this parameter to fetch specific
              transactions.

          ref_number_contains: Filter for transactions whose `refNumber` contains this substring. If you use
              this parameter, you cannot use `refNumberStartsWith` or `refNumberEndsWith`.

          ref_number_ends_with: Filter for transactions whose `refNumber` ends with this substring. If you use
              this parameter, you cannot use `refNumberContains` or `refNumberStartsWith`.

          ref_number_from: Filter for transactions whose `refNumber` is greater than or equal to this
              value. If omitted, the range will begin with the first number of the list. Uses
              a numerical comparison for values that contain only digits; otherwise, uses a
              lexicographical comparison.

          ref_number_starts_with: Filter for transactions whose `refNumber` starts with this substring. If you use
              this parameter, you cannot use `refNumberContains` or `refNumberEndsWith`.

          ref_number_to: Filter for transactions whose `refNumber` is less than or equal to this value.
              If omitted, the range will end with the last number of the list. Uses a
              numerical comparison for values that contain only digits; otherwise, uses a
              lexicographical comparison.

          transaction_date_from: Filter for transactions created on or after this date, in ISO 8601 format
              (YYYY-MM-DD).

          transaction_date_to: Filter for transactions created on or before this date, in ISO 8601 format
              (YYYY-MM-DD).

          updated_after: Filter for objects updated on or after this date and time, in ISO 8601 format
              (YYYY-MM-DDTHH:mm:ss). If you only provide a date (YYYY-MM-DD), the time is
              assumed to be 00:00:00 of that day.

          updated_before: Filter for objects updated on or before this date and time, in ISO 8601 format
              (YYYY-MM-DDTHH:mm:ss). If you only provide a date (YYYY-MM-DD), the time is
              assumed to be 23:59:59 of that day.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Conductor-End-User-Id": conductor_end_user_id, **(extra_headers or {})}
        return self._get_api_list(
            "/quickbooks-desktop/invoices",
            page=SyncMyCursorPage[QbdInvoice],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "id": id,
                        "account_id": account_id,
                        "cursor": cursor,
                        "customer_id": customer_id,
                        "include_line_items": include_line_items,
                        "include_linked_transactions": include_linked_transactions,
                        "limit": limit,
                        "paid_status": paid_status,
                        "ref_number": ref_number,
                        "ref_number_contains": ref_number_contains,
                        "ref_number_ends_with": ref_number_ends_with,
                        "ref_number_from": ref_number_from,
                        "ref_number_starts_with": ref_number_starts_with,
                        "ref_number_to": ref_number_to,
                        "transaction_date_from": transaction_date_from,
                        "transaction_date_to": transaction_date_to,
                        "updated_after": updated_after,
                        "updated_before": updated_before,
                    },
                    invoice_list_params.InvoiceListParams,
                ),
            ),
            model=QbdInvoice,
        )


class AsyncInvoicesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncInvoicesResourceWithRawResponse:
        return AsyncInvoicesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncInvoicesResourceWithStreamingResponse:
        return AsyncInvoicesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        customer_id: str,
        conductor_end_user_id: str,
        accounts_receivable_account_id: str | NotGiven = NOT_GIVEN,
        billing_address: invoice_create_params.BillingAddress | NotGiven = NOT_GIVEN,
        class_id: str | NotGiven = NOT_GIVEN,
        customer_message_id: str | NotGiven = NOT_GIVEN,
        customer_sales_tax_code_id: str | NotGiven = NOT_GIVEN,
        due_date: str | NotGiven = NOT_GIVEN,
        exchange_rate: float | NotGiven = NOT_GIVEN,
        external_id: str | NotGiven = NOT_GIVEN,
        invoice_line_groups: Iterable[invoice_create_params.InvoiceLineGroup] | NotGiven = NOT_GIVEN,
        invoice_lines: Iterable[invoice_create_params.InvoiceLine] | NotGiven = NOT_GIVEN,
        is_finance_charge: bool | NotGiven = NOT_GIVEN,
        is_pending: bool | NotGiven = NOT_GIVEN,
        is_tax_included: bool | NotGiven = NOT_GIVEN,
        is_to_be_emailed: bool | NotGiven = NOT_GIVEN,
        is_to_be_printed: bool | NotGiven = NOT_GIVEN,
        item_sales_tax_id: str | NotGiven = NOT_GIVEN,
        link_to_transaction_ids: List[str] | NotGiven = NOT_GIVEN,
        memo: str | NotGiven = NOT_GIVEN,
        other_field: str | NotGiven = NOT_GIVEN,
        purchase_order_number: str | NotGiven = NOT_GIVEN,
        ref_number: str | NotGiven = NOT_GIVEN,
        sales_representative_id: str | NotGiven = NOT_GIVEN,
        set_credit: Iterable[invoice_create_params.SetCredit] | NotGiven = NOT_GIVEN,
        shipping_address: invoice_create_params.ShippingAddress | NotGiven = NOT_GIVEN,
        shipping_date: str | NotGiven = NOT_GIVEN,
        shipping_method_id: str | NotGiven = NOT_GIVEN,
        shipping_origin: str | NotGiven = NOT_GIVEN,
        template_id: str | NotGiven = NOT_GIVEN,
        terms_id: str | NotGiven = NOT_GIVEN,
        transaction_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> QbdInvoice:
        """
        Creates an invoice.

        Args:
          conductor_end_user_id: The ID of the EndUser to receive this request (e.g.,
              `"Conductor-End-User-Id: {{END_USER_ID}}"`).

          class_id: The class associated with this object. Classes can be used to categorize objects
              or transactions by department, location, or other meaningful segments.

          external_id: An arbitrary globally unique identifier (GUID) the developer can provide to
              track this object in their own system. This value must be formatted as a GUID;
              otherwise, QuickBooks will return an error.

          ref_number: The user-defined identifier for the transaction. It is not required to be unique
              and can be arbitrarily changed by the QuickBooks user. Case sensitive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Conductor-End-User-Id": conductor_end_user_id, **(extra_headers or {})}
        return await self._post(
            "/quickbooks-desktop/invoices",
            body=await async_maybe_transform(
                {
                    "customer_id": customer_id,
                    "accounts_receivable_account_id": accounts_receivable_account_id,
                    "billing_address": billing_address,
                    "class_id": class_id,
                    "customer_message_id": customer_message_id,
                    "customer_sales_tax_code_id": customer_sales_tax_code_id,
                    "due_date": due_date,
                    "exchange_rate": exchange_rate,
                    "external_id": external_id,
                    "invoice_line_groups": invoice_line_groups,
                    "invoice_lines": invoice_lines,
                    "is_finance_charge": is_finance_charge,
                    "is_pending": is_pending,
                    "is_tax_included": is_tax_included,
                    "is_to_be_emailed": is_to_be_emailed,
                    "is_to_be_printed": is_to_be_printed,
                    "item_sales_tax_id": item_sales_tax_id,
                    "link_to_transaction_ids": link_to_transaction_ids,
                    "memo": memo,
                    "other_field": other_field,
                    "purchase_order_number": purchase_order_number,
                    "ref_number": ref_number,
                    "sales_representative_id": sales_representative_id,
                    "set_credit": set_credit,
                    "shipping_address": shipping_address,
                    "shipping_date": shipping_date,
                    "shipping_method_id": shipping_method_id,
                    "shipping_origin": shipping_origin,
                    "template_id": template_id,
                    "terms_id": terms_id,
                    "transaction_date": transaction_date,
                },
                invoice_create_params.InvoiceCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=QbdInvoice,
        )

    def list(
        self,
        *,
        conductor_end_user_id: str,
        id: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        account_id: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        cursor: str | NotGiven = NOT_GIVEN,
        customer_id: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        include_line_items: bool | NotGiven = NOT_GIVEN,
        include_linked_transactions: bool | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        paid_status: Literal["all", "paid", "not_paid"] | NotGiven = NOT_GIVEN,
        ref_number: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        ref_number_contains: str | NotGiven = NOT_GIVEN,
        ref_number_ends_with: str | NotGiven = NOT_GIVEN,
        ref_number_from: str | NotGiven = NOT_GIVEN,
        ref_number_starts_with: str | NotGiven = NOT_GIVEN,
        ref_number_to: str | NotGiven = NOT_GIVEN,
        transaction_date_from: str | NotGiven = NOT_GIVEN,
        transaction_date_to: str | NotGiven = NOT_GIVEN,
        updated_after: str | NotGiven = NOT_GIVEN,
        updated_before: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[QbdInvoice, AsyncMyCursorPage[QbdInvoice]]:
        """
        Returns a list of invoices.

        Args:
          conductor_end_user_id: The ID of the EndUser to receive this request (e.g.,
              `"Conductor-End-User-Id: {{END_USER_ID}}"`).

          id: The QuickBooks-assigned unique identifier of the transaction to return. You can
              provide one or multiple instances of this parameter to fetch specific
              transactions.

          account_id: Filter for invoices from this account (e.g., accounts receivable, accounts
              payable).

          cursor: The pagination token to use with the `cursor` request parameter to fetch the
              next set of results. This value was returned in the `nextCursor` field of the
              previous response when using the `limit` parameter.

          customer_id: Filter for invoices from this customer.

          include_line_items: Whether to include line items in the response.

          include_linked_transactions: Whether to include linked transactions in the response. For example, a payment
              linked to an invoice.

          limit: The maximum number of objects to return, ranging from 1 to 500. Defaults to 500.
              Include this parameter to paginate through the results. The `nextCursor` field
              in the response will contain the value to use with the `cursor` request
              parameter to fetch the next set of results.

          paid_status: Filter for transactions that are paid, not paid, or both.

          ref_number: The user-defined identifier for the transaction. It is not required to be unique
              and can be arbitrarily changed by the QuickBooks user. Case sensitive. You can
              provide one or multiple instances of this parameter to fetch specific
              transactions.

          ref_number_contains: Filter for transactions whose `refNumber` contains this substring. If you use
              this parameter, you cannot use `refNumberStartsWith` or `refNumberEndsWith`.

          ref_number_ends_with: Filter for transactions whose `refNumber` ends with this substring. If you use
              this parameter, you cannot use `refNumberContains` or `refNumberStartsWith`.

          ref_number_from: Filter for transactions whose `refNumber` is greater than or equal to this
              value. If omitted, the range will begin with the first number of the list. Uses
              a numerical comparison for values that contain only digits; otherwise, uses a
              lexicographical comparison.

          ref_number_starts_with: Filter for transactions whose `refNumber` starts with this substring. If you use
              this parameter, you cannot use `refNumberContains` or `refNumberEndsWith`.

          ref_number_to: Filter for transactions whose `refNumber` is less than or equal to this value.
              If omitted, the range will end with the last number of the list. Uses a
              numerical comparison for values that contain only digits; otherwise, uses a
              lexicographical comparison.

          transaction_date_from: Filter for transactions created on or after this date, in ISO 8601 format
              (YYYY-MM-DD).

          transaction_date_to: Filter for transactions created on or before this date, in ISO 8601 format
              (YYYY-MM-DD).

          updated_after: Filter for objects updated on or after this date and time, in ISO 8601 format
              (YYYY-MM-DDTHH:mm:ss). If you only provide a date (YYYY-MM-DD), the time is
              assumed to be 00:00:00 of that day.

          updated_before: Filter for objects updated on or before this date and time, in ISO 8601 format
              (YYYY-MM-DDTHH:mm:ss). If you only provide a date (YYYY-MM-DD), the time is
              assumed to be 23:59:59 of that day.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Conductor-End-User-Id": conductor_end_user_id, **(extra_headers or {})}
        return self._get_api_list(
            "/quickbooks-desktop/invoices",
            page=AsyncMyCursorPage[QbdInvoice],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "id": id,
                        "account_id": account_id,
                        "cursor": cursor,
                        "customer_id": customer_id,
                        "include_line_items": include_line_items,
                        "include_linked_transactions": include_linked_transactions,
                        "limit": limit,
                        "paid_status": paid_status,
                        "ref_number": ref_number,
                        "ref_number_contains": ref_number_contains,
                        "ref_number_ends_with": ref_number_ends_with,
                        "ref_number_from": ref_number_from,
                        "ref_number_starts_with": ref_number_starts_with,
                        "ref_number_to": ref_number_to,
                        "transaction_date_from": transaction_date_from,
                        "transaction_date_to": transaction_date_to,
                        "updated_after": updated_after,
                        "updated_before": updated_before,
                    },
                    invoice_list_params.InvoiceListParams,
                ),
            ),
            model=QbdInvoice,
        )


class InvoicesResourceWithRawResponse:
    def __init__(self, invoices: InvoicesResource) -> None:
        self._invoices = invoices

        self.create = to_raw_response_wrapper(
            invoices.create,
        )
        self.list = to_raw_response_wrapper(
            invoices.list,
        )


class AsyncInvoicesResourceWithRawResponse:
    def __init__(self, invoices: AsyncInvoicesResource) -> None:
        self._invoices = invoices

        self.create = async_to_raw_response_wrapper(
            invoices.create,
        )
        self.list = async_to_raw_response_wrapper(
            invoices.list,
        )


class InvoicesResourceWithStreamingResponse:
    def __init__(self, invoices: InvoicesResource) -> None:
        self._invoices = invoices

        self.create = to_streamed_response_wrapper(
            invoices.create,
        )
        self.list = to_streamed_response_wrapper(
            invoices.list,
        )


class AsyncInvoicesResourceWithStreamingResponse:
    def __init__(self, invoices: AsyncInvoicesResource) -> None:
        self._invoices = invoices

        self.create = async_to_streamed_response_wrapper(
            invoices.create,
        )
        self.list = async_to_streamed_response_wrapper(
            invoices.list,
        )
