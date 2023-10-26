def compute_checksum_1(length: str, command: str) -> int:
    length_bytes = [int(length[i:i+2], 16) for i in range(0, len(length), 2)]
    command_bytes = [int(command[i:i+2], 16) for i in range(0, len(command), 2)]
    
    checksum1 = sum(length_bytes + command_bytes) & 0xFF
    return checksum1

def compute_checksum_2(length: str, command: str, checksum1: int, data: str) -> int:
    data_bytes = [int(data[i:i+2], 16) for i in range(0, len(data), 2)]
    total_bytes = data_bytes + [checksum1] + [int(length[i:i+2], 16) for i in range(0, len(length), 2)] + [int(command[i:i+2], 16) for i in range(0, len(command), 2)]
    
    checksum2 = sum(total_bytes) & 0xFFFF
    return checksum2

def validate_length(actual_length, command, checksum1, data, checksum2):
    # For a 1-byte checksum, size is 1; for a 2-byte checksum, size is 2
    checksum1_size = 1
    checksum2_size = 2

    # Calculate the total length
    computed_length = (len(command) // 2) + checksum1_size + (len(data) // 2) + checksum2_size
    computed_length_hex = format(computed_length, '04X').upper()
    
    return actual_length == computed_length_hex, computed_length

def get_resp_status(resp, cmd_ack:str=None):
    resp_status_code = resp[6:10]
    print("resp status code: ", resp_status_code)
    status_map = {
        "0003" : "NA",
        "0004" : "ACK",
        "0005" : "NACK",
        cmd_ack: "ACK"
    }

    return status_map[resp_status_code]

