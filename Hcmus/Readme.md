
# Category: Crypto
### Challenge: Substitution 1.
```LP CRWAMZTRDAYW, D HGEHMLMGMLZP CLAYUR LH D JUMYZI ZB UPCRWAMLPT LP NYLCY GPLMH ZB AODLPMUQM DRU RUAODCUI NLMY MYU CLAYURMUQM, LP D IUBLPUI JDPPUR, NLMY MYU YUOA ZB D SUW; MYU "GPLMH" JDW EU HLPTOU OUMMURH (MYU JZHM CZJJZP), ADLRH ZB OUMMURH, MRLAOUMH ZB OUMMURH, JLQMGRUH ZB MYU DEZXU, DPI HZ BZRMY. MYU RUCULXUR IUCLAYURH MYU MUQM EW AURBZRJLPT MYU LPXURHU HGEHMLMGMLZP ARZCUHH MZ UQMRDCM MYU ZRLTLPDO JUHHDTU. YURU LH MYU BODT:```
YCJGH-CMB{PYDPOGP_OLSUH_MZ_AODW_CRWAMZTRDJ}
- Khi mà nhìn vào đoạn trên có thể suy đoán được đây là 1 chuỗi cipher subsitution
- Quăng CMB{PYDPOGP_OLSUH_MZ_AODW_CRWAMZTRDJ} lên https://www.dcode.fr/monoalphabetic-substitution rồi decrypt sẽ ra được flag
FLAG: CTF{NHANLUN_LIVES_TO_PLAY_CRYPTOGRAM}
### Challenge: Substitution 2.
```msg_enc = "MOTRVZLGEYDQCWBHDHDLYJZDQDESRKSAGGUYMNLYDWOFGTFDGOZMGAQKZMFEGTFESLWBYWRYRMESHFETMMZUJQDVYIJLHFSMNQLJIKCREGTODKGGBUHFESGQOYHFQSUZXBRDYFRDJKOTQOZUMSRMRFDSAUSUYGMZMFBEFAXHDGUNRBMFIDIKETGGTUJMAYEFBMIVQUEYMAZJYHRKIMSEJKDMYKKJQHNCRDKMGUYMKYLOTQORMKOHFJMYLGROFGRFSDTAMNQLQKRDOCHDUESLWBYWRREQQFXKSOZMAZPIBEYIJJKFBANKZTPAQDVZSOTOYUZKNURZFBTGUTOQLYLDQDQMRGUTJKJMGQPHIDNQHODKMKZMMZMBERMJTXLHWUYPJIMVFOOSPUDYLDJJRREEQFXMMSUZMAZHIBEYKJJKFUZVZYEBESRFKFDTLJZVAMQBRRGSKHFJAUDKTMRNMTDTFGJMAZPIBEKMTRVTFMKZMMRMBFDGYPHAYKZLWCFBSCSFQVSWZMZIESYHTDAGMFQ_JVYYRB_QFX_PKKEYKVSQJREHA_HD_JZGBMR_FBFG_HG"```

Ở chall này khá là similar với câu thứ nhất nhưng có một số thay đổi, đoạn msg_enc chia làm 5 block, mỗi block được mã hóa cùng với 1 offset nào đó. 
Sau khi reverse đoạn code đã cho thì đoạn msg_enc sẽ quay trở về như câu 1
```msg_enc = "MOTRVZLGEYDQCWBHDHDLYJZDQDESRKSAGGUYMNLYDWOFGTFDGOZMGAQKZMFEGTFESLWBYWRYRMESHFETMMZUJQDVYIJLHFSMNQLJIKCREGTODKGGBUHFESGQOYHFQSUZXBRDYFRDJKOTQOZUMSRMRFDSAUSUYGMZMFBEFAXHDGUNRBMFIDIKETGGTUJMAYEFBMIVQUEYMAZJYHRKIMSEJKDMYKKJQHNCRDKMGUYMKYLOTQORMKOHFJMYLGROFGRFSDTAMNQLQKRDOCHDUESLWBYWRREQQFXKSOZMAZPIBEYIJJKFBANKZTPAQDVZSOTOYUZKNURZFBTGUTOQLYLDQDQMRGUTJKJMGQPHIDNQHODKMKZMMZMBERMJTXLHWUYPJIMVFOOSPUDYLDJJRREEQFXMMSUZMAZHIBEYKJJKFUZVZYEBESRFKFDTLJZVAMQBRRGSKHFJAUDKTMRNMTDTFGJMAZPIBEKMTRVTFMKZMMRMBFDGYPHAYKZLWCFBSCSFQVSWZMZIESYHTDAGMFQ_JVYYRB_QFX_PKKEYKVSQJREHA_HD_JZGBMR_FBFG_HG"
msg = ""
offset = 1
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
size = len(ALPHABET)
def translate(msg, offset):
    msg = ALPHABET.index(msg)
    return (msg - offset) % size
for i in range(0, len(msg_enc), 5):
    for j in range(5):
        if msg_enc[i+j] == '_':
            msg += '_'
        else:
            msg += ALPHABET[translate(msg_enc[i+j], offset)]
    offset = (offset * 3 + 4) % size
print(msg)
```
Sau khi nhận được output quăng output vào https://www.dcode.fr/monoalphabetic-substitution rồi decrypt sẽ ra được flag
FLAG: HCMUS-CTF{NO_SPACES_AND_POLYALPHABETIC_IS_SECURE_ISNT_IT}
### Challenge: Sign me.
Khi nhìn 1 lượt qua source code thì chúng ta có thể suy ra được như sau:
- Chương trình cho chúng ta 4 option:
+ 0 – Get public key ( G and P)
+ 1 – Sign the message, return R and S
+ 2 – Validate signature R and S
+ 3 – Get flag:
Ở get_flag function thì nó cho ta 1 chuỗi random 32 bytes, và yêu cầu chúng ta nhập chuỗi R và S sau đó kiểm tra chuỗi R và S vừa nhập thông qua hàm verify, nếu true thì in ra flag ngược lại thì không. Nghe có vẻ khá là “simple” :D.
Sau khi reverse chương trình và tìm ra coef[i] và X sau đó tính toán R và S thì chúng ta có thể get được flag 
	+ R = g
	+ S = h – XR
 ```
from Crypto.Util.number import *
from base64 import b64decode, b64encode
from hashlib import sha256

from pwn import *
rm = remote("103.245.250.31", 31850)


res = rm.recvuntil(b'Select an option: ').decode()
rm.sendline(b"0")
print(res)
res = rm.recvuntil(b'Select an option: ').decode().strip().split('\n')
g = int(res[0].replace("g = ", ""), 10)
p = int(res[1].replace("p = ", ""), 10)
log.info(f'{g = }')
log.info(f'{p = }')
def FindX():
    payload = b64encode(b"\x00" * 32)
    h = bytes_to_long(sha256(payload).digest())
    log.info("Message: "+payload.decode())
    rm.sendline(b'1')
    rm.sendlineafter(b"Input message you want to sign: ", payload)
    res = rm.recvuntil(b'Select an option: ').decode()
    st = res.strip().split('\n')[0].replace("Signature (r, s):  ", "")
    r, s = eval(st)
    try:
        xr = (h - s) % (p - 1)
        x = (xr * pow(r, - 1, p - 1)) % (p - 1)
    except Exception:
        return None
    return x
x = FindX()
print("Secret Key: ", x)
assert x != None


def sign(pt, m):
    if m % 2 == 0: 
        m += 1
    r = pow(g, m,  p)
    h = bytes_to_long(sha256(pt).digest())
    s = ((h -  x * r) * inverse(m,  p - 1)) % ( p - 1)
    return (r, s)

rm.sendline(b'3')
res = rm.recvuntil(b"Input r: ").decode().strip()
res = res.split('\n')[0].replace("Could you sign this for me:  ", "")
log.info("Message: "  + res)
msg = b64decode(res)

r, s = sign(res.encode(), 1)
rm.sendline(b64encode(long_to_bytes(r)))
rm.sendlineafter(b'Input s: ', b64encode(long_to_bytes(s)))

success(rm.recvline().decode())
```


# Category: Pwn
### Challenge: Print me.
Khi connect với sever xong nhập 1 vài ký tự như cat flag.txt thì sever sẽ trả về như sau 
![image](https://user-images.githubusercontent.com/90976397/168536187-2209927b-9c9c-48ea-be18-a8efc5fd96d7.png)

Chương trình không filter ký tự | => chúng ta có thể bypass được filter bằng cách nhập | sau đó nhập command vào
![image](https://user-images.githubusercontent.com/90976397/168536217-b5f30ecd-5088-41ef-b2f4-f7c219cf5457.png)

Để giải quyết những câu sandbox như này bình thường chúng ta sẽ chiếm quyền điều khiển shell, để chiếm được shell thì chỉ cần nhập |sh là sẽ chiếm được shell
![image](https://user-images.githubusercontent.com/90976397/168536234-d4eb3931-502d-45a3-bcd4-2d5b830ba4e7.png)


