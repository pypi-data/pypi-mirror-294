# -*- coding: utf-8 -*-
"""
@author:lpf
@file: model.py
@time: 2024/9/6  10:38
"""
from enum import Enum


class ModelType(Enum):
    rag_knowledge_prompt_llm_tools = 'rag_knowledge_prompt_llm_tools'
    tools_prompt_llm = 'tools_prompt_llm'


class LLMModeEnum(Enum):
    CHATFLOW = 'chatflow'
    WORKFLOW = 'workflow'
    STEPFLOW = 'stepflow'
    AGENT = 'agent'


class BaseModel(object):
    pass


class ChatModel():
    pass
