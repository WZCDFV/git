"""
天气查询项目 (控制台版)
功能：
1. 查询城市实时天气（温度、体感温度、最高/最低温、湿度、风速、天气描述）
2. 支持连续查询多个城市
3. 查询失败时自动提示重试
4. 保存最近 10 次查询记录到 history.json
5. 启动时加载历史记录，可查看历史
数据来源：wttr.in 免费天气 API
"""

import requests
import json
import os
from datetime import datetime


class Weather:
    """天气查询类，封装 API 调用、数据解析和历史记录管理"""

    def __init__(self, history_file="history,json"):
        """初始化：设置历史记录文件路径，加载已有记录"""
        self.history_file = history_file
        self.history = []
        self.max_history = 10
        self.load_history()

    # ---------- 历史记录管理 ----------
    # load_history（读取 JSON）
    def load_history(self):
        """从 JSON 文件加载历史记录，若文件不存在或格式错误则初始化为空"""
        if not os.path.exists(self.history_file):
            self.history = []
            return

        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                self.history = json.load(f)
            if not isinstance(self.history, list):
                self.history = []
        except (json.JSONDecodeError, IOError):
            self.history = []

    # save_history（写入 JSON）
    def save_history(self):
        """将当前历史记录保存到 JSON 文件"""
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"历史记录保存失败：{e}")

    # add_to_history（添加记录并自动裁剪）
    def add_to_history(self, city, weather_info):
        """添加一条查询记录，并保持最近 max_history 条"""
        record = {
            "city": city,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "temperature": weather_info.get("temperature"),
            "description": weather_info.get("description"),
        }
        self.history.insert(0, record)
        if len(self.history) > self.max_history:
            self.history = self.history[: self.max_history]
        self.save_history()

    # show_history（显示历史）
    def show_history(self):
        """打印历史查询记录"""
        if not self.history:
            print("\n暂无历史记录。")
            return
        print("\n--- 最近查询记录 ---")
        for i, record in enumerate(self.history, 1):
            print(
                f"{i}. {record['time']} | {record['city']} | {record['temperature']} | {record['description']} "
            )
            print("_" * 30)

    # ---------- 天气查询核心 ----------
    def search(self, city):
        """
        根据城市名查询天气，返回包含详细信息的字典。
        若查询失败（网络错误、解析错误、城市不存在等）则返回 None。
        """
        url = f"https://wttr.in/{city}?format=j1"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return None
            data = response.json()  # 解析 JSON 字符串
        except requests.exceptions.RequestException:  # 网络超时、连接失败、DNS 错误
            return None
        except json.JSONDecodeError:  # 返回的不是 JSON（比如 404 页面 HTML）
            return None

        # ---------- 提取关键数据 ----------
        try:
            current = data["current_condition"][0]
            today = data["weather"][0]
            # 构造返回字典，注意 wttr.in 返回的是字符串数字，我们直接拼接单位
            weather_info = {
                "temperature": current["temp_C"] + "°C",
                "feels_like": current["FeelsLikeC"] + "°C",  # 体感温度
                "max_temp": today["maxtempC"] + "°C",  # 最高温
                "min_temp": today["mintempC"] + "°C",  # 最低温
                "humidity": current["humidity"] + "%",  # 湿度
                "wind_speed": current["windspeedKmph"] + " km/h",  # 风速
                "description": current["weatherDesc"][0]["value"],  # 天气描述（如 "晴")
            }
            return weather_info
        except (KeyError, IndexError, TypeError):
            return None

    @staticmethod
    def display_weather(city, info):
        """格式化显示天气信息"""
        print(f"\n{'='*30}")
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
            city = input("请输入城市名:").strip()
            if city.lower() == "q":
                break
            if not city:
                print("城市名不能为空，请重新输入。")
                continue
            print(f"正在查询 {city} 的天气...")
            info = self.search(city)
            if info is None:
                print(f"查询失败，请检查城市名是否正确，或稍后重试。")
                continue
            self.display_weather(city, info)
            self.add_to_history(city, info)

    # ---------- 主程序 ----------


def main():
    weather_app = Weather()  # 实例化，自动加载 history.json

    while True:
        print("\n" + "=" * 30)
        print("       天气查询系统")
        print("=" * 30)
        print("1. 查询天气")
        print("2. 查看历史记录")
        print("0. 退出")
        print("=" * 30)
        choice = input("请选择功能：").strip()

        if choice == "1":
            weather_app.query_loop()  # 进入子菜单
        elif choice == "2":
            weather_app.show_history()
        elif choice == "0":
            print("感谢使用，再见！")
            break
        else:
            print("输入错误，请重新选择。")


if __name__ == "__main__":
    main()
