"""
图书管理系统（控制台版）
功能：
1. 添加图书（防止重名）
2. 查看图书（按价格排序，显示总数量/总价值/平均价格）
3. 查询图书
4. 删除图书（二次确认）
5. 修改图书
6. 借阅管理（借书、还书）
0. 退出
"""
class Book:
    def __init__(self, title: str, author: str, price: float):
        self.title = title.strip()
        self.author = author.strip()
        self.price = price
        self.status = "可借阅"

    def __str__(self):
        # 格式化输出图书信息
        return f"《{self.title}》 | 作者:{self.author} | 价格:{self.price:.2f}元 | 状态:{self.status}"
    def to_dict(self):
        # 转换为字典（备用）
        return {
            "title": self.title,
            "author": self.author,
            "price": self.price,
            "status": self.status
        }

class Library:
    # 图书馆类，管理所有图书
    def __init__(self):
        self.books = []
        # 基础功能
    def add_book(self):
        # 添加图书，防止书名重复
        print("\n--- 添加图书 ---")
        title = input("请输入书名:").strip()
        if not title:
            print("书名不能为空")
            return
        
        # 检查是否已存在同名书籍（忽略大小写和首尾空格）
        if self.find_book(title):
            print(f"添加失败:图书《{title}》已存在!")
            return
        
        author = input("请输入作者:").strip()
        if not author:
            print("作者不能为空!")
            return
        
        try:
            price = float(input("请输入胡价格:"))
            if price < 0:
                print("价格不能为负数!")
                return
        except ValueError:
            print("价格输入错误,必须为数字!")
        new_book = Book(title,author,price)
        self.books.append(new_book)
        print(f"图书《{title}》添加成功!")

    def show_students(self):
        # 显示所有图书（按价格从低到高排序），同时展示总数量、总价值、平均价格
        print("\n--- 查看图书 ---")
        if not self.books:
            print("暂无图书")
            return
        
        # 按价格排序
        sorted_books = sorted(self.books, key=lambda b: b.price)
        print("图书列表（价格从低到高）：")
        for i, book in enumerate(sorted_books, 1):
            print(f"{i}.{book}")

        # 统计信息
        total = len(self.books)
        total_price = sum(book.price for book in self.books)
        avg_price = total_price / total if total > 0 else 0
        print(f"总数量{total}")
        print(f"图书总价值{total_price:.2f}元")
        print(f"平均值{avg_price:.2f}元")

    def search_book(self):
        print("\n--- 查询图书 ---")
        title = input("请输入要查询的书名：").strip()
        if not title:
            print("书名不能为空!")
            return
        book = self._find_book(title)
        if book:
            print("查询结果") 
            print(book)
        else:
            print(f"未找到图书《{title}》")
    
    def delete_book(self):
        print("\n--- 删除图书 ---")
        title = input("请输入要删除的书名：").strip()
        if not title:
            print("书名不能为空!")
            return
        book = self._find_book(title)
        if not book:
            print(f"未找到图书《{title}》")
            return
        # 显示图书信息并确认
        print("将要删除以下图书：")
        print(book)
        confirm = input("确认删除?(y/n)").strip().lower()
        if confirm == "y":
            self.books.remove(book)
            print(f"图书《{title}》已成功删除")
        else:
            print("已取消删除")

    def modify_book(self):
        print("\n--- 修改图书 ---")
        title = input("请输入要修改的图书:")
        if not title:
            print("书名不能为空!")
            return
        book = self._find_book(title)
        if not book:
            print(f"未找到图书《{title}》")
            return
        print("当前图书信息：")
        print(book)
        print("请选择修改项（留空则不修改）：")
        # 修改书名
        new_title = input("新书名: ").strip()
        if new_title and new_title != title:
            print(f"修改失败:书名《{new_title}》已存在!")
            return
        book.title = new_title

        # 修改作者
        new_author = input("新作者:").strip()
        if new_author:
            book.author = new_author

        # 修改价格
        new_price_str = input("新价格: ").strip()
        if new_price_str:
            try:
                new_price = float(new_price_str)
                if new_price < 0:
                    print("价格不能为负数，修改取消！")
                    return
                book.price = new_price
            except ValueError:
                print("修改成功!")
                print(book)
# 借阅管理
    def borrow_book(self):
        # 借书：将可借阅状态改为已借出
        print("\n--- 借书 ---")
        title = input("请输入要借的书名:").strip()
        if not title:
            print(f"未找到图书《{title}》")
            return
        
        book = self._find_book(title)
        if not book:
            print(f"未找到图书《{title}》。")
            return
        if book.status == "已借出":
            print(f"《{title}》已经被借出，暂时无法借阅。")
        else:
            book.status = "已借出"
            print(f"《{title}》借阅成功，状态已改为“已借出”。")

    def return_book(self):
        # 还书：将已借出状态改为可借阅
        print("\n--- 还书 ---")
        title = input("请输入要还的书名;").strip()
        if not title:
            print("书名不能为空！")
            return
        
        book = self._find_book(title)
        if not book:
            print(f"未找到图书《{title}》。")
            return
        
        if book.status == "可借阅":
            print(f"《{title}》当前为可借阅状态，无需归还。")
        else:
            book.status = "可借阅"
            print(f"《{title}》还书成功，状态已改为“可借阅”。")
    
    def borrow_nemu(self):
        # 借阅管理二级菜单
        while True:
            print("\n--- 借阅管理 ---")
            print("1. 借书")
            print("2. 还书")
            print("0. 返回主菜单")
            choice = input("请选择:").strip()
            if choice == "1":
                self.borrow_book()
            elif choice == "2":
                self.return_book()
            elif choice == "0":
                break
            else:
                print("输入错误，请重新选择！")
    
    def _find_book(self,title: str):
        title = title.strip()
        for book in self.books:
            # 比较时统一转为小写，确保不区分大小写
            if book.title.lower() == title.lower():
                return book
        return None
    
    # 主菜单
    def run(self):
        """系统主菜单循环"""
        while True:
            print("\n" + "=" * 40)
            print("======== 图书管理系统 ========")
            print("1. 添加图书")
            print("2. 查看图书")
            print("3. 查询图书")
            print("4. 删除图书")
            print("5. 修改图书")
            print("6. 借阅管理")
            print("0. 退出")
            print("=" * 40)
            choice = input("请选择功能：").strip()

            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.show_books()
            elif choice == "3":
                self.search_book()
            elif choice == "4":
                self.delete_book()
            elif choice == "5":
                self.modify_book()
            elif choice == "6":
                self.borrow_menu()
            elif choice == "0":
                print("感谢使用图书管理系统，再见！")
                break
            else:
                print("输入错误，请输入 0～6 之间的数字。")
# 程序入口
if __name__ == "__main__":
    lib = Library()
    lib.run()


        


        
