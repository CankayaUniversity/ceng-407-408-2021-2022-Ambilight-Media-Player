import yeelight
from yeelight.main import Bulb, discover_bulbs

bulbs = discover_bulbs(timeout=5, interface=False)
print (bulbs)
'''
The output after running the above code block is as follows.
[{'ip': '192.168.1.101', 'port': 55443, 'capabilities':
{'id': '0x000000001964g2ap', 'model': 'color4', 'fw_ver': '37',
'support': 'get_prop set_default set_power
toggle set_bright set_scene cron_add cron_get
cron_del start_cf stop_cf set_ct_abx adjust_ct
set_name set_adjust adjust_bright adjust_color
set_rgb set_hsv set_music udp_sess_new udp_sess_keep_alive
udp_chroma_sess_new', 'power': 'off', 'bright': '100',
'color_mode': '1', 'ct': '4708', 'rgb': '6172712',
'hue': '9', 'sat': '57', 'name': ''}}]
'''
#If you want to access any feature of the lamps found,
#a code like the one below can be used.
bulbList=[]
for b in bulbs:
    bulbList.append(b['ip'])
print (bulbList)
