import requests

url = "https://httpbin.org/delay/3"

try:
    response = requests.get(url, timeout=2)
    print(f"状态码: {response.status_code}")
    print("响应内容:", response.text[:100])
except requests.exceptions.Timeout:
    print("请求超时：服务器响应时间过长，请稍后重试。")
except requests.exceptions.ConnectionError:
    print("连接错误：无法连接到服务器，请检查网络。")
except requests.exceptions.RequestException as e:
    print(f"请求过程中发生其他异常: {e}")
