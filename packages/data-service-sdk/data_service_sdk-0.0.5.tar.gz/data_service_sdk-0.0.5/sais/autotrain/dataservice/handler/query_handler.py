import json
import logging
import os
import time

import requests

from sais.autotrain.dataservice.auth.auth_info import EnvVarCredentialsProvider
from sais.autotrain.dataservice.config.const import LOGGER_NAME, ENDPOINT
from sais.autotrain.dataservice.model.data_model import Task, StatusEnum, QueryNWPRequest, QueryStationRequest, \
    QueryObservationRequest, BaseRsp

logger = logging.getLogger(LOGGER_NAME)
logging.basicConfig(level=logging.INFO)


class QueryNWPHandler(object):
    def __init__(self, endpoint=ENDPOINT, auth_provider: EnvVarCredentialsProvider = None):
        self.endpoint = endpoint
        self.auth_provider = auth_provider

    def submit_query_task(self, query: QueryNWPRequest):
        """提交查询任务并返回任务ID"""
        url = f"{self.endpoint}/api/v1/query"
        headers = {
            # "Authorization": f"Bearer {self.auth_provider.token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=query.model_dump(by_alias=True, exclude_none=True), headers=headers)
        query_result_json = response.json()
        if query_result_json.get('success'):
            logger.info(f"Query task submitted successfully. Task ID: {query_result_json.get('data').get('task_id')}")
            return query_result_json.get('data').get('task_id')
        else:
            logger.error(f"Failed to submit query task. Response: {query_result_json}")
            raise ValueError(f"Failed to submit query task.")

    def query_task_status(self, task_id):
        """通过任务ID查询任务状态"""
        url = f"{self.endpoint}/api/v1/query/{task_id}"
        headers = {
            # "Authorization": f"Bearer {self.auth_provider.token}"
        }
        response = requests.get(url, headers=headers)
        query_result_json = response.json()
        if query_result_json.get('success'):
            logger.info(f"Query task status: {query_result_json.get('data')}")
            return Task(**query_result_json.get('data'))
        else:
            logger.error(f"Failed to query task status. Response: {query_result_json}")
            raise ValueError(f"Failed to query task status.{query_result_json.get('msg')}")

    def wait_for_task_completion(self, task_id, poll_interval=5):
        """
        轮询查询任务状态直到任务完成
        状态：
            - PENDING: 等待执行
            - RUNNING: 执行中
            - FINISHED: 完成（已成功生成json文件）
            - FAILED: 失败
        """
        while True:
            task = self.query_task_status(task_id)
            if task.status == StatusEnum.FINISHED:
                if os.path.exists(task.file_path):
                    with open(task.file_path, 'r') as file:
                        return json.load(file)
                else:
                    return None
            elif task.status == StatusEnum.FAILED:
                raise Exception(f"Query task failed. Task ID: {task.task_id}")
            time.sleep(poll_interval)  # 轮询间隔

    def execute_query(self, query_params):
        """封装的查询功能函数，提交查询任务并轮询直到返回任务状态结果"""
        task_id = self.submit_query_task(query_params)
        print(f"Query task submitted with task ID: {task_id}")
        return self.wait_for_task_completion(task_id)


class QueryStationRelatedHandler(object):
    def __init__(self, endpoint=ENDPOINT, auth_provider: EnvVarCredentialsProvider = None):
        self.endpoint = endpoint
        self.auth_provider = auth_provider

    def execute_query_station(self, query_params):
        """封装的查询功能函数，提交查询任务并轮询直到返回任务状态结果"""
        station_data = self.submit_query_station(query_params)
        return station_data

    def execute_query_observation(self, query_params):
        """封装的查询功能函数，提交查询任务并轮询直到返回任务状态结果"""
        observation_data = self.submit_query_observation(query_params)
        return observation_data

    def submit_query_observation(self, query: QueryObservationRequest):
        """提交观测查询"""
        url = f"{self.endpoint}/api/v1/observation/query"
        headers = {
            # "Authorization": f"Bearer {self.auth_provider.token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=query.model_dump(by_alias=True, exclude_none=True), headers=headers)
        query_result_json = response.json()
        if query_result_json.get('success'):
            logger.info(f"Query observation submitted successfully.")
            return BaseRsp(**query_result_json.get('data'))
        else:
            logger.error(f"Failed to submit query observation. Response: {query_result_json}")
            raise ValueError(f"Failed to submit query observation.{query_result_json.get('msg')}")

    def submit_query_station(self, query: QueryStationRequest):
        """提交场站查询"""
        url = f"{self.endpoint}/api/v1/station/query"
        headers = {
            # "Authorization": f"Bearer {self.auth_provider.token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=query.model_dump(by_alias=True, exclude_none=True), headers=headers)
        query_result_json = response.json()
        if query_result_json.get('success'):
            logger.info(f"Query station submitted successfully.")
            return BaseRsp(**query_result_json.get('data'))
        else:
            logger.error(f"Failed to submit query station. Response: {query_result_json}")
            raise ValueError(f"Failed to submit query station.{query_result_json.get('msg')}")



