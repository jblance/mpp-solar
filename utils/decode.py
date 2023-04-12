from struct import unpack

s = "fc08d900fc08f401d90088138813e00101000000"
s_bytes = bytes.fromhex(s)

_len = 2

for x in range(0, len(s_bytes), _len):
    sub = s[(x * 2) : (x * 2) + (_len * 2)]
    subb = s_bytes[x : x + _len]
    decode = unpack("<h", subb)
    print(f"{sub} {decode[0]}")
