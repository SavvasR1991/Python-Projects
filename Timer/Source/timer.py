from tkinter import *
import time
import xlwt,csv
import os
from datetime import date
import datetime
import sys

timeW = 0
breakTime = 0

class StopWatch(Frame):  
    """ Implements a stop watch frame widget. """                                                                
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._running = 0
        self._hour = 0
        self.timestr = StringVar()
        
        self._startBreak = 0.0        
        self._elapsedtimeBreak = 0.0
        self._runningBreak = 0
        self._hoursBreak = 0
        self.timestrBreak = StringVar() 
        
        self.makeWidgets()  
        self.makeWidgetsBreak()      
        
    def makeWidgets(self):                         
        """ Make the time label. """
        l = Label(self, textvariable=self.timestr)
        self._setTime(self._elapsedtime)
        l.pack(fill=X, expand=NO, pady=2, padx=2) 
        
    def makeWidgetsBreak(self):                         
        """ Make the time label. """
        l = Label(self, textvariable=self.timestrBreak)
        self._setTimeBreak(self._elapsedtimeBreak)
        l.pack(fill=X, expand=NO, pady=2, padx=2)        
    
    def _update(self): 
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)
        global timeW 
        global breakTime
        timeW = self.timestr.get()
        breakTime = self.timestrBreak.get()
        if self._hour == 8 :
            self.Stop()
            self.StopBreak()
            self.StoreResults()   
        
    def _updateBreak(self): 
        """ Update the label with elapsed time. """
        self._elapsedtimeBreak = time.time() - self._startBreak
        self._setTimeBreak(self._elapsedtimeBreak)
        self._timer2 = self.after(50, self._updateBreak)
    
    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        m, s = divmod(int(elap), 60)
        h, m = divmod(m, 60)
        self._hour = h 
        self.timestr.set('{:02d}:{:02d}:{:02d}'.format(h, m, s))

    def _setTimeBreak(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        m, s = divmod(int(elap), 60)
        h, m = divmod(m, 60)
        self._hoursBreak = h 
        self.timestrBreak.set('{:02d}:{:02d}:{:02d}'.format(h, m, s))

    def StoreResults(self):   
        global timeW
        global breakTime
        excelTitles = ["DAY","WORKING TIME","BREAK"]
        filename = 'SavvarRostantisWorkTime.csv'
        file_exists = os.path.isfile(filename)
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        with open(filename, mode='a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=excelTitles)
            if not file_exists:
                writer.writeheader()   
            writer.writerow({'DAY': str(d1),'WORKING TIME': str(timeW) , 'BREAK': str(breakTime)})
        self.message()
        sys.exit()
        
    def message(self):
        root = Tk()
        root.title("FINALLYYYY !!!!!!!!!!")
        root.resizable(False, False)
        root.geometry('{}x{}'.format(1000, 600))
        label_0 = Label(root, text="GET THE HELL OUT ",width=20,font=("bold", 50))
        label_0.place(x=50,y=200)
        root.mainloop()
        
    def Start(self):                                                     
        """ Start the stopwatch, ignore if running. """
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1        
            
    def StartBreak(self):                                                     
        """ Start the stopwatch, ignore if running. """
        if not self._runningBreak:            
            self._startBreak = time.time() - self._elapsedtimeBreak
            self._updateBreak()
            self._runningBreak = 1     
    
    def StopBreak(self):                                    
        """ Stop the stopwatch, ignore if stopped. """
        if self._runningBreak:
            self.after_cancel(self._timer2)            
            self._elapsedtimeBreak = time.time() - self._startBreak    
            self._setTime(self._elapsedtimeBreak)
            self._runningBreak = 0
    
    def Stop(self):                                    
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0
    
    def Reset(self):                                  
        """ Reset the stopwatch. """
        self._start = time.time()         
        self._elapsedtime = 0.0    
        self._setTime(self._elapsedtime)
        self._hour = 0
        
        self._startBreak = time.time()         
        self._elapsedtimeBreak = 0.0    
        self._setTimeBreak(self._elapsedtimeBreak)
        self._hourBreak = 0
        
    def FrameStart():      
        root = Tk()
        root.title("Working Timer")
        root.resizable(False, False)
        root.geometry('{}x{}'.format(250, 100))
        sw = StopWatch(root)
        sw.pack(side=TOP)
        btnStart = Button(root, text='Start', command=sw.Start).pack(side=LEFT)
        btn_start = Button(root, text='StartBreak', command=sw.StartBreak).pack(side=LEFT)
        Button(root, text='StopBreak', command=sw.StopBreak).pack(side=LEFT)
        Button(root, text='Reset', command=sw.Reset).pack(side=LEFT)
        Button(root, text='Quit', command=root.quit).pack(side=LEFT)
        root.mainloop()

def main():
    StopWatch.FrameStart()
    
if __name__ == '__main__':
    main()