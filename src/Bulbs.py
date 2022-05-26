import yeelight
import time
from yeelight.main import Bulb, discover_bulbs
from yeelight import enums
from PyQt5.QtWidgets import QMessageBox

def __init__(self):
    super().__init__()

def discoverBulbs(self):
    bulbs = discover_bulbs(timeout=5, interface=False)
    time.sleep(1)
    bulbList=[]
    for b in bulbs:
        bulbList.append(b['ip'])
    popup= QMessageBox()
    popup.setWindowTitle("Discovery Results")
    popup.setText("Search completed")
    popup.setIcon(QMessageBox.Information)
    res= popup.exec_()
    return bulbList
    
def testBulb(self,ip):
        bulb = Bulb(ip, effect="smooth")
        try:
            try:
                bulb.stop_music()
                bulb.turn_off()
            except:
                pass
            bulb.turn_on()
            bulb.start_music(55443)
            bulb.set_rgb(255,255,255)
            time.sleep(1)
            bulb.turn_off()
            bulb.turn_on()
            bulb.set_rgb(255,0,0)
            time.sleep(1)
            bulb.set_rgb(255,255,255)
            bulb=None
            return True
        except:
            bulb=None
            return False        
