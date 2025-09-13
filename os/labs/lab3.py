import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.process import Process  # 假设Process类定义了进程相关属性和方法
from src.myos import MyOS        # 假设MyOS类提供了系统调用处理的基础功能

def my_run():
    """实现支持WRITE_DOUBLE系统调用的主运行循环"""
    # 初始化操作系统实例
    os_instance = MyOS()
    
    # 主运行循环：持续处理进程直到没有可运行的进程
    while True:
        # 获取下一个要运行的进程（由调度器决定）
        current_proc = os_instance.scheduler(os_instance.processes)
        
        # 如果没有可运行的进程，退出循环
        if not current_proc:
            print("所有进程已执行完毕，退出系统")
            break
        
        print(f"正在运行进程: {current_proc.name} (PID: {current_proc.pid})")
        
        # 检查进程是否有系统调用请求
        if current_proc.syscall == "WRITE_DOUBLE":
            # 处理WRITE_DOUBLE系统调用：将参数乘以2后输出
            try:
                # 获取系统调用参数
                value = current_proc.arg
                # 执行翻倍操作
                result = value * 2
                # 输出结果
                print(f"系统调用 WRITE_DOUBLE: {value} * 2 = {result}")
                # 标记系统调用已完成
                current_proc.syscall = None
                current_proc.arg = None
            except Exception as e:
                print(f"处理WRITE_DOUBLE系统调用时出错: {str(e)}")
        
        # 模拟进程执行（此处简化处理，实际可能需要更多状态管理）
        current_proc.execute_step()
        
        # 检查进程是否已完成
        if current_proc.is_complete():
            print(f"进程 {current_proc.name} (PID: {current_proc.pid}) 已完成")
            os_instance.remove_process(current_proc)
    
