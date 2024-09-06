# -*- coding: utf-8 -*-
"""
@author:lpf
@file: base_node.py
@time: 2024/9/4  16:46
"""


class BaseNode:

    def __init__(self, node_id, node_type, config):
        self.node_id = node_id
        self.node_type = node_type
        self.title = node_id
        self.config = config
