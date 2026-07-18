import csv

total_salary = 0
count = 0

try:
    with open("employees.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_salary += int(row["工资"])
            count += 1
    if count == 0:
        print("文件中没有员工数据。")
    else:
        average_salary = total_salary / count
        print(f"员工总人数：{count}")
        print(f"工资总额：{total_salary} 元")
        print(f"平均工资：{average_salary:.2f} 元")
except FileNotFoundError:
    print("错误：文件 employees.csv 不存在，请先运行写入程序生成该文件。")
except KeyError:
    print("错误：“工资”列包含非数字内容，无法计算。")
except ValueError:
    print("错误：“工资”列包含非数字内容，无法计算。")
except IOError as e:
    print(f"文件操作失败：{e}")
