import requests

url = "https://httpbin.org/post"
payload = {"username": "张三", "score": 95, "tags": ["python", "http"]}

try:
    response = requests.post(url, json=payload, timeout=5)
    print(f"状态码:{response.status_code}")
    resp_data = response.json()
    sent_back = resp_data.get("json")
    if sent_back == payload:
        print("✅ 验证通过：服务器返回的数据与发送的 JSON 一致")
    else:
        print("❌ 验证失败：返回数据与发送数据不匹配")
        print("发送:", payload)
        print("返回:", sent_back)
    # 打印完整的响应内容（美化输出）
    import json

    print("\n完整响应:")
    print(json.dumps(resp_data, ensure_ascii=False, indent=2))
except requests.exceptions.Timeout:
    print("请求超时，请检查网络或稍后重试。")
except requests.exceptions.ConnectionError:
    print("连接失败，请检查网络。")
except KeyboardInterrupt:
    print("\n程序被用户手动终止。")
except Exception as e:
    print(f"其他错误: {e}")
