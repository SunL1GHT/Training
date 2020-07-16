import cv2
import sys
from ctypes import *
from camera.MINDVISION import *
from camera.LBAS import *
from camera.GalaxyCam import *
from camera.USBWebCam import *
# from GigECamera  import *
import socket
import fcntl
import struct



class CameraInterface():
    def __init__(self,name,camindex):
        print("get in camera class")
        if name.lower() == "mindvision":
            self.cam = MindVisionCamera("libMVSDK.so")
        elif name.lower() == "lbas":
            #self.cam = LBASCamera("libMvCameraControl.so")
            self.cam = LBASCamera("/opt/LBAS/Samples_LinuxSDK/lib/64/libMvCameraControl.so",camindex)
        elif name.lower() == "galaxy":
            self.cam = GalaxyCam("/usr/lib/libgxiapi.so",camindex)
            
        elif name.lower() == "usb":
            self.cam = USBWebCam()
        
        else:
            print("other camera..")
        

        self.open_status = False
        self.set_cam_ip()
        



  
    def open(self):
        self.open_status = self.cam.cam_init_state and self.cam.open() 
        # print("exposure time:             ",self.CameraGetExposureTime())
        return self.open_status
    
    def close(self):
        if not self.open_status:
            return
        if self.cam.camera_isOpen:
            status = self.cam.close()
            self.open_status = False
        return status

    # 开启抓流
    def start_grab(self):
        print("self.open_status:       ",self.open_status)
        if not self.open_status:
            return
        status = self.cam.start_grab()
        return status

    # 关闭抓流
    def stop_grab(self):
        if not self.open_status:
            return
        status = self.cam.stop_grab()
        return status

    def save(self,fname,img):
        if not self.open_status:
            return
        status = self.cam.save(fname,img)
        return status
    
    def pop_frame(self):
        if not self.open_status:
            return
        image = self.cam.pop_frame()
        return image
    
    def save_cv_image(self,image,fname):
        if not self.open_status:
            return
        status = self.cam.save_cv_image(image,fname)
        return status

    def CameraGetExposureTime(self):

        if not self.open_status:
            return
        #
        return self.cam.CameraGetExposureTime()

    def CameraSetExposureTime(self,val):
        # if not self.open_status:
        #     return
        print("set camera exposure time: ",val)
        status = self.cam.CameraSetExposureTime(val)
        return status

    def CameraSetOffsetX(self,val):
        status = self.cam.CameraSetOffsetX(val)
        return status
    
    def CameraGetImageResolution(self):
        dict = self.cam.CameraGetImageResolution()
        return dict

    def CameraSetImageResolution(self,width,height):
        if not self.open_status:
            return
        status = self.cam.CameraSetImageResolution(width,height)
        return status

    #取消相机的自动曝光
    def CameraSetAeState(self):
        if not self.open_status:
            return
        status = self.cam.CameraSetAeState()
        return status


    def set_image_channelOption(self,val):
        if not self.open_status:
            return
        print("val set image channel========== ",val)
        status = self.cam.set_image_channelOption(val)
        return status

    def getCamIpStr(self):
        
        return self.cam.getCamIpStr()

    def getDeviceIdStr(self):
        
        return self.cam.getCamDeviceID()

    def set_cam_ip(self):
        pass
        # print(self.get_ip_address())
    

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #获取本机电脑名
        myname = socket.getfqdn(socket.gethostname(  ))
        #获取本机ip
        myaddr = socket.gethostbyname(myname)
        return myaddr
        
        # return socket.inet_ntoa(fcntl.ioctl(
        #     s.fileno(),
        #     0x8915,  # SIOCGIFADDR
        #     struct.pack('256s', ifname[:15])
        # )[20:24])
  


    def getCamInfo(self):
        
        info = CamInfo()
        info= self.cam.get_cam_info_for_display()
        # print("hhhhhhhhhhhhhhhhh",info)
        # return info
        return info.width,info.height,info.x_offset,info.y_offset,info.exposure_time


    def save_feature_file(self):
        self.cam.MV_CC_FeatureSave()