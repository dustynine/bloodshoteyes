#!/usr/bin/env python

import sys
import getopt
import time
import gi
import os

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

ONE_SECOND = 1000

ICONS = (
        os.path.abspath("./tray/icon00.png"),
        os.path.abspath("./tray/icon25.png"),
        os.path.abspath("./tray/icon50.png"),
        os.path.abspath("./tray/icon75.png")
        )


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


class Scheduler():
    def __init__(self):
        pass


class TrayMeny():
    pass


class TrayIcon():
    def __init__(self, work_mins):
        #self,menu = menu
        self.work_mins = work_mins
        self.count = 0
        self.current_icon = ICONS[self.count]
        self.tray_object = Gtk.StatusIcon()
        self.tray_object.set_from_file(self.current_icon)
        self.tray_object.connect("popup-menu", self.show_menu)

        self.quater_time = self.work_mins * ONE_SECOND / 4
        self.quater_timeout = GObject.timeout_add(self.quater_time,
                self.change_icon)

    def show_menu():
         print("mama imma menu")

    def change_icon(self):
        if self.count == 3:
            self.count = 0
            self.current_icon = ICONS[0]
        else:
            self.count += 1
            self.current_icon = ICONS[self.count]


class ReminderPopup(Gtk.Window):
    def __init__(self, work_mins, rest_secs, vpatient, noskip, nopost,
            fraction):
        Gtk.Window.__init__(self,
                            border_width = 10,
                            decorated    = False,
                            deletable    = False,
                            resizable    = False,
                            can_focus    = False,
                            is_focus     = False)
        self.work_secs = 60 * work_mins
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
        self.display_seconds = int(self.rest_secs)
        if self.waiting:
            self.pbar.set_text("--:--")
        else:
            self.pbar.set_text('{0:d}:{1:02d}'.format(
                self.display_seconds//60,
                self.display_seconds % 60))
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
        print("++ Window created")

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
        #Gtk.main_quit()
        self.waiting = self.vpatient
        self.destroy()

    def on_postpone(self, button):
        sleep_time = 60 * postpone_mins
        Gtk.main_quit()
        self.destroy()
        pass


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
            work_mins = float(arg)
            sleep_time = 60 * work_mins
        elif opt in ("-r","--rest"):
            rest_secs = float(arg) * 60
            fraction = 0.05 / (rest_secs)
        elif opt in "--postpone-by":
            postpone_mins = float(arg)
        elif opt in "--very-patient":
            vpatient = True
        elif opt in "--noskip":
            noskip = True
        elif opt in "--nopostpone":
            nopost = True
        # elif opt in "--curtain":
        #     curtain = True

    print("== "+time.strftime("%H:%M", time.localtime())+" Initiated")
    tray_icon = TrayIcon(work_mins)
    Gtk.main()
    while True:
        time.sleep(sleep_time)
        print("== " + time.strftime("%H:%M", time.localtime()) + \
                " Rest sequence starts now")
        pop = ReminderPopup(work_mins, rest_secs, vpatient, noskip, nopost,
                fraction)
        # здесь был Gtk.main()
        pop.show_all()
        print("-- Window destroyed")
        print("== " + time.strftime("%H:%M", time.localtime()) + \
                " Work timer starts now")


if __name__ == "__main__":
    main()

