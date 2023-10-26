from utils.checksum_tools import compute_checksum_1, compute_checksum_2
import serial
from datetime import datetime
import time

# Initialize Serial Communication
ser = serial.Serial('COM9', 115200, timeout=1)

FRAME_START = '7E'
FRAME_END = '7F'


def validate_ad_ports(command:str, ports:list, pins:int, measures:int, expected_resp:str):

    for port in ports:
        for pin in range(pins):


            data = f"{port:02X}{pin:02X}{5:02X}"

            length = "000B"

            
            checksum1 = compute_checksum_1(length, command)
            checksum2 = compute_checksum_2(length, command, checksum1, data)
            cmd = f'{FRAME_START} {length} {command} {checksum1:02X} {data} {checksum2:04X} {FRAME_END}'

            byte_command = bytes.fromhex(cmd)
            ser.write(byte_command)
            time.sleep(0.5)

            # Read Hexadecimal Response
            received_data = ser.read(45)
            time.sleep(0.5)
            resp = received_data.hex().upper()
            status = "OK"
            if not expected_resp in resp:
                print(f"error with cmd: {cmd}")
                status = "BAD"

            with open(f"mem-read-requests-and-responses/{str(datetime.now().strftime('%Y-%m-%d %H %M %S'))}.txt", mode='w') as file:
                file.write(f"memory type: {mode:02X}\n")
                file.write(f"Req: {cmd.upper()}\n")
                file.write(f"Resp: {resp.upper()}\n")
                file.write(f"Status: {status}\n")
                file.write("---------------------\n")



def validate_cmd(command:str, modes, data_dict:dict, expected_resp:str):

    for mode in modes: 


        data = hex(mode)[2:].zfill(2).upper()
        data += ''.join([hex(value)[2:].zfill(2).upper() for value in data_dict.values()])

        length = "000B"

        
        checksum1 = compute_checksum_1(length, command)
        checksum2 = compute_checksum_2(length, command, checksum1, data)
        cmd = f'{FRAME_START} {length} {command} {checksum1:02X} {data} {checksum2:04X} {FRAME_END}'

        byte_command = bytes.fromhex(cmd)
        ser.write(byte_command)
        time.sleep(0.5)

        # Read Hexadecimal Response
        received_data = ser.read(45)
        time.sleep(0.5)
        resp = received_data.hex().upper()
        status = "OK"
        if not expected_resp in resp:
            print(f"error with cmd: {cmd}")
            status = "BAD"

        with open(f"mem-read-requests-and-responses/{str(datetime.now().strftime('%Y-%m-%d %H %M %S'))}.txt", mode='w') as file:
            file.write(f"memory type: {mode:02X}\n")
            file.write(f"Req: {cmd.upper()}\n")
            file.write(f"Resp: {resp.upper()}\n")
            file.write(f"Status: {status}\n")
            file.write("---------------------\n")


ser.close()