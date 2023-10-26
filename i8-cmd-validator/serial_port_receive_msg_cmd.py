from utils.checksum_tools import compute_checksum_1, compute_checksum_2

import serial
from datetime import datetime
import time, sys

# Initialize Serial Communication
ser = serial.Serial('COM9', 115200, timeout=1)

frame_start = "7E"
command = "6152"



frame_end = "7F"

def main():
    with open(f"requests-and-responses/serial-port-recv-msg/{str(datetime.now().strftime('%Y-%m-%d %H %M %S'))}.txt", mode='w') as file:
        for port_number in [0x01]: 

                data_dict = {
                    'baud_rate' : 0x05,
                    'number_of_bytes': 0x01,
                    
                    'idle_time_1' : 0x01 # 0x01 is equal to 10ms
                }

                data = hex(port_number)[2:].zfill(2).upper()
                data += ''.join([hex(value)[2:].zfill(2).upper() for key, value in data_dict.items()])
                print(data)
                length = "0008" 

                checksum1 = compute_checksum_1(length, command)

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
                if not "6153" in resp:
                    print(f"error with cmd: {cmd}")
                    status = "BAD"

                
                file.write(f"port number: {port_number:02X}\n")
                file.write(f"Req: {cmd.upper()}\n")
                file.write(f"Resp: {resp.upper()}\n")
                file.write(f"Status: {status}\n")
                file.write("---------------------\n")


    ser.close()


if __name__ == "__main__":
     main()