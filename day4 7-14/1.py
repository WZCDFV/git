class Car:
    def __init__(self,brand,color):
        self.brand = brand,
        self.color = color,
        self.speed = 0
        self.is_started = False
    def start(self):
        if self.is_started:
            print(f"{self.brand} 已经启动了，无需重复启动。")
        else:
            self.is_started = True
            print(f"{self.color} 的 {self.brand} 启动了，当前速度：{self.speed} km/h")
    def stop(self):
        if not self.is_started:
            print(f"{self.brand}还未启动,无需重复启动。")
        else:
            self.is_started = False
            self.speed = 0
            print(f"{self.brand} 已停止，速度归零。")
# 交互
if __name__ == "__main__":
    brand_input = input("请输入汽车品牌")
    color_input = input("请输入汽车颜色")
    my_car = Car(color_input,brand_input)

    while True:
        print("\n选择操作:1-启动  2-停止  0-退出")
        op = input("请输入:")
        if op == "1":
            my_car.start()
        elif op == "2":
            my_car.stop()
        elif op == "0":
            print("再见!")
            break
        else:
            print("无效输入，请重新选择。")
