# History Logger widget
import gi
import random


import logsystem
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GObject, GLib, Gdk, cairo

"""
This widget can be rendered horizontally, or vertically. As such, the word 'length' refers to the axis along
which the different log entries are rendered. If this widget is being rendered horizontally, then this would
refer to the width.

150 character long message length will represent 100% of the visible preview of a line.  

This widget was made with the intention of being able to express multiple syslog files refered to as 
'regions'. Because regions can be of a known size, but unknown number of text lines, a certain fudge is
required. The rendering of a region is broken into two parts: Known text lines, and unknown. When rendered,
these two parts will be divided based on the % of total bytes of the file which they are expressing. This
will most likely change the look of the minimap when zoomed out.
"""

class LogMinimapRegion:
    def __init__(self, relative_filename, log_bytes):
        self._relative_filename = relative_filename
        self._log_bytes = log_bytes
        self._lines = []
        self._render_lines = []
        self._known_percent = float(0)

    def append_line(self, line_length):
        self._lines.append(line_length)
        self._known_percent = float(sum(self._lines)) / float(self._log_bytes)

class LogMinimapModel:
    def __init__(self):
        self._render_size_length = -1  # In horizontal layout, this would be the width

        self._regions = []
        self._total_size = 0
        self._view = None

    def append_region(self, region):
        self._regions.append(region)
        self._total_size += region._log_bytes

    def get_region(self, name):
        for n in self._regions:
            if n._relative_filename == name:
                return n

        return None

    def replace_region(self, old_region, new_region):
        pass

    def _set_view(self, view):
        self._view = view

    def rebuild_minimap(self, length):
        self._render_size_length = length
        rcount = len(self._regions)

        left_pos = 0
        for n in self._regions:
            region_percent = float(n._log_bytes) / float(self._total_size)
            n.p1 = left_pos
            n.p2 = left_pos + int(float(length) * region_percent)
            cell_length = n.p2 - n.p1
            left_pos = n.p2

            # Build the preview for lines
            n._render_lines = []
            if len(n._lines) == 0:
                continue

            render_line_size = (n._known_percent * float(cell_length)) / float(len(n._lines))
            render_line_start = float(0)
            render_line_end_int = -1
            for k in n._lines:
                line_start = int(render_line_start)
                line_end = int(render_line_start + render_line_size)
                line_quantity = float(k / 300)

                if line_start > render_line_end_int or False:
                    n._render_lines.append((render_line_start, line_end, line_quantity))
                    render_line_end_int = line_end # This is to optimize out lines piled ontop of eachother
                                                   # a better solution would be to average out the lines that are
                                                   # to be rendered in the same spot, then it appear more consistant

                render_line_start = render_line_start + render_line_size

        if self._view is not None:
            self._view.queue_draw()








class LogMinimapView(Gtk.DrawingArea):
    class Horizontal:
        pass

    class Vertical:
        pass

    def __init__(self):
        super().__init__()
        self._last_render_size_width = -1
        self._last_render_size_height = -1

        self.set_size_request(500,50)
        self._mouse_in_cell = -1
        self.view_area_center = -1
        self.view_area_width = 30
        self.button1_down = False
        self._model = None
        self._orientation = self.Horizontal
        self._zoom = 1

        # setup events
        self.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)
        self.add_events(Gdk.EventMask.BUTTON1_MOTION_MASK)
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.add_events(Gdk.EventMask.POINTER_MOTION_HINT_MASK)
        self.connect("motion-notify-event", self.mouse_move)
        self.connect("leave-notify-event", self.mouse_leave)
        self.connect("button-press-event", self.mouse_button_press)
        self.connect("button-release-event", self.mouse_button_release)
        self.connect("draw", self.draw)


    def set_model(self, model):
        if model is not None:
            model._set_view(self)

        self._model = model


        self.queue_draw()

    def mouse_button_press(self, widget, event):
        self.view_area_center = event.x
        self.button1_down = True
        self.queue_draw()
        pass

    def mouse_button_release(self, widget, event):
        self.button1_down = False

    def mouse_leave(self, widget, event):
        self._mouse_in_cell = -1
        self.queue_draw()

    def mouse_move(self, widget, event):
        if self._model is None:
            return

        for index, n in enumerate(self._model._regions):
            if self._orientation == self.Horizontal:
                if event.x > n.p1 and event.x < n.p2:
                    self._mouse_in_cell = index
                    self.queue_draw()
                    break

    def draw(self, widget, cr):
        cr.show_page()
        width = self.get_allocated_width()
        height = self.get_allocated_height()

        if self._model is None:
            return

        if self.model_requires_rebuild(width):
            if self._orientation == self.Horizontal:
                self._model.rebuild_minimap(width * self._zoom)
            else:
                self._model.rebuild_minimap(height * self._zoom)

        cell_top = 0
        cell_bottom = height
        alternating_background = 0

        for index, n in enumerate(self._model._regions):
            hovering = False

            if self._mouse_in_cell == index:
                hovering = True

            cell_left = n.p1
            cell_right = n.p2


            if alternating_background == 0:
                alternating_background = 1
            else:
                alternating_background = 0


            if not hovering:
                if alternating_background == 0:
                    cr.set_source_rgb(0.2, 0.2, 0.2)
                else:
                    cr.set_source_rgb(0.25, 0.25, 0.25)
            else:
                cr.set_source_rgb(0.4, 0.4, 0.4)

            cr.move_to(cell_left, cell_top)
            cr.line_to(cell_left, cell_bottom)
            cr.line_to(cell_right, cell_bottom)
            cr.line_to(cell_right, cell_top)
            cr.line_to(cell_left, cell_top)
            cr.fill()

            for j in n._render_lines:

                line_start, line_end, line_quantity = j
                cr.set_source_rgb(line_quantity,line_quantity , line_quantity)

                line_left = cell_left + line_start
                line_right = line_end
                line_bottom = cell_bottom
                line_top = cell_bottom - int(float(cell_bottom) * line_quantity)

                cr.move_to(line_left, line_bottom)
                cr.line_to(line_left, line_top)
                cr.line_to(line_right, line_top)
                cr.line_to(line_right, line_bottom)
                cr.line_to(line_left, line_bottom)
                cr.stroke()

            text_height = 10
            cr.move_to(cell_left + 11, cell_top + 11 + text_height)
            cr.set_source_rgb(0.3, 0.3, 0.3)
            cr.show_text(n._relative_filename )
            cr.move_to(cell_left + 10, cell_top + 10 + text_height)
            cr.set_source_rgb(1,1,1)
            cr.show_text(n._relative_filename )


    def model_requires_rebuild(self, width):

        if self._model._render_size_length != width:
            return True
        else:
            return False
