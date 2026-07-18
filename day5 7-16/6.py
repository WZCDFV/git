import json
import os
from datetime import datetime


class Record:
    """单条账单记录（数据模型层）"""

    def __init__(self, record_type, money, remark, date=None):
        self.type = record_type
        self.money = float(money)
        self.remark = remark
        # 统一使用 date 字段，如果未传则使用今天
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        """序列化：将对象转成字典"""
        return {
            "type": self.type,
            "money": self.money,
            "remark": self.remark,
            "date": self.date,
        }

    @staticmethod
    def from_dict(data):
        """反序列化：从字典创建 Record 对象"""
        return Record(
            record_type=data["type"],
            money=data["money"],
            remark=data.get("remark", ""),
            date=data.get("date", ""),
        )

    def __str__(self):
        return f"{self.date} | {self.type} | ￥{self.money:.2f} | {self.remark}"


class AccountBook:
    """记账本管理类（业务逻辑层 + 控制层）"""

    def __init__(self, filename="account.json"):
        self.filename = filename
        self.records = []

    # ---------- 持久化 ----------
    def load(self):
        """从 JSON 文件加载数据"""
        if not os.path.exists(self.filename):
            print("未找到数据文件，已创建新账本。")
            self.records = []
            return
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.records = [Record.from_dict(item) for item in data]
            print(f"数据加载成功，共 {len(self.records)} 条记录。")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"数据文件损坏或格式错误：{e}，已清空账本。")
            self.records = []
        except Exception as e:
            print(f"加载数据时发生未知错误：{e}")
            self.records = []

    def save(self):
        """将内存中的记录写入 JSON 文件"""
        try:
            data = [record.to_dict() for record in self.records]  # 修正：调用 to_dict
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"保存失败: {e}")
        except Exception as e:
            print(f"保存时发生未知错误：{e}")

    # ---------- 显示与输入验证 ----------
    @staticmethod
    def print_header():
        """打印表格表头"""
        print("-" * 60)
        print(f"{'序号':<6}{'日期':<12}{'类型':<8}{'金额':<12}{'备注'}")
        print("-" * 60)

    def display_records(self, records, show_index=True):
        """显示记录列表"""
        if not records:
            print("暂无记录")
            return
        self.print_header()
        for idx, record in enumerate(records, start=1):
            if show_index:
                print(
                    f"{idx:<6}{record.date:<12}{record.type:<8}￥{record.money:<11.2f}{record.remark}"
                )
            else:
                print(
                    f"{'':<6}{record.date:<12}{record.type:<8}￥{record.money:<11.2f}{record.remark}"
                )
        print("-" * 60)

    @staticmethod
    def input_money(prompt="请输入金额："):
        """输入金额，验证为正数"""
        while True:
            s = input(prompt).strip()
            if not s:
                print("金额不能为空，请重新输入。")
                continue
            try:
                val = float(s)
                if val <= 0:
                    print("金额必须为正数，请重新输入。")
                    continue
                return val
            except ValueError:
                print("输入无效，请输入数字（例如 100 或 99.9）。")

    @staticmethod
    def input_date(prompt="请输入日期（格式 YYYY-MM-DD，留空为今天）: "):
        """输入日期，验证格式"""
        today = datetime.now().strftime("%Y-%m-%d")
        while True:
            s = input(prompt).strip()
            if not s:
                return today
            try:
                datetime.strptime(s, "%Y-%m-%d")
                return s
            except ValueError:
                print("日期格式错误，请按 YYYY-MM-DD 格式输入（例如 2025-01-15）。")

    # ---------- 核心功能 ----------
    def add(self):
        """添加账单"""
        print("\n--- 添加账单 ---")
        while True:
            t = input("请输入类型（收入/支出）：").strip()
            if t in ("收入", "支出"):
                break
            print("类型只能为“收入”或“支出”，请重新输入。")
        money = self.input_money("请输入金额：")
        remark = input("请输入备注：").strip()
        if not remark:
            remark = "无"
        date = self.input_date()
        record = Record(record_type=t, money=money, remark=remark, date=date)
        self.records.append(record)
        self.save()
        print("记录添加成功！")

    def delete(self):
        """删除账单"""
        if not self.records:
            print("当前没有任何记录，无法删除。")
            return
        print("\n--- 删除账单 ---")
        self.display_records(self.records)
        while True:
            choice = input("请输入要删除的序号（输入 0 取消）：").strip()
            if choice == "0":
                print("已取消删除")
                return
            if not choice.isdigit():
                print("请输入有效数字")
                continue
            index = int(choice) - 1
            if 0 <= index < len(self.records):
                confirm = (
                    input(f"确定要删除以下记录吗？(y/n)\n{self.records[index]}\n")
                    .strip()
                    .lower()
                )
                if confirm == "y":
                    removed = self.records.pop(index)
                    self.save()
                    print(f"已删除：{removed}")
                else:
                    print("已取消")
                return
            else:
                print(f"序号超出范围（1~{len(self.records)}），请重新输入。")

    def modify(self):
        """修改账单"""
        if not self.records:
            print("当前没有任何记录，无法修改")
            return
        print("\n--- 修改账单 ---")
        self.display_records(self.records)
        while True:
            choice = input("请输入要修改的序号（输入 0 取消）：").strip()
            if choice == "0":
                print("已取消修改")
                return
            if not choice.isdigit():
                print("请输入有效数字")
                continue
            index = int(choice) - 1
            if 0 <= index < len(self.records):
                record = self.records[index]
                print("当前记录信息：")
                print(record)
                print("请输入新的信息（直接回车保留原值）。")
                # 修改类型
                new_type = input(f"类型（收入/支出）[{record.type}]：").strip()
                if new_type:
                    if new_type in ("收入", "支出"):
                        record.type = new_type
                    else:
                        print("类型无效，已保留原值。")
                # 修改金额
                money_str = input(f"金额[{record.money:.2f}]：").strip()
                if money_str:
                    try:
                        new_money = float(money_str)
                        if new_money <= 0:
                            print("金额必须为正数，已保留原值。")
                        else:
                            record.money = new_money
                    except ValueError:
                        print("金额格式错误，已保留原值。")
                # 修改备注
                new_remark = input(f"备注[{record.remark}]：").strip()
                if new_remark:
                    record.remark = new_remark
                # 修改日期
                new_date = input(f"日期（YYYY-MM-DD）[{record.date}]：").strip()
                if new_date:
                    try:
                        datetime.strptime(new_date, "%Y-%m-%d")
                        record.date = new_date
                    except ValueError:
                        print("日期格式错误，已保留原值。")
                self.save()
                print("修改成功！")
                return
            else:
                print(f"序号超出范围（1~{len(self.records)}），请重新输入。")

    def show_all(self):
        """查看账单（排序/筛选）"""
        if not self.records:
            print("暂无记录。")
            return
        print("\n--- 查看账单 ---")
        print("1. 显示全部（按日期排序）")
        print("2. 按金额从高到低排序")
        print("3. 按金额从低到高排序")
        print("4. 只显示收入")
        print("5. 只显示支出")
        print("0. 返回")
        choice = input("请选择查看方式：").strip()
        if choice == "1":
            sorted_records = sorted(self.records, key=lambda r: r.date, reverse=True)
            self.display_records(sorted_records)
        elif choice == "2":
            sorted_records = sorted(self.records, key=lambda r: r.money, reverse=True)
            self.display_records(sorted_records)
        elif choice == "3":
            sorted_records = sorted(self.records, key=lambda r: r.money)
            self.display_records(sorted_records)
        elif choice == "4":
            income_records = [r for r in self.records if r.type == "收入"]
            if not income_records:
                print("没有收入记录。")
            else:
                self.display_records(income_records)
        elif choice == "5":
            expense_records = [r for r in self.records if r.type == "支出"]
            if not expense_records:
                print("没有支出记录")
            else:
                self.display_records(expense_records)
        elif choice == "0":
            return
        else:
            print("输入错误，请重新选择。")

    def statistics(self):
        """统计信息"""
        total_income = sum(r.money for r in self.records if r.type == "收入")
        total_expense = sum(r.money for r in self.records if r.type == "支出")
        balance = total_income - total_expense
        print("\n--- 统计信息 ---")
        print(f"总记录数：{len(self.records)}")
        print(f"总收入：￥{total_income:.2f}")
        print(f"总支出：￥{total_expense:.2f}")
        print(f"当前余额：￥{balance:.2f}")

    # ---------- 主循环 ----------
    def run(self):
        """启动交互式主循环"""
        self.load()
        while True:
            print("\n" + "=" * 30)
            print("       记账本 (v2.0)")
            print("=" * 30)
            print("1. 添加账单")
            print("2. 查看账单")
            print("3. 修改账单")
            print("4. 删除账单")
            print("5. 统计信息")
            print("0. 退出")
            print("=" * 30)
            choice = input("请选择功能：").strip()
            if choice == "1":
                self.add()
            elif choice == "2":
                self.show_all()
            elif choice == "3":
                self.modify()
            elif choice == "4":
                self.delete()
            elif choice == "5":
                self.statistics()
            elif choice == "0":
                self.save()
                print("记账本已关闭，数据已保存。再见！")
                break
            else:
                print("无效选项，请输入 0~5 之间的数字。")


# ---------- 程序入口 ----------
if __name__ == "__main__":
    app = AccountBook()
    app.run()
