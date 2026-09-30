"""JSONL 流量解析器。"""

import json
from typing import List, Dict, Any
from datetime import datetime
from .models import TrafficEvent


class TrafficParser:
    """解析脱敏的 JSONL 抓包数据。"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.events: List[TrafficEvent] = []
    
    def parse(self) -> List[TrafficEvent]:
        """逐行解析 JSONL 文件。"""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    event = self._classify_event(data)
                    self.events.append(event)
                except json.JSONDecodeError as e:
                    print(f"[错误] 第 {line_num} 行：{e}")
        return self.events
    
    def _classify_event(self, data: Dict[str, Any]) -> TrafficEvent:
        """根据 friendly_name 分类事件。"""
        friendly_name = data.get("friendly_name", "")
        timestamp_str = data.get("timestamp", datetime.now().isoformat())
        
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except:
            timestamp = datetime.now()
        
        if "caa" in friendly_name:
            event_type = "caa"
        elif "login" in friendly_name:
            event_type = "login"
        elif "dbl" in friendly_name.lower():
            event_type = "dbl"
        else:
            event_type = "other"
        
        return TrafficEvent(
            timestamp=timestamp,
            friendly_name=friendly_name,
            event_type=event_type,
            raw_data=data
        )
    
    def get_caa_events(self) -> List[TrafficEvent]:
        """获取所有 CAA 事件。"""
        return [e for e in self.events if e.event_type == "caa"]
    
    def stats(self) -> Dict[str, Any]:
        """统计信息。"""
        return {
            "total_events": len(self.events),
            "caa_events": len(self.get_caa_events()),
            "dbl_events": sum(1 for e in self.events if e.event_type == "dbl"),
        }
