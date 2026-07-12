correct_password = "python123" #预设正确代码
max_attempts = 3 #最大尝试次数
attempts = 0 #当前尝试次数

while attempts < max_attempts:
    password = input("请输入密码: ")
    if password == correct_password:
        print("密码正确，欢迎登录！")
        break
    attempts += 1
    print(f"密码错误你还有{max_attempts - attempts}次机会")
else:
    print("尝试次数过多，账户已锁定。")