from Crypto.Util.number import *
from base64 import b64decode, b64encode
from hashlib import sha256

from pwn import *
rm = remote("103.245.250.31", 31850)



res = rm.recvuntil(b'Select an option: ').decode()
rm.sendline(b"0")
print(res)
res = rm.recvuntil(b'Select an option: ').decode().strip().split('\n')
g = int(res[0].replace("g = ", ""), 10)
p = int(res[1].replace("p = ", ""), 10)
log.info(f'{g = }')
log.info(f'{p = }')
def FindX():
    payload = b64encode(b"\x00" * 32)
    h = bytes_to_long(sha256(payload).digest())
    log.info("Message: "+payload.decode())
    rm.sendline(b'1')
    rm.sendlineafter(b"Input message you want to sign: ", payload)
    res = rm.recvuntil(b'Select an option: ').decode()
    st = res.strip().split('\n')[0].replace("Signature (r, s):  ", "")
    r, s = eval(st)
    try:
        xr = (h - s) % (p - 1)
        x = (xr * pow(r, - 1, p - 1)) % (p - 1)
    except Exception:
        return None
    return x
x = FindX()
print("Secret Key: ", x)
assert x != None



def sign(pt, m):
    if m % 2 == 0: 
        m += 1
    r = pow(g, m,  p)
    h = bytes_to_long(sha256(pt).digest())
    s = ((h -  x * r) * inverse(m,  p - 1)) % ( p - 1)
    return (r, s)

rm.sendline(b'3')
res = rm.recvuntil(b"Input r: ").decode().strip()
res = res.split('\n')[0].replace("Could you sign this for me:  ", "")
log.info("Message: "  + res)
msg = b64decode(res)

r, s = sign(res.encode(), 1)
rm.sendline(b64encode(long_to_bytes(r)))
rm.sendlineafter(b'Input s: ', b64encode(long_to_bytes(s)))

success(rm.recvline().decode())
