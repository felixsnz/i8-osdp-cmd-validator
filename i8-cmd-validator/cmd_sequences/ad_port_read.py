from utils.checksum_tools import compute_checksum_1, compute_checksum_2, validate_length, get_resp_status
from utils.singleton import Singleton
from device.handler import DeviceHandler
from report_generator.report import Report
from utils.constants import FRAME_END, FRAME_START
import sys
from serial import Serial
from datetime import datetime


length = "0008"
hex_command = "6030"
command_name = "A/D Port Read Request"

sg = Singleton()

def seq(device:DeviceHandler, report: Report):
    

    
    for port_number in [0,5]:  # Byte 1: 0x00 to 0x05
        for port_pin in range(16):  # Byte 2: 0x00 to 0x0F

            data = f"{port_number:02X}{port_pin:02X}{5:02X}"
            checksum1 = compute_checksum_1(length, hex_command)
            checksum2 = compute_checksum_2(length, hex_command, checksum1, data)
            cmd = f'{FRAME_START}{length}{hex_command}{checksum1:02X}{data}{checksum2:04X}{FRAME_END}'

            valid_length, computed_length = validate_length(length, hex_command, checksum1, data, checksum2)

            if not valid_length:
                 print(f"input length: {length}, was different to computed length: {hex(computed_length)}")


            device.send_cmd(cmd)

            resp = device.read_response()

            report.append(
                [
                    device.name,
                    f'[{hex_command}] {command_name}',
                    f'Port {port_number}; Pin {port_pin}',
                    FRAME_START,
                    length,
                    hex_command,
                    checksum1,
                    data,
                    checksum2,
                    FRAME_END,
                    cmd,
                    resp,
                    get_resp_status(resp)
                ]
            )

        

