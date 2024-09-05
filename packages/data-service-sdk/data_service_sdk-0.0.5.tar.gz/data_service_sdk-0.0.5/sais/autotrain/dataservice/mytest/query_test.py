# from sais.autotrain.dataservice.auth.auth_info import EnvVarCredentialsProvider
# from sais.autotrain.dataservice.config.const import ENDPOINT
# from sais.autotrain.dataservice.handler.query_handler import QueryStationRelatedHandler, QueryNWPHandler
# from sais.autotrain.dataservice.model.data_model import QueryStationRequest, QueryObservationRequest, QueryNWPRequest

from sais.autotrain.dataservice import EnvVarCredentialsProvider, TrainInferHandler, TrainResultRequest, \
    InferResultRequest
from sais.autotrain.dataservice import ENDPOINT
from sais.autotrain.dataservice import QueryStationRelatedHandler, QueryNWPHandler
from sais.autotrain.dataservice import QueryStationRequest, QueryObservationRequest, QueryNWPRequest

# query_station_related = QueryStationRelatedHandler(endpoint=ENDPOINT, auth_provider=EnvVarCredentialsProvider())
# query_station_result = query_station_related.execute_query_station(QueryStationRequest(
#     ids=["1"],
#     # provinces=["山东"],
#     page=1,
#     page_size=10,
#     query_type=0
# ))
# print(f"Query station result: {query_station_result}")
#
# query_observation_result = query_station_related.execute_query_observation(QueryObservationRequest(
#     ids=["1"],
#     # provinces=["山东"],
#     start_time="2023-01-01 00:00:05",
#     end_time="2024-01-01 00:00:05",
#     page=1,
#     page_size=10,
#     query_type=0
# ))
# print(f"Query observation result: {query_observation_result}")


# 全页遍历
# page = 1
# page_size = 1000
# while True:
#     query_observation_result_item = query_station_related.execute_query_observation(QueryObservationRequest(
#         ids=["1"],
#         # provinces=["山东"],
#         start_time="2023-01-01 00:00:05",
#         end_time="2024-07-01 00:00:05",
#         page=page,
#         page_size=page_size,
#         query_type=0
#     ))
#     if len(query_observation_result_item.records) == 0:
#         break
#     else:
#         print(f"Query observation result: {query_observation_result_item}")
#     page += 1


# query_nwp = QueryNWPHandler(endpoint=ENDPOINT, auth_provider=EnvVarCredentialsProvider())
# query_nwp.execute_query(query_params=QueryNWPRequest(
#     src="ec/gfs",
#     start_time="24010100",
#     period_interval=24,
#     period=365,
#     start_hour=0,
#     end_hour=24,
#     forecast_interval=1,
#     coords=[{"req_lat": 35.0, "req_lon": 109.9}],
#     vars=[
#         "tp",
#         "t2m"
#     ],
#     levels=[
#         "309",
#         "387",
#         "899",
#         "484",
#         "565",
#         "268",
#         "644",
#         "100",
#         "500",
#         "374",
#         "322",
#         "261",
#         "600"
#     ]))


# train_infer_handler = TrainInferHandler(endpoint="http://localhost:10115", auth_provider=EnvVarCredentialsProvider())
# train_result = train_infer_handler.execute_train_result_submit(TrainResultRequest(
#     train_config_id=1,
#     model_name="model1.pkl",
#     data_start_time="2023-01-01 00:00:00",
#     data_end_time="2023-12-31 00:00:00",
#     train_start_time="2024-09-10 10:00:00",
#     train_end_time="2024-09-10 10:10:00",
#     train_status=3,  # 3：成功 4：失败
#     train_error_msg="success"
# ))
# print(f"submit train result: {train_result}")
#
# infer_result = train_infer_handler.execute_infer_result_submit(InferResultRequest(
#     infer_config_id=1,
#     model_id=1,
#     station_id=1,
#     infer_start_time="2024-09-10 10:00:00",
#     infer_end_time="2024-09-10 10:10:00",
#     infer_status=3,  # 3：成功 4：失败
#     infer_error_msg="success",
#     items=[
#         {
#             "time": "2024-09-10 10:00:00",
#             "station_id": 1,
#             "radiation": 11.1,
#             "power": 9.8,
#         }
#     ]
# ))
# print(f"submit infer result: {infer_result}")
