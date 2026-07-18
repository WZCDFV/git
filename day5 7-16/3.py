import json

# ---------- 1. 准备数据 ----------
students = [
    {"name": "张三", "age": 20, "score": 85},
    {"name": "李四", "age": 21, "score": 92},
    {"name": "王五", "age": 19, "score": 78}
]

# ---------- 2. 写入 JSON 文件 ----------
try:
    with open("students.json","w", encoding="utf-8") as f:
        json.dump(students,f, ensure_ascii=False,indent=4)
        print("学生列表已保存为 students.json")
except IOError as e:
    print(f"写入文件失败：{e}")

# ---------- 3. 读取 JSON 文件并打印 ----------
try:
    with open("students.json","r", encoding="utf-8") as f:
        loaded_students = json.load(f)
    print("\n读取到的学生信息: ")
    for stu in loaded_students:
        print(f"姓名:{stu['name']},年龄:{stu['age']},成绩:{stu['score']}")   
except FileNotFoundError:
    print("错误：文件 students.json 不存在。")
except IOError as e:
    print(f"读取文件失败：{e}")
except json.JSONDecodeError:
    print("错误：文件内容不是合法的 JSON 格式。")