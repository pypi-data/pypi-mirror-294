from dataclasses import dataclass
from .BaseDataModel import BaseDataModel

@dataclass
class Temperature(BaseDataModel):
    """See BaseDataModel"""
    temperature: float
