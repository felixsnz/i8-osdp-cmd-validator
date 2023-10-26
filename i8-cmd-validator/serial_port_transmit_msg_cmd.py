from utils.checksum_tools import compute_checksum_1, compute_checksum_2, validate_length
import serial
from datetime import datetime
import time, sys

FRAME_START = "7E"
FRAME_END = "7F"

command = "6151"
length = "0009"

out_path = "requests-and-responses/serial-port-trans-msg/"




def main():
    ser = serial.Serial('COM9', 115200, timeout=1)
    today_str = str(datetime.now().strftime('%Y-%m-%d %H %M %S'))
    for port_number in [0x01]: 

            data_dict = {
                'baud_rate' : 0x05,
                'number_of_bytes': 0x01,
                
                'char_1' : 0x01
            }

            data = hex(port_number)[2:].zfill(2).upper()
            data += ''.join([hex(value)[2:].zfill(2).upper() for key, value in data_dict.items()])
            
            checksum1 = compute_checksum_1(length, command)

            checksum2 = compute_checksum_2(length, command, checksum1, data)

            valid_length, computed_length =validate_length(length, command, checksum1, data, checksum2)

            if not valid_length:
                 print(f"input length: {length}, was different to computed length: {computed_length}")
            
            cmd = f'{FRAME_START} {length} {command} {checksum1:02X} {data} {checksum2:04X} {FRAME_END}'

            byte_command = bytes.fromhex(cmd)
            ser.write(byte_command)
            time.sleep(0.5)

            # Read Hexadecimal Response
            received_data = ser.read(45)
            time.sleep(0.5)
            resp = received_data.hex().upper()
            status = "OK"
            if not "0004" in resp:
                print(f"error with cmd: {cmd}")
                status = "BAD"

            with open(f"{out_path}{today_str}.txt", mode='a') as file:
                file.write(f"port number: {port_number:02X}\n")
                file.write(f"Req: {cmd.upper()}\n")
                file.write(f"Resp: {resp.upper()}\n")
                file.write(f"Status: {status}\n")
                file.write("---------------------\n")
    ser.close()


if __name__ == "__main__":
     main()