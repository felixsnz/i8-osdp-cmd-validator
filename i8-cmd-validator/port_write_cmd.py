from utils.checksum_tools import compute_checksum_1, compute_checksum_2, validate_length, get_resp_status
import serial
from datetime import datetime
import time, sys

FRAME_START = "7E"
FRAME_END = "7F"
length = "000A"
command = "602C"

out_path = "requests-and-responses/port-write/"

ports = {
    "MCU Port P0"              : 0x0,
    "MCU Port P1"            : 0x1,
    "MCU Port P2"   : 0x2,
    "MCU Port P3"             : 0x3,
    "MCU Port P4"             : 0x4,
    "MCU Port P5"            : 0x5,
    "MCU Port P6"           : 0x6,
    "MCU Port P7"              : 0x7,
    "MCU Port P8"        : 0x8,
    "Port Expansion U8": 0x20,
    "Port Expansion U9 LED Driver OUT1-15": 0x21,
    "Port Expansion U9 LED Driver OUT16-28": 0x22,

}

def main():
    # Initialize Serial Communication
    ser = serial.Serial('COM9', 115200, timeout=1)
    today_str = str(datetime.now().strftime('%Y-%m-%d %H %M %S'))

    for port_desc, port_number in list(ports.items())[9:]: 
            
            data_dict = {
                    
                'pin_mask_high_byte' : 0x11,
                'pin_mask_low_byte': 0x11,


                'port_write_data_high' : 0x01,
                'port_write_data_low' : 0x01 
                    
            }


            
            data = hex(port_number)[2:].zfill(2).upper()
            data += ''.join([hex(value)[2:].zfill(2).upper() for value in data_dict.values()])



            checksum1 = compute_checksum_1(length, command)
            checksum2 = compute_checksum_2(length, command, checksum1, data)

            valid_length, computed_length = validate_length(length, command, checksum1, data, checksum2)

            if not valid_length:
                 print(f"input length: {length}, was different to computed length: {hex(computed_length)}")
            cmd = f'{FRAME_START} {length} {command} {checksum1:02X} {data} {checksum2:04X} {FRAME_END}'

            byte_command = bytes.fromhex(cmd)
            ser.write(byte_command)
            time.sleep(0.5)

            # Read Hexadecimal Response
            received_data = ser.read(45)
            time.sleep(0.5)
            resp = received_data.hex().upper()
            status = get_resp_status(resp)

            with open(f"{out_path}{today_str}.txt", mode='a') as file:
                file.write(f"port number: {port_number:02X} - {port_desc}:\n")
                file.write(f"Req: {cmd.upper()}\n")
                file.write(f"Resp: {resp.upper()}\n")
                file.write(f"Status: {status}\n")
                file.write("---------------------\n")
    ser.close()

if __name__ == "__main__":
     main()






