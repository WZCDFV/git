try:
    with open("next.txt","r", encoding="utf-8") as f:
        content = f.read()
        lines = content.splitlines()

    char_count = len(content)
    word_count = len(content.split())
    line_count = len(lines)
    print(f"字符数（含空格和标点）：{char_count}")
    print(f"英文单词数：{word_count}")
    print(f"行数：{line_count}")
except FileNotFoundError:#捕获 FileNotFoundError 异常，即当 next.txt 文件不存在时触发
    print("错误：文件 next.txt 不存在，请先运行写入程序生成该文件。")
except IOError as e: #IOError捕获其他 I/O 相关异常（如权限不足、磁盘错误等）
    print(f"文件读取失败：{e}")

