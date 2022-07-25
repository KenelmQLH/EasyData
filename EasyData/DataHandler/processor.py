from multiprocessing import Process, Pool
import multiprocessing
from datetime import datetime
import os
import pandas as pd

from EasyData.FileHandler import save_pkl, get_pkl
from copy import deepcopy


class ParallelHandlerForIterable(object):
    def __init__(self, num_processor=2, log_details=True):
        assert num_processor >=2 and num_processor <= multiprocessing.cpu_count()
        self.num_processor = num_processor
        self.log_details = log_details

    def _process(self, n, map_func, part_items, argc=None):
        if self.log_details:
            start_time = datetime.now()
            print(f"子进程{n}[{os.getpid()}]开始: {start_time}")
        
        ret_items = []
        for item in part_items:
            ret_item = map_func(item, *argc)
            ret_items.append(ret_item)
        
        if self.log_details:
            end_time = datetime.now()
            print(f"子进程{n}[{os.getpid()}]结束: {end_time}（共花费 {end_time-start_time} s )")
        return (n, ret_items) 

    def run(self, items, map_func, argc=None):

        _items = deepcopy(items)
        total_size = len(_items)
        part_size = int(total_size / self.num_processor)
        
        if self.log_details:
            start_time = datetime.now()
            print(f"[并行处理开始] (主进程[{os.getpid()}]):  time={start_time}")

        pool = Pool(processes=self.num_processor)
        workers = []
        # 启动多进程
        for i in range(self.num_processor):
            start = i*part_size
            end = (i+1)*part_size if (i+1)*part_size < total_size else total_size
            part_items = _items[start: end]
            workers.append(
                pool.apply_async(self._process, (i, map_func, part_items, argc))
            )

        pool.close() # # 关闭进程池，表示不能再往进程池中添加进程，需要在join之前调用
        #进程阻塞
        pool.join()
        
        results = []
        for p in workers:
            results.append( p.get() )
        results.sort(key=lambda x: x[0], reverse=False) # 从小到大顺序排列

        results_items = []
        for res in results:
            print(f"Add res{res[0]}")
            results_items.extend(res[1])
        
        if self.log_details:
            end_time = datetime.now()
            print(f"[并行处理结束] (主进程[{os.getpid()}]) time={end_time}（共花费 {end_time-start_time} s )")
            print("[debug] results_items' example", results_items[0])
        
        return results_items
