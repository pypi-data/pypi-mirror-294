# coding:utf-8
import time
from multiprocessing import Process, Manager
import sys
from uuid import uuid1


def main():
    pp = ProcessPool(2)
    for num in range(1, 10):
        pp.run(a1, (num,))
    pp.wait()

    
def a1(a):
    pp = ProcessPool(2)
    for num in range(10, 20):
        pp.run(a2, (num, a))
    pp.wait()

    
def a2(a, b):
    print(b, a)


class ProcessPool():
    """ 维护一个线程池 """
    
    def __init__(self, size, while_wait_time=0.1):
        self.size = size
        self.running_pro = Manager().list()
        self.while_wait_time = while_wait_time
        
    def run(self, func, args):
        """ 主线程命令当前线程池从空闲线程中取一个线程执行给入的方法，如果池满，则主线程等待 """
        if len(self.running_pro) < self.size:
            process_id = uuid1()
            self.running_pro.append(process_id)
            p = myProcess(func, args=args, running_pro=self.running_pro, process_id=process_id)
            p.start()
        else:
            while len(self.running_pro) >= self.size:
                time.sleep(self.while_wait_time)
            return self.run(func, args)
        
    def wait(self):
        """ 主线程等待，直到线程池不存在活动线程 """
        while len(self.running_pro) > 0:
            time.sleep(self.while_wait_time)
    
    def get_running_num(self):
        return len(self.running_pro)


class myProcess (Process):

    def __init__(self, func, args, running_pro, process_id):
        Process.__init__(self)
        Process.daemon = True
        self.func = func
        self.args = args
        self.running_pro = running_pro
        self.process_id = process_id

    def run(self):
        try:
            self.func(*self.args)
        finally:
            self.running_pro.remove(self.process_id)
            sys.exit()


if __name__ == '__main__':
    main()
