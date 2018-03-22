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


class LogHistoryView(Gtk.DrawingArea):
    sample_log_large = [LogRegion(798773), LogRegion(1122067), LogRegion(227212), LogRegion(1374550), LogRegion(943567)]
    sample_log_small = [LogRegion(6170), LogRegion(65176), LogRegion(49020), LogRegion(59926), LogRegion(49267)]

    def __init__(self):
        super().__init__()
        self.connect("draw", self.draw)

        self._log = self.sample_log_large
        self._last_render_size_width = -1
        self._last_render_size_height = -1
        self.set_size_request(1500,50)
        self.mouse_in_cell = -1
        self.view_area_center = -1
        self.view_area_width = 30
        self.button1_down = False

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
        for index, n in enumerate(reversed(self._log)):
            cell_start = n.x1
            cell_end = n.x2
            if event.x >= cell_start and event.x < cell_end:
                self.mouse_in_cell = index
                self.queue_draw()
        if self.button1_down == True and self.view_area_center != event.x:
            self.view_area_center = event.x
            self.queue_draw()

    def draw(self, widget, cr):
        cr.show_page()
        width = self.get_allocated_width()
        height = self.get_allocated_height()

        if self.render_size_change(width, height):
            self.update_log_render_size(width, height)
        for index, n in enumerate(reversed(self._log)):
            cell_width = n.x2 - n.x1
            cell_start = n.x1
            cell_end = n.x2

            mystery_width = cell_width - int((float(cell_width * n.preview_percent)))
            known_width = cell_width - mystery_width

            draw_mystery_area = False
            if draw_mystery_area:
                # Draw the area where we don't have any preview bytes loaded
                cr.set_source_rgb(0.2, 0.2, 0.2)
                cr.move_to(cell_start, 0)
                cr.line_to(cell_start, height)
                cr.line_to(cell_start + float(mystery_width), height)
                cr.line_to(cell_start + float(mystery_width), 0)
                cr.line_to(cell_start, 0)
                cr.fill()

            if index == self.mouse_in_cell:
                cr.set_source_rgb(0.3,0.3,0.3)
                cr.move_to(cell_start, 0)
                cr.line_to(cell_start, height)
                cr.line_to(cell_end, height)
                cr.line_to(cell_end, 0)
                cr.line_to(cell_start, 0)
                cr.fill()


            log_lines_per_pixel = float(len(n.message_line_lengths)) / float(known_width)
            if log_lines_per_pixel < 1:
                raise Exception("Not implemented")

            minimum_render_width = 4 # Although this does provide more of an aestheticlly pleasing visual, it may
            # overlook patterns in the text. It may be important to look for patterns while
            # generating the list



            if n.render_line_heights is None:
                log_lines = len(n.message_line_lengths)
                render_lines_height = []

                while log_lines > 0 :
                    lines_sample_index_start = int(log_lines-(log_lines_per_pixel * minimum_render_width))
                    lines_sample_index_end = int(log_lines-(log_lines_per_pixel * minimum_render_width) + (log_lines_per_pixel * minimum_render_width))

                    lines_sample = n.message_line_lengths[lines_sample_index_start:lines_sample_index_end]
                    lines_average_length = sum(lines_sample) / (log_lines_per_pixel * minimum_render_width)

                    render_lines_height.append(lines_average_length)
                    log_lines = log_lines - (log_lines_per_pixel * minimum_render_width)

                n.render_line_heights = render_lines_height
            else:
                render_lines_height = n.render_line_heights



            # Now render the damn lines!
            for indexy, d in enumerate(render_lines_height):
                if d == 0:
                    continue
                coyl = 0.6 #float(float(indexy) / float(len(render_lines_height)))
                cr.set_source_rgb(coyl, coyl, coyl)
                line_start = cell_start + cell_width - known_width + (indexy * minimum_render_width)
                cr.move_to(line_start, height)
                cr.line_to(line_start, d * height)
                cr.line_to(line_start+minimum_render_width, d * height)
                cr.line_to(line_start+minimum_render_width, height)
                cr.line_to(cell_start, height)
                cr.fill()
                cr.new_path()

        if self.view_area_center != -1:
            # Draw the red line
            cr.set_source_rgba(0.7, 0, 0, 0.7)
            cr.set_line_width(3)
            cr.move_to(self.view_area_center, 0)
            cr.line_to(self.view_area_center, height)
            cr.stroke()
            cr.set_line_width(1)

            # Draw the view area
            half_view_width = float(self.view_area_width) / 2

            cr.set_source_rgba(0.8, 0.8, 0.8, 0.3)
            cr.move_to(self.view_area_center - half_view_width, 0)
            cr.line_to(self.view_area_center - half_view_width, height)
            cr.line_to(self.view_area_center + half_view_width, height)
            cr.line_to(self.view_area_center + half_view_width, 0)
            cr.line_to(self.view_area_center - half_view_width, 0)
            cr.fill()








    def render_size_change(self, width, height):
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



