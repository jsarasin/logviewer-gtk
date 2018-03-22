def cat(self, widget, allocation):
    if self.watch_goto_bottom.get_active():
        self.suspend_schooling_margin_check = True
        self.log_messages_goto_bottom()
        self.suspend_schooling_margin_check = False




####################################################################################################################
## Log Messages Tree View                                                                store and column management
####################################################################################################################
# Create the combos
# # TODO: Not Generic Enough
# # TODO: Complete. I could probably add these as hidden columns same as above and then make a lamba to iterate over the treeview and do its magic
# if column_combo != '':
#     label = Gtk.Label()
#     label.set_text(column_combo)
#     combo = Gtk.ComboBoxText()
#     combo.append_text("All")
#     combo.set_active(0)
#     box = Gtk.Box(Gtk.Orientation.HORIZONTAL, 5)
#     box.set_homogeneous(True)
#     box.pack_start(label, True, True, 0)
#     box.pack_start(combo, True, True, 0)
#
#     self.message_filter_combos.add(box)
#     box.show_all()

#                                                                                  clear_messages_columns_and_combos
def clear_messages_columns_and_combos(self):
    return
    treeview = self.treeview_log_messages

    columns = treeview.get_columns()
    for n in columns:
        treeview.remove_column(n)

    for n in self.message_filter_combos.get_children():
        n.destroy()


# get_older_message_count
def get_older_message_count(self, service_name, service_module):
    if service_name not in self.older_messages_count:
        self.older_messages_count[service_name] = dict()

    if service_module not in self.older_messages_count[service_name]:
        self.older_messages_count[service_name][service_module] = 0

    return self.older_messages_count[service_name][service_module]


#                                                                                       increase_older_message_count
def increase_older_message_count(self, service_name, service_module, count):
    old_count = self.get_older_message_count(service_name, service_module)

    self.older_messages_count[service_name][service_module] = old_count


#                                                                                           load_more_older_messages
def load_more_older_messages(self, service_name, module_name, quantity=1000, auto_decompress=False):
    if auto_decompress:
        raise Exception("Auto Decompress not implemented")

    tree_store = self.get_message_tree_store(service_name, module_name)
    loaded_messages = self.get_older_message_count(service_name, module_name)
    new_message_count = self._logger.get_older_message_count(service_name, module_name)

    new_messages = self._logger.get_message_range(service_name, module_name, loaded_messages, new_message_count)

    if len(new_messages) == 0:
        return
    self.treeview_log_messages.set_model(None)
    self.append_messages_to_treestore(tree_store, service_name, new_messages)
    self.treeview_log_messages.set_model(tree_store)


def update_messages:



def get_messages_columns(self, service_name, service_module):
    def create_messages_columns(service_name, service_module):
        service_columns = self._logger.get_service_module_columns(service_name, service_module).GetColumns()
        if service_columns is None:
            return []

        column_list = []

        index = 0
        for column_index, column in enumerate(service_columns):
            column_key, column_display_name, column_type, column_combo, column_visible = column

            # Just a regular column
            if column_combo == '':
                column_renderer = Gtk.CellRendererText()
                column_value = Gtk.TreeViewColumn(column_display_name, column_renderer, text=index)
                column_value.set_sort_column_id(index)
                column_value.set_resizable(True)
                if column_visible == False:
                    column_value.set_visible(False)
                column_list.append(column_value)
                index = index + 1

        return column_list

    # This is fucked but it's late
    # TODO: Make this not fucked

    if service_name not in self.messages_columns:
        self.messages_columns[service_name] = dict()

    if service_module not in self.messages_columns[service_name]:
        new_messages_columns = self.create_messages_columns(service_name, service_module)
        self.messages_columns[service_name][service_module] = new_messages_columns

    return self.messages_columns[service_name][service_module]

#                                                                                 get_message_list_item_from_message
def get_message_list_item_from_message(self, service_name, service_module, message):
    service_columns = self._logger.get_service_module_columns(service_name, service_module).GetColumns()
    listy = []

    tooltip_column = self._logger.get_service_module_columns(service_name, service_module).GetTooltipColumn()

    i = 0
    for index, column in enumerate(service_columns):
        column_key, column_display_name, column_type, column_combo, column_visible = column

        if column_combo == '':
            if i == tooltip_column:
                column_value = str(message[column_key]).replace("&", "&amp;").replace("<", "&lt;")
            else:
                column_value = str(message[column_key])
            listy.append(column_value)
            i = i + 1

    return listy


#                                                                               create_message_tree_store_gtk_object
def create_message_tree_store_gtk_object(self, service_name, service_module):
    service_columns = self._logger.get_service_module_columns(service_name, service_module).GetColumns()

    types = []
    for n in service_columns:
        column_key, column_display_name, column_type, column_combo, column_visible = n
        if column_combo == '':
            types.append(str)

    gtk_tree_store = Gtk.TreeStore()

    gtk_tree_store.set_column_types(types)

    return gtk_tree_store


#                                                                                       append_messages_to_treestore
def append_messages_to_treestore(self, tree_store, service_name, service_module, messages):
    last_top_level_iterator = None  # TREE VIEW NODE HACK

    parent = None

    for index, n in enumerate(messages):
        print("messages: %s" % n)
        if n['message'][0:1] == ' ':  # TREE VIEW NODE HACK
            indented = True  # TREE VIEW NODE HACK
            n['message'] = "    " + n['message']  # TREE VIEW NODE HACK
        else:  # TREE VIEW NODE HACK
            indented = False  # TREE VIEW NODE HACK

            if indented:  # TREE VIEW NODE HACK
                parent = last_top_level_iterator  # TREE VIEW NODE HACK
            else:  # TREE VIEW NODE HACK
                parent = None  # TREE VIEW NODE HACK

        list_item = self.get_message_list_item_from_message(service_name, service_module, n)

        iterator = tree_store.append(parent, list_item)

        if indented is False:  # TREE VIEW NODE HACK
            last_top_level_iterator = iterator.copy()  # TREE VIEW NODE HACK

        self.increase_older_message_count(service_name, service_module, len(messages))


# create_message_tree_store
def create_message_tree_store(self, service_name, service_module):
    tree_store = self.create_message_tree_store_gtk_object(service_name, service_module)

    # Prime the logger to get some messages if there aren't already some
    # messages = self._logger.all_messages_for(service_name, service_module)
    #
    # if messages is None:
    #     self._logger.get_more_messages(service_name, service_module)
    #     messages = self._logger.all_messages_for(service_name, service_module)

    messages = None
    # No messages to get, return an empty treestore
    if messages is None:
        return tree_store

    self.append_messages_to_treestore(tree_store, service_name, service_module, messages)

    return tree_store


#                                                                                             get_message_list_store
def get_message_tree_store(self, service_name, service_module):
    if service_name not in self.messages_tree_stores:
        return None

    if service_module not in self.messages_tree_stores[service_name]:
        return None

    return self.messages_tree_stores[service_name][service_module]


#                                                                                          initialize_new_tree_store
def initialize_new_tree_store(self, service_name, service_module):
    if service_name not in self.messages_tree_stores:
        self.messages_tree_stores[service_name] = dict()
    if service_module in self.messages_tree_stores[service_name]:
        raise Exception("Tried to initialize a new tree store even though one existed")

    new_tree_store = self.create_message_tree_store(service_name, service_module)
    self.messages_tree_stores[service_name][service_module] = new_tree_store

    return self.messages_tree_stores[service_name][service_module]

    # increase_older_message_count


####################################################################################################################
## Log Messages                                                                                         UI Callbacks
####################################################################################################################
#                                                                                           update_messages_treeview
def change_messages_treeview_model(self, service_name, service_module):
    columns = self.get_messages_columns(service_name, service_module)

    self.clear_messages_columns_and_combos()
    for n in columns:
        self.treeview_log_messages.append_column(n)

    tree_store = self.get_message_tree_store(service_name, service_module)
    if tree_store is None:
        tree_store = self.initialize_new_tree_store(service_name, service_module)

    self.treeview_log_messages.set_model(tree_store)

    tooltip_column = self._logger.get_service_module_columns(service_name, service_module).GetTooltipColumn()

    if tooltip_column != None:
        self.treeview_log_messages.set_tooltip_column(tooltip_column)
    else:
        self.treeview_log_messages.set_tooltip_column(-1)

    return self.messages_tree_stores[service_name]


#                                                                            treeview_log_messages_single_item_popup
# Popup menu on the treeview_log_messages - When they have just one item selected
def treeview_log_messages_single_item_popup(self, event_time, copy_text, copy_raw_message, model, iterator):
    self.treeview_log_messages_popup = Gtk.Menu()

    mi_copy_cell_value = Gtk.MenuItem("Copy '" + str(copy_text) + "'")
    mi_copy_cell_value.connect("activate", self.treeview_log_messages_copy_text)
    self.treeview_log_messages_popup.append(mi_copy_cell_value)

    mi_copy_message = Gtk.MenuItem("Copy Raw Selected Message")
    mi_copy_message.connect("activate", self.treeview_log_messages_copy_line)
    self.treeview_log_messages_popup.append(mi_copy_message)

    mi_sep = Gtk.SeparatorMenuItem()
    self.treeview_log_messages_popup.append(mi_sep)
    mi_inspect = Gtk.MenuItem("Inspect Message")
    self.treeview_log_messages_popup.append(mi_inspect)

    self.treeview_log_messages_popup.show_all()
    self.treeview_log_messages_popup.popup(None, None, None, None, 3, event_time)

    return True


#                                                                                    treeview_log_messages_copy_text
def treeview_log_messages_copy_text(self, widget):
    self.clipboard.set_text(self.copy_text, -1)


#                                                                                         treeview_log_messages_line
def treeview_log_messages_copy_line(self, widget):
    self.clipboard.set_text(self.copy_line, -1)


#                                                                             treeview_log_messages_multi_item_popup
# Popup menu on the treeview_log_messages - When they have multiple items selected
def treeview_log_messages_multi_item_popup(self, event_time, copy_text, copy_raw_message, model, iterator):
    self.treeview_log_messages_popup = Gtk.Menu()

    mi_copy_cell_value = Gtk.MenuItem("Copy '" + str(copy_text) + "'")
    mi_copy_cell_value.connect("activate", self.treeview_log_messages_copy_text)
    self.treeview_log_messages_popup.append(mi_copy_cell_value)

    mi_copy_message = Gtk.MenuItem("Copy Raw Selected Messages")
    mi_copy_message.connect("activate", self.treeview_log_messages_copy_line)
    self.treeview_log_messages_popup.append(mi_copy_message)

    mi_sep = Gtk.SeparatorMenuItem()
    self.treeview_log_messages_popup.append(mi_sep)
    mi_inspect = Gtk.MenuItem("Inspect Messages")
    self.treeview_log_messages_popup.append(mi_inspect)

    self.treeview_log_messages_popup.show_all()
    self.treeview_log_messages_popup.popup(None, None, None, None, 3, event_time)

    return True


#                                                                                        treeview_log_messages_click
# Popup menu on the treeview_log_messages
def treeview_log_messages_click(self, tv, event):
    self.watch_goto_bottom.set_active(False)
    if event.button == 3:
        right_click_path = self.treeview_log_messages.get_path_at_pos(event.x, event.y)

        if right_click_path != None:
            self.treeview_log_messages.grab_focus()

            columns = self.treeview_log_messages.get_columns()
            rc_path, rc_col, rc_cellx, rc_celly = right_click_path

            selected_model, selected_iterators = self.treeview_log_messages.get_selection().get_selected_rows()

            # Get what text is in the cell the user right clicked on
            right_click_column_index = (columns.index(rc_col))
            right_click_iterator = selected_model.get_iter(rc_path)
            right_click_column_text = selected_model[right_click_iterator][right_click_column_index]

            self.copy_text = right_click_column_text

            # Get the raw message of the selected row
            for raw_text_index, n in enumerate(columns):
                if n.get_title() == "Raw Line":
                    break;

            # The user only has one item selected
            if len(selected_iterators) == 1:
                # TODO: This can corrupt the message. We should be getting this directly from the logger using the index
                raw_selected = selected_model[selected_iterators][raw_text_index].replace('&lt;', '<').replace('&amp;',
                                                                                                               '&')

                self.copy_line = raw_selected + "\n"
                self.treeview_log_messages_single_item_popup(event.time, right_click_column_text, raw_selected,
                                                             selected_model, selected_iterators)

            # The user has multiple items selected
            elif len(selected_iterators) > 1:
                raw_lines = []
                for n in selected_iterators:
                    raw_selected = selected_model[n][raw_text_index].replace('&lt;', '<').replace('&amp;', '&') + "\n"
                    raw_lines.append(raw_selected)

                self.copy_line = ''.join(raw_lines)

                self.treeview_log_messages_multi_item_popup(event.time, right_click_column_text, raw_selected,
                                                            selected_model, selected_iterators)

            return True


def treeview_log_messages_scrolled(self, widget, user_data):
    vscrollbar = self.treeview_log_messages_scrolled_window.get_vscrollbar();
    adjustment = vscrollbar.get_adjustment()

    value = adjustment.get_value()
    max = adjustment.get_upper() - adjustment.get_page_size()
    margin = adjustment.get_step_increment() * 2

    if value > max - margin:
        in_margin = True
    else:
        in_margin = False

    # When new items are being added, then we don't want to deal with timings and that
    # Hopefully if the user is trying to drag out the message with get through somewhere!
    if self.suspend_schooling_margin_check:
        in_margin = True

        # If the person is watching and following - and scrolls up two then toggle off follow
        # if self.watch_toggle.get_active() and self.watch_goto_bottom.get_active() and not in_margin:
        #     self.watch_goto_bottom.set_active(False)




    ####################################################################################################################
    ## Watch and Follow Log Messages
    ####################################################################################################################
    def watch_toggle_toggled(self, widget):
        if self.watch_toggle.get_active():
            self.watching_revealer.set_reveal_child(True)
        else:
            self.watching_revealer.set_reveal_child(False)
            self.watch_goto_bottom.set_active(False)

    def watch_goto_bottom_toggled(self, widget):
        self.log_messages_goto_bottom()

    def load_more_old_messages_now(self, widget):
        self.load_more_older_messages(self._selected_service, self._selected_module)
    def log_messages_goto_bottom(self):
        vscrollbar = self.treeview_log_messages_scrolled_window.get_vscrollbar();
        adjustment = vscrollbar.get_adjustment()
        adjustment.set_value(adjustment.get_upper())

# for n in self._logger.get_services():
#     icon = icon_for_service(n)
#     if icon is not None:
#         icon = icon.scale_simple(32, 32,  GdkPixbuf.InterpType.BILINEAR)
#     text = n
#     parent = tree_store.append(None, [text, icon, False])
#
#     modules = self._logger.get_service_modules(n)
#
#     # If there's only one service module, and its name matches the service name, then don't create child objects
#     if len(modules) == 1:
#         if modules[0] == n:
#             pass
#
#     # There are multiple modules for this service, create child objects
#     else:
#         for m in modules:
#             text = m[0]
#             empty = m[1]
#             tree_store.append(parent, [text, None, empty])
#
# return tree_store
