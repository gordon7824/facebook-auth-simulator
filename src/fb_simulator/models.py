"""数据模型：脱敏事件与状态表示。"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field


class DeviceInfo(BaseModel):
    """设备信息（脱敏）。"""
    device_id: str = Field(..., description="设备 ID")
    family_device_id: str = Field(..., description="设备族 ID")
    machine_id: str = Field(..., description="机器指纹")
    app_id: str = Field(default="6628568379", description="FB iOS App ID")


class RegInfoState(BaseModel):
    """注册信息状态（累积字段）。"""
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birthdate: Optional[str] = None
    gender: Optional[str] = None
    password_encrypted: Optional[str] = None
    current_step: int = 0
    waterfall_id: Optional[str] = None
    reg_context: Optional[str] = None


class TrafficEvent(BaseModel):
    """通用流量事件。"""
    timestamp: datetime
    friendly_name: str
    event_type: str
    raw_data: Dict[str, Any]
    redacted: bool = False
