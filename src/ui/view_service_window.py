import os

import cairo
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GdkPixbuf, GObject, GLib, Gdk

from CellRendererImageText import CellRendererImageText
from icon_for_service import icon_for_service
from datetime import datetime, time, date

class ViewServiceWindow():
    def __init__(self, logger, service_name, service_module):
        self._logger = logger
        self._service_name = service_name
        self._service_module = service_module

        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/view_service_window.glade")

        self.connect_builder_objects()

        self.window.show_all()
        self.update_items()

    def close_window_button(self, widget):
        self.window.destroy()

    def window_closed(self, widget, event):
        self.window.destroy()
            #self.window.close()

    def draw_breadcrumb_arrow(self, widget, cairo_context):
        width = widget.get_allocated_width()
        height = widget.get_allocated_height()

        self.label_service_name.get_style_context().add_class(" #label_service_name { background-color: #FFF; } ")

        horrible_hack = Gtk.Entry()
        style = horrible_hack.get_style_context()
        style.save();
        style.set_state(Gtk.StateFlags.SELECTED)
        crumb_arrow_color = style.get_background_color(Gtk.StateFlags.SELECTED)
        style.restore()
        horrible_hack.destroy()

        cairo_context.set_source_rgba(crumb_arrow_color.red, crumb_arrow_color.green, crumb_arrow_color.blue, crumb_arrow_color.alpha)
        cairo_context.move_to(0, 0)
        cairo_context.line_to(width, height / 2)
        cairo_context.line_to(0, height)
        cairo_context.line_to(0, 0)
        cairo_context.fill()
        return

    #                                                                                            connect_builder_objects
    def connect_builder_objects(self):
        self.window = self.builder.get_object("view_service_window")
        self.window.set_title("View Service Information")
        self.window.connect("delete-event", self.window_closed)

        self.breadcrum_arrow = self.builder.get_object('breadcrum_arrow')
        self.breadcrum_arrow.connect('draw', self.draw_breadcrumb_arrow)

        self.label_service_name = self.builder.get_object("label_service_name")
        self.label_service_module = self.builder.get_object("label_service_module")

        self.service_icon = self.builder.get_object("service_icon")
        self.treeview_service_information = self.builder.get_object("treeview_service_information")
        self.create_filenames_columns()

        self.view_service_window_close_button = self.builder.get_object("view_service_window_close_button")
        self.view_service_window_close_button.connect("clicked", self.close_window_button)

        self.icon_theme = Gtk.IconTheme.get_default()

    #                                                                                           create_filenames_columns
    def create_filenames_columns(self):
        # The filename column
        renderer = CellRendererImageText()
        column = Gtk.TreeViewColumn("Log Files", renderer,text=0, pixbuf=1)
        self.treeview_service_information.append_column(column)

        # The modified column
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Modified", renderer, text=2)
        column.set_fixed_width(100)
        column.set_max_width(100)
        self.treeview_service_information.append_column(column)


    #                                                                                         create_filenames_liststore
    def create_filenames_liststore(self):
        return None
        listview = Gtk.ListStore(str, GdkPixbuf.Pixbuf, str)

        for n in self._logger.get_service_module_sources(self._service_name, self._service_name):
            filename = n['filename']
            modified = datetime.fromtimestamp(n['modified'])

            if (filename.find(".gz") != -1):
                icon = self.icon_theme.load_icon("gnome-mime-application-x-compress", 32, Gtk.IconLookupFlags.FORCE_SVG)
                icon = icon.scale_simple(28, 28,  GdkPixbuf.InterpType.BILINEAR)
            else:
                icon = self.icon_theme.load_icon("gnome-mime-text-plain", 32, Gtk.IconLookupFlags.FORCE_SVG)
                icon = icon.scale_simple(28, 28,  GdkPixbuf.InterpType.BILINEAR)


            listview.append([filename, icon, str(modified)])

        return listview

    #                                                                                                       update_items
    def update_items(self):
        self.label_service_name.set_label(self._service_name)

        if self._service_module is not None:
            self.label_service_module.set_label(self._service_module)
        else:
            self.label_service_module.set_label('')

        icon = icon_for_service(self._service_name)

        if icon is not None:
            self.service_icon.set_visible(True)
            self.service_icon.set_from_pixbuf(icon.scale_simple(64, 64,  GdkPixbuf.InterpType.BILINEAR))
        else:
            self.service_icon.set_visible(False)

        self.treeview_service_information.set_model(self.create_filenames_liststore())
        #self.treeview_service_information.columns_autosize()