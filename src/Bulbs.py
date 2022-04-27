import yeelight
import time
from yeelight.main import Bulb
from yeelight.main import discover_bulbs
from yeelight import enums
from PyQt5.QtWidgets import QMessageBox

def __init__(self):
    super().__init__()

def discoverBulbs(self):
    bulbs = discover_bulbs(timeout=5, interface=False)
    time.sleep(1)
    list=""
    i=0
    for b in bulbs:
        i=i+1
        list=list+str(i)+". Ip Address of the Lamp= "+b['ip']+"\n"
    popup= QMessageBox()
    popup.setWindowTitle("Discovery Results")
    popup.setText(list)
    popup.setIcon(QMessageBox.Information)
    res= popup.exec_()
    
def testBulb(self,ip):
        bulb = Bulb(ip, effect="smooth")
        try:
            try:
                bulb.stop_music()
                bulb.turn_off()
            except:
                pass
            bulb.turn_on()
            bulb.start_music(2000)
            
            bulb.set_rgb(255,255,255)
            time.sleep(1)
            bulb.turn_off()
            bulb.turn_on()
            bulb.set_rgb(255,0,0)
            time.sleep(1)
            bulb.set_rgb(255,255,255)
            bulb=None
            #bulb.turn_off()
            return True
        except:
            bulb=None
            return False        
