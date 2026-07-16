class Calculator:
    @staticmethod
    def add(a,b):
        return a + b
    @staticmethod
    def subtract(a,b):
        return a - b
    @staticmethod
    def multiply(a,b):
        return a * b
    @staticmethod
    def divide(a,b):
        if b == 0:
            return
        return a / b
# 交互
if __name__ == "__main__":
    print("===== 简易计算器（静态方法版）=====")
    try:
        num1 = float(input("请输入第一个数字："))
        num2 = float(input("请输入第二个数字："))
    except ValueError:
        print("输入无效，请输入数字。")
        exit()
    print("\n选择运算:")
    print("1. 加法")
    print("2. 减法")
    print("3. 乘法")
    print("4. 除法")
    op = input("请输入编号 (1/2/3/4):")
    if op == "1":
        res = Calculator.add(num1, num2)
        print(f"{num1} + {num2} = {res}")
    elif op == "2":
        res = Calculator.subtract(num1, num2)
        print(f"{num1} - {num2} = {res}")
    elif op == "3":
        res = Calculator.multiply(num1, num2)
        print(f"{num1} * {num2} = {res}")
    elif op == "4":
        res = Calculator.divide(num1, num2)
        print(f"{num1} ÷ {num2} = {res}")
    else:
        print("无效的选择")