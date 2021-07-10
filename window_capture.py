import os
import re

def get_window_dimensions():
    #* Using xwininfo to find the location of the pocof1 screen and get the id using wmctrl -l
    window_id = ''
    titles = os.popen('wmctrl -l').read().split('\n')
    for title in titles:
        if 'POCO F1' in title:
            window_id = title[:10]
            break

    win_info = os.popen('xwininfo -id {}'.format(window_id)).read().split('\n')
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
