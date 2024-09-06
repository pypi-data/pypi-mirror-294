from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Address(BaseModel):
    id: UUID
    address: Optional[str]
    currency: str
    network: str
    balance: Optional[Union[int, float]]
    label: str


class GetAddressesOutputData(BaseModel):
    addresses: List[Address]


class GetAddressesParams(BaseModel):
    currency: Optional[str] = None
    label: Optional[str] = None


class CreateAddressInputData(BaseModel):
    currency: str
    network: str
    label: str


class CreateAddressOutputData(BaseModel):
    address: Address


class Transaction(BaseModel):
    id: UUID
    direction: str
    txhash: Optional[str]
    currency: str
    network: Optional[str]
    amount: Union[str, float]
    from_address: Optional[str] = Field(alias="from")
    to_address: Optional[str] = Field(alias="to")
    input: Optional[str]
    label: Optional[str]


class GetTransactionsOutputData(BaseModel):
    transactions: List[Transaction]


class GetAddressTransactionsOutputData(BaseModel):
    # transaction - bitpapa pay отдает в таком виде ответ
    transaction: List[Transaction]


class NewTransactionInputData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    direction: str = Field(default="offchain")
    currency: str
    amount: Union[int, float]
    from_address: str = Field(alias="from")
    to_address: str = Field(alias="to")
    network: str
    label: str = Field(default="")


class NewTransactionOutputData(BaseModel):
    transaction: Transaction


class WithdrawalTransactionInputData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    direction: str = Field(default="withdrawal")
    currency: str
    amount: Union[int, float]
    to_address: str = Field(alias="to")
    network: str
    label: str = ""


class WithdrawalTransactionOutputData(BaseModel):
    transaction: Transaction


class RefillTransactionInputData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    direction: str = Field(default="refill")
    currency: str
    amount: Union[int, float]
    from_address: str = Field(alias="from")
    network: str
    label: str = Field(default="")


class RefillTransactionOutputData(BaseModel):
    transaction: Transaction
