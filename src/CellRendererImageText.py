# Custom CellRenderer to _maybe_ render and  image and some text

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
from gi.repository import GObject

class CellRendererImageText(Gtk.CellRenderer):
    text = GObject.Property(type=str)
    pixbuf = GObject.Property(type=GdkPixbuf.Pixbuf, default='')
    empty = GObject.Property(type=bool, default=False)

    text_pixbuf_space = 10

    def __init__(self):
        Gtk.CellRenderer.__init__(self)
        self.text_renderer = Gtk.CellRendererText()
        self.pixbuf_renderer = Gtk.CellRendererPixbuf()

    def do_get_size(self, widget, cell_area):
        height = self.pixbuf_renderer.get_size(widget, cell_area).height
        height2 = self.text_renderer.get_size(widget, cell_area).height
        if height2 > height:
            height = height2

        width = self.text_renderer.get_size(widget, cell_area).width
        width = width + self.pixbuf_renderer.get_size(widget, cell_area).width + 5
        height = 28
        return (0, 0, width, height)

    def do_get_preferred_width(self, widget):
        cell_area = Gdk.Rectangle()
        cell_area.x = 0
        cell_area.y = 0
        cell_area.width = 300
        cell_area.height = 30
        width = self.text_renderer.get_size(widget, cell_area).width
        width = width + self.pixbuf_renderer.get_size(widget, cell_area).width + 5
        # TODO: This is broke

        return (500,width)

    def do_render(self, cr, widget, background_area, cell_area, flags):
        text_render_area = cell_area.copy()

        icon_render_area = cell_area.copy()
        icon_render_area.width = icon_render_area.height

        if(self.pixbuf != None):
            text_render_area.x = text_render_area.x + icon_render_area.width + self.text_pixbuf_space

        self.text_renderer.set_property("text", self.text)
        if self.empty:
            self.text_renderer.set_property("foreground-rgba", Gdk.RGBA(0.5, 0.5, 0.5, 1.0))
        else:
            pass
            #self.text_renderer.set_property("foreground-rgba", Gdk.RGBA(1.0, 1.0, 1.0, 1.0))

        self.text_renderer.render(cr, widget, background_area, text_render_area, flags)

        if self.pixbuf != None:
            self.pixbuf_renderer.set_property("pixbuf", self.pixbuf)
            self.pixbuf_renderer.render(cr, widget, background_area, icon_render_area, flags)
