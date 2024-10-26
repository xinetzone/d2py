def test_drawing():
    from tkinter import Tk
    from d2py.gui.tkinterx.graph.base import Drawing
    from d2py.gui.tkinterx.graph.selector import SelectorFrame
    root = Tk()
    selector = SelectorFrame(root)
    # or TrajectoryDrawing
    meta = Drawing(root, selector, background='lightgray')
    # Makes the master widget change as the canvas size
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    meta.grid(row=0, column=0, sticky='nwes')
    selector.grid(row=1, column=0, sticky='nwes')
    root.mainloop()