import requests
import json

def get_response_data(url, Bearer_token, To_send, **kwargs):
    headers = {
        "Authorization": f"Bearer {Bearer_token}",
        "Content-Type": "application/json"
    }
    # 如果有额外的变量参数，添加到请求数据中
    if 'variables' in kwargs:
        variables = kwargs['variables']
        data = {
        "messages": [
            {
                "dataId": "s76n1kps9gn4yg14n2ojp",
                "role": "user",
                "content": json.dumps(To_send, ensure_ascii=False)
            }
        ],
        "responseChatItemId": "awvm21nnzhrsnoer28",
        "chatId": "OzFzcGPhMWe1Dl9c4o",
        "detail": True,
        "stream": False,
        "variables": variables
    }
    else:
        data = {
            "messages": [
                {
                    "dataId": "s76n1kps9gn4yg14n2ojp",
                    "role": "user",
                    "content": json.dumps(To_send, ensure_ascii=False)
                }
            ],
            "responseChatItemId": "awvm21nnzhrsnoer28",
            "chatId": "OzFzcGPhMWe1Dl9c4o",
            "detail": True,
            "stream": False,
            
        }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        return {"error": f"Request failed with status code {response.status_code}"}
    text_output = response.json()['responseData'][-1]["textOutput"]
    
    # 解析JSON字符串为Python对象
    try:
        return json.loads(text_output)  # 这里是关键！
    except json.JSONDecodeError:
        # 如果不是有效JSON，返回原始字符串
        return {"raw_text": text_output}

