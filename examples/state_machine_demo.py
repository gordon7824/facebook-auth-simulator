#!/usr/bin/env python
"""示例：CAA 注册状态机演示。"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.fb_simulator.state_machine import CAAStateMachine


def main():
    print("Facebook CAA 注册状态机演示\n")
    
    machine = CAAStateMachine()
    result = machine.init_registration(
        waterfall_id="waterfall_abc123",
        reg_context="AX_encoded_context"
    )
    print(f"初始化: {json.dumps(result, indent=2)}\n")
    
    steps = [
        (0, {"phone": "+251900000000"}),
        (1, {"first_name": "John", "last_name": "Doe"}),
        (2, {"birthdate": "1990-01-01"}),
        (3, {"gender": "M"}),
        (4, {"phone": "+251900000000"}),
        (5, {"password_encrypted": "<encrypted>"}),
        (8, {}),
    ]
    
    for step, data in steps:
        result = machine.submit_step(step, data)
        print(f"步骤 {step}: 下一步 = {result['next_step']}")
    
    print(f"\n完成: {machine.is_complete()}")


if __name__ == "__main__":
    main()
