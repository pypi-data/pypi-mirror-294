# coding:utf-8
import multiprocessing
from uuid import uuid1


def main():
    pass


class ProcessPool():
    """ 维护一个线程池 """
    
    def __init__(self, size):
        self.size = size
        self.result_map = {}
        self.pool = multiprocessing.Pool(self.size)
        
    def run(self, func, args):
        process_id = uuid1()
        self.result_map[process_id] = self.pool.apply_async(func=func, args=args)
        return process_id
        
    def wait(self):
        self.pool.close()
        self.pool.join()

    def get_results(self):
        return self.result_map
    
    def get_result(self, process_id):
        return self.result_map[process_id]


if __name__ == '__main__':
    main()
