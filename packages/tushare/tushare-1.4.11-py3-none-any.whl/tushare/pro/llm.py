import json

import requests
try:
    import sseclient
except:
    raise ImportError("sseclient not found, please install it using 'pip install sseclient-py'.")


from tushare import get_token

BASE_URL = "http://api.waditu.com/dataapi"
# BASE_URL = "http://127.0.0.1:8000/dataapi"
API_KEY_PREFIX = "tsgpt-"


class LlmClent:
    def __init__(self, token=None, timetout=120):
        if not token:
            token = get_token()
        self.token = token
        self.timeout = timetout

    def chat_query(self, model, messages, temperature=None, max_tokens=None, pretty=False):
        """
        model string 模型名称， doubao-pro-128k
        messages list 消息列表
            [
                {
                  "role": "user",
                  "content": "Hello World"
                }
            ]
        pretty bool 是否只返回回答内容文本
        """
        resp = requests.post(
            f'{BASE_URL}/llm/{model}',
            json={"params": {
                "stream": False,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }},
            headers={"Authorization": f"tstoken-{self.token}"},
            timeout=self.timeout
        )
        if resp.status_code != 200:
            raise Exception(f"请求出现错误，{resp.content}")

        resp_data = resp.json()
        if resp_data.get('code') not in (0, None):
            raise Exception(resp_data['msg'])
        if pretty:
            return resp_data['choices'][0]["message"]["content"]
        else:
            return resp_data

    def chat_stream(self, model, messages, temperature=None, max_tokens=None, pretty=False):
        """
        model string 模型名称， doubao-pro-128k
        messages list 消息列表
            [
                {
                  "role": "user",
                  "content": "Hello World"
                }
            ]
        pretty bool 是否只返回回答内容文本
        """
        resp = requests.post(
            f'{BASE_URL}/llm/{model}',
            json={"params": {
                "stream": True,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }},
            headers={"Authorization": f"tstoken-{self.token}"},
            timeout=self.timeout, stream=True
        )
        if resp.status_code != 200:
            raise Exception(f"请求出现错误，{resp.content}")

        for e in sseclient.SSEClient(resp).events():
            e_data = json.loads(e.data)
            if pretty:
                yield e_data["choices"][0]["delta"]["content"]
            else:
                yield e_data


def test_chart_query():
    c = LlmClent()
    dd = c.chat_query("doubao-pro-128k", [{
        "role": "user",
        "content": "你好"
    }])
    print(dd)
    dd = c.chat_query("doubao-pro-128k", [{
        "role": "user",
        "content": "你好"
    }], pretty=True)
    print(dd)


def test_chart_stream():
    c = LlmClent()
    dd = c.chat_stream("doubao-pro-128k", [
        {
            "role": "user",
            "content": "你好"
        }
    ])
    for d in dd:
        print(d)

    dd = c.chat_stream("doubao-pro-128k", [
        {
            "role": "user",
            "content": "你好"
        }
    ], pretty=True)
    for d in dd:
        print(d)
