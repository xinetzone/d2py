from tkinter import Tk
from d2py.gui.tkinterx.graph.base import Canvas

class Window(Tk):
    def __init__(self, screenName=None, baseName=None, className='Tk', useTk=True, sync=False, use=None):
        super().__init__(screenName=screenName, baseName=baseName, className=className, useTk=useTk, sync=sync, use=use)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
    def show(self):
        kw = {
            'color': 'purple',
            'dash': 2,
            'width': 2,
            'tags': 'test '
        }
        canvas = Canvas(self)
        canvas.draw_graph('line', [20, 20, 100, 200], **kw)
        canvas.draw_graph('oval', [50, 80, 100, 200], fill='red', **kw)
        canvas.draw_graph('rectangle', [170, 80, 220, 200], fill='yellow', **kw)
        canvas.draw_graph('arc', [180, 100, 250, 260],
                        fill='lightblue', style='chord', **kw)
        canvas.draw_graph('polygon', [(70, 80), (20, 70), (30, 90)], fill='purple', **kw)
        canvas.grid(row=0, column=0, sticky='nwes')
        print(canvas.gettags(1))
        print(canvas.find_withtag('graph'))

if __name__ == "__main__":
    root = Window()
    root.show()
    root.mainloop()
