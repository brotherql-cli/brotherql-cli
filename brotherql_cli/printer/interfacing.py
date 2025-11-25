import logging
# Disable all messages at or below WARNING level
logging.disable(logging.WARNING)

from brotherql_cli.appconfig import load_config, set_config
from brotherql_cli.printer.searching import find_ip, ip_in_local_subnet
from brotherql_cli.label import generate_image

import functools

from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster

def __affirm_ip(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # print("[DEBUG] Initial IP check")
        ip = load_config()["IP"]
        if ip == "":
            set_config("IP", find_ip())
        elif not ip_in_local_subnet(ip):
            set_config("IP", find_ip())
            
        try:
            # print("[DEBUG] Initial print attempt")
            return func(*args, **kwargs)
        except:
            # print("[DEBUG] Replacing outdated IP")
            set_config("IP", find_ip())
            return func(*args, **kwargs)
    return wrapper

@__affirm_ip
def print_from_lines(label_lines:list[str]):
    config = load_config()

    # print("[DEBUG] Generating label image")
    image = generate_image(label_lines)
    qlr = BrotherQLRaster(config["MODEL"])

    printer_ip = config["IP"]

    # print("[DEBUG] Converting label to printer instructions")
    instructions = convert(
        qlr=qlr, 
        images=[image],  # Takes a list of file names or PIL objects.
        label='62', 
        rotate='0',  # 'Auto', '0', '90', '270'
        threshold=70.0,  # Black and white threshold in percent.
        dither=False, 
        compress=False, 
        dpi_600=False, 
        red=config["REDLABEL"],
        hq=True,  # False for low quality.
        cut=True
    )  

    # print("[DEBUG] Sending to print")
    send(instructions=instructions, printer_identifier=printer_ip, backend_identifier='network', blocking=True)