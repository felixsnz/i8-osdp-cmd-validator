from utils.checksum_tools import compute_checksum_1, compute_checksum_2

import serial
from datetime import datetime
import time, sys

# Initialize Serial Communication
ser = serial.Serial('COM9', 115200, timeout=1)

frame_start = "7E"
length = "0006"
command = "603C"

checksum1 = compute_checksum_1(length, command)

frame_end = "7F"


with open(f"requests-and-responses/fw-id/{str(datetime.now().strftime('%Y-%m-%d %H %M %S'))}.txt", mode='w') as file:
    for memory_type in [0x0]: 

            data_dict = {
 
            }

            data = hex(memory_type)[2:].zfill(2).upper()
            data += ''.join([hex(value)[2:].zfill(2).upper() for key, value in data_dict.items()])

            checksum2 = compute_checksum_2(length, command, checksum1, data)
            cmd = f'{frame_start} {length} {command} {checksum1:02X} {data} {checksum2:04X} {frame_end}'

            byte_command = bytes.fromhex(cmd)
            ser.write(byte_command)
            time.sleep(0.5)

            # Read Hexadecimal Response
            received_data = ser.read(45)
            time.sleep(0.5)
            resp = received_data.hex().upper()
            status = "OK"
            if not "603D" in resp:
                print(f"error with cmd: {cmd}")
                status = "BAD"

            
            file.write(f"memory type: {memory_type:02X}\n")
            file.write(f"Req: {cmd.upper()}\n")
            file.write(f"Resp: {resp.upper()}\n")
            file.write(f"Status: {status}\n")
            file.write("---------------------\n")


ser.close()