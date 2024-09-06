# -*- coding: utf-8 -*-
"""
@author:lpf
@file: test.py
@time: 2024/9/4  16:46
"""

import asyncio
import os

from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent

# 提供好的浏览器自动化工具
from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from langchain.tools.playwright.utils import (
create_async_playwright_browser,
create_sync_playwright_browser
)

import nest_asyncio

from settings import API_KEY, BASE_ADDRESS

nest_asyncio.apply()

os.environ["LANGCHAIN_TRACING"] = "true"

async_browser = create_async_playwright_browser(headless=False)
browser_toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
tools = browser_toolkit.get_tools()

llm = ChatOpenAI(model_name="gpt-3.5-turbo-0613", temperature=0, openai_api_key=API_KEY, openai_api_base=BASE_ADDRESS)

# 初始化一个Structured类型的Agent
agent_chain = initialize_agent(tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)


async def run():
    response = await agent_chain.arun(input="打开百度，并看一下网页标题")
    print(response)


if __name__ == '__main__':
    asyncio.run(run())
