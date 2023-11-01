from utils.checksum_tools import get_resp_status
from serial import Serial


class DeviceHandler():

    def __init__(self, name, serial_adapter) -> None:
        self.name = name
        self.serial:Serial = serial_adapter
    
    def send_cmd(self, cmd):
        byte_command = bytes.fromhex(cmd)
        self.serial.write(byte_command)
    
    def read_response(self, bytes_size=45):
        # Read Hexadecimal Response
        received_data = self.serial.read(bytes_size)
        return received_data.hex().upper()