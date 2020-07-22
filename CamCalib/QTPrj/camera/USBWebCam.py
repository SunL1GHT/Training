import cv2
import sys

class USBWebCam():
    def __init__(self):
        #VideoCapture(2)  2这个参数需要具体看外接的USB相机是几  在cmd中输入：ls /dev | grep video
        self.cap = cv2.VideoCapture(2) # on ubuntu18.04
        print(self.cap)
        # self.cap = cv2.VideoCapture(0)  # on windows 10
        self.frame = None
        self.cam_init_state = True
        self.camera_isOpen = True

        #logi  usb相机默认图像尺寸是640*480，可以自定义尺寸

        # width = 960
        # height = 720
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


    def open(self):
        self.camera_isOpen = True
        return True

    def close(self):
        self.cap.release()

    def pop_frame(self):
        ret, frame = self.cap.read()

        if ret:
            frame = cv2.flip(frame,1,dst=None)
            frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
            self.frame = frame
            return frame
        else :
            self.frame = None
            return None

    def save(self, fname,img):
        image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(fname,image)
    
 
