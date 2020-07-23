from ctypes import *
import numpy as np
import cv2
import os

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *



API_STATUS_OK = 0
# CAMERA_WIDTH = 640  #2592
# CAMERA_HEIGHT = 480 #2048
FEATURE_FILE = "./camera/LBASFeature.ini"
# CAMERA_WIDTH = 2592  #2592
# CAMERA_HEIGHT = 2048 #2048
# CAMERA_WIDTH = 2448  #2592
# CAMERA_HEIGHT = 2048 #2048
CAMERA_WIDTH = 1280  #2592
CAMERA_HEIGHT = 960 #2048




''' 结构体定义 camera SDK中C的结构体转换为python中的class '''

''' GIGE设备信息结构体 MV_GIGE_DEVICE_INFO
    Members
    nIpCfgOption 
    IP配置选项 
    nIpCfgCurrent 
    当前的IP配置 
    nCurrentIp 
    当前的设备IP 
    nCurrentSubNetMask 
    当前的子网掩码 
    nDefultGateWay 
    默认网关 
    chManufacturerName 
    制造商名称 
    chModelName 
    型号名称 
    chDeviceVersion 
    设备版本 
    chManufacturerSpecificInfo 
    制造批次等信息 
    chSerialNumber 
    序列号 
    chUserDefinedName 
    自定义的名字 
    nNetExport 
    网口IP地址 
    nReserved 
    保留字节 
'''
class MV_GIGE_DEVICE_INFO(Structure):
    _fields_ = [
                ("nIpCfgOption",                c_uint),
                ("nIpCfgCurrent",               c_uint),
                ("nCurrentIp",                  c_uint),
                ("nCurrentSubNetMask",          c_uint),
                ("nDefultGateWay",              c_uint),
                ("chManufacturerName",          c_char * 32),
                ("chModelName",                 c_char * 32),
                ("chDeviceVersion",             c_char * 32),
                ("chManufacturerSpecificInfo",  c_char * 48),
                ("chSerialNumber",              c_char * 16),
                ("chUserDefinedName",           c_char * 16),
                ("nNetExport",                  c_uint),
                ("nReserved",                   c_uint * 4)
            ]
''' USB设备信息结构体 MV_USB3_DEVICE_INFO
    Members
    CrtlInEndPoint 
    控制输入端点 
    CrtlOutEndPoint 
    控制输出端点 
    StreamEndPoint 
    流端点 
    EventEndPoint 
    事件端点 
    idVendor 
    供应商ID号 
    idProduct 
    产品ID号 
    nDeviceNumber 
    设备号 
    chDeviceGUID 
    设备GUID号 
    chVendorName 
    供应商名字 
    chModelName 
    型号名字 
    chFamilyName 
    家族名字 
    chDeviceVersion 
    设备版本号 
    chManufacturerName 
    制造商名字 
    chSerialNumber 
    序列号 
    chUserDefinedName 
    用户自定义名字 
    nbcdUSB 
    支持的USB协议 
    nReserved 
    保留字节 
'''
class MV_USB3_DEVICE_INFO(Structure):
    _fields_ = [
                ("CrtlInEndPoint",              c_ubyte),
                ("CrtlOutEndPoint",             c_ubyte),
                ("StreamEndPoint",              c_ubyte),
                ("EventEndPoint",               c_ubyte),
                ("idVendor",                    c_ushort),
                ("idProduct",                   c_ushort),
                ("nDeviceNumber",               c_uint),
                ("chDeviceGUID",                c_ubyte * 64),
                ("chVendorName",                c_ubyte * 64),
                ("chModelName",                 c_ubyte * 64),
                ("chFamilyName",                c_ubyte * 64),
                ("chDeviceVersion",             c_ubyte * 64),
                ("chManufacturerName",          c_ubyte * 64),
                ("chSerialNumber",              c_ubyte * 64),
                ("nbcdUSB",                     c_uint),
                ("nReserved",                   c_uint * 3)
            ]
'''设备信息结构体
    Members
    chPortID 
    端口号 
    chModelName 
    型号名称 
    chFamilyName 
    家族名称 
    chDeviceVersion 
    设备版本号 
    chManufacturerName 
    制造商名称 
    chSerialNumber 
    序列号 
    nReserved 
    保留字节 

'''
class MV_CamL_DEV_INFO(Structure):
    _fields_ = [
                ("chPortID",            c_ubyte * 64),
                ("chModelName",         c_ubyte * 64),
                ("chFamilyName",        c_ubyte * 64),
                ("chDeviceVersion",     c_ubyte * 64),
                ("chManufacturerName",  c_ubyte * 64),
                ("chSerialNumber",      c_ubyte * 64),
                ("nReserved",           c_uint  * 38)
            ]


'''special info 
    参数包含：MV_GIGE_DEVICE_INFO
             MV_USB3_DEVICE_INFO
             MV_CamL_DEV_INFO
'''
class SpecialInfo(Union):
    _fields_ = [
                ("stGigEInfo",      MV_GIGE_DEVICE_INFO),
                ("stUsb3VInfo",     MV_USB3_DEVICE_INFO),
                ("stCamLInfo",      MV_CamL_DEV_INFO)
    ]

class MV_CC_DEVICE_INFO(Structure):
    _fields_ = [
                ("nMajorVer",       c_uint),
                ("nMinorVer",       c_uint),
                ("nMacAddrHigh",    c_uint),
                ("nMacAddrLow",     c_uint),
                ("nTLayerType",     c_uint),
                ("nReserved",       c_uint*4),
                ("specialInfo",     SpecialInfo)
            ]


# 设备信息列表
class MV_CC_DEVICE_INFO_LIST(Structure):
    _fields_ = [
                ("nDeviceNum", c_int),              # 在线设备数量
                ("pDeviceInfo", POINTER(MV_CC_DEVICE_INFO) * 256)        # 在线设备信息，每位数组表示一台设备，最多支持256台设备 
            ]
'''#64位int类型参数值
    Members
        nCurValue 
        当前值 
        nMax 
        最大值 
        nMin 
        最小值 
        nInc 
        增量 
        nReserved 
        保留，置为0 
'''
class MVCC_INTVALUE_EX(Structure):
    _fields_ = [
                ("nCurValue",c_longlong),
                ("nMax",c_longlong),
                ("nMin",c_longlong),
                ("nInc",c_longlong),
                ("nReserved",c_longlong * 4)
            ]


'''#枚举类型参数值
    Members
        nCurValue 
        当前值 
        nSupportedNum 
        支持的有效数据个数 
        nSupportValue 
        支持的枚举类型，每位数组表示一种类型，最多支持nSupportValue种类型 
        nReserved 
        保留，置为0 
'''
class MVCC_ENUMVALUE(Structure):
    _fields_ = [
                 ("nCurValue",c_uint),
                 ("nSupportedNum",c_uint),
                 ("nSupportValue",c_uint * 64),
                 ("nReserved",c_uint * 4)
            ]


'''string类型参数值
    Members
        chCurValue 
        当前值 
        nReserved 
        保留，置为0 
'''
class MVCC_STRINGVALUE(Structure):
    _fields_ = [
                ("chCurValue",c_char*256),
                ("nReserved",c_uint*4)
            ]


class MvGvspPixelType:
    MV_GVSP_PIX_MONO                        = 0x01000000
    MV_GVSP_PIX_COLOR                       = 0x02000000
    PixelType_Gvsp_Undefined                = -1
    PixelType_Gvsp_Mono1p                   =   (MV_GVSP_PIX_MONO | (1<<16) | 0x0037)
    PixelType_Gvsp_Mono2p                   =   (MV_GVSP_PIX_MONO | (2<<16) | 0x0038)
    PixelType_Gvsp_Mono4p                   =   (MV_GVSP_PIX_MONO | (4<<16) | 0x0039)
    PixelType_Gvsp_Mono8                    =   (0x01000000 | (8<<16) | 0x0001)
    PixelType_Gvsp_Mono8_Signed             =   (0x01000000 | (8<<16)  | 0x0002)
    PixelType_Gvsp_Mono10                   =   (MV_GVSP_PIX_MONO | (16<<16) | 0x0003)
    PixelType_Gvsp_Mono10_Packed            =   (MV_GVSP_PIX_MONO | (12<<16) | 0x0004)
    PixelType_Gvsp_Mono12                   =   (MV_GVSP_PIX_MONO | (16<<16) | 0x0005)
    PixelType_Gvsp_Mono12_Packed            =   (MV_GVSP_PIX_MONO | (12<<16) | 0x0006)
    PixelType_Gvsp_Mono14                   =   (MV_GVSP_PIX_MONO | (16<<16) | 0x0025)
    PixelType_Gvsp_Mono16                   =   (MV_GVSP_PIX_MONO | (16<<16) | 0x0007)
        # Bayer buffer format defines 
    PixelType_Gvsp_BayerGR8                 =   (MV_GVSP_PIX_MONO | (8<<16) | 0x0008)
    PixelType_Gvsp_BayerRG8                 =   (MV_GVSP_PIX_MONO | (8<<16) | 0x0009)
    PixelType_Gvsp_BayerGB8                 =   (MV_GVSP_PIX_MONO | (8<<16) | 0x000A)
    PixelType_Gvsp_BayerBG8                 =   (MV_GVSP_PIX_MONO | (8<<16) | 0x000B)
    PixelType_Gvsp_BayerGR10                =   (MV_GVSP_PIX_MONO | (16<<16) | 0x000C)
    PixelType_Gvsp_BayerRG10                =   (MV_GVSP_PIX_MONO | (16<<16) | 0x000D)
    PixelType_Gvsp_BayerGB10                =   (MV_GVSP_PIX_MONO | (16<<16) | 0x000E)
    PixelType_Gvsp_BayerBG10                =   (MV_GVSP_PIX_MONO | (16<<16) | 0x000F)
    PixelType_Gvsp_BayerGR12                =   (MV_GVSP_PIX_MONO | (16<<16) | 0x0010)
    PixelType_Gvsp_BayerRG12                =   (MV_GVSP_PIX_MONO | (16<<16) | 0x0011)
    PixelType_Gvsp_BayerGB12                =   (MV_GVSP_PIX_MONO | (16<<16) | 0x0012)
    PixelType_Gvsp_BayerBG12                =   (MV_GVSP_PIX_MONO | (16<<16) | 0x0013)
    PixelType_Gvsp_BayerGR10_Packed         =   (MV_GVSP_PIX_MONO | (12<<16) | 0x0026)
    PixelType_Gvsp_BayerRG10_Packed         =   (MV_GVSP_PIX_MONO | (12<<16) | 0x0027)
    PixelType_Gvsp_BayerGB10_Packed         =   (MV_GVSP_PIX_MONO | (12<<16) | 0x0028)
    PixelType_Gvsp_BayerBG10_Packed         =   (MV_GVSP_PIX_MONO | (12<<16) | 0x0029)
    PixelType_Gvsp_BayerGR12_Packed         =   (MV_GVSP_PIX_MONO | (12<<16) | 0x002A)
    PixelType_Gvsp_BayerRG12_Packed         =   (MV_GVSP_PIX_MONO | (12<<16) | 0x002B)
    PixelType_Gvsp_BayerGB12_Packed         =   (MV_GVSP_PIX_MONO | (12<<16) | 0x002C)
    PixelType_Gvsp_BayerBG12_Packed         =   (MV_GVSP_PIX_MONO | (12<<16) | 0x002D)
    PixelType_Gvsp_BayerGR16                =   (MV_GVSP_PIX_MONO | (16<<16) | 0x002E)
    PixelType_Gvsp_BayerRG16                =   (MV_GVSP_PIX_MONO | (16<<16) | 0x002F)
    PixelType_Gvsp_BayerGB16                =   (MV_GVSP_PIX_MONO | (16<<16) | 0x0030)
    PixelType_Gvsp_BayerBG16                =   (MV_GVSP_PIX_MONO | (16<<16) | 0x0031)
        # RGB Packed buffer format defines 
    PixelType_Gvsp_RGB8_Packed              =   (0x02000000 | (24<<16) | 0x0014)
    PixelType_Gvsp_BGR8_Packed              =   (MV_GVSP_PIX_COLOR | (24<<16) | 0x0015)
    PixelType_Gvsp_RGBA8_Packed             =   (MV_GVSP_PIX_COLOR | (32<<16) | 0x0016)
    PixelType_Gvsp_BGRA8_Packed             =   (MV_GVSP_PIX_COLOR | (32<<16) | 0x0017)
    PixelType_Gvsp_RGB10_Packed             =   (MV_GVSP_PIX_COLOR | (48<<16) | 0x0018)
    PixelType_Gvsp_BGR10_Packed             =   (MV_GVSP_PIX_COLOR | (48<<16) | 0x0019)
    PixelType_Gvsp_RGB12_Packed             =   (MV_GVSP_PIX_COLOR | (48<<16) | 0x001A)
    PixelType_Gvsp_BGR12_Packed             =   (MV_GVSP_PIX_COLOR | (48<<16) | 0x001B)
    PixelType_Gvsp_RGB16_Packed             =   (MV_GVSP_PIX_COLOR | (48<<16) | 0x0033)
    PixelType_Gvsp_RGB10V1_Packed           =   (MV_GVSP_PIX_COLOR | (32<<16) | 0x001C)
    PixelType_Gvsp_RGB10V2_Packed           =   (MV_GVSP_PIX_COLOR | (32<<16) | 0x001D)
    PixelType_Gvsp_RGB12V1_Packed           =   (MV_GVSP_PIX_COLOR | (36<<16) | 0X0034)
    PixelType_Gvsp_RGB565_Packed            =   (MV_GVSP_PIX_COLOR | (16<<16) | 0x0035)
    PixelType_Gvsp_BGR565_Packed            =   (MV_GVSP_PIX_COLOR | (16<<16) | 0X0036)
        # YUV Packed buffer format defines 
    PixelType_Gvsp_YUV411_Packed            =   (MV_GVSP_PIX_COLOR | (12<<16) | 0x001E)
    PixelType_Gvsp_YUV422_Packed            =   (MV_GVSP_PIX_COLOR | (16<<16) | 0x001F)
    PixelType_Gvsp_YUV422_YUYV_Packed       =   (MV_GVSP_PIX_COLOR | (16<<16) | 0x0032)
    PixelType_Gvsp_YUV444_Packed            =   (MV_GVSP_PIX_COLOR | (24<<16) | 0x0020)
    PixelType_Gvsp_YCBCR8_CBYCR             =   (MV_GVSP_PIX_COLOR | (24<<16) | 0x003A)
    PixelType_Gvsp_YCBCR422_8               =   (MV_GVSP_PIX_COLOR | (16<<16) | 0x003B)
    PixelType_Gvsp_YCBCR422_8_CBYCRY        =   (MV_GVSP_PIX_COLOR | (16<<16) | 0x0043)
    PixelType_Gvsp_YCBCR411_8_CBYYCRYY      =   (MV_GVSP_PIX_COLOR | (12<<16) | 0x003C)
    PixelType_Gvsp_YCBCR601_8_CBYCR         =   (MV_GVSP_PIX_COLOR | (24<<16) | 0x003D)
    PixelType_Gvsp_YCBCR601_422_8           =   (MV_GVSP_PIX_COLOR | (16<<16) | 0x003E)
    PixelType_Gvsp_YCBCR601_422_8_CBYCRY    =   (MV_GVSP_PIX_COLOR | (16<<16) | 0x0044)
    PixelType_Gvsp_YCBCR601_411_8_CBYYCRYY  =   (MV_GVSP_PIX_COLOR | (12<<16) | 0x003F)
    PixelType_Gvsp_YCBCR709_8_CBYCR         =   (MV_GVSP_PIX_COLOR | (24<<16) | 0x0040)
    PixelType_Gvsp_YCBCR709_422_8           =   (MV_GVSP_PIX_COLOR | (16<<16) | 0x0041)
    PixelType_Gvsp_YCBCR709_422_8_CBYCRY    =   (MV_GVSP_PIX_COLOR | (16<<16) | 0x0045)
    PixelType_Gvsp_YCBCR709_411_8_CBYYCRYY  =   (MV_GVSP_PIX_COLOR | (12<<16) | 0x0042)
        # RGB Planar buffer format defines 
    PixelType_Gvsp_RGB8_Planar              =   (MV_GVSP_PIX_COLOR | (24<<16) | 0x0021)
    PixelType_Gvsp_RGB10_Planar             =   (MV_GVSP_PIX_COLOR | (48<<16) | 0x0022)
    PixelType_Gvsp_RGB12_Planar             =   (MV_GVSP_PIX_COLOR | (48<<16) | 0x0023)
    PixelType_Gvsp_RGB16_Planar             =   (MV_GVSP_PIX_COLOR | (48<<16) | 0x0024)
    # 自定义的图片格式 MV_GVSP_PIX_CUSTOM没找到定义
    # PixelType_Gvsp_Jpeg                     =   (MV_GVSP_PIX_CUSTOM | (24<<16) | 0x0001)



class MV_FRAME_OUT_INFO_EX(Structure):
    _fields_ = [
                ("nWidth",c_ushort),
                ("nHeight",c_ushort),
                ("enPixelType",c_uint32),
                ("nFrameNum",c_uint),
                ("nDevTimeStampHigh",c_uint),
                ("nDevTimeStampLow",c_uint),
                ("nReserved0",c_uint),
                ("nHostTimeStamp",c_int64),
                ("nFrameLen",c_uint),
                ("nSecondCount",c_int),
                ("nCycleCount",c_int),
                ("nCycleOffset",c_int),
                ("fGain",c_float),
                ("fExposureTime",c_float),
                ("nAverageBrightness",c_uint),
                ("nRed",c_uint),
                ("nGreen",c_uint),
                ("nBlue",c_uint),
                ("nFrameCounter",c_uint),
                ("nTriggerIndex",c_uint),
                ("nInput",c_uint),
                ("nOutput",c_uint),
                ("nLostPacket",c_uint),
                ("nOffsetX",c_ushort),
                ("nOffsetY",c_ushort),
                ("nReserved",c_int*41)
            ]

class MV_FRAME_OUT(Structure):
    _fields_=[
        ("pBufAddr",POINTER(c_ubyte)),
        ("stFrameInfo", MV_FRAME_OUT_INFO_EX),
        ("nRes",c_int*16)

    ]






        

class MVCC_INTVALUE(Structure):
    _fields_ = [
                 ("nCurValue",c_uint),
                 ("nMax",c_uint),
                 ("nMin",c_uint),
                 ("nInc",c_uint),
                 ("nReserved",c_uint*4)
            ]




class MVCC_FLOATVALUE(Structure):
    _fields_ = [
                ("fCurValue",c_float),
                ("fMax",c_float),
                ("fMin",c_float),
                ("nReserved",c_float)
            ]


class CamInfo():
    x_offset = None
    y_offset = None
    width = None
    height = None
    exposure_time = None







class CustomizedSignal(QObject):
    connect_fail_signal = Signal()
    connect_success_signal = Signal()



#-------------------------------------------------------------------------------------------
''' ctypes函数封装 
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




'''
    相机操作流程
    1 枚举子网内指定的传输协议对应的所有设备
    2 选择查找到的第一台在线设备，创建设备句柄
    3 连接设备
    4 ...其他处理
    5 关闭设备，释放资源
    6 销毁句柄，释放资源
'''


'''
    图像采集显示
    1 主动取流[目前先采取该方式]
    2 回调出流
'''



'''
    操作接口
    
    枚举子网内指定的传输协议对应的所有设备
    int MV_CC_EnumDevices(
        unsigned int              nTLayerType,
        MV_CC_DEVICE_INFO_LIST    *pstDevList,
    );
'''
class LBASCamera():
    def __init__(self, libname,camindex):
        self.sdk = CDLL(libname)
        self.libc = CDLL("libc.so.6")   # malloc
        self.m_handle = None
        
        # libc接口
        self._memcpy                     = wrap_func(self.libc, "memcpy",                   c_void_p,   [c_void_p, c_void_p, c_uint])
        self._malloc                     = wrap_func(self.libc, "malloc", POINTER(c_uint8), [c_int,])
        self._memset                     = wrap_func(self.libc, "memset", POINTER(c_uint8), [c_void_p,c_int,c_uint])
        # sdk接口
        self._MV_CC_EnumDevices          = wrap_func(self.sdk, "MV_CC_EnumDevices",         c_int,      [c_uint,POINTER(MV_CC_DEVICE_INFO_LIST)])
        self._MV_CC_EnumDevicesEx     = wrap_func(self.sdk,"MV_CC_EnumDevicesEx",      c_int,     [c_uint,POINTER(MV_CC_DEVICE_INFO_LIST),c_char_p])        
        self._MV_CC_CreateHandle         = wrap_func(self.sdk, "MV_CC_CreateHandle",        c_int,      [POINTER(c_void_p),POINTER(MV_CC_DEVICE_INFO)])
        self._MV_CC_OpenDevice           = wrap_func(self.sdk, "MV_CC_OpenDevice",          c_int,      [c_void_p,c_uint,c_ushort])
        self._MV_CC_CloseDevice          = wrap_func(self.sdk, "MV_CC_CloseDevice",         c_int,      [c_void_p])
        self._MV_CC_DestroyHandle        = wrap_func(self.sdk,"MV_CC_DestroyHandle",        c_int,      [c_void_p])
        self._MV_CC_GetIntValue          = wrap_func(self.sdk,"MV_CC_GetIntValue",          c_int,      [c_void_p,c_char_p,POINTER(MVCC_INTVALUE)])
        self._MV_CC_GetIntValueEx        = wrap_func(self.sdk,"MV_CC_GetIntValueEx",        c_int,      [c_void_p,c_char_p,POINTER(MVCC_INTVALUE_EX)])
        # self._MV_CC_GetEnumValue         = wrap_func(self.sdk,"MV_CC_GetEnumValue",         c_int,      [c_void_p,c_char_p,POINTER(MVCC_ENUMVALUE)])
        self._MV_CC_GetFloatValue        = wrap_func(self.sdk,"MV_CC_GetFloatValue",        c_int,      [c_void_p,c_char_p,POINTER(MVCC_FLOATVALUE)])
        # self._MV_CC_GetBoolValue         = wrap_func(self.sdk,"MV_CC_GetBoolValue",         c_int,      [c_void_p,c_char_p,POINTER(c_bool)])
        self._MV_CC_GetStringValue       = wrap_func(self.sdk,"MV_CC_GetStringValue",       c_int,      [c_void_p,c_char_p,POINTER(MVCC_STRINGVALUE)])
        
        self._MV_CC_SetIntValue         = wrap_func(self.sdk,"MV_CC_SetIntValue",           c_int,      [c_void_p,c_char_p,c_uint])
        self._MV_CC_SetIntValueEx        = wrap_func(self.sdk,"MV_CC_SetIntValueEx",        c_int,      [c_void_p,c_char_p,c_uint])
        # self._MV_CC_SetEnumValue         = wrap_func(self.sdk,"MV_CC_SetEnumValue",         c_int,      [c_void_p,c_char_p,c_uint])
        # self._MV_CC_SetEnumValueByString = wrap_func(self.sdk,"MV_CC_SetEnumValueByString", c_int,      [c_void_p,c_char_p,c_char_p])
        self._MV_CC_SetFloatValue        = wrap_func(self.sdk,"MV_CC_SetFloatValue",        c_int,      [c_void_p,c_char_p,c_float])
        # self._MV_CC_SetBoolValue         = wrap_func(self.sdk,"MV_CC_SetBoolValue",         c_int,      [c_void_p,c_char_p,c_bool])
        # self._MV_CC_SetStringValue       = wrap_func(self.sdk,"MV_CC_SetStringValue",       c_int,      [c_void_p,c_char_p,c_char_p])
        # self._MV_CC_SetCommandValue      = wrap_func(self.sdk,"MV_CC_SetCommandValue",      c_int,      [c_void_p,c_char_p])
        self._MV_CC_GetImageForRGB   = wrap_func(self.sdk,"MV_CC_GetImageForRGB",   c_int,      [c_void_p,POINTER(c_ubyte),c_uint,POINTER(MV_FRAME_OUT_INFO_EX),c_int])
        self._MV_CC_GetImageForBGR   = wrap_func(self.sdk,"MV_CC_GetImageForBGR",   c_int,      [c_void_p,POINTER(c_ubyte),c_uint,POINTER(MV_FRAME_OUT_INFO_EX),c_int])
        self._MV_CC_GetOneFrameTimeout   = wrap_func(self.sdk,"MV_CC_GetOneFrameTimeout",   c_int,      [c_void_p,POINTER(c_ubyte),c_uint,POINTER(MV_FRAME_OUT_INFO_EX),c_int])
        # self._MV_CC_GetImageBuffer   = wrap_func(self.sdk,"MV_CC_GetImageBuffer",   c_int,      [c_void_p,POINTER(MV_FRAME_OUT),c_uint])

        self._MV_CC_StartGrabbing   = wrap_func(self.sdk,"MV_CC_StartGrabbing", c_int, [c_void_p])
        self._MV_CC_StopGrabbing    = wrap_func(self.sdk,"MV_CC_StopGrabbing",  c_int, [c_void_p])
        self._MV_CC_SetPixelFormat  = wrap_func(self.sdk,"MV_CC_SetPixelFormat",c_int, [c_void_p,c_uint])
        self._MV_CC_GetPixelFormat  = wrap_func(self.sdk,"MV_CC_GetPixelFormat",c_int,[c_void_p,POINTER(MVCC_ENUMVALUE)])
        self._MV_CC_GetDeviceInfo   =  wrap_func(self.sdk,"MV_CC_GetDeviceInfo", c_int,[c_void_p,POINTER(MV_CC_DEVICE_INFO)])
        self._MV_GIGE_ForceIpEx       =  wrap_func(self.sdk,"MV_GIGE_ForceIpEx",c_int,[c_void_p,c_uint,c_uint,c_uint])
        self._MV_CC_FeatureSave      =  wrap_func(self.sdk,"MV_CC_FeatureSave",c_int,[c_void_p,c_char_p])
        self._MV_CC_FeatureLoad      =  wrap_func(self.sdk,"MV_CC_FeatureLoad",c_int,[c_void_p,c_char_p])



        self.info = CamInfo()
        self.rgb_buf = self._malloc(CAMERA_WIDTH*CAMERA_HEIGHT*3)
        self.mono_buf = self._malloc(CAMERA_WIDTH*CAMERA_HEIGHT*1)
        self.bgr_buf = self._malloc(CAMERA_WIDTH*CAMERA_HEIGHT*3)
        self.image_width = CAMERA_WIDTH#1280
        self.image_height = CAMERA_HEIGHT #960
        self.channel = 3
        self.cam_index = camindex

        # self.signal = CustomizedSignal()
        # self.reConnect_timer = QTimer(self,interval=1000)
        # self.reConnect_timer.timeout.connect(self.forceIp)
        # self.reConnect_timer.setSignalShot(True)
        # self.reConnect_count = 0


        # self.rgb_buf = self._malloc(1280*960*3)
        # self.mono_buf = self._malloc(1280*960*1)
        # self.bgr_buf = self._malloc(1280*960*3)
        self.pbyBuffer = POINTER(c_uint8)()
        self.image = None   # used for save
        self.camera_isOpen = False    #用来表示当前相机是否已经打开
        self.cam_init_state = None        

        self.cam_init_state = self.forceIp()
        # self.tryReConnectToCam()

    def api_status(self,status):
        if status == API_STATUS_OK:
            return True
        else:
            return False

    def MV_CC_FeatureLoad(self):
        if not os.path.exists(FEATURE_FILE):
            self.MV_CC_FeatureSave()
        
        string = FEATURE_FILE
        c_s = create_string_buffer(string.encode('utf-8'))
        status = self._MV_CC_FeatureLoad(self.m_handle,c_s)
        print("MV_CC_FeatureLoad   status:   ",status)
        return self.api_status(status)



    def MV_CC_FeatureSave(self):
        string = FEATURE_FILE
        c_s = create_string_buffer(string.encode('utf-8'))
        status = self._MV_CC_FeatureSave(self.m_handle,c_s)
        print("MV_CC_FeatureSave   status:   ",status)
        return self.api_status(status)

    def MV_GIGE_ForceIpEx(self):
        nIP = c_uint(0xc0a80533)
        nSubNetMask = c_uint(0xffffff00)
        nDefultGateWay = c_uint(0xc0a80501)
        status = self._MV_GIGE_ForceIpEx(self.m_handle,nIP,nSubNetMask,nDefultGateWay)
            
        print("MV_GIGE_ForceIpEx status:   ",status)
        return self.api_status(status)
        

    def MV_CC_GetDeviceInfo(self):
        struDeviceInfo = MV_CC_DEVICE_INFO()
        self._memset(byref(struDeviceInfo),0,sizeof(MV_CC_DEVICE_INFO))
        status = self._MV_CC_GetDeviceInfo(self.m_handle,byref(struDeviceInfo))
        print("info:      ",struDeviceInfo.SpecialInfo.stGigEInfo.nCurrentIp)
        return self.api_status(status)



    #枚举子网内指定的传输协议对应的所有设备
    def MV_CC_EnumDevices(self):
        nTLayerType = c_uint(1) #MV_GIGE_DEVICE  0x00000001 GigE设备 
        
        self.m_stDevList = MV_CC_DEVICE_INFO_LIST()
        status = self._MV_CC_EnumDevices(nTLayerType,byref(self.m_stDevList))
        print("MV_CC_EnumDevices status: ",status, "self.m_stDevList.nDeviceNum:", self.m_stDevList.nDeviceNum)
        return self.api_status(status)

    # #枚举子网内指定的传输协议和指定厂商的所有设备。
    def MV_CC_EnumDevicesEx(self):
        nTLayerType = c_uint(1) #MV_GIGE_DEVICE  0x00000001 GigE设备 
        
        self.m_stDevList = MV_CC_DEVICE_INFO_LIST()
        status = self._MV_CC_EnumDevicesEx(nTLayerType,byref(self.m_stDevList),b'GEV')





        print("MV_CC_EnumDevicesEx status: ",status, "self.m_stDevList.nDeviceNum:", self.m_stDevList.nDeviceNum)
        return self.api_status(status)
        

    # #选择查找到的第一台在线设备，创建设备句柄
    # def MV_CC_CreateHandle(self):
    #     self.m_handle = c_void_p(None)
    #     # m_stDevInfo  = MV_CC_DEVICE_INFO()
    #     status = 0

    #     for index in range(0,self.m_stDevList.nDeviceNum):
    #         print("index === ",index,type(index))
    #         nDeviceIndex = 0
    #         m_stDevInfo  = MV_CC_DEVICE_INFO()
    #         #有疑惑  self.m_stDevList.acDescription[nDeviceIndex]
    #         #######????????????????????????
    #         #######????????????????????????
    #         self._memcpy(byref(m_stDevInfo),self.m_stDevList.pDeviceInfo[index],sizeof(MV_CC_DEVICE_INFO))
    #         status = self._MV_CC_CreateHandle(byref(self.m_handle),byref(m_stDevInfo)) or status
    #         print("MV_CC_CreateHandle status: ",status)
    #         # return self.api_status(status)
        
    #     return self.api_status(status)


    def get_cam_info_for_display(self):

        #获取相机的width
        self.info.width = self.MV_CC_GetIntValueEx("Width")
        self.info.height = self.MV_CC_GetIntValueEx("Height")
        self.info.x_offset = self.MV_CC_GetIntValueEx("OffsetX")
        self.info.y_offset = self.MV_CC_GetIntValueEx("OffsetY")
        self.info.exposure_time = self.CameraGetExposureTime()

        return self.info

        
    #选择查找到的第一台在线设备，创建设备句柄
    def MV_CC_CreateHandle(self):
        self.m_handle = c_void_p(None)
        status = 0

        if self.cam_index >= self.m_stDevList.nDeviceNum:
            return False

        nDeviceIndex = 0
        m_stDevInfo  = MV_CC_DEVICE_INFO()
        self._memcpy(byref(m_stDevInfo),self.m_stDevList.pDeviceInfo[self.cam_index],sizeof(MV_CC_DEVICE_INFO))
        status = self._MV_CC_CreateHandle(byref(self.m_handle),byref(m_stDevInfo)) or status
        print("MV_CC_CreateHandle status: ",status)

 

        return self.api_status(status)


     #获取相机的曝光时间
    def CameraGetExposureTime(self):
        if self.m_handle == None:
            return
        string = 'ExposureTime'
        exposure = self.MV_CC_GetFloatValue(string).fCurValue
        print("exposure time ===== ",exposure)
        return exposure
    #设置相机的曝光时间
    def CameraSetExposureTime(self,val):
        if self.m_handle == None:
            return

        print("get in set exposure time    val ==== ",val)
        exposure = self.CameraGetExposureTime()
        if val == int(exposure):
            return
        string = 'ExposureTime'
        status = self.MV_CC_SetFloatValue(string,val)
        self.info.exposure_time = val


        # #重新生成ini文件
        # # os.remove(FEATURE_FILE)
        # self.MV_CC_FeatureSave()
        # self.get_cam_info_for_display()

        return status

    #设置相机的x偏移
    def CameraSetOffsetX(self,val):
        print("new offset x =====  ",val)
        if val == self.info.x_offset:
            return
        string = "OffsetX"
        status = self.MV_CC_SetIntValue(string,val)



        return self.api_status(status)

    #


    #连接设备
    def MV_CC_OpenDevice(self):
        nAccessMode = 1#c_uint(1)
        nSwitchoverKey = 0#c_ushort(0)
        status = self._MV_CC_OpenDevice(self.m_handle,nAccessMode,nSwitchoverKey)
        print("MV_CC_OpenDevice status: ",status)
        

        return self.api_status(status)

    #关闭设备，释放资源
    def MV_CC_CloseDevice(self):
        status = self._MV_CC_CloseDevice(self.m_handle)
        print("MV_CC_CloseDevice status: ",status)

    #销毁句柄，释放资源
    def MV_CC_DestroyHandle(self):
        status = self._MV_CC_DestroyHandle(self.m_handle)
        print("MV_CC_DestroyHandle status: ",status)

    


    #获取相机int型节点值（支持64位）
    def MV_CC_GetIntValue(self,string):
        if self.m_handle == None:
            return
        c_s = create_string_buffer(string.encode('utf-8'))
        stIntvalue  = MVCC_INTVALUE()
        status = self._MV_CC_GetIntValue(self.m_handle,c_s,byref(stIntvalue))
        print("MV_CC_GetIntValue status: ",status,"   value:  ",stIntvalue.nCurValue)
        return stIntvalue


    def MV_CC_GetIntValueEx(self,string):
        stIntvalue  = MVCC_INTVALUE_EX()
        c_s = create_string_buffer(string.encode('utf-8'))
        status = self._MV_CC_GetIntValueEx(self.m_handle,c_s,byref(stIntvalue))
        print("MV_CC_GetIntValue status: ",status,"      val ======= ",stIntvalue.nCurValue)
        return stIntvalue.nCurValue

        


    #获取相机Enum型节点值
    def MV_CC_GetEnumValue(self,string):
        struEnumValue = MVCC_ENUMVALUE 
        status = self._MV_CC_GetEnumValue(self.m_handle,string,byref(struEnumValue))
        print("MV_CC_GetEnumValue status: ",status)
        return struEnumValue


    #获取相机float型节点值
    def MV_CC_GetFloatValue(self,string):
        if self.m_handle == None:
            return
        stFloatvalue  = MVCC_FLOATVALUE()
        c_s = create_string_buffer(string.encode('utf-8'))
        status = self._MV_CC_GetFloatValue(self.m_handle,c_s,byref(stFloatvalue))
        print("MV_CC_GetFloatValue status: ",status,"    value:        ",stFloatvalue.fCurValue)
        return stFloatvalue

    #获取相机bool型节点值
    def MV_CC_GetBoolValue(self,string):
        stIntvalue  = bool
        status = self._MV_CC_GetIntValue(self.m_handle,string,byref(stIntvalue))
        print("MV_CC_GetFloatValue status: ",status)
        return stIntvalue

    #获取相机string型节点值
    def MV_CC_GetStringValue(self,string):
        if self.m_handle == None:
            return
        c_s = create_string_buffer(string.encode('utf-8'))
        struStringValue = MVCC_STRINGVALUE() 
        status = self._MV_CC_GetStringValue(self.m_handle,c_s,byref(struStringValue))
        print("MV_CC_GetStringValue status: ",status,"    device id:   ",struStringValue.chCurValue)
        return struStringValue


    def MV_CC_SetIntValue(self,string,val):
        c_s = create_string_buffer(string.encode('utf-8'))
        status = self._MV_CC_SetIntValue(self.m_handle,c_s,val)
        print("MV_CC_SetIntValue status: ",status)
        return self.api_status(status)


    #设置相机int型节点值（支持64位）
    def MV_CC_SetIntValueEx(self,string,val):
        if self.m_handle == None:
            return
        
        c_s = create_string_buffer(string.encode('utf-8'))
        status = self._MV_CC_SetIntValueEx(self.m_handle,c_s , val)
        print("MV_CC_SetIntValueEx status: ",status)
        return self.api_status(status)
        

    #设置相机Enum型节点值
    def MV_CC_SetEnumValue(self,string,val):
        status = self._MV_CC_SetEnumValue(self.m_handle,string,val)
        print("MV_CC_SetEnumValue status: ",status)

    #设置相机Enum型节点值
    def MV_CC_SetEnumValueByString(self,string,val):
        status = self._MV_CC_SetEnumValueByString(self.m_handle,string,val)
        print("MV_CC_SetEnumValueByString status: ",status)

    #设置相机float型节点值
    def MV_CC_SetFloatValue(self,string,val):
        if self.m_handle == None:
            return
        c_s = create_string_buffer(string.encode('utf-8'))
        status = self._MV_CC_SetFloatValue(self.m_handle,c_s,val)
        print("MV_CC_SetFloatValue status: ",status)

    #设置相机bool型节点值
    def MV_CC_SetBoolValue(self,string,val):
        status = self._MV_CC_SetBoolValue(self.m_handle,string,val)
        print("MV_CC_SetBoolValue status: ",status)

    #设置相机string型节点值
    def MV_CC_SetStringValue(self,string,val):
        status = self._MV_CC_SetStringValue(self.m_handle,string,val)
        print("MV_CC_SetStringValue status: ",status)

    #设置相机Command型节点
    def MV_CC_SetCommandValue(self,string,val):
        status = self._MV_CC_SetCommandValue(self.m_handle,string,val)
        print("MV_CC_SetCommandValue status: ",status)


    #开始采集图像
    def MV_CC_StartGrabbing(self):
        status = self._MV_CC_StartGrabbing(self.m_handle)
        # print("MV_CC_StartGrabbing status: ",status)
        return self.api_status(status)


    # def MV_CC_GetImageBuffer(self):
    #     stOutFrame = MV_FRAME_OUT()
    #     status = self._MV_CC_GetImageBuffer(self.m_handle,byref(stOutFrame),1000)

        




    #获取一帧图片，支持获取chunk信息喝设置超时时间
    #def MV_CC_GetOneFrameTimeout(self,pFrameBuf,nBufSize,stInfo,nMsec):
    def MV_CC_GetOneFrameTimeout(self):
        stInfo = MV_FRAME_OUT_INFO_EX()
        # nbsize = c_uint(3*1280*960)
        nbsize = self.image_width*self.image_height*self.channel
        status = self._MV_CC_GetOneFrameTimeout(self.m_handle, self.rgb_buf, nbsize, byref(stInfo), 1000)    
        # status = self._MV_CC_GetOneFrameTimeout(self.m_handle, self.mono_buf, nbsize, byref(stInfo), 1000)    
        # status = self._MV_CC_GetOneFrameTimeout(self.m_handle,pFrameBuf,nBufSize,byref(stInfo),nMsec)
        #print("MV_CC_GetOneFrameTimeout status: ",status)
        # image = np.ctypeslib.as_array(self.rgb_buf, (3,960,1280))#mindvision
        image = np.ctypeslib.as_array(self.rgb_buf, (960,1280,3))#LBAS

        return image

    def MV_CC_GetImageForRGB(self):
        stInfo = MV_FRAME_OUT_INFO_EX()
        # nbsize = 3*1280*960
        nbsize =self.image_width*self.image_height*self.channel
        status = self._MV_CC_GetImageForRGB(self.m_handle, self.rgb_buf, nbsize, byref(stInfo), 1000)    
        image = np.ctypeslib.as_array(self.rgb_buf, (self.image_height,self.image_width,self.channel ))   # shape differ with MINDVISION(3,1024,1280)
        # print(image.shape)
        # nbsize = 3*960*960
        # status = self._MV_CC_GetImageForRGB(self.m_handle, self.rgb_buf, nbsize, byref(stInfo), 1000)    
        # image = np.ctypeslib.as_array(self.rgb_buf, (960,960,3))   # shape differ with MINDVISION(3,1024,1280)

        self.image = image
        return image

    def MV_CC_GetImageForBGR(self):
        stInfo = MV_FRAME_OUT_INFO_EX()
        # nbsize = 3*1280*960
        nbsize = self.image_width*self.image_height*self.channel
        status = self._MV_CC_GetImageForBGR(self.m_handle, self.rgb_buf, nbsize, byref(stInfo), 1000)    
        image = np.ctypeslib.as_array(self.rgb_buf, (self.image_height,self.image_width,self.channel ))   # shape differ with MINDVISION(3,1024,1280)
        return image

    def MV_CC_StopGrabbing(self):
        status = self._MV_CC_StopGrabbing(self.m_handle)
        # print("MV_CC_StopGrabbing status: ",status)
        
    def MV_CC_SetPixelFormat(self,val):
        print("val ==== ",val)

        if val == 0:
            status = self._MV_CC_SetPixelFormat(self.m_handle,MvGvspPixelType.PixelType_Gvsp_Mono8)
        else:
            status = self._MV_CC_SetPixelFormat(self.m_handle,MvGvspPixelType.PixelType_Gvsp_RGB8_Packed)
        print("MV_CC_SetPixelFormat status: ",status)
        return self.api_status(status)


    def MV_CC_GetPixelFormat(self):
        enumVal = MVCC_ENUMVALUE()
        status = self._MV_CC_GetPixelFormat(self.m_handle,byref(enumVal))
        print("ddddd ==== ",status,enumVal.nSupportValue[8],enumVal.nSupportValue[7],enumVal.nSupportValue[6],enumVal.nSupportValue[9])
        return self.api_status(status)

    # def tryReConnectToCam(self):
    #     self.reConnect_timer.start()

    def cam_init(self):
        print("get in cam init..")
        

        if not self.MV_CC_EnumDevicesEx():    # 枚举设备成功
            return False
        if self.m_stDevList.nDeviceNum == 0:    # 设备数量
            # self.tryReConnectToCam()
            return False
        if not self.MV_CC_CreateHandle():   #创建句柄成功
            return False
        if not self.MV_CC_OpenDevice(): # 打开设备成功
            return False

        # self.reConnect_timer.stop()
        # self.MV_CC_FeatureLoad()

        return True

    def open(self):
        # print("get in open..")
        # if not self.MV_CC_EnumDevicesEx():    # 枚举设备成功
        #     return False
        # if self.m_stDevList.nDeviceNum == 0:    # 设备数量
        #     return False
        # if not self.MV_CC_CreateHandle():   #创建句柄成功
        #     return False
        # if not self.MV_CC_OpenDevice(): # 打开设备成功
        #     return False


        # self.getCamDeviceID()
        #设置图像通道选项  黑白色和彩色
        # self.MV_CC_SetPixelFormat(MvGvspPixelType.PixelType_Gvsp_Mono8)

        if not self.cam_init_state:
            self.cam_init()

        
        if not self.MV_CC_StartGrabbing():  # 抓流成功
            return False

        self.camera_isOpen = True
    
        return True

    def getCamIpStr(self):
        print("self.cam_init_state ============== ",self.cam_init_state)
        if not self.cam_init_state:
            return ""

        stIntvalue  = MVCC_INTVALUE()
        stIntvalue = self.MV_CC_GetIntValue("GevCurrentIPAddress")
        x = bin(stIntvalue.nCurValue)
        ipstr = ""
        for i in range(2,34,8):
            temp = x[i:i+8]
            ans = int(temp,2)
            ipstr = ipstr+str(ans)+"."
        ipstr = ipstr[0:len(ipstr)-1]
        return ipstr    

    def getCamDeviceID(self):
        if not self.cam_init_state:
            return ""
        struStringValue = MVCC_STRINGVALUE()
        struStringValue=self.MV_CC_GetStringValue("DeviceID")
        # print(struStringValue.chCurValue)
        # print(type(struStringValue.chCurValue))
        return str(struStringValue.chCurValue,encoding = "utf-8")

        

    def close(self):
        print("get in close..")
        self.camera_isOpen = False
        self.MV_CC_StopGrabbing()
        self.MV_CC_CloseDevice()
        self.MV_CC_DestroyHandle()
        self.cam_init_state = False

     # 开启抓流
    def start_grab(self):
        # print("start grab...")
        return self.MV_CC_StartGrabbing()

    # 关闭抓流
    def stop_grab(self):
        # print("stop grab...")
        return self.MV_CC_StopGrabbing()

    def save(self,fname,img):
        image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(fname, image)
        # print("get in save,fname === ",fname)

    def pop_frame(self):
        # self.start_grab()
        image = self.MV_CC_GetImageForRGB()
        # image = self.MV_CC_GetImageForBGR()
        # self.stop_grab()
        return image

    

    def set_image_channelOption(self,val):
        print("self.camera_isOpen ==== ",self.camera_isOpen)
        if self.camera_isOpen:
            self.MV_CC_StopGrabbing()
        status = self.MV_CC_SetPixelFormat(val)
        self.MV_CC_StartGrabbing()
        return status



    def forceIp(self):
        # self.reConnect_count += 1
        print("get in cam init..")
        if not self.MV_CC_EnumDevicesEx():    # 枚举设备成功
            return False
        if self.m_stDevList.nDeviceNum == 0:    # 设备数量
            return False
        if not self.MV_CC_CreateHandle():   #创建句柄成功
            return False
        if not self.MV_GIGE_ForceIpEx():
            return False
        if not self.MV_CC_CreateHandle():   #创建句柄成功
            return False

        self.cam_init_state = True
        self.cam_init()
        
        return True

