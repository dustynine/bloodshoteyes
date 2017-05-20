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

        grid = Gtk.Grid(column_spacing = 50, row_spacing=7)
        self.add(grid)

        self.progressbar = Gtk.ProgressBar()

        start_button = Gtk.Button.new_with_label("Rest")
        start_button.connect("clicked", \
                self.start_button_clicked)

        postpone_button = Gtk.Button.new_with_label("Postpone")
        postpone_button.connect("clicked", \
                self.postpone_button_clicked)
        
        grid.attach(self.progressbar, 0, 0, 2, 1)
        grid.attach(postpone_button, 0, 1, 1, 1)
        grid.attach(start_button, 1, 1, 1, 1)
        

        self.timeout_id = GObject.timeout_add(50, self.on_timeout, resttime)

    def start_button_clicked(self, button):
        Gtk.main_quit() # for now
    
    def postpone_button_clicked(self, button):
        print("Хуй")
        #pop.destroy() # for now

    def on_timeout(self, resttime):
        """
        update value on the progress bar
        """
        value = self.progressbar.get_fraction() + fraction
        # print(new_value) # debug, remove later

        if time.time() == timeout or time.time() > timeout:
            Gtk.main_quit()
            pop.destroy()
        
        if value > 1:
            value = 0

        self.progressbar.set_fraction(value)

        # as this is a timeout function, return True so that it
        # continues to get called
        return True

print(time.asctime() + " Started.")
running = True
while(running):
    time.sleep(60*worktime)
    # popup shows up now
    timeout = time.time() + 60*resttime
    print(time.asctime() + " Rest timer starts now. ")
    pop = ReminderPopup()
    pop.connect("delete-event", Gtk.main_quit) # delete when postpone button is working
    pop.show_all()
    Gtk.main()
    # aaaand it's gone
    print(time.asctime() + " Work timer starts now.")
