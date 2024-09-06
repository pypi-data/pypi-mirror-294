# -*- coding: utf-8 -*-
"""
@author:lpf
@file: initialize.py
@time: 2024/9/5  16:15
"""
from typing import Optional
from enum import Enum


class AgentType(Enum):
    rag_knowledge_prompt_llm_tools = 'rag_knowledge_prompt_llm_tools'
    tools_prompt_llm = 'tools_prompt_llm'


def initialize_agent(tools: None,
                     llm: None,
                     agent_type: Optional[AgentType] = None,
                     agent_config: Optional[AgentType] = None):
    return True  # FlowModel
