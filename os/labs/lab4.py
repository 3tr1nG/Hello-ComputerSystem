import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.process import Process  # 假设Process类定义了进程相关属性和方法
from src.myos import MyOS        # 假设MyOS类提供了系统核心功能

def my_run():
    """实现支持FORK系统调用的主运行循环"""
    # 初始化操作系统实例
    os_instance = MyOS()
    # 用于生成新PID的计数器（实际系统中可能更复杂）
    next_pid = 1001  # 假设初始PID从1001开始
    
    print("操作系统启动，开始处理进程...")
    
    # 主运行循环：持续处理进程直到没有可运行的进程
    while True:
        # 获取下一个要运行的进程（由调度器决定）
        current_proc = os_instance.scheduler(os_instance.processes)
        
        # 如果没有可运行的进程，退出循环
        if not current_proc:
            print("所有进程已执行完毕，操作系统关闭")
            break
        
        print(f"\n正在运行进程: {current_proc.name} (PID: {current_proc.pid})")
        
        # 检查进程是否请求了FORK系统调用
        if hasattr(current_proc, 'syscall') and current_proc.syscall == "FORK":
            print(f"检测到FORK系统调用：进程 {current_proc.pid} 正在创建子进程")
            
            # 生成新的PID
            child_pid = next_pid
            next_pid += 1  # 更新PID计数器
            
            # 创建子进程（复制父进程的大部分属性）
            child_proc = Process(
                pid=child_pid,
                name=f"{current_proc.name}_child",
                priority=current_proc.priority,
                # 复制父进程的状态（简化处理）
                state=current_proc.state,
                # 重置子进程的系统调用状态
                syscall=None,
                parent_pid=current_proc.pid  # 记录父进程PID
            )
            
            # 将子进程添加到系统进程列表
            os_instance.add_process(child_proc)
            
            # 标记父进程的FORK调用已完成，并设置返回值
            current_proc.syscall = None
            current_proc.return_value = child_pid  # 父进程得到子进程PID
            print(f"FORK成功：子进程创建 (PID: {child_proc.pid})，父进程 (PID: {current_proc.pid})")
        
        # 模拟进程执行一步
        current_proc.execute_step()
        
        # 检查进程是否已完成
        if current_proc.is_complete():
            print(f"进程 {current_proc.name} (PID: {current_proc.pid}) 执行完毕")
            os_instance.remove_process(current_proc)
