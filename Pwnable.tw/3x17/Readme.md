# Pwnable.tw - 3x17 [150 pts]
### Preview 

![image](https://user-images.githubusercontent.com/90976397/179390562-d21a8f1f-9b3c-41dc-a669-c5c3579702ac.png)

Đây là một câu khá là hay và lạ trên pwnable.tw, nó dùng kỹ thuật ghi đè fini_array, một technique khá là cũ nhưng đáng để tìm hiểu.

### Let's get started

Download file binary về và thực hiện một số thao tác cơ bản: kiểm tra loại file, có bị stripped hay không, checksec, kiểm tra lỗi cơ bản,..... 

![image](https://user-images.githubusercontent.com/90976397/179390710-162b3ab5-b63b-4bfc-9f5e-7d153c8c9692.png)

![image](https://user-images.githubusercontent.com/90976397/179390720-24db558e-50f5-4af6-a7cd-7df98d9f21b8.png)

Một file binary ELF 64-bit LSB executable và bị stripped. 

*Dành cho những bạn nào không biết stripped là gì*

` stripped là gì? 
Khi mình compile một file executable bằng command gcc với flag -g thì nó sẽ bao gồm những thông tin về debug, có nghĩa là với mỗi instruction sẽ có những thông tin cái mà mỗi dòng của source code sẽ đẻ ra nó, tên của biến sẽ được giữ lại để có thể liên kết với bộ nhớ phù hợp trong thời gian chạy, ngoài ra stripped sẽ loại bỏ những cái thông tin của debug và những dữ liệu khác bao gồm trong file thực thi cái mà không cần thiết trong việc thực hiện để có thể giảm thiểu bộ nhớ của file thực thi.
Nôm na là khi một file bị stripped thì các tên của các biến, các hàm và những thông tin về debug thì sẽ bị xóa đi. Nhưng thực tế thì chúng ta có thể tìm thấy địa chỉ hàm main bằng command start trong gdb `


