import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.process import Process

def priority_scheduler(procs: list[Process]) -> Process:
    # 优先级调度器实现：选择优先级最高的进程
    # 假设优先级数值越小表示优先级越高
    if not procs:  # 检查进程列表是否为空
        return None
    
    # 找到优先级最高的进程（最小的优先级数值）
    highest_priority_proc = procs[0]
    for proc in procs[1:]:
        if proc.priority < highest_priority_proc.priority:
            highest_priority_proc = proc
    
    return highest_priority_proc
    
