class Employee:
    def __init__(self,name,work,num):
        self.name = name
        self.work = work
        self.num = num
    def show_info(self):
        print(f"姓名:{self.name}")
        print(f"职位:{self.work}")
        print(f"工资:{self.num}")
# 交互
if __name__ == "__main__":
    name = input("请输入员工姓名：")
    work = input("请输入员工职位：")
    num = float(input("请输入员工工资："))
    
    emp = Employee(name,work,num)
    print("\n员工信息如下:")
    emp.show_info()