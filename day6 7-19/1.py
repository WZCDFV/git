import requests

url = "https://httpbin.org/get"
try:
    response = requests.get(url, timeout=5)
    print(response.status_code)
    print(response.text)
except requests.exceptions.Timeout:
    print("请求超时，请检查网络或稍后重试。")
except requests.exceptions.ConnectionError:
    print("连接失败，请检查网络。")
