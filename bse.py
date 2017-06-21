#!/usr/bin/env python

import sys
import getopt
import time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject


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


def main():
    # input check (shitty)
    if len(sys.argv) == 1:
        usage()
        sys.exit(1)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "w:r:",
                ["work=", "rest=", "patient=", "postpone-by=", "very-patient",
                 "noskip", "nopostpone"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)


    vpatient = False
    noskip   = False
    nopost   = False
    postpone_mins = 5
    for opt, arg in opts:
        if opt in ("-w","--work"):
            work_mins = float(arg)
        elif opt in ("-r","--rest"):
            rest_mins = float(arg)
        # elif opt in "--patient":
        #     patience = float(arg)
        # elif opt in "--postpone-by":
        #     postpone_mins = float(arg)
        elif opt in "--very-patient":
            vpatient = True
        elif opt in "--noskip":
            noskip = True
        elif opt in "--nopostpone":
            nopost = True
    fraction = 0.05 / (rest_mins*60)
    sleep_time = 60 * work_mins


    class ReminderPopup(Gtk.Window):
        def __init__(self):
            Gtk.Window.__init__(self,
                                border_width = 10,
                                decorated    = False,
                                deletable    = False,
                                resizable    = False,
                                can_focus    = False,
                                is_focus     = False)
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
            self.waiting = vpatient
            self.display_seconds = int(rest_mins * 60)
            if self.waiting:
                self.pbar.set_text("--:--")
            else:
                self.pbar.set_text('{0:d}:{1:02d}'.format(self.display_seconds//60, self.display_seconds % 60))
                self.rest_button.set_sensitive(False)
                self.postpone_button.set_sensitive(False)
            if not vpatient:
                global rest_timeout
                rest_timeout = time.time() + 60*rest_mins
            if noskip:
                self.skip_button.set_sensitive(False)
            if nopost:
                self.postpone_button.set_sensitive(False)

            self.timeout_id = GObject.timeout_add(50, self.on_timeout)
            self.timer_timeout = GObject.timeout_add(1000, self.on_display)
            print("++ Window created")

        def on_timeout(self):
            if self.waiting:
                self.pbar.pulse()
            else:
                value = self.pbar.get_fraction() + fraction
                if time.time() > rest_timeout:
                    Gtk.main_quit()
                    self.destroy()
                    value = 0.0
                    self.waiting = vpatient
                    # sleep_time =  60 * work_mins
                    # print(str(sleep_time) +'when window dies')
                self.pbar.set_fraction(value)
            return True

        def on_display(self):
            if self.waiting:
                self.pbar.set_text("--:--")
            else:
                self.display_seconds -= 1
                self.pbar.set_text('{0:d}:{1:02d}'.format(self.display_seconds//60, self.display_seconds % 60))
            return True

        def on_rest(self, button):
            self.waiting = False
            global rest_timeout
            rest_timeout = time.time() + 60*rest_mins
            self.rest_button.set_sensitive(False)
            self.postpone_button.set_sensitive(False)

        def on_skip(self, button):
            Gtk.main_quit()
            self.waiting = vpatient
            self.destroy()

        def on_postpone(self, button):
            # global sleep_time
            # sleep_time = 60 * postpone_mins
            # print(str(sleep_time)+'after postpone button is pressed')
            # Gtk.main_quit()
            # self.destroy()
            pass

    print("== "+time.strftime("%H:%M", time.localtime())+" Initiated")
    while True:
        # print(str(sleep_time)+'before main loop sleep')
        time.sleep(sleep_time)
        print("== " + time.strftime("%H:%M", time.localtime()) + " Rest sequence starts now")
        pop = ReminderPopup()
        pop.show_all()
        Gtk.main()
        print("-- Window destroyed")
        print("== " + time.strftime("%H:%M", time.localtime()) + " Work timer starts now")


if __name__ == "__main__":
    main()

