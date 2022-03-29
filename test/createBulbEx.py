###############################################################################
####Referance is https://yeelight.readthedocs.io/_/downloads/en/latest/pdf/####
####This example shows how to create a bulb and make its basic settings.#######
###############################################################################
import yeelight
import time
from yeelight.main import Bulb

bulb = Bulb('192.168.1.100', effect="smooth")
#The sample code below will create a new lamp and turn it on.
#After 2 seconds, the lamp will be turned off.
bulb.turn_on()
time.sleep(5)
bulb.turn_off()

#Toggle the bulb's power
time.sleep(5)
bulb.toggle()

bulb.start_music(55443) #Removes the limitation of data to be sent to the bulb

#Adjusting the bulb brightness
bulb.set_brightness(100)
for i in range(100,0,-20):
    bulb.set_brightness(i)
    time.sleep(1)

bulb.set_brightness(100)

