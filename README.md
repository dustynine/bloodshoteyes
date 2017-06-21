# BloodshotEyes
Simple Python program that will remind you to take a break and give rest to your bloodshot eyes. With only dependency is GTK 3.0

Usage:   bse.py -w <mins to work> -r <mins to rest> [OPTIONS]
         -w <minutes>, --work <minutes> : Time in minutes you spend looking at the screen
         -r <minutes>, --rest <minutes> : Time in minutes you spend resting
   
Options: --very-patient  : Wait infinitely until either of three buttons is pressed
         --noskip        : Deny yourself the right to skip a break at all
         --nopostpone    : Deny yourself the right to postpone a break at all
