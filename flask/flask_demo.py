# -*- coding: UTF-8 -*-
"""
# basic flask demo to show how to pass http header to downstream
"""
import os
import requests
from flask import Flask
from request_wrapper import instrument


app = Flask(__name__)

http_port = os.getenv("HTTP_PORT", 8000)
downstream = os.getenv("DOWNSTREAM_URL", "http://www.baidu.com")
instrument()


@app.route("/")
def hello_world():
    """
    # 基本的函数
    :return:
    """
    if downstream:
        response_content = requests.get(downstream).content
    else:
        response_content = "<p>Hello, World!</p>"
    return response_content


if __name__ == "__main__":
    app.run(
        host="0.0.0.0", port=http_port
    )
