"""测试状态机。"""

import pytest
from src.fb_simulator.state_machine import CAAStateMachine


def test_caa_state_machine():
    """测试状态机。"""
    machine = CAAStateMachine()
    result = machine.init_registration("waterfall_123", "AX_ctx_456")
    
    assert result["status"] == "initialized"
    
    result = machine.submit_step(0, {"phone": "+251900000000"})
    assert result["current_step"] == 0
    assert result["next_step"] == 1
