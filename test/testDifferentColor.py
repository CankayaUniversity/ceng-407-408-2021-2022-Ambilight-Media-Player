#It is tested by sending different rgb codes to the lamp
from yeelight import Bulb
import time

bulb = Bulb('192.168.1.100', effect="smooth")
bulb.turn_on()
bulb.set_brightness(100)

getMusicMode=bulb.get_properties()
if getMusicMode['music_on']=='0':
    bulb.start_music(55443)
else:
    bulb.stop_music()
    time.sleep(1)
    bulb.start_music(55443)
while bulb.music_mode:
    for r in range(1,256,5):
        for g in range(1,256,5):
            for b in range(1,256,5):
                bulb.set_rgb(r,g,b)
                time.sleep(0.1)
            time.sleep(0.1)
        time.sleep(0.1)
                
            

    
