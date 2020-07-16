from ctypes import *
import numpy as np
import cv2 

''' 结构体定义 camera SDK中C的结构体转换为python中的class '''

API_STATUS_OK = 0 # 

class tSdkCameraDevInfo(Structure):
    _fields_ = [("acProductSeries", c_char*32),
                ("acProductName", c_char*32),
                ("acFriendlyName", c_char*32),
                ("acLinkName", c_char*32),
                ("acDriverVersion", c_char*32),
                ("acSensorType", c_char*32),
                ("acPortType", c_char*32),
                ("acSn", c_char*32),
                ("uInstance", c_uint)
            ]

#触发模式描述
class tSdkTrigger(Structure):
    _fields_ = [
                ("iIndex", c_int),
                ("acDescription", c_char*32)
            ]

#相机的分辨率描述
class tSdkImageResolution(Structure):
    _fields_ = [
                ("iIndex", c_int),
                ("acDescription", c_char*32),
                ("uBinSumMode", c_uint),
                ("uBinAverageMode", c_uint),
                ("uSkipMode", c_uint),
                ("uResampleMask", c_uint),
                ("iHOffsetFOV", c_int),
                ("iVOffsetFOV", c_int),
                ("iWidthFOV", c_int),
                ("iHeightFOV", c_int),
                ("iWidth", c_int),
                ("iHeight", c_int),
                ("iWidthZoomHd", c_int),
                ("iHeightZoomHd", c_int),
                ("iWidthZoomSw", c_int),
                ("iHeightZoomSw", c_int)
            ]

#相机白平衡色温模式描述信息
class tSdkColorTemperatureDes(Structure):
    _fields_ = [
                ("iIndex", c_int),
                ("acDescription", c_char*32)
            ]

#相机输出的图像数据格式
class tSdkMediaType(Structure):
    _fields_ = [
                ("iIndex", c_int),
                ("acDescription", c_char*32),
                ("iMediaType", c_uint)
            ]

#相机帧率描述信息
class tSdkFrameSpeed(Structure):
    _fields_ = [
                ("iIndex",c_int),
                ("acDescription",c_char*32)
            ]
            
#传输分包大小描述(主要是针对网络相机有效)
class tSdkPackLength(Structure):
    _fields_ = [
                 ("iIndex",c_int),
                 ("acDescription",c_char*32),
                 ("iPackSize",c_uint)    
            ]

#预设的LUT表描述    
class tSdkPresetLut(Structure):
    _fields_ = [
                ("iIndex",c_int),
                ("acDescription",c_char*32)
            ]
#AE算法描述
class tSdkAeAlgorithm(Structure):
    _fields_ = [
                ("iIndex",c_int),
                ("acDescription",c_char*32)
            ]

#RAW转RGB算法描述
class tSdkBayerDecodeAlgorithm(Structure):
    _fields_ = [
                ("iIndex",c_int),
                ("acDescription",c_char*32)
            ]

#相机曝光功能范围定义
class tSdkExpose(Structure):
    _fields_ = [
                ("uiTargetMin",c_uint),
                ("uiTargetMax",c_uint),
                ("uiAnalogGainMin",c_uint),
                ("uiAnalogGainMax",c_uint),
                ("fAnalogGainStep",c_float),
                ("uiExposeTimeMin",c_uint),
                ("uiExposeTimeMax",c_uint)
            ]

#相机的分辨率设定范围，用于构件UI
class tSdkResolutionRange(Structure):
    _fields_ = [
                ("iHeightMax",c_int),
                ("iHeightMin",c_int),
                ("iWidthMax",c_int),
                ("iWidthMin",c_int),
                ("uSkipModeMask",c_uint),
                ("uBinSumModeMask",c_uint),
                ("uBinAverageModeMask",c_uint),
                ("uResampleMask",c_uint)
            ]

#饱和度设定的范围
class tSaturationRange(Structure):
    _fields_ = [
                ("iMin",c_int),
                ("iMax",c_int)
            ]

#伽马的设定范围
class tGammaRange(Structure):
    _fields_ = [
                ("iMin",c_int),
                ("iMax",c_int)
            ]

#对比度的设定范围
class tContrastRange(Structure):
    _fields_ = [
                ("iMin",c_int),
                ("iMax",c_int)
            ]

#锐化的设定范围
class tSharpnessRange(Structure):
    _fields_ = [
                ("iMin",c_int),
                ("iMax",c_int)
            ]

#ISP模块的使能信息
class tSdkIspCapacity(Structure):
    _fields_ = [
                ("bMonoSensor",c_bool),
                ("bWbOnce",c_bool),
                ("bAutoWb",c_bool),
                ("bAutoExposure",c_bool),
                ("bManualExposure",c_bool),
                ("bAntiFlick",c_bool),
                ("bDeviceIsp",c_bool),
                ("bForceUseDeviceIsp",c_bool),
                ("bZoomHD",c_bool)
            ]

class tSdkCameraCapbility(Structure):
    _fields_ = [
            ("pTriggerDesc", POINTER(tSdkTrigger)),
            ("iTriggerDesc", c_int),
            ("pImageSizeDesc", POINTER(tSdkImageResolution)),
            ("iImageSizeDesc", c_int),
            ("pClrTempDesc", POINTER(tSdkColorTemperatureDes)),
            ("iClrTempDesc", c_int),
            ("pMediaTypeDesc", POINTER(tSdkMediaType)),
            ("iMediaTypdeDesc", c_int),
            ("pFrameSpeedDesc", POINTER(tSdkFrameSpeed)),
            ("iFrameSpeedDesc",c_int),
            ("pPackLenDesc",POINTER(tSdkPackLength)),
            ("iPackLenDesc",c_int),
            ("iOutputIoCounts",c_int),
            ("iInputIoCounts",c_int),
            ("pPresetLutDesc",POINTER(tSdkPresetLut)),
            ("iPresetLut",c_int),
            ("iUserDataMaxLen",c_int),
            ("bParamInDevice",c_int),
            ("pAeAlmSwDesc",POINTER(tSdkAeAlgorithm)),
            ("iAeAlmSwDesc",c_int),
            ("pAeAlmHdDesc",POINTER(tSdkAeAlgorithm)),
            ("iAeAlmHdDesc",c_int),
            ("pBayerDecAlmSwDesc",POINTER(tSdkBayerDecodeAlgorithm)),
            ("iBayerDecAlmSwDesc",c_int),
            ("pBayerDecAlmHdDesc",POINTER(tSdkBayerDecodeAlgorithm)),
            ("iBayerDecAlmHdDesc",c_int),
            ("sExposeDesc",tSdkExpose),
            ("sResolutionRange",tSdkResolutionRange),
           # ("sRgbGainRange",tRgbGainRange),
            ("sSaturationRange",tSaturationRange),
            ("sGammaRange",tGammaRange),
            ("sContrastRange",tContrastRange),
            ("sSharpnessRange",tSharpnessRange),
            ("sIspCapacity",tSdkIspCapacity)
            ]

class tSdkFrameHead(Structure):
    _fields_ = [("uiMediaType", c_uint16),
                ("uBytes", c_uint16),
                ("iWidth", c_int16),
                ("iHeight", c_int16),
                ("iWidthZoomSw", c_int16),
                ("iHeightZoomSw", c_int16),
                ("bIsTrigger", c_bool),
                ("uiTimeStamp", c_uint16),
                ("uiExpTime", c_uint16),
                ("fAnalogGain", c_float),
                ("iGamma", c_int16),
                ("iContrast", c_int16),
                ("iSaturation", c_int16),
                ("fRgain", c_float),
                ("fGgain", c_float),
                ("fBgain", c_float),
            ]



'''
    ctypes函数封装 
    功能：将c的函数按照ctypes的格式要求封装，返回给python代码调用
    输入    lib         CDLL类，例如 mvsdk = CDLL("libMVSDK.so")
            funcname    函数名，用字符串表示
            restype     函数返回类型，ctypes类型
            argtypes    函数参数列表，ctypes类型 array表示
'''
def wrap_func(lib, funcname, restype, argtypes):
    """Simplify wrapping ctypes functions"""
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func

class MindVisionCamera():
    def __init__(self, libname):
        self.sdk = CDLL(libname)
        self.libc = CDLL("libc.so.6")   # malloc
        # 相机属性
        self.hCamera = c_int()
        self.tCameraEnumList = tSdkCameraDevInfo()
        self.cam_reso = tSdkImageResolution()
        self.expo_time = c_double()
        self.sFrameInfo = tSdkFrameHead()        
        # libc接口
        self._malloc = wrap_func(self.libc, "malloc", POINTER(c_uint8), [c_int,])
        self._release = wrap_func(self.libc, "free", None, [POINTER(c_uint8),])
        # sdk接口
        self._CameraSdkInit = wrap_func(self.sdk, 'CameraSdkInit', c_int, [c_int])
        self._CameraEnumerateDevice = wrap_func(self.sdk, 'CameraEnumerateDevice', c_int, [POINTER(tSdkCameraDevInfo), POINTER(c_int)])
        self._CameraInit = wrap_func(self.sdk, 'CameraInit', c_int, [POINTER(tSdkCameraDevInfo), c_int, c_int, POINTER(c_int)])
        self._CameraGetImageResolution = wrap_func(self.sdk, "CameraGetImageResolution", c_int, [c_int, POINTER(tSdkImageResolution)])
        self._CameraSetImageResolution = wrap_func(self.sdk, "CameraSetImageResolution", c_int, [c_int, POINTER(tSdkImageResolution)])
        self._CameraPlay = wrap_func(self.sdk, "CameraPlay", c_int, [c_int,])
        self._CameraSetIspOutFormat = wrap_func(self.sdk, "CameraSetIspOutFormat", c_int, [c_int, c_uint])
        self._CameraSetAeState = wrap_func(self.sdk, "CameraSetAeState", c_int, [c_int, c_bool])
        self._CameraGetExposureTime = wrap_func(self.sdk, "CameraGetExposureTime", c_int, [c_int, POINTER(c_double)])
        self._CameraSetExposureTime = wrap_func(self.sdk, "CameraSetExposureTime", c_int, [c_int, c_double])
        self._CameraGetImageBuffer = wrap_func(self.sdk, "CameraGetImageBuffer", c_int, [c_int, POINTER(tSdkFrameHead), POINTER(POINTER(c_uint8)), c_uint16])
        self._CameraImageProcess = wrap_func(self.sdk, "CameraImageProcess", c_int, [c_int, POINTER(c_uint8), POINTER(c_uint8), POINTER(tSdkFrameHead)])
        self._CameraReleaseImageBuffer = wrap_func(self.sdk, "CameraReleaseImageBuffer", c_int, [c_int, POINTER(c_uint8)])
        self._CameraUnInit = wrap_func(self.sdk, "CameraUnInit", c_int, [c_int,])
        # 图像缓冲区
        self.rgb_buf = self._malloc(1280*1024*3)
        self.pbyBuffer = POINTER(c_uint8)()
        print('self.rgb_buf: ', self.rgb_buf, 'self.pbyBuffer: ', self.pbyBuffer)

        # # 相机初始化
        # self.CameraSdkInit(1)
        # self.CameraEnumerateDevice()
        # self.CameraInit()
        # self.CameraGetImageResolution()
        # #self.CameraSetImageResolution()
        # self.CameraGetImageResolution()
        # self.CameraPlay()
        # self.CameraSetIspOutFormat()
        # self.CameraSetAeState()
        # self.CameraGetExposureTime()
        # self.CameraSetExposureTime()
        # self.CameraGetExposureTime()
        # self.prepareCam()

    def api_status(self,status):
        if status == API_STATUS_OK:
            return True
        else:
            return False

    def CameraSdkInit(self, i):
        status = self._CameraSdkInit(i)
        print("CameraSdkInit: ", status)
        return self.api_status(status)

    def CameraEnumerateDevice(self):
        iCameraCounts = c_int(1)    # 调用前必须初始       
        status = self._CameraEnumerateDevice(byref(self.tCameraEnumList), byref(iCameraCounts))
        print("CameraEnumerateDevice: ",status)
        print("camera number: ",iCameraCounts.value)

        return self.api_status(status)

    def CameraInit(self):
        status = self._CameraInit(byref(self.tCameraEnumList), -1, -1, byref(self.hCamera))
        print("CameraInit: ", status)
        return self.api_status(status)

    def CameraGetImageResolution(self):
        status = self._CameraGetImageResolution(self.hCamera, byref(self.cam_reso))
        print("CameraGetImageResolution: ", status)
        print("iWidth: ", self.cam_reso.iWidth, "iHeight: ", self.cam_reso.iHeight)
        dict = {'width':self.cam_reso.iWidth,'height':self.cam_reso.iHeight}
        return dict


    def CameraSetImageResolution(self,width,height):
        self.cam_reso.iHOffsetFOV = 0;
        self.cam_reso.iVOffsetFOV = 0;
        self.cam_reso.iWidth  = width;
        self.cam_reso.iHeight = height;
        self.cam_reso.uSkipMode = 1;
        self.cam_reso.iWidthFOV = width;
        self.cam_reso.iHeightFOV = height;
        self.cam_reso.iIndex = 1;

        status = self._CameraSetImageResolution(self.hCamera, byref(self.cam_reso))
        print("CameraSetImageResolution: ", status)
        return self.api_status(status)


    def CameraSetImageResolution(self):
        #MEANUALLY SET RESOLUTION
        # self.cam_reso.iHOffsetFOV = 320;
        # self.cam_reso.iVOffsetFOV = 256;
        # self.cam_reso.iWidth  = 640;
        # self.cam_reso.iHeight = 512;
        # self.cam_reso.uSkipMode = 1;
        # self.cam_reso.iWidthFOV = 640;
        # self.cam_reso.iHeightFOV = 512;
        # self.cam_reso.iIndex = 1;

        self.cam_reso.iHOffsetFOV = 0;
        self.cam_reso.iVOffsetFOV = 0;
        self.cam_reso.iWidth  = 1280;
        self.cam_reso.iHeight = 1024;
        self.cam_reso.uSkipMode = 1;
        self.cam_reso.iWidthFOV = 1280;
        self.cam_reso.iHeightFOV = 1024;
        self.cam_reso.iIndex = 1;


        status = self._CameraSetImageResolution(self.hCamera, byref(self.cam_reso))
        print("CameraSetImageResolution: ", status)
        return self.api_status(status)

    def CameraPlay(self):
        status = self._CameraPlay(self.hCamera)
        print("CameraPlay: ", status)
        return self.api_status(status)

    def CameraSetIspOutFormat(self):
        status = self._CameraSetIspOutFormat(self.hCamera, 0x01000000 | 0x00080000 | 0x0001)
        print("CameraSetIspOutFormat: ", status)
        return self.api_status(status)

    def CameraSetAeState(self):
        status = self._CameraSetAeState(self.hCamera, False)
        print("CameraSetAeState: ", status)
        return self.api_status(status)

    def CameraGetExposureTime(self):
        status = self._CameraGetExposureTime(self.hCamera, byref(self.expo_time))
        print("CameraGetExposureTime: ", self.expo_time)
        return self.expo_time

    def CameraSetExposureTime(self):
        status = self._CameraSetExposureTime(self.hCamera, c_double(20000.0))
        # status = self._CameraSetExposureTime(self.hCamera, c_double(16000.0))
        print("CameraSetExposureTime: ", status)
        return self.api_status(status)

    def CameraGetImageBuffer(self):
        status = self._CameraGetImageBuffer(self.hCamera, byref(self.sFrameInfo), byref(self.pbyBuffer), 1000)
        return self.api_status(status)


    def CameraImageProcess(self):
        status = self._CameraImageProcess(self.hCamera, self.pbyBuffer, self.rgb_buf, byref(self.sFrameInfo))
        #print('CameraImageProcess: ', status)
        return self.api_status(status)

    def CameraReleaseImageBuffer(self):
        status = self._CameraReleaseImageBuffer(self.hCamera, self.pbyBuffer)
        return self.api_status(status)


    def pop_frame(self):
        self.CameraGetImageBuffer()
        self.CameraImageProcess()
        self.CameraReleaseImageBuffer()
        # image = np.ctypeslib.as_array(self.rgb_buf, (512, 640))
        image = np.ctypeslib.as_array(self.rgb_buf, (1024, 1280))
        return image

    def release(self):
        status = self._release(self.rgb_buf)
        return self.api_status(status)

    def save_cv_image(self,image,fname):
        return cv2.imwrite(fname,image)

    def save(self, fname):
        # image = np.ctypeslib.as_array(self.rgb_buf, (512, 640))
        image = np.ctypeslib.as_array(self.rgb_buf, (1024, 1280))

        return cv2.imwrite(fname, image)

    def close(self):
        status_1 = self.release()
        status_2 = self.CameraUnInit()
        return (self.api_status(status_1)) and (self.api_status(status_2))

    def CameraUnInit(self):
        status = self._CameraUnInit(self.hCamera)
        return self.api_status(status)

    def prepareCam(self):
        # 相机初始化
        status1 = self.CameraSdkInit(1)
        status2 = self.CameraEnumerateDevice()
        status3 = self.CameraInit()
        self.CameraGetImageResolution()
        status4 = self.CameraPlay()
        status5 = self.CameraSetIspOutFormat()
        status6 = self.CameraSetAeState()
        self.CameraGetExposureTime()
        status7 = self.CameraSetExposureTime()
        self.CameraGetExposureTime()

        status = status1 and status2 and status3 and status4 and status5 and status6 and status7
        print("status es:  ",status1,status2,status3,status4,status5,status6,status7,status)
        return status
    
    def open(self):
        # 图像缓冲区
        self.rgb_buf = self._malloc(1280*1024*3)
        self.pbyBuffer = POINTER(c_uint8)()
        # print('self.rgb_buf: ', self.rgb_buf, 'self.pbyBuffer: ', self.pbyBuffer)
        status = self.prepareCam()
        return status
        
    def set_image_channelOption(self,val):
        return False










