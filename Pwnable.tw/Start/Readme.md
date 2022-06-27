# Pwnable.tw - Start
# Preview
https://pwnable.tw/challenge/#1


![image](https://user-images.githubusercontent.com/90976397/175880176-b2aaf146-d684-4e84-afa7-504fbd3be629.png)

 ```"Just a start" như mô tả của challenge này, chỉ là một sự khởi đầu ( nghe khá là simple :D, hoặc là không) ```

Tải file binary về và check xem thử nó cho ta những gì. 

![image](https://user-images.githubusercontent.com/90976397/175884743-683e415b-e2e6-4dc9-9733-1dfcd954d1d3.png)



![image](https://user-images.githubusercontent.com/90976397/175884807-838589d1-163d-4ad3-b138-c6ece7c57af8.png)

* Một file ELF executable 32-bits và không bị stripped

Check xem thử có những mitigation nào

![image](https://user-images.githubusercontent.com/90976397/175885003-ccb50269-6c33-4629-b134-9860e8658094.png)

* Tất cả mitigation đều bị disable :DD. Một vùng đất màu mỡ để khai thác :) 

Let's see what it does 

![image](https://user-images.githubusercontent.com/90976397/175885844-aa895b96-065f-43a2-9b01-f9875cc7f257.png) 

* Một chương trình khá là basic, pop up lên 1 chuỗi "Let's start the CTF:" và sau đó cho chúng ta nhập 1 chuỗi bất kỳ. 

Ngó qua một chút về những function mà chúng ta có thể làm việc 

![image](https://user-images.githubusercontent.com/90976397/175886352-51883eed-aa36-4439-82c6-f624c9b632bf.png)

Có vẻ như chương trình chỉ cho chúng ta làm việc loanh quanh ở hàm start

Quăng nó vô IDA để disassemble xem nó cho ta những thứ gì.
> Btw bạn có thể quăng nó vô bất kỳ cái nào (miễn là có chức năng disassemble :) ) để có thể disassemble file xem thử nó có cái gì ở trong đó, mình recommend nên dùng IDA hoặc Ghidra vì hai cái này nó rất là đa năng và có ích trong việc giải một câu binary pwn, ngoài ra bạn có thể debug bằng một trong hai cái đó, rất là useful :D. 

> Dành cho những bạn mới chơi thì mình khuyến khích các bạn đọc assembly code thay vì nhấn f5 để đọc pseudocode, việc này giúp các bạn hiểu file một cách tường tận và rõ hơn về các chức năng của các hàm cũng như xem thử lỗi nó nằm ở đâu và lỗi như nào. 

![3ofv7m](https://user-images.githubusercontent.com/90976397/175890901-50b50e64-cfd2-4724-82bb-7babe46deb9c.png)



* Hàm start rất là đơn giản 

![image](https://user-images.githubusercontent.com/90976397/175888356-077a2d13-d2a5-4d4b-9245-70cabe8c67be.png)

Mổ xẻ cái hàm này nào :DD 

![image](https://user-images.githubusercontent.com/90976397/175891190-214acf7a-06ef-4c3f-b78c-c6828cdcd080.png)

* stack pointer và offset của hàm exit được đẩy vào stack 
* tất cả thanh ghi eax, ebx, ecx, edx đều được clear (dành cho những bạn nào chưa biết thì hàm xor khi xor với chính nó thì sẽ bằng 0)

![image](https://user-images.githubusercontent.com/90976397/175892310-c6a26f3f-e6b1-4bb4-9423-b33dacbae285.png)

* sau đó nó đẩy chuỗi "Let's start the CTF:" vô stack 

![image](https://user-images.githubusercontent.com/90976397/175892914-bc4e3154-055b-4cdb-8f33-45f4e5be733b.png)

* mov ecx, esp: nó đẩy stack pointer vô ecx. Điều này có nghĩa là ecx sẽ giữ cái con trỏ, trỏ đến cái chuỗi mà chúng ta sẽ làm việc ở đó. 
* mov dl, 14h: dl đóng vai trò như là size của cái chuỗi mà chúng ta thực hiện. 0x14 đổi qua decimal là 20. 
* mov bl, 1: bl được định nghĩa là file descriptor. Có nghĩa là chúng ta sẽ sử dụng stdout. 
* mov al, 4: al được định nghĩa là syscall nào mà chúng ta muốn gọi, ở đây là 4 có nghĩa syscall chúng ta muốn gọi là sys_write. 
> int 80h: theo định nghĩa ở trên stackoverflow thì: "INT is the assembly mnemonic for "interrupt". The code after it specifies the interrupt code. (80h/0x80 or 128 in decimal is the Unix System Call interrupt) When running in Real Mode (16-bit on a 32-bit chip), interrupts are handled by the BIOS". Mình đọc xong cũng chả hiểu cái vẹo gì  :)). Nói tóm lại int 80h nó giống như là một cái tín hiệu để ngắt quãng cái flow của chương trình để chuyển flow của chương trình sang interrupt handler ở đây là 0x80. Ở linux, 0x80 được định nghĩa là một system call 
> Tổng kết lại ở trên có nghĩa là chúng ta sẽ lấy 20 characters từ stack và in ra màn hình console của user thông qua hàm sys_write.











