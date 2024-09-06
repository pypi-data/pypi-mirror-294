# -*- coding: utf-8 -*-
"""
@author:lpf
@file: workflow.py
@time: 2024/9/6  10:37
"""
# -*- coding: utf-8 -*-
"""
@author:lpf
@file: myagent.py
@time: 2024/9/5  12:45
"""


class LLMAgent:
    """
    step:
        1.prompt
        2.llm(分类)
        3.result
        4.tools ['工作流:分布',llm(并行推荐)] ,
        5.result
    """
    pass


class StartAgent:
    """
    step:
        1.prompt
        2.llm(分类)
        3.result
        4.tools ['工作流:分布',llm(并行推荐),'非冶金']
        5.result
    """
    pass


class ToolsAgent:
    """
    step:
        1.tools（）
        2.prompt
        3.llm(回复)
        4.result
    """
    pass


class WorkFlow(object):

    # 运行workflow
    def run_workflow(self, nodes):
        current_node = nodes[0]
        while True:
            if not current_node:
                break
            if current_node['data'].type == 'end':
                break
            result = self.run_workflow_node(current_node)
            next_node = {}
            current_node = next_node
        result = current_node
        return result

    # 运行节点
    def run_workflow_node(self, current_node):
        node_data = current_node['data']
        if len(node_data) > 1:
            return {}
        elif len(node_data) == 1:
            return {}
        else:
            return {}


if __name__ == '__main__':
    input = {
        'session_id': '1',
        'message_id': '1',
        'toward': 'input',  # input or output

        'model_id': "",
        'model_type': "",  # 分类 或llm
        'model_name': "",  # 分类 或llm

        'input_type': 'text',  # text file
        'questions': [],  # {'content':'使用仿真完成任务'}
        'file': '',  # file文件,目前传递的是文件路径'f:/test.xlsx'
        'created_at': '',
        'updated_at': '',
        # 控制
        "stream": True,  # 是否是流式输出
        "client_stop": False,  # 主动结束对话
        "flow_stop": False,  # 主动结束流程
    }

    config = {
        'graphs': {  # 图
            'nodes': [{
                'id': 'node_1',
                'type': 'node_type',
                'height': 240,
                'width': 240,
                'selected': False,
                'sourcePosition': "right",
                'targetPosition': "left",
                'position': {'x': 100, 'y': 50},
                'data': [{
                    'type': 'start',  # start,llm,http,
                    'title': '开始',
                }]
            }
            ],
            'edges': [{
                'id': "1725502303931-1-1725502306040-target",
                'type': "custom",
                'source': "1725502303931",
                'sourceHandle': "1",
                'target': "1725502306040",
                'targetHandle': "target",
                'zIndex': 0,
                'data': [{
                    'isInIteration': False,
                    'sourceType': "question-classifier",
                    'targetType': "end"
                }]
            }
            ]
        },
        'draft': {  # 草稿:graphs图
            'nodes': [{
                'id': 'node_1',
                'type': 'node_type',
                'height': 240,
                'width': 240,
                'selected': False,
                'sourcePosition': "right",
                'targetPosition': "left",
                'position': {'x': 100, 'y': 50},
                'data': [{
                    'type': 'start',  # start,llm,http,
                    'title': '开始',
                }]
            }
            ],
            'edges': [{
                'id': "1725502303931-1-1725502306040-target",
                'type': "custom",
                'source': "1725502303931",
                'sourceHandle': "1",
                'target': "1725502306040",
                'targetHandle': "target",
                'zIndex': 0,
                'data': [{
                    'isInIteration': False,
                    'sourceType': "question-classifier",
                    'targetType': "end"
                }]
            }
            ]
        },
    }

    nodes = config['graphs']['nodes']

    if input:
        agent = ToolsAgent
    else:
        agent = ToolsAgent
