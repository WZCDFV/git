def average(scores):
    if not scores:
        raise ValueError("不能为空")
    return sum(scores) / len(scores)
print(average([66,89,99,100]))