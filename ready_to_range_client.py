import socket
from time import sleep
from pypozyx import*
from pypozyx.tools.version_check import perform_latest_version_check
import time


prf='1'
chanel = '5'
pos = 'go'
class Data(object):
    def __init__(self, nickname, data='empty'):
        self.nickname = nickname
        self.data = []
class Session(object):
    def __init__(self, pozyx, ip, port, anchor,range_step_mm = 1000, ranging_protocol= PozyxConstants.RANGE_PROTOCOL_PRECISION, remote_id = None):
        self.pozyx = pozyx
        self.destination_id = anchor
        self.range_step_mm = range_step_mm
        self.remote_id = remote_id
        self.ip = ip
        self.protocol = ranging_protocol
        self.port= port
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.data = Data('tag1')
        self.distance=0
        self.timestamp = 0
        self.RSS = 0
        
        
    def setup(self):
        
        print("-------------------POZYX RANGINF V{} --------------".format(version))
        print("NOTES: ")
        print("  - Change the parameters: ")
        print("\tdestination_id(target device")
        print("\trange_step(mm)")
        print("")
        print("- Approach target device to see range and")
        print("led control")
        print("")
        #self.pozyx.clearDevice(self.remote_id)
        
        if self.remote_id is None:
            for device_id in [None,self.remote_id, self.destination_id]:
                self.pozyx.printDeviceInfo(device_id)
                
        print("")
        print("----------POZYX RANGING{} -------------".format(version))
        print("START Ranging")
        
        self.sock.connect((self.ip,self.port))
        self.sock.recv(100)
        led_config = 0x0
        self.pozyx.setLedConfig(led_config,self.remote_id)
        self.pozyx.setLedConfig(led_config,self.destination_id)
        self.pozyx.setRangingProtocol(self.protocol,self.remote_id)
        
    def loop(self):
        device_range = DeviceRange()
        status = self.pozyx.doRanging(self.destination_id,device_range,self.remote_id)
        self.data.data = device_range
        msg = str(self.data.data)
        if status == True:
            #print(msg)
            print(msg)
            #if self.ledControl(device_range.distance) == POZYX_FAILURE:
                #a=10
                #print("ERROR Ranging local %s") % self.pozyx.getErrorMessage(error_code)
            #else:
                #print("Error Ranginf, couldn't retrieve local error")
                
    def ledControl(self, distance):
        status = POZYX_SUCCESS
        ids = [self.remote_id, self.destination_id]
        for id in ids:
            status &= self.pozyx.setLed(4, (distance < range_step_mm),id)
            status &= self.pozyx.setLed(3, 2*(distance < range_step_mm),id)
            status &= self.pozyx.setLed(2, 3*(distance < range_step_mm),id)
            status &= self.pozyx.setLed(1, 4*(distance < range_step_mm),id)
        return status
    
    
if __name__ == "__main__":
    check_pypozyx_version = True
    if check_pypozyx_version:
        perform_latest_version_check()
        
    serial_port = get_first_pozyx_serial_port()
    if serial_port is None:
        print("No Pozyx connected. Check your USB cable on your device")
        quit()
        
        
    remote_id = None
    remote = False
    if not remote:
        remote_id = None
    
    destination_id = 0x6724
    range_step_mm = 1000
    ranging_protocol = PozyxConstants.RANGE_PROTOCOL_PRECISION
    ip = '192.168.0.17'
    pozyx = PozyxSerial(serial_port)
    r = Session(pozyx,ip,8000,destination_id,range_step_mm,ranging_protocol,remote_id)
    r.setup()
    while True:
        r.loop()




        