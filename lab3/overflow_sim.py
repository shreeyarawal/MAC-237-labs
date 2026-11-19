TOKEN = "53a02c136d8c3722"

BUF_LEN = 64
FRAME_LEN = 80
SFP_OFF = 64
RET_OFF = 72

RETURN_TO = 0x401136
SAVED_FP = 0x7FFDDEADBEEF

def new_frame():
    frame = bytearray(FRAME_LEN)
    frame[SFP_OFF:RET_OFF] = SAVED_FP.to_bytes(8, "little")
    frame[RET_OFF:FRAME_LEN] = RETURN_TO.to_bytes(8, "little")
    return frame

def get_return_address(frame):
    return int.from_bytes(frame[RET_OFF:FRAME_LEN], "little")

def unsafe_copy(frame, data):
    for i, value in enumerate(data[:FRAME_LEN]):
        frame[i] = value
    return frame

def safe_copy(frame, data):
    count = min(len(data), BUF_LEN - 1)
    frame[:count] = data[:count]
    frame[count] = 0
    return frame

print("MAC237 Lab 3 - Session 8")
print("Token:", TOKEN)

frame = new_frame()
print("\nPart A: Stack frame")
print("Buffer: bytes 0-63")
print("Saved frame pointer: bytes 64-71")
print("Return address: bytes 72-79")

payload = b"A" * 72 + b"B" * 8
frame = unsafe_copy(new_frame(), payload)

print("\nPart B: Unsafe copy")
print("Original return address:", hex(RETURN_TO))
print("Modified return address:", hex(get_return_address(frame)))

assert get_return_address(frame) != RETURN_TO
print("CHECK PASS: Buffer overflow detected")

frame = safe_copy(new_frame(), payload)

print("\nPart C: Safe copy")
print("Return address:", hex(get_return_address(frame)))

assert get_return_address(frame) == RETURN_TO
assert frame[63] == 0
print("CHECK PASS: Bounds checking works")

maximum = 2**32 - 1
wrapped = (maximum + 1) & maximum

print("\nPart D: Integer overflow")
print("Wrapped value:", wrapped)

assert wrapped == 0

data = bytearray(b"A" * 8)

print("\nPart E: Missing null terminator")
print("Null terminator present:", 0 in data)

assert 0 not in data

print("CHECK PASS: Integer and string checks")
print("\nSession 8 simulation completed.")
