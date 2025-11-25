from pathlib import Path
import typer
import yaml

APP_NAME = "brotherql-cli"

from typing import TypedDict

class ConfigSchema(TypedDict):
    IP: str
    MODEL: str
    ATTEMPTS: int
    REDLABEL: bool

CONF_PATH:Path = Path(typer.get_app_dir(APP_NAME)) / "config.yaml"

from brotherql_cli.cli.exceptionhandle import PrintException
def __gen_new_config() -> None:
    if not CONF_PATH.parent.exists():
        try:
            CONF_PATH.parent.mkdir()
        except Exception as e:
            raise PrintException(e)
    with open(CONF_PATH, "x") as f:
        yaml.dump(ConfigSchema(IP="", MODEL="QL-820NWB", ATTEMPTS=4, REDLABEL=False), f, default_flow_style=False)

def __affirm_configfile() -> None:
    if not CONF_PATH.is_file():
        if CONF_PATH.exists():
            raise TypeError("Config file path is occupied by a folder, please remove it so config can be generated")
        __gen_new_config()

def load_config() -> ConfigSchema:
    __affirm_configfile()
    with open(CONF_PATH, "r") as f:
        config = yaml.safe_load(f)
    try:
        schema = ConfigSchema(config)
        for key in ConfigSchema.__annotations__.keys():
            if key not in schema.keys():
                if key == "IP": schema["IP"] = ""
                elif key == "MODEL": schema["MODEL"] = "QL-820NWB"
                elif key == "ATTEMPTS": schema["ATTEMPTS"] = 4
                elif key == "REDLABEL": schema["REDLABEL"] = False

        return schema
    except:
        __gen_new_config()
        return ConfigSchema(IP="", MODEL="QL-820NWB", ATTEMPTS=4, REDLABEL=False)

def set_config(item:str, val) -> ConfigSchema:
    __affirm_configfile()
    config = load_config()
    config[item] = val
    with open(CONF_PATH, "w") as f:
        yaml.dump(config, f, default_flow_style=False)
    return config