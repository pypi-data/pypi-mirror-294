# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2024/8/16 15:01
# @File : endpoint_api_endpoint.py
# @Software: PyCharm
"""
import re
from typing import Optional

endpoint_name_regex = re.compile(
    r'workspaces/(?P<workspaceID>[^/]+)/endpointhubs/(?P<endpointHubName>[^/]+)/endpoints/(?P<localName>[^/]+)'
)


class EndpointName:
    """
    EndpointName
    """
    def __init__(self, workspace_id: str, endpoint_hub_name: str, local_name: str):
        self.workspace_id = workspace_id
        self.endpoint_hub_name = endpoint_hub_name
        self.local_name = local_name

    def get_name(self) -> str:
        """
        获取完整的endpoint name
        :return:
        """
        return f"workspaces/{self.workspace_id}/endpointhubs/{self.endpoint_hub_name}/endpoints/{self.local_name}"


def parse_endpoint_name(name: str) -> Optional[EndpointName]:
    """
    解析endpoint name，返回EndpointName对象
    Args:
        name (str): endpoint name字符串
    Returns:
        Optional[EndpointName]: EndpointName对象
    """
    m = endpoint_name_regex.match(name)
    if not m:
        return None
    return EndpointName(
        workspace_id=m.group('workspaceID'),
        endpoint_hub_name=m.group('endpointHubName'),
        local_name=m.group('localName')
    )
