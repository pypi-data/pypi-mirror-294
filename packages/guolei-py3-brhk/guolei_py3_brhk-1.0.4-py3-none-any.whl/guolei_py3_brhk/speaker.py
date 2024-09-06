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
from typing import Iterable

from addict import Dict
from guolei_py3_requests import requests_request, RequestsResponseCallable
from requests import Response


class RequestsResponseCallable(RequestsResponseCallable):
    @staticmethod
    def status_code_200_json_addict_errcode_0_errmsg_ok(response: Response = None):
        json_addict = RequestsResponseCallable.status_code_200_json_addict(response=response)
        return json_addict.errcode == 0 and json_addict.errmsg == "ok"


class Api(object):
    """
    博瑞皓科 收款云音箱云喇叭 API Class

    See https://www.yuque.com/lingdutuandui/ugcpag/umbzsd?
    """

    def __init__(
            self,
            base_url: str = "https://speaker.17laimai.cn",
            token: str = "",
            id: str = "",
            version: str = "1"
    ):
        """
        :param base_url: base url
        :param token: 代理商的 token, 预先通过安全渠道分配，使得代理商对该  SPEAKERID 有操作权限，强烈推荐做为程序常量隐藏在程序内部。
        :param id: 指该云音箱标签上的的 SN/ID
        :param version: 按音箱标签上标注的VERSION版本，由用户配置时选择，预留1-9供选择
        """
        self._base_url = base_url
        self._token = token
        self._id = id
        self._version = version

    @property
    def base_url(self) -> str:
        """
        base url
        :return:
        """
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, value: str = ""):
        self._base_url = value

    @property
    def token(self) -> str:
        """
        代理商的 token, 预先通过安全渠道分配，使得代理商对该  SPEAKERID 有操作权限，强烈推荐做为程序常量隐藏在程序内部。
        :return:
        """
        return self._token

    @token.setter
    def token(self, value: str = ""):
        self._token = value

    @property
    def id(self) -> str:
        """
        指该云音箱标签上的的 SN/ID
        :return:
        """
        return self._id

    @id.setter
    def id(self, value: str = ""):
        self._id = value

    @property
    def version(self) -> str:
        """
        按音箱标签上标注的VERSION版本，由用户配置时选择，预留1-9供选择
        :return:
        """
        return self._version

    @version.setter
    def version(self, value: str = ""):
        self._version = value

    def notify(
            self,
            message: str = "",
            requests_response_callable=RequestsResponseCallable.status_code_200_json_addict_errcode_0_errmsg_ok,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ) -> bool:
        """
        通知语音播报（不支持WIFI版，流量版专用）

        将通知消息提交到云音箱服务器、服务器将支付结果推送给云音箱，云音箱接收后播报。

        备注：该接口为流量版（2G\4G）音箱专用接口，通过流量版（2G\4G）音箱自带的TTS播放，WIFI版音箱不可用

        @see https://www.yuque.com/lingdutuandui/ugcpag/umbzsd#yG8IS

        :param message: 通知消息内容， 可推送任意中文（多音字可能有误差）、阿拉伯数字、英文字母，限制64个字符以内  。 数字处理策略见3.1.1备注
如果需要断句，则添加逗号“,”编码格式UTF-8
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_errcode_0_errmsg_ok
        :param requests_request_args: requests.request(*requests_request_args,**requests_request_kwargs)
        :param requests_request_kwargs: requests.request(*requests_request_args,**requests_request_kwargs)
        :return: True=发送成功 False=发送失败
        """
        if not isinstance(message, str):
            raise TypeError(f"message:{message} must be str")
        if not len(message):
            raise ValueError(f"message:{message} must be str and not empty")
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict({
            "url": f"{self.base_url}/notify.php",
            "method": "POST",
            "data": {
                "token": self.token,
                "id": self.id,
                "version": self.version,
                "message": message.encode("utf-8"),
            },
            **requests_request_kwargs,
        })
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )
