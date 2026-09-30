"""本地 CAA 注册状态机。"""

from typing import Dict, Any, Optional
from .models import RegInfoState


class CAAStateMachine:
    """Bloks 驱动的注册状态机（本地模拟）。"""
    
    STEP_SEQUENCE = [
        (0, "手机号预取"),
        (1, "姓名"),
        (2, "生日"),
        (3, "性别"),
        (4, "手机号确认"),
        (5, "密码"),
        (8, "提交建号"),
    ]
    
    def __init__(self):
        self.state = RegInfoState()
        self.history = []
    
    def init_registration(self, waterfall_id: str, reg_context: str) -> Dict[str, Any]:
        """初始化注册。"""
        self.state = RegInfoState(
            current_step=0,
            waterfall_id=waterfall_id,
            reg_context=reg_context
        )
        self.history = [(0, self.state.copy())]
        return {"status": "initialized", "current_step": 0}
    
    def submit_step(self, step: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """提交步骤数据。"""
        if step not in [s[0] for s in self.STEP_SEQUENCE]:
            return {"error": f"Invalid step: {step}"}
        
        for key, value in data.items():
            setattr(self.state, key, value)
        
        self.state.current_step = step
        self.history.append((step, self.state.copy()))
        next_step = self._get_next_step(step)
        
        return {
            "status": "step_submitted",
            "current_step": step,
            "next_step": next_step,
            "reg_info": self.state.dict(exclude_none=True)
        }
    
    def _get_next_step(self, current_step: int) -> Optional[int]:
        """获取下一步。"""
        steps = [s[0] for s in self.STEP_SEQUENCE]
        try:
            idx = steps.index(current_step)
            return steps[idx + 1] if idx + 1 < len(steps) else None
        except ValueError:
            return None
    
    def is_complete(self) -> bool:
        """检查是否完成。"""
        return self.state.current_step == 8 and self.state.password_encrypted is not None
