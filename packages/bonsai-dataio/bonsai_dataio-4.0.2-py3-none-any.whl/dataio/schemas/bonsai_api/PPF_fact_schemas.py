from typing import Optional

import pandas as pd
from pydantic import Field

import dataio.schemas.bonsai_api.facts as schemas
from dataio.schemas.bonsai_api.base_models import FactBaseModel
from dataio.tools import BonsaiTableModel


class Use(FactBaseModel):
    location: str
    product: str
    activity: str
    unit: str
    value: float
    associated_product: Optional[str] = None
    flag: Optional[str] = (
        None  # TODO flag rework. Can be uncertainty, can be other. Different meanings across data sources.
    )
    time: int
    product_origin: Optional[str] = None  # Where the used product comes from.
    product_type: str = Field(
        default="use"
    )  # set automatically based on what data class is used

    def __str__(self) -> str:
        return f"{self.location}-{self.product}-{self.product_type}-{self.activity}-{self.time}-{self.value}-{self.unit}"


class Supply(FactBaseModel):
    location: str
    product: str
    activity: str
    unit: str
    value: float
    product_destination: Optional[str] = None
    associated_product: Optional[str] = None
    flag: Optional[str] = (
        None  # TODO flag rework. Can be uncertainty, can be other. Different meanings across data sources.
    )
    time: int
    product_type: str = Field(
        default="supply"
    )  # set automatically based on what data class is used. This can also be joint or combined product, but maybe needs to be a different attribute?

    def __str__(self) -> str:
        return f"{self.location}-{self.product}-{self.product_type}-{self.activity}-{self.time}-{self.value}-{self.unit}"


class ProductionVolumes(FactBaseModel):
    location: str
    product: str
    activity: Optional[str] = None
    unit: str
    value: float
    flag: Optional[str] = None  # TODO flag rework
    time: int
    inventory_time: Optional[int] = None
    source: str
    comment: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.location}-{self.product}-{self.activity}-{self.time}-{self.value}-{self.unit}"


class Emissions(FactBaseModel):
    time: int
    year_emission: Optional[int] = (
        None  # TODO Rework into how we want to handle delayed emissions
    )
    location: str
    activity: str
    activity_unit: str
    emission_substance: str
    compartment: str  # location of emission, such as "Emission to air"
    product: str
    product_unit: str
    value: float
    unit: str
    flag: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.location}-{self.emission_substance}-{self.activity}-{self.activity_unit}-{self.time}-{self.value}-{self.unit}"


class TransferCoefficient(FactBaseModel):  # Similar to use
    location: Optional[str] = None
    output_product: str
    input_product: str
    activity: str
    coefficient_value: float
    unit: str
    flag: Optional[str] = (
        None  # TODO flag rework. Can be uncertainty, can be other. Different meanings across data sources.
    )
    time: Optional[int] = None

    def __str__(self) -> str:
        return f"{self.location}-{self.product}-{self.activity}-{self.time}-{self.coefficient_value}"


class Resource(Use):
    def __init__(self, **data):
        super().__init__(**data)
        self.product_type = "resource"


class PackagingData(Supply):
    def __init__(self, **data):
        super().__init__(**data)
        self.product_type = "packaging_data"


class WasteUse(Use):
    waste_fraction: bool

    def __init__(self, **data):
        super().__init__(**data)
        self.product_type = "waste_use"


class WasteSupply(Supply):
    waste_fraction: bool

    def __init__(self, **data):
        super().__init__(**data)
        self.product_type = "waste_supply"


class PropertyOfProducts(FactBaseModel):
    location: Optional[str] = None
    product: str
    value: float
    activity: Optional[str] = None
    unit: str
    description: Optional[str] = None


class Trade(FactBaseModel):
    time: int
    product: str
    export_location: str
    import_location: str
    value: float
    quantity: float
    unit: str
    flag: Optional[str] = None  # TODO flag rework
