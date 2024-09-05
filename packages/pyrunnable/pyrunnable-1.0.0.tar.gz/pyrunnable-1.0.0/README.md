# pyrunnable

a wrapper around threading.Thread with convenience functions like

- on_start (called after starting the runnable with .start)
- on_stop (called after stopping the runnable with .stop)
- work (executed cyclically until .stop is called)

that you can override, as well as

- stop

which i was missing in threading.Thread

## how to...

### ... install

```shell script
pip install pyrunnable
```

### ... use it

```python
from pyrunnable import Runnable
from time import sleep

class ThreadedObject(Runnable):
    def on_start(self):
        print("starting")
    
    def work(self):
        print("working")
        sleep(0.2)

    def on_stop(self):
        print("stopping")

o = ThreadedObject()
try:
    o.start()
    o.join()  # Runnable inherits threading.Thread
except KeyboardInterrupt:
    o.stop()
```
