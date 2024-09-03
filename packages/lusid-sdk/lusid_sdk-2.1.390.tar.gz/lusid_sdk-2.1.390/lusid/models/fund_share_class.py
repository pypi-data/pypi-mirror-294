# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, Dict
from pydantic.v1 import Field, StrictStr, constr, validator
from lusid.models.lusid_instrument import LusidInstrument

class FundShareClass(LusidInstrument):
    """
    LUSID representation of a FundShareClass.  A ShareClass represents a pool of shares, held by investors, within a fund. A ShareClass can represent a differing investment approach by either Fees, Income, Currency Risk and Investor type.  # noqa: E501
    """
    short_code: constr(strict=True, min_length=1) = Field(..., alias="shortCode", description="A short identifier, unique across a single fund, usually made up of the ShareClass components. Eg \"A Accumulation Euro Hedged Class\" could become \"A Acc H EUR\".")
    fund_share_class_type: constr(strict=True, min_length=1) = Field(..., alias="fundShareClassType", description="The type of distribution that the ShareClass will calculate. Can be either 'Income' or 'Accumulation' - Income classes will pay out and Accumulation classes will retain their ShareClass attributable income.    Supported string (enumeration) values are: [Income, Accumulation].")
    distribution_payment_type: constr(strict=True, min_length=1) = Field(..., alias="distributionPaymentType", description="The tax treatment applied to any distributions calculated within the ShareClass. Can be either 'Net' (Distribution Calculated net of tax) or 'Gross' (Distribution calculated gross of tax).    Supported string (enumeration) values are: [Gross, Net].")
    hedging: constr(strict=True, min_length=1) = Field(..., description="A flag to indicate the ShareClass is operating currency hedging as a means to limit currency risk as part of it's investment strategy.    Supported string (enumeration) values are: [Invalid, None, ApplyHedging].")
    dom_ccy: StrictStr = Field(..., alias="domCcy", description="The domestic currency of the instrument.")
    instrument_type: StrictStr = Field(..., alias="instrumentType", description="The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashFlowsLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap, CashPerpetual, CapFloor, CashSettled, CdsIndex, Basket, FundingLeg, FxSwap, ForwardRateAgreement, SimpleInstrument, Repo, Equity, ExchangeTradedOption, ReferenceInstrument, ComplexBond, InflationLinkedBond, InflationSwap, SimpleCashFlowLoan, TotalReturnSwap, InflationLeg, FundShareClass, FlexibleLoan, UnsettledCash, Cash")
    additional_properties: Dict[str, Any] = {}
    __properties = ["instrumentType", "shortCode", "fundShareClassType", "distributionPaymentType", "hedging", "domCcy"]

    @validator('instrument_type')
    def instrument_type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('QuotedSecurity', 'InterestRateSwap', 'FxForward', 'Future', 'ExoticInstrument', 'FxOption', 'CreditDefaultSwap', 'InterestRateSwaption', 'Bond', 'EquityOption', 'FixedLeg', 'FloatingLeg', 'BespokeCashFlowsLeg', 'Unknown', 'TermDeposit', 'ContractForDifference', 'EquitySwap', 'CashPerpetual', 'CapFloor', 'CashSettled', 'CdsIndex', 'Basket', 'FundingLeg', 'FxSwap', 'ForwardRateAgreement', 'SimpleInstrument', 'Repo', 'Equity', 'ExchangeTradedOption', 'ReferenceInstrument', 'ComplexBond', 'InflationLinkedBond', 'InflationSwap', 'SimpleCashFlowLoan', 'TotalReturnSwap', 'InflationLeg', 'FundShareClass', 'FlexibleLoan', 'UnsettledCash', 'Cash'):
            raise ValueError("must be one of enum values ('QuotedSecurity', 'InterestRateSwap', 'FxForward', 'Future', 'ExoticInstrument', 'FxOption', 'CreditDefaultSwap', 'InterestRateSwaption', 'Bond', 'EquityOption', 'FixedLeg', 'FloatingLeg', 'BespokeCashFlowsLeg', 'Unknown', 'TermDeposit', 'ContractForDifference', 'EquitySwap', 'CashPerpetual', 'CapFloor', 'CashSettled', 'CdsIndex', 'Basket', 'FundingLeg', 'FxSwap', 'ForwardRateAgreement', 'SimpleInstrument', 'Repo', 'Equity', 'ExchangeTradedOption', 'ReferenceInstrument', 'ComplexBond', 'InflationLinkedBond', 'InflationSwap', 'SimpleCashFlowLoan', 'TotalReturnSwap', 'InflationLeg', 'FundShareClass', 'FlexibleLoan', 'UnsettledCash', 'Cash')")
        return value

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> FundShareClass:
        """Create an instance of FundShareClass from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> FundShareClass:
        """Create an instance of FundShareClass from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return FundShareClass.parse_obj(obj)

        _obj = FundShareClass.parse_obj({
            "instrument_type": obj.get("instrumentType"),
            "short_code": obj.get("shortCode"),
            "fund_share_class_type": obj.get("fundShareClassType"),
            "distribution_payment_type": obj.get("distributionPaymentType"),
            "hedging": obj.get("hedging"),
            "dom_ccy": obj.get("domCcy")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj
