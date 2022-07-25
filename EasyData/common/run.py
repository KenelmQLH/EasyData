import platform
import os


def log_processor_info():
    print(f"Environment: {platform.node()}".center(50, '='))
    print(f"PID: {os.getpid()}".center(50, '='))



