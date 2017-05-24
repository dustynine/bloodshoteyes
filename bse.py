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
            ["work=","rest=","patient","patient","very-patient"])
except getopt.GetoptError:
    print("bse.py -w <mins to work> -r <mins to rest>")
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-w","--work"):
        worktime = float(arg)
    elif opt in ("-r","--rest"):
        resttime = float(arg)
    elif opt in "--very-patient":
        waiting = True

# set a fraction by which progress bar will progress
# according to rest time
fraction = 0.05 / (resttime * 60)

class ReminderPopup(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, \
                title           = "Take a break now.", \
                border_width    = 10, \
                #default_width   = 250, \
                #default_height  = 70, \
                decorated       = False, \
                deletable       = False, \
                resizable       = False) 
        self.set_keep_above(True)
        self.stick()
        self.set_focus(None)

        self.grid = Gtk.Grid(column_spacing = 7, row_spacing=7)
        self.add(self.grid)

        self.progressbar = Gtk.ProgressBar()

        self.rest_button = Gtk.Button.new_with_label("Rest")
        self.rest_button.connect("clicked", self.rest_button_clicked)

        self.postpone_button = Gtk.Button.new_with_label("Postpone")
        self.postpone_button.connect("clicked", self.postpone_button_clicked)
        
        self.skip_button = Gtk.Button.new_with_label("Skip")
        self.skip_button.connect("clicked", self.skip_button_clicked)
        
        self.grid.attach(self.progressbar, 0, 0, 3, 1)
        self.grid.attach(self.rest_button, 0, 1, 1, 1)
        self.grid.attach(self.skip_button, 1, 1, 1, 1)
        self.grid.attach(self.postpone_button, 2, 1, 1, 1)
        
        print("-- Window created")

        self.timeout_id = GObject.timeout_add(50, self.on_timeout, resttime)
    
    def on_timeout(self, resttime):
        """
        main logic
        """
        if waiting:
            self.progressbar.pulse()
        else:
            value = self.progressbar.get_fraction() + fraction
            # print(new_value) # debug, remove later

            if time.time() == timeout or time.time() > timeout:
                Gtk.main_quit()
                self.destroy()
            
            if value > 1:
                value = 0

            self.progressbar.set_fraction(value)

        # as this is a timeout function, return True so that it
        # continues to get called
        return True

    def rest_button_clicked(self, button):
        waiting = False
        # pop.progressbar.set_fraction(0.0)

    def postpone_button_clicked(self, button):
        Gtk.main_quit()
        self.destroy()
        exit(0) # for now

    def skip_button_clicked(self, button):
        Gtk.main_quit()
        self.destroy()

print(time.asctime() + " Started.")
while(True):
    time.sleep(60*worktime)
    # ^ FIX: work timer gradually adds one second
    # popup shows up now
    timeout = time.time() + 60*resttime
    print(time.asctime() + " Rest timer starts now. ")
    pop = ReminderPopup()
    pop.show_all()
    Gtk.main()
    print("-- Window destroyed")
    # aaaand it's gone
    print(time.asctime() + " Work timer starts now.")
