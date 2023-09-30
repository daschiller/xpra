#!/usr/bin/env python3
# Copyright (C) 2020-2021 Antoine Martin <antoine@xpra.org>
# Xpra is released under the terms of the GNU GPL v2, or, at your option, any
# later version. See the file COPYING for details.

from xpra.platform import program_context
from xpra.platform.gui import force_focus
from xpra.gtk.gtk_util import add_close_accel
from xpra.gtk.pixbuf import get_icon_pixbuf

import sys
import gi
gi.require_version("Gtk", "3.0")  # @UndefinedVariable
from gi.repository import Gtk, GLib  # @UnresolvedImport


def change_callback(entry, window):
    print("text=%s" % entry.get_text())
    window.set_title(entry.get_text())

def make_window():
    window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
    window.set_size_request(400, 100)
    window.set_position(Gtk.WindowPosition.CENTER)
    window.connect("delete_event", Gtk.main_quit)
    icon = get_icon_pixbuf("font.png")
    if icon:
        window.set_icon(icon)
    entry = Gtk.Entry()
    entry.set_max_length(50)
    entry.connect("changed", change_callback, window)
    title = "Hello"

    if len(sys.argv)>1:
        title = sys.argv[1]
    entry.set_text(title)
    entry.show()
    window.add(entry)
    return window

def main():
    with program_context("window-title", "Window Title"):
        w = make_window()
        add_close_accel(w, Gtk.main_quit)
        from xpra.gtk.signals import register_os_signals
        def signal_handler(*_args):
            Gtk.main_quit()
        register_os_signals(signal_handler)
        def show_with_focus():
            force_focus()
            w.show_all()
            w.present()
        GLib.idle_add(show_with_focus)
        Gtk.main()
        return 0

if __name__ == "__main__":
    main()
