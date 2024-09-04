#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
qywx Webhook Class Library
-------------------------------------------------
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/guolei_py3_qywx
=================================================
"""
from typing import Callable, Iterable

import requests
from addict import Dict


class Api(object):
    """
    企业微信 群机器人 Webhook Api Class
    @see https://developer.work.weixin.qq.com/document/pa    th/91770
    """

    def __init__(
            self,
            base_url: str = "https://qyapi.weixin.qq.com/cgi-bin/webhook",
            key: str = "",
            mentioned_list: list = [],
            mentioned_mobile_list: list = []
    ):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770
        :param base_url: base url
        :param key: key
        :param mentioned_list:
        :param mentioned_mobile_list:
        """
        self._base_url = base_url
        self._key = key
        self._mentioned_list = mentioned_list
        self._mentioned_mobile_list = mentioned_mobile_list

    @property
    def base_url(self):
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def mentioned_list(self):
        return self._mentioned_list

    @mentioned_list.setter
    def mentioned_list(self, value):
        self._mentioned_list = value

    @property
    def mentioned_mobile_list(self):
        return self._mentioned_mobile_list

    def send(
            self,
            requests_request_func_kwargs_url_path="/send",
            requests_request_func_kwargs_json: dict = None,
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        if not isinstance(self.base_url, str):
            raise TypeError("self.base_url must be a string")
        if not len(self.base_url):
            raise ValueError("self.base_url must be a string and not empty")
        if not isinstance(self.key, str):
            raise TypeError("self.key must be a string")
        if not len(self.key):
            raise ValueError("self.key must be a string and not empty")
        requests_request_func_kwargs_json = Dict(requests_request_func_kwargs_json)
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
        requests_request_func_kwargs.setdefault("method", "POST")
        requests_request_func_kwargs.json = Dict(
            **requests_request_func_kwargs_json,
            **requests_request_func_kwargs.json,
        )
        requests_request_func_kwargs.params = Dict({
            **{
                "key": self.key,
            },
            **requests_request_func_kwargs.params,
        })
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if json_addict.errcode == 0 and json_addict.errmsg == "ok":
                return True, response.status_code, json_addict
        return False, response.status_code, Dict({})

    def send_text(
            self,
            content: str = "",
            mentioned_list: list = [],
            mentioned_mobile_list: list = [],
            send_func_kwargs: dict = {}
    ):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%96%87%E6%9C%AC%E7%B1%BB%E5%9E%8B
        :param content:
        :param mentioned_list:
        :param mentioned_mobile_list:
        :param send_func_kwargs:
        :return:
        """
        if not isinstance(self.mentioned_list, list):
            self.mentioned_list = []
        if not isinstance(self.mentioned_mobile_list, list):
            self.mentioned_mobile_list = []
        send_func_kwargs = Dict(send_func_kwargs)
        send_func_kwargs.requests_request_func_kwargs_json = Dict({
            "msgtype": "text",
            "text": {
                "content": content,
                "mentioned_list": self.mentioned_list + mentioned_list,
                "mentioned_mobile_list": self.mentioned_mobile_list + mentioned_mobile_list,
            }
        })
        return self.send(**send_func_kwargs)

    def send_markdown(
            self,
            content: str = "",
            mentioned_list: list = [],
            mentioned_mobile_list: list = [],
            send_func_kwargs: dict = {}
    ):
        """
        https://developer.work.weixin.qq.com/document/path/91770#markdown%E7%B1%BB%E5%9E%8B
        :param content:
        :param mentioned_list:
        :param mentioned_mobile_list:
        :param send_func_kwargs:
        :return:
        """
        if not isinstance(self.mentioned_list, list):
            self.mentioned_list = []
        if not isinstance(self.mentioned_mobile_list, list):
            self.mentioned_mobile_list = []
        send_func_kwargs = Dict(send_func_kwargs)
        send_func_kwargs.requests_request_func_kwargs_json = Dict({
            "msgtype": "markdown",
            "markdown": {
                "content": content,
                "mentioned_list": self.mentioned_list + mentioned_list,
                "mentioned_mobile_list": self.mentioned_mobile_list + mentioned_mobile_list,
            }
        })
        return self.send(**send_func_kwargs)

    def send_file(
            self,
            media_id: str = "",
            mentioned_list: list = [],
            mentioned_mobile_list: list = [],
            send_func_kwargs: dict = {}
    ):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%96%87%E4%BB%B6%E7%B1%BB%E5%9E%8B
        :param media_id:
        :param mentioned_list:
        :param mentioned_mobile_list:
        :param send_func_kwargs:
        :return:
        """
        if not isinstance(self.mentioned_list, list):
            self.mentioned_list = []
        if not isinstance(self.mentioned_mobile_list, list):
            self.mentioned_mobile_list = []
        send_func_kwargs = Dict(send_func_kwargs)
        send_func_kwargs.requests_request_func_kwargs_json = Dict({
            "msgtype": "file",
            "file": {
                "media_id": media_id,
                "mentioned_list": self.mentioned_list + mentioned_list,
                "mentioned_mobile_list": self.mentioned_mobile_list + mentioned_mobile_list,
            }
        })
        return self.send(**send_func_kwargs)

    def send_voice(
            self,
            media_id: str = "",
            mentioned_list: list = [],
            mentioned_mobile_list: list = [],
            send_func_kwargs: dict = {}
    ):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E8%AF%AD%E9%9F%B3%E7%B1%BB%E5%9E%8B
        :param media_id:
        :param mentioned_list:
        :param mentioned_mobile_list:
        :param send_func_kwargs:
        :return:
        """
        if not isinstance(self.mentioned_list, list):
            self.mentioned_list = []
        if not isinstance(self.mentioned_mobile_list, list):
            self.mentioned_mobile_list = []
        send_func_kwargs = Dict(send_func_kwargs)
        send_func_kwargs.requests_request_func_kwargs_json = Dict({
            "msgtype": "voice",
            "voice": {
                "media_id": media_id,
                "mentioned_list": self.mentioned_list + mentioned_list,
                "mentioned_mobile_list": self.mentioned_mobile_list + mentioned_mobile_list,
            }
        })
        return self.send(**send_func_kwargs)

    def upload_media(
            self,
            requests_request_func_kwargs_url_path="/upload_media",
            requests_request_kwargs_files=None,
            requests_request_func_kwargs_params_type: str = "file",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0%E6%8E%A5%E5%8F%A3
        :param requests_request_func_kwargs_url_path:
        :param requests_request_kwargs_files:
        :param requests_request_func_kwargs_params_type:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
        :return:
        """
        if not isinstance(self.base_url, str):
            raise TypeError("self.base_url must be a string")
        if not len(self.base_url):
            raise ValueError("self.base_url must be a string and not empty")
        if not isinstance(self.key, str):
            raise TypeError("self.key must be a string")
        if not len(self.key):
            raise ValueError("self.key must be a string and not empty")
        if not isinstance(requests_request_func_kwargs_params_type, str):
            requests_request_func_kwargs_params_type = "file"
        if requests_request_func_kwargs_params_type.lower() not in ["file", "voice"]:
            requests_request_func_kwargs_params_type = "file"
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
        requests_request_func_kwargs.setdefault("method", "POST")
        requests_request_func_kwargs.files = requests_request_kwargs_files
        requests_request_func_kwargs.params = Dict({
            **{
                "key": self.key,
                "type": requests_request_func_kwargs_params_type,
            },
            **requests_request_func_kwargs.params,
        })
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if json_addict.errcode == 0 and json_addict.errmsg == "ok":
                return True, response.status_code, json_addict
        return False, response.status_code, Dict({})
