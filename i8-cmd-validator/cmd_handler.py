import serial

# Initialize Serial Communication
ser = serial.Serial('COM9', 115200, timeout=1)

# Send Hexadecimal Command
hex_command = '7E 0006 603C A2 0000 0144 7F'
# hex_command = '7E 000A 602C 96 01 80 01 12 34 018a 7F'
hex_command = '7E 0006 602E 94 0022 014A 7F'
hex_command = '7E 0006 602E 94 0020 0148 7F'
#hex_command = '7E 0008 6030 98 00 00 00 0130 7F'
byte_command = bytes.fromhex(hex_command)
ser.write(byte_command)

# Read Hexadecimal Response
received_data = ser.read(45)
hex_data = received_data.hex()
print(f"Received data in Hex: {hex_data.upper()}")

# Close the Serial Port
ser.close()
