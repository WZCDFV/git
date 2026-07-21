import requests


def request_json(url, timeout=10):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.RequestException, ValueError):
        return None


if __name__ == "__main__":
    url = "https://httpbin.org/get"
    result = request_json(url)
    if result:
        print("状态码: 200")
        print("返回内容:")
        print(result)
    else:
        print("请求失败或返回非JSON数据")
