BUFFER_SIZE = 64
FRAME_SIZE = 80

frame = bytearray(FRAME_SIZE)

print("MAC237 Lab 3 - Session 8")
print("Buffer Overflow Simulation")

def unsafe_copy(data):
    for i in range(min(len(data), FRAME_SIZE)):
        frame[i] = data[i]

def safe_copy(data):
    for i in range(min(len(data), BUFFER_SIZE)):
        frame[i] = data[i]

payload = b"A" * 72 + b"B" * 8

unsafe_copy(payload)
assert frame[72:80] == b"B" * 8
print("CHECK PASS: Overflow detected")

frame = bytearray(FRAME_SIZE)
safe_copy(payload)
assert frame[72:80] == b"\x00" * 8
print("CHECK PASS: Bounds enforced")

MAX_UINT32 = 2**32 - 1
wrapped = (MAX_UINT32 + 1) & MAX_UINT32
assert wrapped == 0
print("CHECK PASS: Integer overflow demonstrated")

name = bytearray(b"A" * 8)
assert 0 not in name
print("CHECK PASS: Missing terminator demonstrated")
