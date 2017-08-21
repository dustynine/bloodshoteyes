#!/usr/bin/env python

import sys
import getopt
import time
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GObject


ONE_SECOND = 1000

ICONS = (os.path.abspath("./tray/icon00.png"),
         os.path.abspath("./tray/icon25.png"),
         os.path.abspath("./tray/icon50.png"),
         os.path.abspath("./tray/icon75.png"))

# class Bse(Gtk.Application):
#     def __init__(self, application_id, flags):
#         Gtk.Application.__init__(self, application_id = application_id,
#                 flags = flags)
#         self.connect("activate", self.create_manager)
#
#     def create_manager(self, *args):
#         pass


class Manager(Gtk.Application):
    def __init__(self, **kwargs):
        Gtk.Application.__init__(self,
                application_id="com.github.dustynine.bloodshoteyes",
                flags = Gio.ApplicationFlags.FLAGS_NONE)
        for (key, value) in kwargs.items():
            setattr(self, key, value)

        self.set_work_end()

        self.connect("startup", self.start_manager)
        self.connect("activate", self.initiate)

        self.idle = GObject.idle_add(self.idle_func)
        self.first_timeout = GObject.timeout_add(self.work_secs*ONE_SECOND, self.start_break)

    def initiate(self, event):
        print("== "+time.strftime("%H:%M", time.localtime())+" Initiated")

    def start_manager(self, event):
        self.tray = Tray(self)
        # pass
        # print('started')
        # while time.time() < self.work_end:
        #     time.sleep(1)
        #     print('ted')
        # else:
        #     self.start_break()

    def idle_func(self):
        print("I LIVE")
        time.sleep(1)
        return True

    def set_work_end(self):
        self.work_end = time.time() + self.work_secs

    def get_work_time_left(self):
        print(self.work_end - time.time())
        return self.work_end - time.time()

    def start_break(self, item=None):
        print("boom! break!")
        return False

    def pause_all(self):
        pass


class Tray(Gtk.StatusIcon):
    def __init__(self, manager):
        Gtk.StatusIcon.__init__(self)#, size=15)
        self.manager= manager
        self.count = 0
        self.set_from_file(ICONS[self.count])
        #self.set_from_stock(Gtk.STOCK_OPEN)
        self.connect("popup-menu", self.show_menu)
        self.set_visible(True)

    def show_menu(self, event, button, time):
        try:
            menu = Gtk.Menu()
            menu.time_left_item = Gtk.MenuItem(to_digit_display(self.manager.get_work_time_left()))
            menu.pause_item= Gtk.MenuItem("Pause")
            menu.break_now_item = Gtk.MenuItem("Break now")
            menu.quit_item = Gtk.MenuItem("Quit")

            menu.append(menu.time_left_item)
            menu.append(menu.break_now_item)
            menu.append(menu.pause_item)
            menu.append(menu.quit_item)

            menu.quit_item.connect("activate", self.manager.do_quit_mainloop)
            menu.break_now_item.connect("activate", self.manager.start_break)

            menu.quit_item.show()
            menu.break_now_item.show()
            menu.pause_item.show()
            menu.time_left_item.show()

            menu.popup(None, None, None, event, button, time)
        except Exception as e:
            print(e)
            exit(0)


class ReminderPopup(Gtk.Window):
    def __init__(self, work_secs, rest_secs, vpatient, noskip, nopost,
            fraction):
        Gtk.Window.__init__(self,
                            border_width = 10,
                            decorated    = False,
                            deletable    = False,
                            resizable    = False,
                            can_focus    = False,
                            is_focus     = False)
        self.work_secs = work_secs
        self.rest_secs = rest_secs
        self.vpatient = vpatient
        self.waiting = vpatient
        self.noskip = noskip
        self.nopost = nopost
        self.fraction = fraction

        self.set_keep_above(True)
        self.stick()
        self.set_skip_taskbar_hint(True)
        self.set_position(Gtk.WindowPosition.CENTER)
        # defining gui
        self.grid = Gtk.Grid(column_spacing=7, row_spacing=6)
        self.add(self.grid)
        self.pbar = Gtk.ProgressBar()
        self.pbar.set_show_text(True)
        self.rest_button = Gtk.Button.new_with_label("Rest")
        self.rest_button.connect("clicked", self.on_rest)
        self.postpone_button = Gtk.Button.new_with_label("Postpone")
        self.postpone_button.connect("clicked", self.on_postpone)
        self.skip_button = Gtk.Button.new_with_label("Skip")
        self.skip_button.connect("clicked", self.on_skip)
        self.grid.attach(self.pbar, 0, 0, 3, 1)
        self.grid.attach(self.rest_button, 0, 1, 1, 1)
        self.grid.attach(self.skip_button, 1, 1, 1, 1)
        self.grid.attach(self.postpone_button, 2, 1, 1, 1)
        # digit display
        self.display_seconds = int(self.rest_secs)
        if self.waiting:
            self.pbar.set_text("--:--")
        else:
            self.pbar.set_text('{0:d}:{1:02d}'.format(self.display_seconds//60, self.display_seconds % 60))
            self.rest_button.set_sensitive(False)
            self.postpone_button.set_sensitive(False)

        if not self.vpatient:
            self.rest_end = time.time() + self.rest_secs
        if self.noskip:
            self.skip_button.set_sensitive(False)
        if self.nopost:
            self.postpone_button.set_sensitive(False)

        self.main_timeout = GObject.timeout_add(50, self.on_timeout)
        self.timer_timeout = GObject.timeout_add(ONE_SECOND, self.on_display)
        print("++ Window create d")

    def on_timeout(self):
        if self.waiting:
            self.pbar.pulse()
        else:
            value = self.pbar.get_fraction() + self.fraction
            if time.time() > self.rest_end:
                Gtk.main_quit()
                self.destroy()
                value = 0.0
                self.waiting = self.vpatient
                sleep_time =  self.work_secs
                # if curtain:
                #     self.unfullscreen()
            self.pbar.set_fraction(value)
        return True

    def on_display(self):
        if self.waiting:
            self.pbar.set_text("--:--")
        else:
            self.display_seconds -= 1
            self.pbar.set_text(
                    '{0:d}:{1:02d}'.format(self.display_seconds//60,
                                           self.display_seconds % 60))
        return True

    def on_rest(self, button):
        self.waiting = False
        self.rest_end = time.time() + self.rest_secs
        # if curtain:
        #     self.fullscreen()
        self.rest_button.set_sensitive(False)
        self.postpone_button.set_sensitive(False)

    def on_skip(self, button):
        # Gtk.main_quit()
        self.waiting = self.vpatient
        self.destroy()

    def on_postpone(self, button):
        # sleep_time = postpone_secs
        # Gtk.main_quit()
        # self.destroy()
        pass


def usage():
    print("\n"
          "Usage:  bse.py -w <mins to work> -r <mins to rest> [OPTIONS]\n"
          "        -w <minutes>, --work <minutes> : Time to work\n"
          "        -r <minutes>, --rest <minutes> : Time to relax\n"
          "\n"
          "Options:--patient <minutes> : Wait for some time before starting a break\n"
          "        --very-patient : Wait until you decide to take a break\n"
          "    [!] You CAN'T be patient and very-patient at the same time\n"
          "        --noskip : Deny yourself the right to skip a break\n"
          "        --nopostpone: Deny yourself the right to postpone a break\n")


def to_digit_display(seconds):
    return '{0:d}:{1:02d}'.format(int(seconds//60), int(seconds % 60))


def main():
    # input check (shitty)
    if len(sys.argv) == 1:
        usage()
        sys.exit(1)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "w:r:",
                ["work=", "rest=", "postpone-by=", "very-patient",
                 "noskip", "nopostpone"])#, "curtain"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    vpatient = False
    noskip   = False
    nopost   = False
    curtain  = False
    postpone_mins = 5

    for opt, arg in opts:
        if opt in ("-w","--work"):
            work_secs = float(arg) * 60
        elif opt in ("-r","--rest"):
            rest_secs = float(arg) * 60
            fraction = 0.05 / (rest_secs)
        elif opt in "--postpone-by":
            postpone_secs = float(arg) * 60
        elif opt in "--very-patient":
            vpatient = True
        elif opt in "--noskip":
            noskip = True
        elif opt in "--nopostpone":
            nopost = True
        # elif opt in "--curtain":
        #     curtain = True


    manager = Manager(work_secs=work_secs,
                      rest_secs=rest_secs)

    manager.run()

if __name__ == "__main__":
    main()
