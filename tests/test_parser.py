"""测试流量解析器。"""

import pytest
import json
import tempfile
from pathlib import Path
from src.fb_simulator.parser import TrafficParser


def test_parser_basic():
    """测试基本解析。"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False, encoding='utf-8') as f:
        test_data = [
            {"timestamp": "2026-09-30T13:09:02Z", "friendly_name": "caa.reg.welcome"},
            {"timestamp": "2026-09-30T13:09:03Z", "friendly_name": "caa.reg.name.async"},
        ]
        for item in test_data:
            f.write(json.dumps(item) + "\n")
        temp_path = f.name
    
    try:
        parser = TrafficParser(temp_path)
        events = parser.parse()
        assert len(events) == 2
        assert events[0].event_type == "caa"
    finally:
        Path(temp_path).unlink()
