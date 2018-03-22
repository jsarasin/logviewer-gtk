#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GObject, GLib

import os

from ui.main_window import MainWindow
from ui.view_service_window import ViewServiceWindow


log_viewer = MainWindow()

Gtk.main()

