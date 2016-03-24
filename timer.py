import time
from collections import OrderedDict
from functools import wraps

global g_timers
g_timers = OrderedDict()

def named_timer(name): 
    global g_timers
    if name not in g_timers: 
        g_timers[name] = SimpleTimer(name)
    try: 
        return g_timers[name] 
    except KeyError, e: 
        raise RuntimeError('Failed to retrieve timer {:}'.format(e))

def timeitmethod(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try: 
            name = ''.join([args[0].__class__.__name__, '::', func.__name__])
        except: 
            raise RuntimeError('timeitmethod requires first argument to be self')
        named_timer(name).start()
        r = func(*args, **kwargs)
        named_timer(name).stop()
        return r
    return wrapper


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        named_timer(name).start()
        r = func(*args, **kwargs)
        named_timer(name).stop()
        return r
    return wrapper

class SimpleTimer: 
    def __init__(self, name='', hz=1.0): 
        self.name_ = name
        
        self.counter_ = 0
        self.last_ = time.time()
        self.period_ = 0
        
        self.last_print_ = time.time()        
        self.last_fps_ = 0

    def poll(self): 
        self.counter_ += 1
        now = time.time()
        dt = (now - self.last_)

        if (now-self.last_print_) > 1: 
            T = dt / self.counter_
            print('%s: %4.3f ms (avg over %i iterations)' % (self.name_, T * 1e3, self.counter_))
            self.last_ = now
            self.last_print_ = now
            self.counter_ = 0

    def poll_piecemeal(self): 
        self.counter_ += 1
        now = time.time()
        dt = (now - self.last_)
        self.period_ += dt

        if (now-self.last_print_) > 1:
            T = self.period_ / self.counter_
            fps = 1.0 / T
            print('%s: %4.3f ms (avg over %i iterations)' % (self.name_, T * 1e3, self.counter_))
            self.last_ = now
            self.last_print_ = now
            self.last_fps_ = fps
            self.counter_ = 0
            self.period_ = 0
            
    def start(self): 
        self.last_ = time.time()

    def stop(self): 
        self.poll_piecemeal()

    @property
    def fps(self): 
        return self.last_fps_
        
