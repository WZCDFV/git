students = [
    {'name':'Alice','score':99},
    {'name':'bot','score':60},
    {'name':'bot','score':77},
    {'name':'monesy','score':100}
]
sorted_students = sorted(students,key=lambda s:s['score'],reverse=True)
print(sorted_students)