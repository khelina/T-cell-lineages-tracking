from threading import Thread
import tkinter as tk
win= tk.Tk()
class CustomThread(Thread):
    def _init_(self,group=None,target=None,name=None,args=(), kwargs={},Verbose=None):
        Thread._init_(self,group,name,args,kwargs)
        self._return=None
        
    def run(self):
        if self._target is not None:
            self._return=self._target(*self._args,**self._kwargs)
            
    def join(self):
        Thread.join(self)
        return self._return
global val
val=5
def add(n1,n2):
    result=n1+n2+val
    
    return result, val
##################################
thread=CustomThread(target=add,args=(5,4))
thread.start()
a=thread.join()
print("a=",a)
win.mainloop()
####################
#print(thread.join())