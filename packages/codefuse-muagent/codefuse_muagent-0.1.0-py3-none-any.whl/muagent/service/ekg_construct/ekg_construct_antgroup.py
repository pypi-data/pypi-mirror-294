from loguru import logger
import re
import json
from typing import List, Dict
import numpy as np
import random
import uuid
from redis.commands.search.field import (
    TextField,
    NumericField,
    VectorField,
    TagField
)
from jieba.analyse import extract_tags


from muagent.schemas.ekg import *
from muagent.schemas.db import *
from muagent.schemas.common import *
from muagent.db_handler import *
from muagent.orm import table_init

from muagent.connector.configs.generate_prompt import *

from muagent.llm_models.llm_config import EmbedConfig, LLMConfig
from muagent.llm_models import *


from muagent.base_configs.env_config import KB_ROOT_PATH

from muagent.llm_models.get_embedding import get_embedding
from muagent.utils.common_utils import getCurrentDatetime, getCurrentTimestap
from muagent.utils.common_utils import double_hashing
from .ekg_construct_base import EKGConstructService



def getClassFields(model):
    # 收集所有字段，包括继承自父类的字段
    all_fields = set(model.__annotations__.keys())
    for base in model.__bases__:
        if hasattr(base, '__annotations__'):
            all_fields.update(getClassFields(base))
    return all_fields



class EKGConstructAntGroupService(EKGConstructService):

    def __init__(
            self, 
            embed_config: EmbedConfig,
            llm_config: LLMConfig,
            db_config: DBConfig = None,
            vb_config: VBConfig = None,
            gb_config: GBConfig = None,
            tb_config: TBConfig = None,
            sls_config: SLSConfig = None,
            do_init: bool = False,
            kb_root_path: str = KB_ROOT_PATH,
        ):
        super().__init__(
            embed_config, llm_config, db_config, vb_config, 
            gb_config, tb_config, sls_config, do_init, kb_root_path
        )

    def alarm2graph(
            self, 
            alarms: List[dict],
            alarm_analyse_content: dict,
            teamid: str,   
            rootid: str,
            graphid: str = "",
            do_save: bool = False,
        ):
        ancestor_list, all_intent_list = self.get_intents_by_alarms(alarms)
        
        graph_datas_by_pathid = {}
        for path_id, diagnose_path in enumerate(alarm_analyse_content["diagnose_path"]):

            content = f"路径:{diagnose_path['name']}\n"
            cur_count = 1
            for idx, step in enumerate(diagnose_path['diagnose_step']):
                step_text = step['content'] if type(step['content']) == str else \
                    step['content']['textInfo']['text']
                step_text = step_text.strip('[').strip(']')
                step_text_no_time = EKGConstructAntGroupService.remove_time(step_text)
                # continue update
                content += f'''{cur_count}. {step_text_no_time}\n'''
                cur_count += 1
            
            result = self.create_ekg(
                content, teamid, service_name="text2graph", rootid=rootid, graphid=graphid,
                intent_nodes=ancestor_list, all_intent_list=all_intent_list, 
                do_save= do_save
            )
            graph_datas_by_pathid[path_id] = result
        
        return self.returndsl(graph_datas_by_pathid, intents=ancestor_list)

    def yuque2graph(self, **kwargs):
        # get yuque loader
        
        # 
        self.create_ekg()
        # yuque_url, write2kg, intent_node

        # get_graph(yuque_url)
        # graph_id from md(yuque_content)

        # yuque_dsl ==|code2graph|==> node_dict, edge_list, abnormal_dict

        # dsl2graph => write2kg
        pass
    
    def dsl2graph(self, ) -> dict:
        # dsl, write2kg, intent_node, graph_id

        # dsl ==|code2graph|==> node_dict, edge_list, abnormal_dict

        # dsl2graph => write2kg
        pass

    def get_intent_by_alarm(self, alarm: dict, ) -> EKGIntentResp:
        '''according content search intent'''
        import requests
        error_type = alarm.get('errorType', '')
        title = alarm.get('title', '')
        content = alarm.get('content', '')
        biz_code = alarm.get('bizCode', '')

        if not error_type or not title or not content or not biz_code:
            return None, None
        
        alarm = {
            'type': 'ANTEMC_DINGTALK',
            'user_input': {
                'bizCode': biz_code,
                'title': title,
                'content': content,
                'execute_type': 'gql',
                'errorType': error_type
            }
        }
        
        body = {
            'features': {
                'query': alarm
            }
        }
        intent_url = 'https://paiplusinferencepre.alipay.com/inference/ff998e48456308a9_EKG_route/0.1'
        headers = {
                'Content-Type': 'application/json;charset=utf-8',
                'MPS-app-name': 'test',
                'MPS-http-version': '1.0'
            }
        ans = requests.post(intent_url, json=body, headers=headers)

        ans_json = ans.json()
        output = ans_json.get('resultMap').get('output')
        logger.debug(f"{body}")
        logger.debug(f"{output}")
        output_json = json.loads(output)
        res = output_json[-1]
        all_intent = output_json
        return res, all_intent
    
    def get_intents(self, alarm_list: list[dict], ) -> EKGIntentResp:
        '''according contents search intents'''
        ancestor_list = set()
        all_intent_list = []
        for alarm in alarm_list:
            ancestor, all_intent = self.get_intent_by_alarm(alarm)
            if ancestor is None:
                continue
            ancestor_list.add(ancestor)
            all_intent_list.append(all_intent)

        return list(ancestor_list), all_intent_list

    def get_intents_by_alarms(self, alarm_list: list[dict], ) -> EKGIntentResp:
        '''according contents search intents'''
        ancestor_list = set()
        all_intent_list = []
        for alarm in alarm_list:
            ancestor, all_intent = self.get_intent_by_alarm(alarm)
            if ancestor is None:
                continue
            ancestor_list.add(ancestor)
            all_intent_list.append(all_intent)

        return list(ancestor_list), all_intent_list

    @staticmethod
    def preprocess_json_contingency(content_dict, remove_time_flag=True):
        # 专门处理告警数据合并成文本
        # 将对应的 content json 预处理为需要的样子，由于可能含有多个 path，用 dict 存储结果
        diagnose_path_list = content_dict.get('diagnose_path', [])
        res = {}
        if diagnose_path_list:
            for idx, diagnose_path in enumerate(diagnose_path_list):
                path_id = idx
                path_name = diagnose_path['name']
                content = f'路径:{path_name}\n'
                cur_count = 1

                for idx, step in enumerate(diagnose_path['diagnose_step']):
                    step_name = step['name']

                    if type(step['content']) == str:
                        step_text = step['content']
                    else:
                        step_text = step['content']['textInfo']['text']
                    
                    step_text = step_text.strip('[')
                    step_text = step_text.strip(']')

                    # step_text = step['step_summary']

                    step_text_no_time = EKGConstructAntGroupService.remove_time(step_text)
                    to_append = f'''{cur_count}. {step_text_no_time}\n'''
                    cur_count += 1

                    content += to_append
                    
                res[path_id] = {
                    'path_id': path_id,
                    'path_name': path_name,
                    'content': content
                }
        return res
    
    @staticmethod
    def remove_time(text):
        re_pat = '''\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}(:\d{2})*'''
        text_res = re.split(re_pat, text)
        res = ''
        for i in text_res:
            if i:
                i_strip = i.strip('，。\n')
                i_strip = f'{i_strip}'
                res += i_strip
        return res
