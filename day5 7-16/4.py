import csv

employees = [
    {"姓名": "张三", "部门": "技术部", "工资": 8000},
    {"姓名": "李四", "部门": "市场部", "工资": 6500},
    {"姓名": "王五", "部门": "人事部", "工资": 7000},
]
# 定义 表头字段顺序 这个列表会决定 CSV 文件第一行的列标题及各列数据的存放顺序
fieldnames = ["姓名", "部门", "工资"]
try:
    with open("employees.csv", "w", newline="", encoding="utf-8") as f:
        write = csv.DictWriter(f, fieldnames=fieldnames)
        # 写入头部
        write.writeheader()
        # 逐行写入员工数据
        write.writerows(employees)
    print("employees.csv 创建成功！")
    # 读取并打印文件内容，验证结果
    print("\n文件内容: ")
    with open("employees.csv", "r", encoding="utf-8") as f:
        print(f.read())
except IOError as e:
    print(f"文件操作失败：{e}")
