# "r"	读取（文件必须存在）
# "w"	写入（覆盖原内容）
# "a"	追加（末尾添加）
# "rb"	二进制读取
# "wb"	二进制写入

print("请输入内容（输入空行并回车结束）：")
lines = []
while True:
    line = input()
    if line == "":
        break
    lines.append(line) 
    content = "\n".join(lines) #"\n" 表示“换行符”，相当于我们在键盘上敲了一次回车。
    #join 会把列表中的每个元素用换行符连起来。
# 把文字写进文件里
try:
    with open("next.txt","w",encoding="utf-8")as f:
#with ... as f 是上下文管理器，它会在代码块执行完毕后自动关闭文件（无论是否发生异常），避免资源泄露
#encoding="utf-8"告诉电脑用能存中文的编码方式，否则中文可能变成乱码
        f.write(content)
except IOError as e:
    print(f"文件写入失败：{e}")