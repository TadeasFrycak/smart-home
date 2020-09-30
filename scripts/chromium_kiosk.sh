#!/bin/bash
xset s noblank
xset s off
xset -dpms

unclutter -root &

sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/pi/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/pi/.config/chromium/Default/Preferences

/usr/bin/chromium-browser --incognito --disable-pinch --overscroll-history-navigation=0 --no-touch-pinch --noerrdialogs --disable-infobars --disable-notifications --start-maximized --start-fullscreen --no-sandbox  --disable-session-crashed-bubble --kiosk --no-first-run '192.168.0.100:5000' &

while true; do
   xdotool key F5;
   sleep 10000
done
