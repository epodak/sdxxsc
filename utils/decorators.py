import functools
import logging
import time
from typing import Any, Callable
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def print_log(
    log_args: bool = True,
    log_result: bool = True,
    log_time: bool = True
) -> Callable:
    """
    装饰器函数，用于记录函数的调用信息
    
    Args:
        log_args (bool): 是否记录函数参数
        log_result (bool): 是否记录函数返回值
        log_time (bool): 是否记录函数执行时间
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name = func.__name__
            # 记录开始时间
            start_time = time.time()
            
            # 记录函数调用信息
            call_info = f"调用函数: {func_name}"
            if log_args and (args or kwargs):
                args_str = f"参数: args={args}, kwargs={kwargs}"
                call_info += f"\n{args_str}"
            
            logger.info(call_info)
            
            try:
                # 执行原函数
                result = func(*args, **kwargs)
                
                # 记录执行结果
                if log_result:
                    logger.info(f"函数 {func_name} 返回值: {result}")
                
                # 记录执行时间
                if log_time:
                    end_time = time.time()
                    execution_time = end_time - start_time
                    logger.info(f"函数 {func_name} 执行时间: {execution_time:.4f} 秒")
                
                return result
            
            except Exception as e:
                # 记录异常信息
                logger.error(f"函数 {func_name} 执行出错: {str(e)}", exc_info=True)
                raise
            
        return wrapper
    return decorator 