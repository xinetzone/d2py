from .canvas import GraphMeta
from .shape import Rectangle
from .. import ParamDict
from PIL import Image, ImageTk


class DrawMeta(GraphMeta):
    graph_type = ParamDict()
    color = ParamDict()
    def __init__(self, master=None,  graph_type='rectangle', color='blue',  min_size=7, cnf={}, **kw):
        '''
        '''
        super().__init__(master, cnf, **kw)
        self.min_rect = Rectangle([0, 0, min_size, min_size])
        self.move_bbox = ['none']*4
        self.graph_type, self.color = graph_type, color
        self.bunch = {}  # 记录 canvas 对象

    @property
    def record_bbox(self):
        _record_bbox = self._record_bbox
        if 'none' in _record_bbox:
            return
        else:
            return Rectangle(_record_bbox)

    def mouse_draw_graph(self, width=1, tags=None, **kw):
        if self.graph_type == 'point':
            width=0
            return self.create_point(self._record_bbox[2:], self.color, width, tags, **kw)
        else:
            return self.create_graph(self.graph_type, self._record_bbox, self.color, width, tags, **kw)
    
    def drawing(self, width=1, tags=None, **kw):
        if self.record_bbox:
            self.delete('temp')
            if self.graph_type in ['line', 'point'] or not self.record_bbox < self.min_rect:
                return self.mouse_draw_graph(width, tags, activedash=10, **kw)

    def refresh_graph(self, event, **kw):
        if self.graph_type:
            self.after(5, lambda: self.drawing(
                width=2, tags='temp', dash=10, **kw))

    def finish_drawing(self, *event,  **kw):
        if self.graph_type and self.record_bbox:
            self.drawing(width=1, tags=None, **kw)
        self.reset(event)

    def reset(self, *event):
        self._record_bbox[:2] = ['none']*2

    def bind_drawing(self, master):
        master.bind('<B1-Motion>', self.refresh_graph)
        master.bind('<ButtonRelease-1>', self.finish_drawing)

    
class DrawRectangle(DrawMeta):
    def __init__(self, master=None, alpha=0.2, color='blue', graph_type='rectangle',
                 min_size=7, mask_color='red', cnf={}, **kw):
        '''
        '''
        super().__init__(master, graph_type, color, min_size, cnf, **kw)
        self.alpha= alpha
        self.mask_color = mask_color
        self.rectangle_selector = []
        self.tag_bind('mask', "<ButtonPress-1>", self.scroll_start)
        self.tag_bind('mask', "<B1-Motion>", self.scroll_move)

    def scroll_start(self, event):
        self.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        # self.move('current', w, h)
        # graph_id = self.find_withtag('current')
        # self.select_from(graph_id, 1)
        self.scan_dragto(event.x, event.y, gain=1)

    def create_mask(self, size, alpha, fill):
        '''设置透明蒙版'''
        fill = self.master.winfo_rgb(fill) + (alpha,)
        return Image.new('RGBA', size, fill)
        
    def draw_mask(self, x1, y1, x2, y2):
        size = x2-x1, y2-y1
        alpha = int(self.alpha * 255)
        image = self.create_mask(size, alpha, self.mask_color)
        self.rectangle_selector.append(ImageTk.PhotoImage(image))
        return self.create_image(x1, y1, image=self.rectangle_selector[-1], anchor='nw', tags='mask')

    def finish_drawing(self, *event,  **kw):
        if self.graph_type and self.record_bbox:
            if graph_id := self.drawing(width=1, tags=None, **kw):
                bbox = self.bbox(graph_id)
                mask = self.draw_mask(*bbox)
        self.reset(event)
