def factorial(n):
    # n! = 1 * 2 * 3 * ... * n,0! = 1
    if not isinstance(n,int):
        # isinstance() 是 Python 的内置函数，用来检查一个对象是否是指定类型
        raise TypeError("n 必须是整数")
    if n < 0:
        raise ValueError("阶乘只对非负整数有定义")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
print(factorial(6))









