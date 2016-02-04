# swico.py

**switch** the **color** of Obmenu and Dmenu and your gtkrc out of Obmenu itself.

## what you need to do
+ download this script and make it executable
+ download [PIL - the Python Imaging Library](https://github.com/python-pillow/Pillow)
+ download [dominat-colour.py from ZeevG](https://github.com/ZeevG/python-dominant-image-colour) and since there are issues while importing it as a library uncomment the very first line within the script and change the minus to an underscore in the name
+ copy your theme or your themes from */usr/share/themes/* to *$HOME/.themes/*
+ see the default directories in the main function and edit

## options
+ set the color for selected background
```python
swico.py -b #644833
```

+ set the foreground color
```python
swico.py -f #f7f7f7
```

+ get the background color from current wallpaper (Zeev's work)
```python
swico.py -i
```

+ i automated the backup function, so after a time there will be lots of backup files which you can remove with the following statement (feel free to comment the lines 97, 140, 167, 193)
```python
swico.py --remove
```

+ get the console output
```python
swico.py -v
```
+ **each file which will be manipulated will be backed up!**

+ of course you have to set the path variables. change it in the code (better) or give it as command each time
  - **--path_n** needs to lead to the bg-saved.cfg in your nitrogen folder to get the current wallpaper
    - */home/frodo/.config/nitrogen/bg-saved.cfg*
  - **--path_r** needs to lead to the rc.xml for the dMenu itself and the current theme
    - */home/frodo/.config/openbox/rc.xml*
  - **--path_t** needs to lead to your .themes folder for the themerc and gtkrc
    - */home/frodo/.themes/*
  - **--path_a** needs to point to your awesome theme.lua
    - */home/frodo/.config/awesome/themes/default/theme.lua*
  - **--path_ai** pointing to your icon folder which you need to copy from /usr/share/awesome/icons
    - *home/frodo/.config/awesome/icons/*

## so far
this works on my machine with **antergos/arch-linux** and **openbox**/**awesome** with **nitrogen**

## TODO
- function to set the layout back

## bugs or something like that
- if the gtkrc is edited it takes some time for pcmanfm to recognize the change (i think). nevertheless it works. it will eventually after reboot. be careful.. can be ugly.. maybe comment the line 350 so there are no changes
- i have currently no working solution for awesome being automatically restarted...
