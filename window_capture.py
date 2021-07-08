import os
import re
# from gi.repository import Gtk
# from Xlib import display, X
# from PIL import Image

# W,H = 200,200
# dsp = display.Display()
# try:
#     root = dsp.screen().root
#     raw = root.get_image(0, 0, W,H, X.ZPixmap, 0xffffffff)
#     image = Image.frombytes("RGB", (W, H), raw.data, "raw", "BGRX")
#     image.show()
# finally:
#     dsp.close()

def get_window_dimensions():
    #* Using xwininfo to find the location of the pocof1 screen and get the id using wmctrl -l
    window_id = ''
    titles = os.popen('wmctrl -l').read().split('\n')
    for title in titles:
        if 'POCO F1' in title:
            window_id = title[:10]
            break

    win_info = os.popen('xwininfo -id {}'.format(window_id)).read().split('\n')
    top_left_x = 0
    top_left_y = 0
    width = 0
    height = 0

    # print(win_info)
    win_dim = []
    for i in win_info:
        i = i.replace(' ', '')
        if 'Absolute' in i or 'Width' in i or 'Height' in i:
            if re.match('.*?([0-9]+)$', i) == None:
                last_digits = None
            else:
                last_digits = re.match('.*?([0-9]+)$', i).group(1)

            win_dim.append(last_digits)
    
    win_dim = map(int, win_dim)


    return tuple(win_dim)

