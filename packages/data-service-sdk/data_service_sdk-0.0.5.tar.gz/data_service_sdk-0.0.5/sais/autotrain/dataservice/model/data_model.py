from decimal import Decimal
from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, Field


class Coordinate(BaseModel):
    req_lat: float
    req_lon: float


class QueryNWPRequest(BaseModel):
    """
    Query request model
    src: str - 数据源，如：ec、gfs
    start_time: str - 数据源发布起始时间，如：24010100，24年01月01号00点
    period_interval: int - 相邻两次的发布时间，如：24，单位：小时
    period: int - 从发布起始时间往后取的发布时次长度，如：365
    start_hour: int - 单次发布时间点往后取的时间点起点，如：0，单位：小时
    end_hour: int - 单次发布时间点往后取的时间点起点，如：24，单位：小时
    forecast_interval: int - 数据点的时间间隔，如：1，单位：hour
    req_lat: float - 请求的纬度，如：35.0
    req_lon: float - 请求的经度，如：109.9
    vars: List[str] - 变量列表，如：['t2m']
    levels: List[str] - 层列表，如：['100']
    """
    src: str
    start_time: str
    period_interval: int
    period: int
    start_hour: int
    end_hour: int
    forecast_interval: int
    # req_lat: float
    # req_lon: float
    coords: List[Coordinate]
    vars: List[str]
    levels: Optional[List[str]] = None


class QueryStationRequest(BaseModel):
    query_type: int = Field(default=0, description="查询类型，0：基于场站查询，1：基于子场查询 ")
    ids: list[int] = Field(default=[], description="场站或子场id列表")
    provinces: list[str] = Field(default=[], description="省份列表")
    page: int = Field(default=1, description="页码")
    page_size: int = Field(default=500, description="每页条数")


class QueryObservationRequest(BaseModel):
    query_type: int = Field(default=0, description="查询类型，0：基于场站查询，1：基于子场查询")
    ids: list[int] = Field(default=[], description="场站或子场id列表")
    provinces: list[str] = Field(default=[], description="省份列表")
    start_time: str = Field(description="开始时间")
    end_time: str = Field(description="结束时间")
    page: int = Field(default=1, description="页码")
    page_size: int = Field(default=500, description="每页条数")


class StatusEnum(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    FAILED = "FAILED"


class Task(BaseModel):
    task_id: str
    status: StatusEnum
    file_path: Optional[str] = None
    start_time: Optional[str] = None  # YYYY-MM-DD HH:MM:SS


class StationsDto(BaseModel):
    id: int = Field(default=None, description="场站id")
    code: Optional[str] = None
    types: str
    capacity: Optional[float] = None
    province: Optional[str] = None
    longitude: Decimal
    latitude: Decimal
    altitude: Optional[float] = None
    hub_height: Optional[float] = None


class ObservationsDto(BaseModel):
    time: str
    station_id: int
    sub_station_id: Optional[int] = None
    radiation: Optional[float] = None
    windspeed: Optional[float] = None
    power: Optional[float] = None


class BaseRsp(BaseModel):
    page: int = 0
    page_size: int = 0
    records: Union[List[StationsDto], List[ObservationsDto], None] = None
