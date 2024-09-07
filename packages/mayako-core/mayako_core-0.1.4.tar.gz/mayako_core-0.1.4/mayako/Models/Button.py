from dataclasses import dataclass
from .BaseDataModel import BaseDataModel

@dataclass
class Button(BaseDataModel):
    """See BaseDataModel"""
    is_pressed: bool