# BloodshotEyes
Simple Python program that will remind you to take a break and give rest to your bloodshot eyes. With only dependency is GTK 3.0

<h2>Usage:</h2>   <h3>bse.py -w [minutes] -r [minutes] [OPTIONS] </h3>
         <p>-w [minutes] : Time in minutes you spend looking at the screen
         <p>-r [minutes] : Time in minutes you spend resting
   
<h3>Options:</h3> <p>--very-patient  : Wait infinitely until either of three buttons is pressed
         <p>--noskip        : Deny yourself the right to skip a break at all
         <p>--nopostpone    : Deny yourself the right to postpone a break at all
         
<h2>Configuration</h2>
<p> If you're using bspwm add the following line in your bspwmrc file `bspc rule -a Bse.py manage=off`
