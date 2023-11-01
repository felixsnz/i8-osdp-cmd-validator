from utils.checksum_tools import compute_checksum_1, compute_checksum_2, validate_length, get_resp_status
import serial
from datetime import datetime
import time

# Initialize Serial Communication


frame_start = "7E"
length = "000B"
command = "6032"



frame_end = "7F"

memory_types = {
    "INTERNAL ROM"              : 0x0,
    "INTERNAL FLASH"            : 0x1,
    "INTERNAL 8KB DATA FLASH"   : 0x2,
    "INTERNAL SRAM"             : 0x3,
    "EXTERNAL SRAM"             : 0x80,
    "EXTERNAL FLASH"            : 0x81,
    "EXTERNAL EEPROM"           : 0x82,
    "EXTERNAL RAM"              : 0x83,
    "EXTERNAL TPM FLASH"        : 0x84,
    "EXTERNAL DIGITAL POT"      : 0x85,
    "EXTERNAL SERIAL NOR FLASH" : 0x86,
    "EXTERNAL SD MEMORY CARD"   : 0x87,
    "RTC REGIRSTERS"            : 0x88,
    "RESERVED (RTC)"            : 0x89,
    "RESERVED (RTC)"            : 0x8B,
    "USB HOST PORT FLASH MEMORY": 0x8C
}


def main():
    ser = serial.Serial('COM9', 115200, timeout=1)
    today_str = str(datetime.now().strftime('%Y-%m-%d %H %M %S'))
    for memory_type, memory_type_code in memory_types.items(): 

            data_dict = {
                 
                'start_add_most_sig' : 0x00,
                'start_add_middle_sig': 0x00,
                'start_add_least_sig' : 0x00,
                
                'num_of_bytes_most_sig' : 0x00,
                'num_of_bytes_least_sig' : 0x02,

                 
            }
            data = hex(memory_type_code)[2:].zfill(2).upper()
            data += ''.join([hex(value)[2:].zfill(2).upper() for key, value in data_dict.items()])
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
            status = get_resp_status(resp, "6033")

            with open(f"requests-and-responses/mem-read/{today_str}.txt", mode='a') as file:
                file.write(f"memory type: {memory_type_code:02X} - {memory_type}\n")
                file.write(f"Req: {cmd.upper()}\n")
                file.write(f"Resp: {resp.upper()}\n")
                file.write(f"Status: {status}\n")
                file.write("---------------------\n")


    ser.close()

if __name__ == "__main__":
     main()