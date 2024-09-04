#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
博瑞皓科 Speaker Library
-------------------------------------------------
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/guolei_py3_brhk
=================================================
"""
from typing import Callable

import requests
from addict import Dict


class Api(object):
    """
    博瑞皓科 Speaker Api Class
    """

    def __init__(
            self,
            base_url: str = "https://speaker.17laimai.cn",
            token: str = "",
            id: str = "",
            version: str = "1"
    ):
        """
        @see https://www.yuque.com/lingdutuandui/ugcpag/umbzsd
        :param base_url:
        :param token:
        :param id:
        :param version:
        """
        self._base_url = base_url
        self._token = token
        self._id = id
        self._version = version

    @property
    def base_url(self):
        """
        base url
        :return:
        """
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    def notify(
            self,
            message: str = "",
            requests_request_func_kwargs_url_path: str = "/notify.php",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        @see https://www.yuque.com/lingdutuandui/ugcpag/umbzsd#yG8IS
        :param message:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
        :return:
        """
        if not isinstance(message, str):
            raise TypeError("message must be a string")
        if not len(message):
            raise ValueError("message must be a string and not be empty")
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
        requests_request_func_kwargs.setdefault("method", "POST")
        requests_request_func_kwargs.data = {
            **{
                "token": self.token,
                "id": self.id,
                "version": self.version,
                "message": message.encode("utf-8"),
            },
            **requests_request_func_kwargs.data,
        }
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if json_addict.errcode == 0 and json_addict.errmsg == "ok":
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict({})
