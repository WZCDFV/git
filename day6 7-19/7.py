# 第一部分：模块导入与文档字符串
import requests  # 发送HTTP请求
import json  # 解析JSON响应 读写JSON 历史文件
import os  # 检查文件是否存在 (os.path.exists)
from datetime import datetime  # 获取当前时间,用于记录查询时间戳


#  第二部分：Weather 类定义与初始化
class Weather:
    """天气查询类，封装 API 调用、数据解析和历史记录管理"""

    def __init__(self, history_file="history.json"):
        """初始化：设置历史记录文件路径，加载已有记录"""
        self.history_file = history_file  # 实例变量：文件名，默认 "history.json"
        self.history = []  # 实例变量：内存中的历史记录列表
        self.max_history = 10  # 实例变量：最多保留 10 条记录
        self.load_history()  # 启动时立即加载历史文件

    # 第三部分：历史记录持久化（读、写、增）
    def load_history(self):
        """从 JSON 文件加载历史记录，若文件不存在或格式错误则初始化为空"""
        # 检查历史记录文件是否存在
        if not os.path.exists(self.history_file):
            # 文件不存在，将 history 置为空列表
            self.history = []
            return
        try:
            # 以只读方式打开文件，编码为 utf-8
            with open(self.history_file, "r", encoding="utf-8") as f:
                # 将 JSON 文件内容解析为 Python 列表
                self.history = json.load(f)
            # 确保读取到的数据确实是列表类型，否则初始化为空列表
            if not isinstance(self.history, list):
                self.history = []
        except (json.JSONDecodeError, IOError):
            # JSON 格式错误或文件读取失败时，也初始化为空列表
            self.history = []

    def save_history(self):
        """将当前的历史记录列表写入 JSON 文件"""
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                # 将历史记录列表转为 JSON 字符串并写入文件，ensure_ascii=False 保证中文正常显示，indent=2 使文件格式化美观
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except IOError as e:
            # 文件写入出错时给出提示
            print(f"历史记录保存失败：{e}")

    def add_to_history(self, city, weather_info):
        """
        将一条查询记录添加到历史记录列表，并保持最多 max_history 条
        参数 city: 查询的城市名
        参数 weather_info: 包含温度、天气描述的字典
        """
        # 构造一条记录字典，包含城市、时间、温度和天气描述
        record = {
            "city": city,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "temperature": weather_info.get("temperature"),
            "description": weather_info.get("description"),
        }
        # 将新记录插入到列表最前面（最新记录排第一）
        self.history.insert(0, record)
        # 如果历史记录超过最大条数，仅保留前 max_history 条
        if len(self.history) > self.max_history:
            self.history = self.history[: self.max_history]
        # 将更新后的历史记录保存到文件
        self.save_history()

    def show_history(self):
        """打印所有历史查询记录"""
        # 若历史记录为空，提示用户并返回
        if not self.history:
            print("\n暂无历史记录。")
            return
        print("\n--- 最近查询记录 ---")
        # 遍历历史记录，序号从 1 开始
        for i, record in enumerate(self.history, 1):
            # 打印每条记录的时间、城市、温度和天气描述
            print(
                f"{i}. {record['time']} | {record['city']} | {record['temperature']} | {record['description']}"
            )
        print("-" * 30)

    # ---------- 天气查询核心 ----------
    def search(self, city):
        """
        根据城市名查询天气，返回包含详细信息的字典。
        若查询失败（网络错误、解析错误、城市不存在等）则返回 None。
        """
        # 构造 wttr.in 的 API 请求地址，format=j1 表示返回 JSON 格式数据
        url = f"https://wttr.in/{city}?format=j1"
        try:
            # 发送 GET 请求，超时时间设为 10 秒
            response = requests.get(url, timeout=10)
            # 如果 HTTP 状态码不是 200（成功），说明请求失败（如城市不存在）
            if response.status_code != 200:
                return None
            # 将响应内容解析为 Python 字典
            data = response.json()
        except requests.exceptions.RequestException:
            # 捕获所有网络异常（如超时、连接错误），返回 None
            return None
        except json.JSONDecodeError:
            # 响应内容不是合法的 JSON（例如返回了 HTML 错误页面），返回 None
            return None

        # 尝试从解析后的数据中提取所需天气信息
        try:
            # current_condition 是一个列表，取第一个元素为当前天气状况
            current = data["current_condition"][0]
            # weather 是未来几天的天气预报，取第一个元素为今天的天气
            today = data["weather"][0]

            # 将提取到的各个字段组成字典，统一添加单位
            weather_info = {
                "temperature": current["temp_C"] + "°C",  # 当前温度（摄氏度）
                "feels_like": current["FeelsLikeC"] + "°C",  # 体感温度
                "max_temp": today["maxtempC"] + "°C",  # 今天最高温度
                "min_temp": today["mintempC"] + "°C",  # 今天最低温度
                "humidity": current["humidity"] + "%",  # 湿度
                "wind_speed": current["windspeedKmph"] + " km/h",  # 风速（公里/小时）
                "description": current["weatherDesc"][0][
                    "value"
                ],  # 天气描述（如 Sunny）
            }
            return weather_info
        except (KeyError, IndexError, TypeError):
            # 若数据字段缺失或数据结构不符合预期，返回 None
            return None

    @staticmethod
    def display_weather(city, info):
        """静态方法：格式化显示天气信息，不依赖类的实例属性"""
        print(f"\n{'='*30}")
        print(f"城市：{city}")
        print(f"温度：{info['temperature']}  (体感 {info['feels_like']})")
        print(f"最高温：{info['max_temp']}  /  最低温：{info['min_temp']}")
        print(f"湿度：{info['humidity']}")
        print(f"风速：{info['wind_speed']}")
        print(f"天气：{info['description']}")
        print(f"{'='*30}\n")

    # ---------- 交互式查询流程（连续查询） ----------
    def query_loop(self):
        """连续查询多个城市，直到用户输入 'q' 返回主菜单"""
        print("\n--- 天气查询 ---")
        print("输入城市名查询天气，输入 q 返回主菜单。")
        while True:
            # 获取用户输入的城市名，去除两端空白字符
            city = input("请输入城市名: ").strip()
            # 若输入 'q'（不区分大小写），退出循环，返回主菜单
            if city.lower() == "q":
                break
            # 若输入为空字符串，提示重新输入并继续下一次循环
            if not city:
                print("城市名不能为空，请重新输入。")
                continue

            print(f"正在查询{city}的天气...")
            # 调用 search 方法查询天气
            info = self.search(city)
            # 若查询失败（返回 None），提示用户并继续循环
            if info is None:
                print(f"查询失败，请检查城市名是否正确，或稍后重试。")
                continue

            # 查询成功，显示天气信息
            self.display_weather(city, info)
            # 将本次查询记录添加到历史
            self.add_to_history(city, info)


# ---------- 主程序 ----------
def main():
    # 创建天气查询对象，默认使用 history.json 文件保存历史记录
    weather_app = Weather()

    # 主菜单循环，直到用户选择退出
    while True:
        print("\n" + "=" * 30)
        print("       天气查询系统")
        print("=" * 30)
        print("1. 查询天气")
        print("2. 查看历史记录")
        print("0. 退出")
        print("=" * 30)
        # 读取用户选择的菜单项
        choice = input("请选择功能: ").strip()

        if choice == "1":
            # 进入连续查询天气的交互流程
            weather_app.query_loop()
        elif choice == "2":
            # 显示历史查询记录
            weather_app.show_history
        elif choice == "0":
            # 退出程序
            print("感谢使用，再见！")
            break
        else:
            # 输入不合法，给出提示
            print("输入错误，请重新选择。")


# 判断当前脚本是否作为主程序运行（而非被导入为模块）
if __name__ == "__main__":
    # 如果是主程序，则调用 main 函数启动天气查询系统
    main()
