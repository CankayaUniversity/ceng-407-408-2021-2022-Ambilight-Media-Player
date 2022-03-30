from yeelight import *
from yeelight import transitions as ylTransitions
import time

bulb = Bulb('192.168.123.91', effect="smooth")
bulb.turn_on()
time.sleep(1)


discoTransitions =ylTransitions.disco(150)
myFlow = Flow(count=0, transitions=discoTransitions)
bulb.start_flow(myFlow )
time.sleep(20)

alarmTransitions =ylTransitions.alarm(500)
myFlow = Flow(count=0, transitions=alarmTransitions)
bulb.start_flow(myFlow )
time.sleep(20)

chrisTransitions =ylTransitions.christmas()
myFlow = Flow(count=0, transitions=chrisTransitions)
bulb.start_flow(myFlow )
time.sleep(20)

manualTransitions = [
        RGBTransition(255, 0, 0, duration=1250, brightness=100),
        RGBTransition(0,255, 0, duration=1250, brightness=100),
        RGBTransition(0,0, 255, duration=1250, brightness=100),
    ]

myFlow = Flow(count=0, transitions=manualTransitions)
bulb.start_flow(myFlow )
time.sleep(20)

bulb.set_color_temp(6500)

tempTransitions = [TemperatureTransition(6500, duration=50000), TemperatureTransition(1700, duration=50000)]
myFlow = Flow(count=0, transitions=tempTransitions)
bulb.start_flow(myFlow )
time.sleep(20)
bulb.stop_flow()
bulb.set_rgb(255,255,255)
bulb.turn_off()

