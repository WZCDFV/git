username = "donk"
password = "666"
def login(username,password):
    if username == "donk" and password == "666":
        print("登录成功")
    else:
        print("登录失败")
username = input("请输入用户名:")
password = input("请输入密码:")
login(username,password)
    