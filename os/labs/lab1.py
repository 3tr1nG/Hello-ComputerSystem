import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.process import Process

def sequential_scheduler(procs: list[Process]) -> Process:
    # 顺序调度器实现：返回列表中的第一个进程
    # 检查进程列表是否为空
    if procs:
        return procs[0]
    # 如果没有进程，返回None
    return None


