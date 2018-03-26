# History Logger widget
import gi
import random


import logsystem
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GObject, GLib, Gdk, cairo


class LogRegion:
    preview_percent = property((lambda self: float(self.preview_bytes) / float(self.log_size)),
                               None,
                               None,
                               None)
    log_size = int
    def __init__(self, log_bytes):
        self.log_size = log_bytes
        self.message_line_lengths = []
        self.preview_bytes = 0
        self.render_line_heights = None

        # float(log_bytes * 0.5), [random.randrange(1, 101, 1) for _ in range(100)]
        noisy_preview = []
        remaining = log_bytes

        while(remaining > 0):
            noise = random.randrange(0, 200)
            if noise > remaining:
                noise = remaining

            noisy_preview.append(noise)
            remaining = remaining - noise

        self.append_preview(noisy_preview)


    def append_preview(self, preview_list):
        # preview_list is an array of [len(message)]
        max_in_list = max(preview_list)
        preview_bytes = sum(preview_list)

        for n in preview_list:
            preview_percent = n / max_in_list
            self.message_line_lengths.append(preview_percent)
        self.preview_bytes = self.preview_bytes + preview_bytes

class LogMinimapModel:
    pass

class LogMinimapView(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        self.connect("draw", self.draw)


        # self._last_render_size_width = -1
        # self._last_render_size_height = -1
        self.set_size_request(1500,50)
        self.mouse_in_cell = -1
        self.view_area_center = -1
        self.view_area_width = 30
        self.button1_down = False
        self._model = None

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

        # Gtk.Widget.signals.scroll_event(widget, event)
        # Gtk.Widget.signals.button_press_event(widget, event)      ::button-press-event         Gdk.EventMask.BUTTON_PRESS_MASK
        # Gtk.Widget.signals.button_release_event(widget, event)     ::button-release-event      Gdk.EventMask.BUTTON_RELEASE_MASK
        # Gtk.Widget.signals.enter_notify_event(widget, event)       ::enter-notify-event    Gdk.EventMask.ENTER_NOTIFY_MASK
        # Gtk.Widget.signals.focus_in_event(widget, event)          :focus-in-event          Gdk.EventMask.FOCUS_CHANGE_MASK
        # Gtk.Widget.signals.focus_out_event(widget, event)         ::focus-out-event        Gdk.EventMask.FOCUS_CHANGE_MASK
        # Gtk.Widget.signals.leave_notify_event(widget, event)       ::leave-notify-event    Gdk.EventMask.LEAVE_NOTIFY_MASK

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
        # Find what cell the mouse is in
        # for index, n in enumerate(reversed(self._log)):
        #     cell_start = n.x1
        #     cell_end = n.x2
        #     if event.x >= cell_start and event.x < cell_end:
        #         self.mouse_in_cell = index
        #         self.queue_draw()
        # if self.button1_down == True and self.view_area_center != event.x:
        #     self.view_area_center = event.x
        #     self.queue_draw()

    def draw(self, widget, cr):
        cr.show_page()
        width = self.get_allocated_width()
        height = self.get_allocated_height()

        if self.render_size_changed(width, height):
            self.update_log_render_size(width, height)





    def render_size_changed(self, width, height):
        if width != self._last_render_size_width or height != self._last_render_size_height:
            return True

    def get_total_log_size(self):
        return sum(log.log_size for log in self._log)

    def update_log_render_size(self, width, height):
        self._last_render_size_width = width
        self._last_render_size_height = height

        byte_to_pixel = float(width - len(self._log)) / float(self.get_total_log_size())

        last_x_position = float(0)
        for log in reversed(self._log):
            x1 = last_x_position
            x2 = last_x_position + log.log_size * byte_to_pixel

            log.x1 = int(x1)
            log.x2 = int(x2)
            last_x_position = x2 + 1



