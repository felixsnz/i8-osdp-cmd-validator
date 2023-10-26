from utils.checksum_tools import compute_checksum_1, compute_checksum_2
from validation import validate_cmd
import serial
from datetime import datetime
import time

# Initialize Serial Communication
ser = serial.Serial('COM9', 115200, timeout=1)

FRAME_START = '7E'
FRAME_END = '7F'

command = "6032"

mem_read = {
     "modes" : [0x0,0x1,0x2,0x3,0x80,0x81,0x82,0x83,0x84,0x85,0x86,0x87,0x88,0x89,0x8B,0x8C],
     "data" : 
     {        
        'start_add_most_sig' : 0x00,
        'start_add_middle_sig': 0x00,
        'start_add_least_sig' : 0x00,
        
        'num_of_bytes_most_sig' : 0x00,
        'num_of_bytes_least_sig' : 0x0F,            
    }
}

validate_cmd()
