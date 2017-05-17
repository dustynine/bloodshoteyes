#!/usr/bin/env python

import sys
import getopt
import time
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk, GObject

# input check (shitty)
if len(sys.argv) == 1:
    print("bse.py -w <mins to work> -r <mins to rest>")
    sys.exit(1)
try:
    opts, args = getopt.getopt(sys.argv[1:],"w:r:", \
            ["work=","rest="])
except getopt.GetoptError:
    print("bse.py -w <mins to work> -r <mins to rest>")
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-w","--work"):
        worktime = float(arg)
    elif opt in ("-r","--rest"):
        resttime = float(arg)

fraction = 0.05 / (resttime * 60)
# set a fraction according to rest time

class ReminderPopup(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Take a break now.")
        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.progressbar = Gtk.ProgressBar()
        vbox.pack_start(self.progressbar, True, True, 0)

        self.timeout_id = GObject.timeout_add(50, self.on_timeout, resttime)

    def on_timeout(self, resttime):
        """
        Update value on the progress bar
        """
        new_value = self.progressbar.get_fraction() + fraction
        print(new_value) # debug, remove later

        if new_value > 1:
            new_value = 0
            Gtk.main_quit()
            pop.destroy()

        self.progressbar.set_fraction(new_value)

        # As this is a timeout function, return True so that it
        # continues to get called
        return True

#def main():
#    if len(sys.argv) == 1:
#        print("bse.py -w <mins to work> -r <mins to rest>")
#        sys.exit(1)
#    try:
#        opts, args = getopt.getopt(sys.argv[1:],"w:r:", \
#                ["work=","rest="])
#    except getopt.GetoptError:
#        print("bse.py -w <mins to work> -r <mins to rest>")
#        sys.exit(2)
#
#    for opt, arg in opts:
#        if opt in ("-w","--work"):
#            worktime = float(arg)
#        elif opt in ("-r","--rest"):
#            breaktime = float(arg)
#
#    running = 1
#    while(running):
#        print(time.asctime())
#        time.sleep(60*worktime)
#        # popup shows up now
#        print(time.asctime() + " Go get some rest now.")
#        # time.sleep(60*breaktime)
#        # aaaand it's gone
#        print(time.asctime() + " Ok, now back to work.")

print(time.asctime())
running = True
while(running):
    time.sleep(60*worktime)
    # popup shows up now
    print(time.asctime() + " Go get some rest now.")
    pop = ReminderPopup()
    pop.connect("delete-event", Gtk.main_quit)
    pop.show_all()
    Gtk.main()
    # time.sleep(60*breaktime)
    # aaaand it's gone
    print(time.asctime() + " Ok, now back to work.")
# if __name__ == "__main__":
#     main()
