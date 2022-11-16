import os
import queue
import threading
import contextlib
import time


class ThreadPool(object):
    def __init__(self, max_workers: int = None, max_task_num: int = None):
        self.work_queue = queue.Queue(max_task_num) if max_task_num else queue.Queue()
        self.max_workers = max_workers if max_workers else min(32, (os.cpu_count() or 1) + 4)
        self.thread_name = threading.current_thread().name
        self._shutdown_lock = threading.Lock()
        self.stop_event = object()
        self.cancel = False
        self.terminal = False
        self._shutdown = None
        self.daemon = False
        self.running = None
        self.failure = None
        self.success = None
        self.threads = []
        self.free_threads = []
        self.tasks = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown(wait=True)
        return False

    def run(self, func, /, args: tuple = None, _callback=None):
        """
        线程池执行一个任务

        :param func: 任务函数
        :param args: 任务函数所需参数
        :param _callback: 任务执行失败或成功后执行的回调函数, 回调函数有两个参数
                            1、任务函数执行状态；2、任务函数返回值
                            （默认为None，即：不执行回调函数）
        :return: 如果线程池已经终止则返回True, 否则None
        """
        if self.cancel:
            return
        if len(self.free_threads) == 0 and len(self.threads) < self.max_workers:
            self.generate_thread()
        task = (func, args, _callback)
        self.work_queue.put(task)

    def generate_thread(self):
        """
        创建一个线程
        """
        t = threading.Thread(target=self.call)
        t.daemon = self.daemon
        t.start()
        self.threads.append(t)

    def call(self):
        """
        循环去获取任务函数并执行任务函数
        """
        current_thread = threading.current_thread()
        while True:
            try:
                event = self.work_queue.get(block=False, timeout=180)
                if event == self.stop_event:
                    self.threads.remove(current_thread)
                    break
                func, args, _callback = event
                if not args:
                    args = tuple()
                try:
                    result = func(*args)
                    status = True
                except Exception as e:
                    print(e)
                    result = e
                    status = False
                if _callback is not None:
                    try:
                        _callback(status, result)
                    except Exception as e:
                        print(e)
                with self.worker_state(self.free_threads, current_thread):
                    if self.terminal:
                        event = self.stop_event
                    else:
                        event = self.work_queue.get(block=False, timeout=180)
            except queue.Empty:
                if self._shutdown or self.running <= 0:
                    self.threads.remove(current_thread)
                    return

    def close(self):
        """
        执行完所有的任务后，所有线程停止
        """
        self.cancel = True
        count = len(self.threads)
        while count:
            self.work_queue.put(self.stop_event)
            count -= 1

    def terminate(self):
        """
        无论是否还有任务，终止线程
        """
        self.terminal = True
        while self.threads:
            self.work_queue.put(self.stop_event)
        self.work_queue.queue.clear()

    def shutdown(self, wait=True, *, cancel_futures=False):
        """Clean-up the resources associated with the Executor.

        It is safe to call this method several times. Otherwise, no other
        methods can be called after this one.

        Args:
            wait: If True then shutdown will not return until all running
                futures have finished executing and the resources used by the
                executor have been reclaimed.
            cancel_futures: If True then shutdown will cancel all pending
                futures. Futures that are completed or running will not be
                cancelled.
        """
        with self._shutdown_lock:
            self._shutdown = True
            if cancel_futures:
                # Drain all work items from the queue, and then cancel their
                # associated futures.
                while True:
                    try:
                        work_item = self.work_queue.get_nowait()
                    except queue.Empty:
                        break
                    if work_item is not None:
                        work_item.future.cancel()

            # Send a wake-up to prevent threads calling
            # _work_queue.get(block=True) from permanently blocking.
            self.work_queue.put(self.stop_event)
        if wait:
            for t in self.threads:
                t.join()

    def join(self):
        """
        阻塞线程池上下文，使所有线程执行完后才能继续
        """
        for t in self.threads:
            t.join()

    @contextlib.contextmanager
    def worker_state(self, state_list, worker_thread):
        """
        用于记录线程中正在等待的线程数
        """
        state_list.append(worker_thread)
        try:
            yield
        finally:
            state_list.remove(worker_thread)


def do_something(status, result, *args, **kwargs):
    # status, execute action status
    # result, execute action return value
    pass


def action(iter_num):
    print(iter_num)
    time.sleep(1)


if __name__ == '__main__':
    # How to
    # pool = ThreadPool(5)
    # for i in range(30):
    #     pool.run(action, args=(i,), _callback=do_something)
    with ThreadPool(5) as pool:
        for i in range(30):
            pool.run(action, args=(i,), _callback=do_something)
        # time.sleep(1)
        # print(len(pool.threads), len(pool.free_threads))
        # print(len(pool.threads), len(pool.free_threads))
        # pool.close()
        # pool.terminate()
