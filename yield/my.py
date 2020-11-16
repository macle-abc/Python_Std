import collections
import time


# def future():
#     callback = future.send  # 回调函数为 生成器的 send 方法，当然这种写法有问题，此时生成器还未形成
#     do_something(callback)  # 进行 io 操作，并将 callback 注册为回调函数(进行io操作前，转移控制权)
#     result = yield (io完成后将结果set_result)
#     return result

class InvalidStateError(RuntimeError):
    pass


class EventloopError(RuntimeError):
    pass


class Future:
    _FINISHED = 'finished'
    _PENDING = 'pending'
    _CANCELLED = 'CANCELLED'

    def __init__(self, loop=None):
        if loop is None:
            self._loop = get_event_loop()  # 获取当前的 eventloop
        else:
            self._loop = loop
        self._callbacks = []
        self.status = self._PENDING
        self._blocking = False
        self._result = None

    def _schedule_callbacks(self):
        # 将回调函数添加到事件队列里，eventloop 稍后会运行
        for callbacks in self._callbacks:
            self._loop.add_ready(callbacks)
        self._callbacks = []

    def set_result(self, result):
        self.status = self._FINISHED
        self._result = result
        self._schedule_callbacks()  # future 完成后，执行回调函数

    def add_done_callback(self, callback, *args):
        # 为 future 增加回调函数
        if self.done():
            self._loop.call_soon(callback, *args)
        else:
            handle = Handle(callback, self._loop, *args)
            self._callbacks.append(handle)

    def done(self):
        return self.status != self._PENDING

    def result(self):
        if self.status != self._FINISHED:
            raise InvalidStateError('future is not ready')
        return self._result

    def __iter__(self):
        if not self.done():
            self._blocking = True
        yield self
        assert self.done(), 'future not done'
        return self.result()


# class Future:
#     _FINISHED = 'finished'
#     _PENDING = 'pending'
#     _CANCELLED = 'CANCELLED'
#
#     def __init__(self):
#         self.status = self._PENDING
#
#     def set_result(self, result):
#         # 给future设置结果，并将 future 置为结束状态
#         self.status = self._FINISHED
#         self._result = result
#
#     def done(self):
#         return self.status != self._PENDING
#
#     def result(self):
#         # 获取future 的结果
#         if self.status != self._FINISHED:
#             raise InvalidStateError('future is not ready')
#         return self._result
#
#     def __iter__(self):
#         if not self.done():
#             self._blocking = True
#         yield self  # 返回自身
#         """
#         那么协程的运行路线就已经很清楚了。
#         coro 通过 coro.send(None) 启动，
#         遇到 io 操作，会用 yield 返回一个 future
#         。io 操作完成之后，
#         回调函数通过 coro.send(None) 继续往下进行。
#         直到 coro.send(None) 爆出 StopIteration 异常，协程运行完毕。"""
#         assert self.done(), 'future not done'  # 下一次运行 future 的时候，要确定 future 对应的事件已经运行完毕
#         return self.result()


class Handle:

    def __init__(self, callback, loop, *args):
        self._callback = callback
        self._args = args

    def _run(self):
        self._callback(*self._args)


class Eventloop:

    def __init__(self):
        self._ready = collections.deque()  # 事件队列
        self._stopping = False

    def stop(self):
        self._stopping = True

    def call_soon(self, callback, *args):
        # 将事件添加到队列里
        handle = Handle(callback, self, *args)
        self._ready.append(handle)

    def add_ready(self, handle):
        # 将事件添加到队列里
        if isinstance(handle, Handle):
            self._ready.append(handle)
        else:
            raise EventloopError('only handle is allowed to join in ready')

    def run_once(self):
        # 执行队列里的事件
        ntodo = len(self._ready)
        for i in range(ntodo):
            handle = self._ready.popleft()
            handle._run()

    def run_forever(self):
        while True:
            self.run_once()
            if self._stopping:
                break


_event_loop = None


def get_event_loop():
    global _event_loop
    if _event_loop is None:
        _event_loop = Eventloop()
    return _event_loop


class Task(Future):

    def __init__(self, coro, loop=None):
        super().__init__(loop=loop)
        self._coro = coro  # 协程
        self._loop.call_soon(self._step)  # 启动协程

    def _step(self, exc=None):
        try:
            if exc is None:
                result = self._coro.send(None)
            else:
                result = self._coro.throw(exc)  # 有异常，则抛出异常
        except StopIteration as exc:  # 说明协程已经执行完毕，为协程设置值
            self.set_result(exc.value)
        else:
            if isinstance(result, Future):
                if result._blocking:
                    self._blocking = False
                    result.add_done_callback(self._wakeup, result)
                else:
                    self._loop.call_soon(
                        self._step, RuntimeError('你是不是用了 yield 才导致这个error?')
                    )
            elif result is None:
                self._loop.call_soon(self._step)
            else:
                self._loop.call_soon(self._step, RuntimeError('你产生了一个不合规范的值'))

    def _wakeup(self, future):
        try:
            future.result()  # 查看future 运行是否有异常
        except Exception as exc:
            self._step(exc)
        else:
            self._step()


if __name__ == '__main__':
    # future = Future()  # future对象
    # i = iter(future)
    # f = next(i)  # 交出future的控制权
    # time.sleep(1)  # 遇到io前驱动future运行
    # f.set_result(3)  # io完成set结果
    # next(i)
    def func():
        f = Future()
        i = iter(f)
        next(i)
        time.sleep(1)
        f.set_result(3)
        print(f.result())
        yield from Future()
        return 3


    t = Task(func())
    l = get_event_loop()
    l.run_forever()
