from enum import Enum
from typing import Type, TypeVar, Callable, Any

# config_options = [
#     ('IP', 'Printer's IP address'),
#     ('MODEL', 'Printer's model'),
#     ('ATTEMPTS', 'Number of attempts made when searching for printer's IP')
# ]

T = TypeVar('T', bound=Type)

import re

def _validate_ip(val:str) -> bool:
    if re.match(
        r"^[0-9]{3}\.[0-9]{3}\.[0-9]{1}\.[0-9]{2}$",
        val
    ): return True
    else: return False

def _validate_model(val:str) -> bool:
    return val.startswith('QL-')

def _validate_attempts(val:int) -> bool:
    return 0 < val < 10

def _validate_redLabel(val:bool) -> bool:
    return True

class ConfigField(str, Enum):
    IP = ('IP', "Printer's IP address", str, _validate_ip,
          '[gold1 b]IP[/gold1 b] must be in the form [magenta b]"XXX.XXX.X.XX"[/magenta b] where X are digits') # type: ignore
    MODEL = ('MODEL', "Printer's model", str, _validate_model,
             '[gold1 b]MODEL[/gold1 b] must begin with [magenta b ]"QL-"[/magenta b]') # type: ignore
    ATTEMPTS = ('ATTEMPTS', "Number of attempts made when searching for current printer's IP", int, _validate_attempts,
                '[gold1 b]ATTEMPTS[/gold1 b] must be [magenta b ]greater than 0[/magenta b] and [magenta b ]less than 10[/magenta b]') # type: ignore
    REDLABEL = ('REDLABEL', "Set {[chartreuse3]True[/chartreuse3]} if label supports printing in [red3 b]red[/red3 b], [bright_red b]MUST BE [/bright_red b]{[bright_red b]False[/bright_red b]}[bright_red b] OTHERWISE![/bright_red b]",
                bool, _validate_redLabel, "[gold1 b]REDLABEL[/gold1 b] must be exactly {True} or {False}")

    def __new__(cls, *args, **kwds):
        obj = str.__new__(cls)
        obj._value_ = args[0]
        return obj
    
    def __init__(self, _: str, desc:str, vartype:T, validator:Callable[[T], bool], defin:str):
        self._desc_ = desc
        self._vartype_ = vartype
        self._validator_ = validator
        self._defin_ = defin

    def __str__(self):
        return self.value
    
    @property
    def value(self) -> str:
        return self._value_
    
    @property
    def desc(self) -> str:
        return self._desc_
    
    @property
    def vartype(self) -> Type:
        return self._vartype_
    
    @property
    def validator(self) -> Callable[[Any], bool]:
        return self._validator_
    
    @property
    def defin(self) -> str:
        return self._defin_
    
def autocomplete_config_field(incomplete:str):
    for option in ConfigField:
        if option.value.startswith(incomplete):
            yield (option, option.desc)
    
__all__ = [
    "ConfigField",
    "autocomplete_config_field"
    # "config_options"
]