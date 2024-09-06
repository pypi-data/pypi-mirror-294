# coding:utf-8
import time
from multiprocessing import Process, Value

mylist = []


def one(name):
    print(name, 'begin')
    mylist.append(name)
    time.sleep(10)
    return name


def main():
    pp = ProcessPool(2)
    mylist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for num in mylist:
        pp.run(test, (num,))
    pp.wait()

    
def test(a):
    print(a)


class ProcessPool():
    """ 维护一个线程池 """
    
    def __init__(self, size, while_wait_time=0.5):
        self.size = size
        self.running_num = Value('i', 0)
        self.while_wait_time = while_wait_time
        
    def run(self, func, args):
        """ 主线程命令当前线程池从空闲线程中取一个线程执行给入的方法，如果池满，则主线程等待 """
        if self.running_num.value < self.size:
            p = myProcess(func, args=args, running_num=self.running_num)
            p.start()
            self.running_num.value = self.running_num.value + 1
        else:
            while self.running_num.value >= self.size:
                time.sleep(self.while_wait_time)
            return self.run(func, args)
        
    def wait(self):
        """ 主线程等待，直到线程池不存在活动线程 """
        while self.running_num.value > 0:
            time.sleep(self.while_wait_time)
    
    def get_running_num(self):
        return self.running_num.value


class myProcess (Process):

    def __init__(self, func, args, running_num):
        Process.__init__(self)
        Process.daemon = True
        self.func = func
        self.args = args
        self.running_num = running_num

    def run(self):
        try:
            self.func(*self.args)
        finally:
            self.running_num.value = self.running_num.value - 1


if __name__ == '__main__':
    main()
