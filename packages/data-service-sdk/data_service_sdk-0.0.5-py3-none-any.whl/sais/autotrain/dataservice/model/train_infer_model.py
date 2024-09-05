from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class TrainResultRequest(BaseModel):
    # id: Optional[str] = None
    train_config_id: int
    model_name: Optional[str] = None
    data_start_time: Optional[str] = None
    data_end_time: Optional[str] = None
    train_start_time: str
    train_end_time: str
    train_status: int
    train_error_msg: Optional[str] = None
    model_config = ConfigDict(
        protected_namespaces=()
    )


class InferEntity(BaseModel):
    time: str
    radiation: Optional[float] = None
    windspeed: Optional[float] = None
    power: Optional[float] = None


class InferResultRequest(BaseModel):
    infer_config_id: int
    model_id: int
    station_id: int
    infer_start_time: str
    infer_end_time: str
    infer_status: int
    infer_error_msg: Optional[str] = None
    items_len: Optional[int] = None
    items: List[InferEntity]
    model_config = ConfigDict(
        protected_namespaces=()
    )
