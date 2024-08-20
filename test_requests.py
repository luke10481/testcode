import requests
import pandas as pd
from flask import Flask, request
import pymysql

class AClass:
    def __init__(self):
        self.db = pymysql.connect().cursor()

    def myexecute(self, query):
        self.db.execute(query)

class BClass:
    def __init__(self):
        self.aclass = AClass()

    def nowrun(self, query):
        self.aclass.myexecute(query)

# aclass = AClass()
source = pd.read_sql()
bclass = BClass()
bclass.nowrun(source)

# @app.route("/partial_ssrf")
# def partial_ssrf():
#     user_info = request.args["user_id"]
#     # 打开数据库连接


# df = pd.DataFrame(list(user_info))
# for i in df.to_numpy():
#     resp = requests.get(i)