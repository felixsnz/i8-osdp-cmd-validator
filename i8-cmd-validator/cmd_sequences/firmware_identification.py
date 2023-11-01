from utils.checksum_tools import compute_checksum_1, compute_checksum_2, validate_length, get_resp_status
from utils.constants import FRAME_START, FRAME_END
import serial
from device.handler import DeviceHandler
from report_generator.report import Report


length = "0006"
hex_command = "603C"
command_name = "Firmware Identification Request"

ack_resp = "603D"

lower_nibble_options = {
       "0": "Include Checksum",
       "1": "Doesn't Inlcude Checksum"
}

upper_nibble_options = {
       "0":"Primary MCU"
       #only primary MCU option available
}


def seq(device:DeviceHandler, report: Report):

        for lower_nibble, lower_option in lower_nibble_options.items():
            for upper_nibble, upper_option in upper_nibble_options.items():

                data = f'{upper_nibble}{lower_nibble}'
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
                        f'{lower_option} in {upper_option}',
                        FRAME_START,
                        length,
                        hex_command,
                        f'{checksum1:02X}',
                        data,
                        f'{checksum2:04X}',
                        FRAME_END,
                        cmd,
                        resp,
                        get_resp_status(resp, ack_resp)
                    ]
                )


