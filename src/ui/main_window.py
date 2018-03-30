import os
import gi

import logsystem
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GObject, GLib, Gdk

from LogMinimap import LogMinimapView, LogMinimapModel, LogMinimapRegion


from CellRendererImageText import CellRendererImageText
from ui.view_service_window import ViewServiceWindow
from icon_for_service import icon_for_service

from logsystem import LogSystem, Event, SyslogTarget

from pprint import pprint


# self._services[event.service_name][event.service_module]['minimap_model'] = LogMinimapModel()
# self._services[event.service_name][event.service_module]['treestore'] = Gtk.TreeStore()
# self._services[event.service_name][event.service_module]['columns'] = []
    # column_key, column_display_name, column_type, column_combo, column_visible = n
    # self._services[event.service_name][event.service_module]['columns'].append(n)
# self._services[event.service_name][event.service_module]['sources'] = [dict_source]
    # dict_source = {'relative_filename', 'file_size', 'is_compressed'}


class MainWindow:
    def _logger_callback_message_columns(self, event):
        types = []

        for n in event.columns.columns:
            column_key, column_display_name, column_type, column_combo, column_visible = n
            self._services[event.service_name][event.service_module]['columns'].append(n)
            types.append(column_type)

        # If we're getting this message than the treestore hasn't had its columns types set. Do it here
        self._services[event.service_name][event.service_module]['treestore'] = Gtk.TreeStore()
        treestore = self._services[event.service_name][event.service_module]['treestore']

        treestore.set_column_types(types)

    def _logger_callback_load_older_messages(self, event):
        treestore = self._services[event.service_name][event.service_module]['treestore']
        minimap_model = self._services[event.service_name][event.service_module]['minimap_model']

        minimap_region = minimap_model.get_region(event.source)


        if event.service_name == self._selected_service and event.service_module == self._selected_module:
            this_sm_visible = True
            if self.treeview_messages.get_model() is None:
                full_show_treeview = True
            else:
                full_show_treeview = False
                # GTK will append items to our treestore very slowly if it is visible, hide it if it is
            # self.treeview_messages.set_model(None)
        else:
            this_sm_visible = False
            full_show_treeview = False

        if event.messages is None:
            return

        for message in event.messages:
            columns = []

            for index, column in enumerate(self._services[event.service_name][event.service_module]['columns']):
                column_key, column_display_name, column_type, column_combo, column_visible = column

                columns.append(str(message[column_key]))

            minimap_region.append_line(len(str(message[column_key])))

            treestore.append(None, columns)

        if full_show_treeview:
            self.set_visible_service_module(event.service_name, event.service_module)


        # Update the minimap with the new messages
        if self.log_history_viewer._orientation == LogMinimapView.Horizontal:
            minimap_size = self.log_history_viewer.get_allocated_width()
        elif self.log_history_viewer._orientation == LogMinimapView.Vertical:
            minimap_size = self.log_history_viewer.get_allocated_height()
        minimap_model.rebuild_minimap(minimap_size)

    def _logger_callback_get_service_module_sources(self, event):
        self._services[event.service_name][event.service_module]['sources'] = event.sources

        new_minimap_model = LogMinimapModel()
        self._services[event.service_name][event.service_module]['minimap_model'] = new_minimap_model

        for n in event.sources:
            new_minimap_model.append_region(LogMinimapRegion(n['relative_filename'], n['file_size']))

    def _logger_get_modules(self, event):
        for n in event.modules:

            if event.service_name not in self._services:
                self._services[event.service_name] = dict()

            if n[0] not in self._services[event.service_name]:
                self._services[event.service_name][n[0]] = dict()

            self._services[event.service_name][n[0]]['empty'] = n[1]

            self.append_services_treestore(event.service_name, n[0], n[1])

            self._logger.get_service_module_sources(event.service_name, n[0])

    def _logger_callback(self, event):
        if type(event) == Event.GetServices:
            for n in event.services:
                self._logger.get_service_modules(n)
            return

        if type(event) == Event.GetModules:
            self._logger_get_modules(event)
            return

        if type(event) == Event.GetModuleSources:
            self._logger_callback_get_service_module_sources(event)
            return

        if type(event) == Event.GetModuleColumns:
            self._logger_callback_message_columns(event)
            return

        if type(event) == Event.LoadOlderMessages:
            self._logger_callback_load_older_messages(event)
            return

    def __init__(self):
        # User Interface elements
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/main_window.glade")
        self.window = self.builder.get_object("main_window")
        self.button_watch = self.builder.get_object("watch_toggle")
        self.treeview_services = self.builder.get_object("treeview_log_sources")
        self.treeview_messages = self.builder.get_object("treeview_log_messages")
        self.treeview_messages_scrolled_window = self.builder.get_object("treeview_log_messages_scrolled_window")
        self.revealer_watching = self.builder.get_object("watching_revealer")
        self.button_goto_bottom = self.builder.get_object('watch_goto_bottom')
        self.box_message_filter_combos = self.builder.get_object("message_filter_combos")
        self.button_load_more_messages = self.builder.get_object("load_more_messages")
        self.history_browser_box = self.builder.get_object("history_browser_box")

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        self.connect_builder_objects()


        # Local store
        self._selected_service = None
        self._selected_module = None
        self._services = None


        # Logger setup
        self._services = dict()
        log_root = os.getcwd().rpartition('/')[0] + "/log/"
        self._logger = LogSystem(SyslogTarget(log_root), self._logger_callback)
        self._logger.get_services()

        self.window.show_all()

    def append_services_treestore(self, service_name, service_module, empty):
        iterator = self._services_tree_store.get_iter_first()

        parent = None
        icon = None
        empty = False


        # Search for a parent
        if iterator is not None:
            while(iterator):
                if self._services_tree_store[iterator][0] == service_name:
                    parent = iterator
                    break
                iterator = self._services_tree_store.iter_next(iterator)

        if parent is None:
            icon = icon_for_service(service_name)
            if icon is not None:
                icon = icon.scale_simple(32, 32,  GdkPixbuf.InterpType.BILINEAR)
            parent = self._services_tree_store.append(None, [service_name, icon, False])

        self._services_tree_store.append(parent, [service_module, None, empty])
    ####################################################################################################################
    ## UI functionality utility functions                                                                    Setup of UI
    ####################################################################################################################
    def clear_treewview_messages_columns(self):
        columns = self.treeview_messages.get_columns()
        for n in columns:
            self.treeview_messages.remove_column(n)

    def build_treeview_message_columns(self, service_name, service_module):
        if self._services[service_name][service_module]['columns'] == []:
            print("no columns")
            return

        for index, n in enumerate(self._services[service_name][service_module]['columns']):
            column_key, column_display_name, column_type, column_combo, column_visible = n

            column_renderer = Gtk.CellRendererText()
            column_value = Gtk.TreeViewColumn(column_display_name, column_renderer, text=index)
            column_value.set_resizable(True)
            self.treeview_messages.append_column(column_value)

    ####################################################################################################################
    ## Higher level UI functionality                                                                         Setup of UI
    ####################################################################################################################
    def set_visible_service_module(self, service_name, service_module):
        if service_name is None or service_module is None:
            self.log_history_viewer.set_model(None)
            self.treeview_messages.set_model(None)
            return

        if service_name not in self._services:
            raise Exception("Service: %s not in self._services" % (service_name))

        if service_module not in self._services[service_name]:
            raise Exception("Service module %s:%s not in self._services" % (service_name, service_module))

        self.clear_treewview_messages_columns()

        # Create a new tree store and columns if it doesn't already exist
        if 'treestore' not in self._services[service_name][service_module]:
            self._services[service_name][service_module]['treestore'] = None
            self._services[service_name][service_module]['columns'] = []
            self.treeview_messages.set_model(None)
            self.clear_treewview_messages_columns()

            result1 = self._logger.get_service_module_columns(service_name, service_module)
            result2 = self._logger.load_older_messages(service_name, service_module, 4000)
            if result1 is not None or result2 is not None:
                raise Exception("Unable to request columns or messages for service: %s:%s" % service_name, service_module)
            return

        self.build_treeview_message_columns(service_name, service_module)

        minimap_model = self._services[service_name][service_module]['minimap_model']
        self.log_history_viewer.set_model(minimap_model)
        treestore = self._services[service_name][service_module]['treestore']
        self.treeview_messages.set_model(treestore)


    ####################################################################################################################
    ## UI Calllbacks                                                                                         Setup of UI
    ####################################################################################################################
    def action_view_service_information(self, menu_item):
        model, selection_iterator = self.treeview_services.get_selection().get_selected()

        if selection_iterator is not None:
            object_path = model.get_path(selection_iterator)
            if object_path.get_depth() == 2:
                object_parent_path = object_path.copy()
                object_parent_path.up()
                parent_iterator = model.get_iter(object_parent_path)

                selected_service = model[parent_iterator][0]
                selected_module = model[selection_iterator][0]
            elif object_path.get_depth() == 1:
                selected_module = None
                selected_service = model[selection_iterator][0]
            else:
                raise Exception("That wasn't expected! Trying to select the service module here.")

            view_service = ViewServiceWindow(self._logger, selected_service, selected_module)

    def service_selection_change(self, treeview):
        model, selection_iter = treeview.get_selection().get_selected()
        if selection_iter is None:
            return
        path = model.get_path(selection_iter)
        indicies = path.get_indices()

        has_children = model.iter_has_child(selection_iter)

        # A first level object. This will be the service name
        if len(indicies) == 1:
            self._selected_service = model[selection_iter][0]

            if has_children:
                self._selected_module = None
            else:
                self._selected_module = self._selected_service

        # A second level object, this will be the service module
        elif len(indicies) == 2:
            parent_path = path.copy()
            parent_path.up()
            parent_iter = model.get_iter(parent_path)
            self._selected_service = model[parent_iter][0]
            self._selected_module = model[selection_iter][0]
        else:
            raise Exception("Woo that wasn't expected")

        if self._selected_service is not None:
            if self._selected_module is None:
                # If they have clicked on a module name try and get a module name with the same name. This indicates
                # That there were no submodules detected
                self.clear_treewview_messages_columns()
                self.treeview_messages.set_model(None)
                self.log_history_viewer.set_model(None)
            else:
                self.set_visible_service_module(self._selected_service, self._selected_module)

    def service_selection_activated(self, treeview, path, column):
        # Expand/Collapse a top level row on double click
        if path.get_depth() == 1:
            if treeview.row_expanded(path):
                treeview.collapse_row(path)
            else:
                treeview.expand_row(path, True)

    #                                                                                            treeview_services_click
    def treeview_services_click(self, treeview, event):
        pthinfo = treeview.get_path_at_pos(event.x, event.y)
        model = treeview.get_model()

        if pthinfo is None:
            return
        path, col, cellx, celly = pthinfo
        clicked_item_iterator = model.get_iter(path)


        if event.button == 3:
            treeview.grab_focus()
            treeview.set_cursor(path,col,0)

            self.treeview_services_popup = Gtk.Menu()
            vsi = Gtk.MenuItem("View Service Information " + self._selected_service)
            vsi.connect('activate', self.action_view_service_information )
            self.treeview_services_popup.append(vsi)

            if self._selected_module is not None:
                vmi = Gtk.MenuItem("View Module Information " + self._selected_module)
                vmi.connect('activate', self.action_view_service_information )
                self.treeview_services_popup.append(vmi)

            if self._selected_module is None:
                rescan_sep = Gtk.SeparatorMenuItem()
                self.treeview_services_popup.append(rescan_sep)

                rescan = Gtk.MenuItem("Rescan Service Flat")
                self.treeview_services_popup.append(rescan)


            self.treeview_services_popup.show_all()
            self.treeview_services_popup.popup(None, None, None, None, 3, event.time)

            return False

    def treeview_messages_click(self, tv, event):
        pass

    def treeview_messages_resize(self, allocation, cat):
        pass

    def treeview_messages_vscroll_changed(self, widget, user_data):
        pass

    def load_more_old_messages_now(self, widget):
        result = self._logger.load_older_messages(self._selected_service, self._selected_module, 1000)

    def timer_load_more_messages(self, user_data):
        if self._selected_module is not None and self._selected_service is not None:
            self._logger.load_older_messages(self._selected_service, self._selected_module, 5000)
        return True

    ####################################################################################################################
    ## Glade Initialization of main_window
    ####################################################################################################################
    def messages_setup(self):
        self.treeview_messages.connect("button_press_event", self.treeview_messages_click)
        self.treeview_messages.connect("size-allocate", self.treeview_messages_resize)
        vscrollbar = self.treeview_messages_scrolled_window.get_vscrollbar();
        vscrollbar.connect("value-changed", self.treeview_messages_vscroll_changed, None)

    def service_column_setup(self):
        self._services_tree_store = Gtk.TreeStore(str, GdkPixbuf.Pixbuf, bool)
        self.treeview_services.connect("button_press_event", self.treeview_services_click)
        self.treeview_services.connect("cursor-changed", self.service_selection_change)
        self.treeview_services.connect("row-activated", self.service_selection_activated)
        render_service_name = CellRendererImageText()
        column_service_name = Gtk.TreeViewColumn("Service", render_service_name, text=0, pixbuf=1, empty=2)
        self.treeview_services.append_column(column_service_name)

        self.treeview_services.set_model(self._services_tree_store)

    def connect_builder_objects(self):
        self.window.connect("delete-event", Gtk.main_quit)
        self.service_column_setup()
        self.messages_setup()

        # # self.load_more_old_messages = self.builder.get_object("load_more_old_messages")
        # self.load_more_old_messages.connect("clicked", self.load_more_old_messages_now)


        # Setup the custom log minimap viewer
        self.log_history_viewer = LogMinimapView()
        self.log_history_viewer.show()
        self.log_history_viewer.set_hexpand(True)

        self.history_browser_box.add(self.log_history_viewer)

        # Star the auto load more messages things
        GLib.timeout_add(30, self.timer_load_more_messages, None)


