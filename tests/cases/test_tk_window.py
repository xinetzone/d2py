def test_GraphWindow():
    from d2py.gui.tkinterx.graph.base import GraphScrollable
    from d2py.gui.tkinterx.graph.selector import SelectorFrame
    from d2py.gui.tkinterx.graph.window import Window
    root = Window()
    root.geometry('800x600')
    selector = SelectorFrame(root)
    graph = GraphScrollable(root, selector, background='lightgray') # or Graph
    root.update_edit_menu(graph)
    root.update_file_menu(graph)
    # Makes the master widget change as the canvas size
    selector.pack(side='right', fill='y')
    root.mainloop()