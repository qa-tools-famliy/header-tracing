# -*- coding: UTF-8 -*-
"""
# wrapper for requests, load header and paas to downstream
"""
import os
import functools
from flask import request
from requests.sessions import Session


# 设置默认透传的 headers 中的 key
pass_headers_key = os.getenv("PASS_HEADERS_KEY", "HTTP_EASYENV_ROUTE_KEY")


def instrument():
    """
    # 注入对 requests 请求的注入
    :return:
    """
    wrapped_request = Session.request

    @functools.wraps(wrapped_request)
    def instrumented_request(self, method, url, *args, **kwargs):
        """
        # 与 http.request 保持一致
        :param self:
        :param method:
        :param url:
        :param args:
        :param kwargs:
        :return:
        """
        def get_or_create_headers():
            """
            # 判断原始调用时是否包含headers参数，并将需要透传的 headers 查询并追加至请求体中
            :return:
            """
            headers = kwargs.get("headers")
            if headers is None:
                headers = {}

            request_headers = request.headers
            if pass_headers_key in request_headers:
                headers[pass_headers_key] = request_headers[pass_headers_key]
                kwargs["headers"] = headers

            return headers

        def call_wrapped():
            """
            # 调用原始的请求
            :return:
            """
            return wrapped_request(self, method, url, *args, **kwargs)

        get_or_create_headers()
        return call_wrapped()

    Session.request = instrumented_request
