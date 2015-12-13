# swico.py

**switch** the **color** of Obmenu and Dmenu out of Obmenu itself.

## what you need to do
+ download this script and make it executable
+ download [dominat-colour.py from ZeevG](https://github.com/ZeevG/python-dominant-image-colour) and since there are issues while importing it as a library uncomment the very first line within the script and change the minus to an underscore in the name

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

+ get the console output
```python
swico.py -V
```
+ **each file which will be manipulated will be backed up!**

+ of course you have to set the path variables. change it in the code (better) or give it as command each time
  - **--path_n** needs to lead to the bg-saved.cfg in your nitrogen folder
    - */home/frodo/.config/nitrogen/bg-saved.cfg*
  - **--path_r** needs to lead to the rc.xml
    - */home/frodo/.config/openbox/rc.xml*
  - **--path_t** needs to lead to your .themes folder
    - */home/frodo/.themes/*

## so far
this works on my machine with **antergos/arch-linux** and **openbox** with **nitrogen**

## TODO
- function to delete the backups
- function to set the layout back
- ...i want this to work on pcmanfm...
