students=[
    {
    "name":"Tom",
    "age":20,
    "score":99
    }   
]
# 添加学生
def add_students():
    name = input("姓名:")
    # 先检查重名
    for stu in students:
        if stu["name"] == name:
            print("重名，添加失败")
            return
    age = int(input("年龄:"))
    score = float(input("成绩:"))
    students.append({
        "name":name,
        "age":age,
        "score":score
    })
    print("添加成功!")

# 查看学生
def show_students():
    if len(students) == 0:
        print("暂无数据")
        return
    # 按成绩从高到低排序，生成新列表
    sorted_students = sorted(students,key = lambda s :s["score"],reverse=True)
    # 显示学生总人数
    total_students = len(sorted_students)
    print(f"学生总人数:{total_students}")
    # 显示平均成绩、最高分和最低分
    scores = [stu["score"] for stu in sorted_students]# 提取所有分数
    avg_score = sum(scores) / len(scores)# 平均分
    max_score = max(scores)# 最高分
    min_score = min(scores)# 最低分
    print(f"平均成绩：{avg_score:.2f}")
    print(f"最高分：{max_score}")
    print(f"最低分：{min_score}")
    for i, stu in enumerate(sorted_students,start=1):
        print(i,stu["name"],stu["age"],stu["score"])
# 查询学生
def find_students():
    name = input("请输入姓名:")
    for stu in students:
        if stu["name"] == name:
            print(stu)
            return
    print("未找到")
# 删除学生
def delete_students():
    name = input("删除姓名:")
    for stu in students:
        if stu["name"] == name:
            confirm = input(f"确认删除{name}吗？(y/n:)").lower()
            if confirm == "y":
                students.remove(stu)
                print("删除成功")
            else:
                print("取消删除")
            return
        print("学生不存在")
# 修改学生
def update_students():
    name = input("修改姓名:")
    for stu in students:
        if stu["name"] == name:
            stu["age"] = int(input("新年龄:"))
            stu["score"] = float(input("新成绩"))
            print("修改成功")
            return
        print("没有找到")

while True:
    print("""
    ========学生管理系统========
    1. 添加学生
    2. 查看学生
    3. 修改学生
    4. 删除学生
    5. 查询学生
    0. 退出
    ==========================
    """)
    choice = input("请选择:")
    if choice == "1":
        add_students()
    elif choice == "2":
        show_students()
    elif choice=="3":
        update_students()

    elif choice=="4":
        delete_students()

    elif choice=="5":
        find_students()

    elif choice == "0":
        confirm = input("确认退出码?(y/n):").lower()
        if confirm == "y":
            print("感谢使用:")
        break
    else:
        print("输入错误")