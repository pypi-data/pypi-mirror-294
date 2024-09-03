# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = [
    "CreditCardChargeCreateParams",
    "ExpenseLine",
    "ExpenseLineCustomField",
    "ItemGroupLine",
    "ItemGroupLineCustomField",
    "ItemLine",
    "ItemLineCustomField",
    "ItemLineLinkToTransactionLineItem",
]


class CreditCardChargeCreateParams(TypedDict, total=False):
    account_id: Required[Annotated[str, PropertyInfo(alias="accountId")]]

    conductor_end_user_id: Required[Annotated[str, PropertyInfo(alias="Conductor-End-User-Id")]]
    """
    The ID of the EndUser to receive this request (e.g.,
    `"Conductor-End-User-Id: {{END_USER_ID}}"`).
    """

    exchange_rate: Annotated[float, PropertyInfo(alias="exchangeRate")]

    expense_lines: Annotated[Iterable[ExpenseLine], PropertyInfo(alias="expenseLines")]

    external_id: Annotated[str, PropertyInfo(alias="externalId")]
    """
    An arbitrary globally unique identifier (GUID) the developer can provide to
    track this object in their own system. This value must be formatted as a GUID;
    otherwise, QuickBooks will return an error.
    """

    item_group_lines: Annotated[Iterable[ItemGroupLine], PropertyInfo(alias="itemGroupLines")]

    item_lines: Annotated[Iterable[ItemLine], PropertyInfo(alias="itemLines")]

    memo: str

    payee_id: Annotated[str, PropertyInfo(alias="payeeId")]

    ref_number: Annotated[str, PropertyInfo(alias="refNumber")]
    """The user-defined identifier for the transaction.

    It is not required to be unique and can be arbitrarily changed by the QuickBooks
    user. Case sensitive.
    """

    sales_tax_code_id: Annotated[str, PropertyInfo(alias="salesTaxCodeId")]

    transaction_date: Annotated[str, PropertyInfo(alias="transactionDate")]


class ExpenseLineCustomField(TypedDict, total=False):
    name: Required[str]

    owner_id: Required[Annotated[str, PropertyInfo(alias="ownerId")]]

    value: Required[str]


class ExpenseLine(TypedDict, total=False):
    account_id: Annotated[str, PropertyInfo(alias="accountId")]

    amount: str

    billable_status: Annotated[
        Literal["billable", "has_been_billed", "not_billable"], PropertyInfo(alias="billableStatus")
    ]
    """The billable status of this line item."""

    class_id: Annotated[str, PropertyInfo(alias="classId")]
    """The class associated with this object.

    Classes can be used to categorize objects or transactions by department,
    location, or other meaningful segments.
    """

    customer_id: Annotated[str, PropertyInfo(alias="customerId")]

    custom_fields: Annotated[Iterable[ExpenseLineCustomField], PropertyInfo(alias="customFields")]

    memo: str

    sales_representative_id: Annotated[str, PropertyInfo(alias="salesRepresentativeId")]

    sales_tax_code_id: Annotated[str, PropertyInfo(alias="salesTaxCodeId")]


class ItemGroupLineCustomField(TypedDict, total=False):
    name: Required[str]

    owner_id: Required[Annotated[str, PropertyInfo(alias="ownerId")]]

    value: Required[str]


class ItemGroupLine(TypedDict, total=False):
    item_group_id: Required[Annotated[str, PropertyInfo(alias="itemGroupId")]]

    custom_fields: Annotated[Iterable[ItemGroupLineCustomField], PropertyInfo(alias="customFields")]

    inventory_site_id: Annotated[str, PropertyInfo(alias="inventorySiteId")]

    inventory_site_location_id: Annotated[str, PropertyInfo(alias="inventorySiteLocationId")]

    quantity: float

    unit_of_measure: Annotated[str, PropertyInfo(alias="unitOfMeasure")]


class ItemLineCustomField(TypedDict, total=False):
    name: Required[str]

    owner_id: Required[Annotated[str, PropertyInfo(alias="ownerId")]]

    value: Required[str]


class ItemLineLinkToTransactionLineItem(TypedDict, total=False):
    transaction_id: Required[Annotated[str, PropertyInfo(alias="transactionId")]]

    transaction_line_id: Required[Annotated[str, PropertyInfo(alias="transactionLineId")]]


class ItemLine(TypedDict, total=False):
    amount: str

    billable_status: Annotated[
        Literal["billable", "has_been_billed", "not_billable"], PropertyInfo(alias="billableStatus")
    ]
    """The billable status of this line item."""

    class_id: Annotated[str, PropertyInfo(alias="classId")]
    """The class associated with this object.

    Classes can be used to categorize objects or transactions by department,
    location, or other meaningful segments.
    """

    cost: str

    customer_id: Annotated[str, PropertyInfo(alias="customerId")]

    custom_fields: Annotated[Iterable[ItemLineCustomField], PropertyInfo(alias="customFields")]

    description: str

    expiration_date: Annotated[str, PropertyInfo(alias="expirationDate")]

    inventory_site_id: Annotated[str, PropertyInfo(alias="inventorySiteId")]
    """The ID of the inventory site where the item is stored."""

    inventory_site_location_id: Annotated[str, PropertyInfo(alias="inventorySiteLocationId")]
    """The ID of the inventory site location where the item is stored."""

    item_id: Annotated[str, PropertyInfo(alias="itemId")]

    link_to_transaction_line_item: Annotated[
        ItemLineLinkToTransactionLineItem, PropertyInfo(alias="linkToTransactionLineItem")
    ]

    lot_number: Annotated[str, PropertyInfo(alias="lotNumber")]

    override_item_account_id: Annotated[str, PropertyInfo(alias="overrideItemAccountId")]

    quantity: float

    sales_representative_id: Annotated[str, PropertyInfo(alias="salesRepresentativeId")]

    sales_tax_code_id: Annotated[str, PropertyInfo(alias="salesTaxCodeId")]

    serial_number: Annotated[str, PropertyInfo(alias="serialNumber")]
    """The serial number of the item."""

    unit_of_measure: Annotated[str, PropertyInfo(alias="unitOfMeasure")]
