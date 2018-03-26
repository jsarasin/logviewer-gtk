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
    def __init__(self, log_bytes):
        pass

class LogMinimapModel:
    def __init__(self):
        self._render_size_length = -1  # In horizontal layout, this would be the width

        self._regions = []

        def append_region(region):
            pass

        def replace_region(old_region, new_region):
            pass


class LogMinimapView(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        self._last_render_size_width = -1
        self._last_render_size_height = -1

        self.set_size_request(1500,50)
        self.mouse_in_cell = -1
        self.view_area_center = -1
        self.view_area_width = 30
        self.button1_down = False
        self._model = None

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
        self._model = model

    def mouse_button_press(self, widget, event):
        self.view_area_center = event.x
        self.button1_down = True
        self.queue_draw()
        pass

    def mouse_button_release(self, widget, event):
        self.button1_down = False

    def mouse_leave(self, widget, event):
        self.mouse_in_cell = -1
        self.queue_draw()

    def mouse_move(self, widget, event):
        pass

    def draw(self, widget, cr):
        cr.show_page()
        width = self.get_allocated_width()
        height = self.get_allocated_height()

        if self._model is None:
            return

        if self.model_requires_rebuild(width):
            self._model.rebuild(width)

    def model_requires_rebuild(self, width):
        if self._model._render_size_length != width:
            return True
        else:
            return False
