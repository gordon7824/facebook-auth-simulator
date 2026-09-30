#!/usr/bin/env python
"""示例：解析脱敏的 JSONL 流量文件。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.fb_simulator.parser import TrafficParser


def main():
    traffic_file = "./data/fb_traffic.redacted.jsonl"
    
    if not Path(traffic_file).exists():
        print(f"文件不存在: {traffic_file}")
        return
    
    parser = TrafficParser(traffic_file)
    events = parser.parse()
    print(f"解析成功: {len(events)} 个事件")
    
    stats = parser.stats()
    print(f"\n统计: {stats}")
    
    print("\n前 10 个事件:")
    for i, event in enumerate(events[:10], 1):
        print(f"  {i}. {event.timestamp.strftime('%H:%M:%S')} - {event.friendly_name}")


if __name__ == "__main__":
    main()
