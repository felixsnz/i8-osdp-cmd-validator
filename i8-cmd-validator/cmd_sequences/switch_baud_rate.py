from utils.checksum_tools import compute_checksum_1, compute_checksum_2, validate_length, get_resp_status
import serial
from datetime import datetime
import time

# Initialize Serial Communication


frame_start = "7E"
length = "0006"
command = "602A"

frame_end = "7F"




def main():
    ser = serial.Serial('COM9', 76800, timeout=1)
    today_str = str(datetime.now().strftime('%Y-%m-%d %H %M %S'))
    for baud_selection in [0x5]: 


            data = hex(baud_selection)[2:].zfill(2).upper()
            checksum1 = compute_checksum_1(length, command)
            checksum2 = compute_checksum_2(length, command, checksum1, data)
            valid_length, computed_length = validate_length(length, command, checksum1, data, checksum2)

            if not valid_length:
                 print(f"input length: {length}, was different to computed length: {hex(computed_length)}")
            
            cmd = f'{frame_start} {length} {command} {checksum1:02X} {data} {checksum2:04X} {frame_end}'

            byte_command = bytes.fromhex(cmd)
            ser.write(byte_command)
            time.sleep(0.5)

            # Read Hexadecimal Response
            received_data = ser.read(45)
            time.sleep(0.5)
            resp = received_data.hex().upper()
            status = get_resp_status(resp)

            with open(f"requests-and-responses/switch-baud-rate/{today_str}.txt", mode='a') as file:
                file.write(f"Baud rate selection: {baud_selection:02X} - 115200\n")
                file.write(f"Req: {cmd.upper()}\n")
                file.write(f"Resp: {resp.upper()}\n")
                file.write(f"Status: {status}\n")
                file.write("---------------------\n")


    ser.close()

if __name__ == "__main__":
     main()