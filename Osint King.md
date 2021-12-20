# Category: Mics

### Challenge: OSINT KING.

### Level: Hard

### Description: Will Barrow is an Open-Source Intelligence Analyst, so he keeps his personal information private at all times. However, by mistake, he once revealed his personal information. Try searching and see if you can find any of his secrets, knowing that he is using a social question-and-answer platform and i think it is not the only one since he is an influencer.

# Solve: 

Đầu tiên nhìn vào thì chúng ta có thể thấy ông này hoạt động ở 1 mạng xã hội Question-and-answer thì mình nghĩ liền đến Quora ![image](https://user-images.githubusercontent.com/90976397/146702691-eda68c7f-fa46-4236-87df-6202be63b9ed.png)

Sau khi lên đây search 1 lúc thì sẽ tìm được ông Will Barrow
![image](https://user-images.githubusercontent.com/90976397/146702758-3a669eae-773f-4eac-9a6d-3cb2b2f9251a.png)

Nhìn vào description của ông này thì có vẻ trùng khớp với những gì mô tả
![image](https://user-images.githubusercontent.com/90976397/146702817-68070f48-0652-4c9c-9ee4-a2366d600394.png)

Nhìn vào wall của ông này thì thấy ông này post 1 số status nói về các tips để bảo vệ thông tin cá nhân, chúng ta sẽ không tìm được những gì ở đây. Vào phần Edit, lướt xuống 1 xíu chúng ta sẽ thấy được có 1 số bài post ông này đã xóa đi. Vào đó kiểm tra nhìn lên phần url sẽ tìm được 1 số thứ khá là thú vị

![image](https://user-images.githubusercontent.com/90976397/146703150-81579642-bcf7-4a36-a063-5040c929d31b.png)

https-imgur-com-a-KkR6760 đây là 1 link imgur khi thay vào một số ký tự thì ta sẽ có link gốc "https://imgur.com/a/KkR6760". 

Nhìn vô đây chúng ta sẽ thấy 1 bài post trên GitLab. Điều này có nghĩa rằng ông này có 1 account GitLab 
![image](https://user-images.githubusercontent.com/90976397/146703441-12af76ec-06c9-4238-bdb8-32cd28954e5c.png)
Lên Gitlab search ta sẽ tìm được ông này: https://gitlab.com/9it14b-wi11b4rr0w

![image](https://user-images.githubusercontent.com/90976397/146703518-6eb065cb-8639-4839-b54a-1cfdfc918e5b.png)
![image](https://user-images.githubusercontent.com/90976397/146703538-125f65b9-8ccb-45fb-af12-590135e2278b.png)

Vào project "Hello World", mò xuống contributors, chúng ta sẽ tìm được mail của ổng 
![image](https://user-images.githubusercontent.com/90976397/146703979-856b1b8d-d977-4333-9ae9-2156a3834641.png)

### pr0t0nm4i1-wi11b4rr0w@protonmail.com
Vậy chúng ta đã đi được 1/2 quãng đường 
Khi nhìn vô 1 số bài post của ông này trên Quora chúng ta sẽ tìm được hint ở đây
![image](https://user-images.githubusercontent.com/90976397/146704097-ad5d4c06-51e9-424b-99c7-00d3b58239af.png)

Dùng holehe để tìm xem ông này có dùng mail của ổng để đăng ký các mxh nào khác nữa không
![image](https://user-images.githubusercontent.com/90976397/146704154-67a161a8-4882-4e5e-ae4d-552cf27506ae.png)
bingo: ông này có 1 account trên ello.co. Nhưng có 1 vấn đề đó là sau khi tìm 1 lúc trên ello.co chúng ta sẽ không tìm được tên ông này theo 1 cách đơn giản như vậy. 

Quay lại Quora để tìm các hint xem, thì chúng ta sẽ thấy được ông này có thói quen để 1 số ký tự thành số và có 1 tips
![image](https://user-images.githubusercontent.com/90976397/146704334-e4af8b7e-b964-40af-84fa-cd399be69bb9.png)

sau khi phân tích 1 hồi (3 tiếng) thì mình đã tìm ra được ello-willbarrow => 3110-wi11b4rr0w. Vậy ta đã có link ello của ổng 
### https://ello.co/3110-wi11b4rr0w

Nhưng trên ello của ông này chả có gì ngoài 3 bài post (challenge này khiến mình muốn trầm cảm .... ). Sau khi bế tắc 1 hồi thì mình nhìn thấy ảnh background có gì đó khá là nghi ngờ. Kiểm tra elements thì ta xem tìm được link ảnh gốc https://assets1.ello.co/uploads/user/cover_image/5216858/ello-hdpi-2018abde.jpg 

và cuối cùng phần flag đã tìm được 

![image](https://user-images.githubusercontent.com/90976397/146704772-fbf9ba02-d225-4da4-9412-3edb6a26ea55.png)

ghép phần mail_flag lại ta sẽ có kết quả cuối cùng

### Wanna.One{pr0t0nm4i1-wi11b4rr0w@protonmail.com_Do_you_smile_when_you_find_this_flag?Merry_Xmas}



