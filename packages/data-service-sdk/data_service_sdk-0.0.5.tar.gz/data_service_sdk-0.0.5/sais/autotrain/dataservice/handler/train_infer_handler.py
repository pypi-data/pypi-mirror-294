import json
import logging
import os
import time

import requests

from sais.autotrain.dataservice.auth.auth_info import EnvVarCredentialsProvider
from sais.autotrain.dataservice.config.const import LOGGER_NAME, ENDPOINT
from sais.autotrain.dataservice.model.data_model import Task, StatusEnum, QueryNWPRequest, QueryStationRequest, \
    QueryObservationRequest, BaseRsp
from sais.autotrain.dataservice.model.train_infer_model import TrainResultRequest, InferResultRequest

logger = logging.getLogger(LOGGER_NAME)
logging.basicConfig(level=logging.INFO)


class TrainInferHandler(object):
    def __init__(self, endpoint=ENDPOINT, auth_provider: EnvVarCredentialsProvider = None):
        self.endpoint = endpoint
        self.auth_provider = auth_provider

    def execute_train_result_submit(self, result):
        """执行训练结果提交"""
        submit_result = self.submit_train_result(result)
        return submit_result

    def execute_infer_result_submit(self, result):
        """执行推理结果提交"""
        submit_result = self.submit_infer_result(result)
        return submit_result

    def submit_train_result(self, result: TrainResultRequest):
        """提交场站结果"""
        url = f"{self.endpoint}/api/v1/train/result"
        headers = {
            # "Authorization": f"Bearer {self.auth_provider.token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=result.model_dump(by_alias=True, exclude_none=True), headers=headers)
        result_json = response.json()
        if result_json.get('success'):
            logger.info(f"Submit train result successfully.")
            return True
        else:
            logger.error(f"Failed to submit train result. Response: {result_json}")
            return False

    def submit_infer_result(self, result: InferResultRequest) -> bool:
        """提交推理结果"""
        url = f"{self.endpoint}/api/v1/infer/result"
        headers = {
            # "Authorization": f"Bearer {self.auth_provider.token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=result.model_dump(by_alias=True, exclude_none=True), headers=headers)
        result_json = response.json()
        if result_json.get('success'):
            logger.info(f"Submit infer result successfully.")
            return True
        else:
            logger.error(f"Failed to submit infer result. Response: {result_json}")
            return False
