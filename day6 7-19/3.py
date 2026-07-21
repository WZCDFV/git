def get_status_message(status_code):
    """根据状态码返回对应的提示信息"""
    message = {
        200: "请求成功",
        201: "已创建",
        204: "无内容",
        301: "永久重定向",
        302: "临时重定向",
        400: "请求错误",
        401: "未授权",
        403: "禁止访问",
        404: "未找到",
        405: "方法不允许",
        500: "服务器内部错误",
        502: "网关错误",
        503: "服务不可用",
    }
    return message.get(status_code, f"未知状态码:{status_code}")


print(get_status_message(200))  # 请求成功
print(get_status_message(404))  # 未找到
print(get_status_message(503))  # 服务不可用
print(get_status_message(418))  # 未知状态码: 418
