from utils.checksum_tools import compute_checksum_1, compute_checksum_2, validate_length, get_resp_status
import sys
import serial
from datetime import datetime

frame_start = "7E"
length = "0008"
command = "6030"



#checksum2 = compute_checksum2(length, command, checksum1, data)
frame_end = "7F"



def main():
    
    # Initialize Serial Communication
    ser = serial.Serial('COM9', 115200, timeout=1)

    today_str = str(datetime.now().strftime('%Y-%m-%d %H %M %S'))
    for port_number in [0,5]:  # Byte 1: 0x00 to 0x05
        for port_pin in range(16):  # Byte 2: 0x00 to 0x0F

            data = f"{port_number:02X}{port_pin:02X}{5:02X}"
            checksum1 = compute_checksum_1(length, command)
            checksum2 = compute_checksum_2(length, command, checksum1, data)
            cmd = f'{frame_start}{length}{command}{checksum1:02X}{data}{checksum2:04X}{frame_end}'

            byte_command = bytes.fromhex(cmd)
            ser.write(byte_command)

            # Read Hexadecimal Response
            received_data = ser.read(30)
            resp = received_data.hex().upper()
            status = get_resp_status(resp, "6031")

            with open(f"requests-and-responses/ad-port/{today_str}.txt", mode='a') as file:
                file.write(f"Port number: {port_number}\n")
                file.write(f"port pin: {port_pin}\n")
                file.write(f"Req: {cmd}\n")
                file.write(f"Resp: {resp}\n")
                file.write(f"Status: {status}\n")
                file.write("---------------------\n")
    ser.close()

if __name__ == "__main__":
    main()

