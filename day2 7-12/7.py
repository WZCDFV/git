import random
max_chance = 10
play_again = True

while play_again:
    answer = random.randint(1,10)
    total = 0
    print("Welcome to the guessing game!")

    while total < max_chance:
        remaining = max_chance - total
        try:
            guess = int(input(f"你还有 {remaining} 次机会,请输入一个1到10之间的数字: "))
        except ValueError:
            print("输入无效请输入一个整数:")
            continue
        total += 1
        if guess == answer:
            print(f"恭喜你猜对了!你一共猜了{total}次.")
            break
        elif guess > answer:
            print("你猜的数字太大了!")
        else:
            print("你猜的数字太小了!")
    else:
        # 当 while 循环正常结束（机会用完且未 break）时执行
        print(f"很遗憾，机会用完了！正确答案是 {answer}。")
        choice = input("你想再玩一次吗？(y/n): ").strip().lower()
        if choice != 'y':
            play_again = False
            print("谢谢参与，再见！")
            
