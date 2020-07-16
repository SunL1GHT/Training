from ctypes import *
import numpy as np
import cv2

API_STATUS_OK = 0


class GX_STATUS_LIST:
    GX_STATUS_SUCCESS                   =  0    # Success
    GX_STATUS_ERROR                     = -1      #There is an unspecified internal error that is not expected to occur
    GX_STATUS_NOT_FOUND_TL              = -2      #The TL library cannot be found
    GX_STATUS_NOT_FOUND_DEVICE          = -3      #The device is not found
    GX_STATUS_OFFLINE                   = -4      #The current device is in an offline status
    GX_STATUS_INVALID_PARAMETER         = -5      #Invalid parameter. Generally, the pointer is NULL or the input IP and other parameter formats are invalid
    GX_STATUS_INVALID_HANDLE            = -6      #Invalid handle
    GX_STATUS_INVALID_CALL              = -7      #The interface is invalid, which refers to software interface logic error
    GX_STATUS_INVALID_ACCESS            = -8      #The function is currently inaccessible or the device access mode is incorrect
    GX_STATUS_NEED_MORE_BUFFER          = -9      #The user request buffer is insufficient: the user input buffer size during the read operation is less than the actual need
    GX_STATUS_ERROR_TYPE                = -10      # The type of FeatureID used by the user is incorrect, such as an integer interface using a floating-point function code
    GX_STATUS_OUT_OF_RANGE              = -11      # The value written by the user is crossed
    GX_STATUS_NOT_IMPLEMENTED           = -12      # This function is not currently supported
    GX_STATUS_NOT_INIT_API              = -13      # There is no call to initialize the interface
    GX_STATUS_TIMEOUT                   = -14      # Timeout error

class GX_OPEN_MODE:
    GX_OPEN_SN=0
    GX_OPEN_IP=1
    GX_OPEN_MAC=2
    GX_OPEN_INDEX=3
    GX_OPEN_USERID=4

class GX_ACCESS_MODE:
    GX_ACCESS_READONLY=2
    GX_ACCESS_CONTROL=3
    GX_ACCESS_EXCLUSIVE=4



#------------------------------------------------------------------------------
#  Feature Type Definition
#------------------------------------------------------------------------------
class GX_FEATURE_TYPE:
    GX_FEATURE_INT                      = 0x10000000      #Integer type
    GX_FEATURE_FLOAT                    = 0X20000000      #Floating point type
    GX_FEATURE_ENUM                     = 0x30000000      #Enum type
    GX_FEATURE_BOOL                     = 0x40000000      #Boolean type
    GX_FEATURE_STRING                   = 0x50000000      #String type
    GX_FEATURE_BUFFER                   = 0x60000000      #Block data type
    GX_FEATURE_COMMAND                  = 0x70000000      #Command type

#------------------------------------------------------------------------------
# Feature Level Definition
#------------------------------------------------------------------------------
class GX_FEATURE_LEVEL:
    GX_FEATURE_LEVEL_REMOTE_DEV         = 0x00000000      #Remote device layer
    GX_FEATURE_LEVEL_TL                 = 0x01000000      #TL layer
    GX_FEATURE_LEVEL_IF                 = 0x02000000      #Interface layer    
    GX_FEATURE_LEVEL_DEV                = 0x03000000      #Device layer
    GX_FEATURE_LEVEL_DS                 = 0x04000000      #DataStream layer

class GX_FEATURE_ID:
        #---------DeviceInfomation Section--------------------------
    GX_STRING_DEVICE_VENDOR_NAME               = 0   | GX_FEATURE_TYPE.GX_FEATURE_STRING | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Name of the manufacturer of the device.
    GX_STRING_DEVICE_MODEL_NAME                = 1   | GX_FEATURE_TYPE.GX_FEATURE_STRING | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Model of the device.
    GX_STRING_DEVICE_FIRMWARE_VERSION          = 2   | GX_FEATURE_TYPE.GX_FEATURE_STRING | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Version of the firmware in the device.
    GX_STRING_DEVICE_VERSION                   = 3   | GX_FEATURE_TYPE.GX_FEATURE_STRING | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Version of the device.
    GX_STRING_DEVICE_SERIAL_NUMBER             = 4   | GX_FEATURE_TYPE.GX_FEATURE_STRING | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Device serial number.
    GX_STRING_FACTORY_SETTING_VERSION          = 6   | GX_FEATURE_TYPE.GX_FEATURE_STRING | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Factory parameter version
    GX_STRING_DEVICE_USERID                    = 7   | GX_FEATURE_TYPE.GX_FEATURE_STRING | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #User-programmable device identifier.
    GX_INT_DEVICE_LINK_SELECTOR                = 8   | GX_FEATURE_TYPE.GX_FEATURE_INT    | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects which Link of the device to control.
    GX_ENUM_DEVICE_LINK_THROUGHPUT_LIMIT_MODE  = 9   | GX_FEATURE_TYPE.GX_FEATURE_ENUM   | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Controls if the DeviceLinkThroughputLimit is active.
    GX_INT_DEVICE_LINK_THROUGHPUT_LIMIT        = 10  | GX_FEATURE_TYPE.GX_FEATURE_INT    | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Limits the maximum bandwidth of the data that will be streamed out by the device on the selected Link.
    GX_INT_DEVICE_LINK_CURRENT_THROUGHPUT      = 11  | GX_FEATURE_TYPE.GX_FEATURE_INT    | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #The bandwidth of current device acquisition
    GX_COMMAND_DEVICE_RESET                    = 12  | GX_FEATURE_TYPE.GX_FEATURE_COMMAND| GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #reset device
    GX_INT_TIMESTAMP_TICK_FREQUENCY            = 13  | GX_FEATURE_TYPE.GX_FEATURE_INT    | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Time stamp clock frequency
    GX_COMMAND_TIMESTAMP_LATCH                 = 14  | GX_FEATURE_TYPE.GX_FEATURE_COMMAND| GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Timestamp latch 
    GX_COMMAND_TIMESTAMP_RESET                 = 15  | GX_FEATURE_TYPE.GX_FEATURE_COMMAND| GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #reset Timestamp
    GX_COMMAND_TIMESTAMP_LATCH_RESET           = 16  | GX_FEATURE_TYPE.GX_FEATURE_COMMAND| GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #reset Timestamp latch
    GX_INT_TIMESTAMP_LATCH_VALUE               = 17  | GX_FEATURE_TYPE.GX_FEATURE_INT    | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Timestamp Latch value


        #---------ImageFormat Section--------------------------------
    GX_INT_SENSOR_WIDTH               = 1000 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Effective width of the sensor in pixels.
    GX_INT_SENSOR_HEIGHT              = 1001 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Effective height of the sensor in pixels.
    GX_INT_WIDTH_MAX                  = 1002 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Maximum width of the image (in pixels).
    GX_INT_HEIGHT_MAX                 = 1003 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Maximum height of the image (in pixels).
    GX_INT_OFFSET_X                   = 1004 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Horizontal offset from the origin to the region of interest (in pixels).
    GX_INT_OFFSET_Y                   = 1005 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Vertical offset from the origin to the region of interest (in pixels).
    GX_INT_WIDTH                      = 1006 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Width of the image provided by the device (in pixels).
    GX_INT_HEIGHT                     = 1007 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Height of the image provided by the device (in pixels).
    GX_INT_BINNING_HORIZONTAL         = 1008 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Number of horizontal photo-sensitive cells to combine together.
    GX_INT_BINNING_VERTICAL           = 1009 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Number of vertical photo-sensitive cells to combine together.
    GX_INT_DECIMATION_HORIZONTAL      = 1010 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Horizontal sub-sampling of the image.
    GX_INT_DECIMATION_VERTICAL        = 1011 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Vertical sub-sampling of the image.
    GX_ENUM_PIXEL_SIZE                = 1012 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Total size in bits of a pixel of the image.
    GX_ENUM_PIXEL_COLOR_FILTER        = 1013 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Type of color filter that is applied to the image.
    GX_ENUM_PIXEL_FORMAT              = 1014 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Format of the pixels provided by the device.
    GX_BOOL_REVERSE_X                 = 1015 | GX_FEATURE_TYPE.GX_FEATURE_BOOL | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Flip horizontally the image sent by the device.
    GX_BOOL_REVERSE_Y                 = 1016 | GX_FEATURE_TYPE.GX_FEATURE_BOOL | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Flip vertically the image sent by the device.
    GX_ENUM_TEST_PATTERN              = 1017 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects the type of test pattern that is generated by the device as image source.
    GX_ENUM_TEST_PATTERN_GENERATOR_SELECTOR = 1018 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects which test pattern generator is controlled by the TestPattern feature.
    GX_ENUM_REGION_SEND_MODE          = 1019 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #ROI output mode, see also GX_REGION_SEND_MODE_ENTRY
    GX_ENUM_REGION_MODE               = 1020 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #zone switch, see also GX_REGION_MODE_ENTRY
    GX_ENUM_RREGION_SELECTOR          = 1021 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects the Region of interest to control.
    GX_INT_CENTER_WIDTH               = 1022 |GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #width of window
    GX_INT_CENTER_HEIGHT              = 1023 |GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #height of window
    GX_ENUM_BINNING_HORIZONTAL_MODE   = 1024 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Binning Horizontal mode, see also GX_BINNING_HORIZONTAL_MODE_ENTRY
    GX_ENUM_BINNING_VERTICAL_MODE     = 1025 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Binning vertical mode, see also GX_BINNING_VERTICAL_MODE_ENTRY

        #---------TransportLayer Section-------------------------------
    GX_INT_PAYLOAD_SIZE                              = 2000 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Provides the number of bytes transferred for each image or chunk on the stream channel. 
    GX_BOOL_GEV_CURRENT_IPCONFIGURATION_LLA          = 2001 | GX_FEATURE_TYPE.GX_FEATURE_BOOL | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Controls whether the Link Local Address IP configuration scheme is activated on the given logical link.
    GX_BOOL_GEV_CURRENT_IPCONFIGURATION_DHCP         = 2002 | GX_FEATURE_TYPE.GX_FEATURE_BOOL | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Controls whether the DHCP IP configuration scheme is activated on the given logical link.
    GX_BOOL_GEV_CURRENT_IPCONFIGURATION_PERSISTENTIP = 2003 | GX_FEATURE_TYPE.GX_FEATURE_BOOL | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Controls whether the PersistentIP configuration scheme is activated on the given logical link.
    GX_INT_ESTIMATED_BANDWIDTH                       = 2004 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # EstimatedBandwidth, Unit: Bps(Bytes per second)
    GX_INT_GEV_HEARTBEAT_TIMEOUT                     = 2005 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Controls the current heartbeat timeout in milliseconds.
    GX_INT_GEV_PACKETSIZE                            = 2006 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Specifies the stream packet size, in bytes, to send on the selected channel for a GVSP transmitter or specifies the maximum packet size supported by a GVSP receiver.
    GX_INT_GEV_PACKETDELAY                           = 2007 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Controls the delay (in timestamp counter unit) to insert between each packet for this stream channel.
    GX_INT_GEV_LINK_SPEED                            = 2008 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # It indicates the connection speed in Mbps for the selected network interface.

        #---------AcquisitionTrigger Section---------------------------
    GX_ENUM_ACQUISITION_MODE          = 3000 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Sets the acquisition mode of the device.
    GX_COMMAND_ACQUISITION_START      = 3001 | GX_FEATURE_TYPE.GX_FEATURE_COMMAND | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Starts the Acquisition of the device.
    GX_COMMAND_ACQUISITION_STOP       = 3002 | GX_FEATURE_TYPE.GX_FEATURE_COMMAND | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Stops the Acquisition of the device at the end of the current Frame.
    GX_INT_ACQUISITION_SPEED_LEVEL    = 3003 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Setting the speed level of acquiring image.
    GX_INT_ACQUISITION_FRAME_COUNT    = 3004 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Number of frames to acquire in MultiFrame Acquisition mode.
    GX_ENUM_TRIGGER_MODE              = 3005 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Controls if the selected trigger is active.
    GX_COMMAND_TRIGGER_SOFTWARE       = 3006 | GX_FEATURE_TYPE.GX_FEATURE_COMMAND | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Generates an internal trigger.
    GX_ENUM_TRIGGER_ACTIVATION        = 3007 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Specifies the activation mode of the trigger.
    GX_ENUM_TRIGGER_SWITCH            = 3008 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Control external trigger signal is valid, see also GX_TRIGGER_SWITCH_ENTRY
    GX_FLOAT_EXPOSURE_TIME            = 3009 | GX_FEATURE_TYPE.GX_FEATURE_FLOAT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Sets the Exposure time when ExposureMode is Timed and ExposureAuto is Off.
    GX_ENUM_EXPOSURE_AUTO             = 3010 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Sets the automatic exposure mode when ExposureMode is Timed.
    GX_FLOAT_TRIGGER_FILTER_RAISING   = 3011 | GX_FEATURE_TYPE.GX_FEATURE_FLOAT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Raising edge signal pulse width is smaller than this value is invalid.
    GX_FLOAT_TRIGGER_FILTER_FALLING   = 3012 | GX_FEATURE_TYPE.GX_FEATURE_FLOAT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Falling edge signal pulse width is smaller than this value is invalid.
    GX_ENUM_TRIGGER_SOURCE            = 3013 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Specifies the internal signal or physical input Line to use as the trigger source.
    GX_ENUM_EXPOSURE_MODE             = 3014 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Sets the operation mode of the Exposure (or shutter).
    GX_ENUM_TRIGGER_SELECTOR          = 3015 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects the type of trigger to configure.
    GX_FLOAT_TRIGGER_DELAY            = 3016 | GX_FEATURE_TYPE.GX_FEATURE_FLOAT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Specifies the delay in microseconds (us) to apply after the trigger reception before activating it.
    GX_ENUM_TRANSFER_CONTROL_MODE     = 3017 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects the control method for the transfers.
    GX_ENUM_TRANSFER_OPERATION_MODE   = 3018 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects the operation mode of the transfer.
    GX_COMMAND_TRANSFER_START         = 3019 | GX_FEATURE_TYPE.GX_FEATURE_COMMAND | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Starts the streaming of data blocks out of the device.
    GX_INT_TRANSFER_BLOCK_COUNT       = 3020 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #frame number of transmission. when set GX_ENUM_TRANSFER_OPERATION_MODE as GX_ENUM_TRANSFER_OPERATION_MODE_MULTIBLOCK, this function is actived
    GX_BOOL_FRAMESTORE_COVER_ACTIVE   = 3021 | GX_FEATURE_TYPE.GX_FEATURE_BOOL | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #FrameBufferOverwriteActive
    GX_ENUM_ACQUISITION_FRAME_RATE_MODE      = 3022 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Controls if the acquisitionFrameRate is active, see also GX_ACQUISITION_FRAME_RATE_MODE_ENTRY
    GX_FLOAT_ACQUISITION_FRAME_RATE          = 3023 | GX_FEATURE_TYPE.GX_FEATURE_FLOAT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Controls the acquisition rate (in Hertz) at which the frames are captured.
    GX_FLOAT_CURRENT_ACQUISITION_FRAME_RATE  = 3024 | GX_FEATURE_TYPE.GX_FEATURE_FLOAT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Indicates the maximum allowed frame acquisition rate.
    GX_ENUM_FIXED_PATTERN_NOISE_CORRECT_MODE = 3025 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Controls if the FixedPatternNoise is active, see also GX_FIXED_PATTERN_NOISE_CORRECT_MODE  
    GX_INT_ACQUISITION_BURST_FRAME_COUNT     = 3030 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #frame number of transmission.
    GX_ENUM_ACQUISITION_STATUS_SELECTOR      = 3031 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Acquisition status selection, see also GX_ACQUISITION_STATUS_SELECTOR_ENTRY
    GX_BOOL_ACQUISITION_STATUS               = 3032 | GX_FEATURE_TYPE.GX_FEATURE_BOOL | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Acquisition status
    GX_FLOAT_EXPOSURE_DELAY                  = 30300| GX_FEATURE_TYPE.GX_FEATURE_FLOAT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Delay of exposure

        #----------DigitalIO Section----------------------------------
    GX_ENUM_USER_OUTPUT_SELECTOR      = 4000 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects which bit of the User Output register will be set by UserOutputValue.
    GX_BOOL_USER_OUTPUT_VALUE         = 4001 | GX_FEATURE_TYPE.GX_FEATURE_BOOL | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Sets the value of the bit selected by UserOutputSelector.
    GX_ENUM_USER_OUTPUT_MODE          = 4002 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Output signal can be used for different purposes, flash or a user-defined constant level, see also GX_USER_OUTPUT_MODE_ENTRY
    GX_ENUM_STROBE_SWITCH             = 4003 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Set the flash light switch, see also GX_STROBE_SWITCH_ENTRY
    GX_ENUM_LINE_SELECTOR             = 4004 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects the physical line (or pin) of the external device connector to configure.
    GX_ENUM_LINE_MODE                 = 4005 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Controls if the physical Line is used to Input or Output a signal.
    GX_BOOL_LINE_INVERTER             = 4006 | GX_FEATURE_TYPE.GX_FEATURE_BOOL | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Controls the inversion of the signal of the selected input or output Line.
    GX_ENUM_LINE_SOURCE               = 4007 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects which internal acquisition or I/O source signal to output on the selected Line.
    GX_BOOL_LINE_STATUS               = 4008 | GX_FEATURE_TYPE.GX_FEATURE_BOOL | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Returns the current status of the selected input or output Line.
    GX_INT_LINE_STATUS_ALL            = 4009 | GX_FEATURE_TYPE.GX_FEATURE_INT  | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Returns the current status of all available Line signals at time of polling in a single bit field.
    GX_FLOAT_PULSE_WIDTH              = 4010 | GX_FEATURE_TYPE.GX_FEATURE_FLOAT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV,

        #----------AnalogControls Section----------------------------
    GX_ENUM_GAIN_AUTO                 = 5000 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Sets the automatic gain control (AGC) mode.
    GX_ENUM_GAIN_SELECTOR             = 5001 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects which Gain is controlled by the various Gain features.
    GX_ENUM_BLACKLEVEL_AUTO           = 5003 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Controls the mode for automatic black level adjustment.
    GX_ENUM_BLACKLEVEL_SELECTOR       = 5004 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects which Black Level is controlled by the various Black Level features.
    GX_ENUM_BALANCE_WHITE_AUTO        = 5006 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Controls the mode for automatic white balancing between the color channels.
    GX_ENUM_BALANCE_RATIO_SELECTOR    = 5007 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects which Balance ratio to control.
    GX_FLOAT_BALANCE_RATIO            = 5008 | GX_FEATURE_TYPE.GX_FEATURE_FLOAT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Controls ratio of the selected color component to a reference color component.
    GX_ENUM_COLOR_CORRECT             = 5009 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Color correction, see also GX_COLOR_CORRECT_ENTRY
    GX_ENUM_DEAD_PIXEL_CORRECT        = 5010 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #The dead pixel correct function can eliminate dead pixels in the image, see also GX_DEAD_PIXEL_CORRECT_ENTRY
    GX_FLOAT_GAIN                     = 5011 | GX_FEATURE_TYPE.GX_FEATURE_FLOAT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # The value is an float value that sets the selected gain control in units specific to the camera.
    GX_FLOAT_BLACKLEVEL               = 5012 | GX_FEATURE_TYPE.GX_FEATURE_FLOAT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Controls the analog black level as an absolute physical value.
    GX_BOOL_GAMMA_ENABLE              = 5013 | GX_FEATURE_TYPE.GX_FEATURE_BOOL | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Enable bit of Gamma
    GX_ENUM_GAMMA_MODE                = 5014 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Gamma select, see also GX_GAMMA_MODE_ENTRY
    GX_FLOAT_GAMMA                    = 5015 | GX_FEATURE_TYPE.GX_FEATURE_FLOAT| GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Gamma
    GX_INT_DIGITAL_SHIFT              = 5016 | GX_FEATURE_TYPE.GX_FEATURE_INT  | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #bit select

        #---------CustomFeature Section-------------------------
    GX_INT_ADC_LEVEL                  = 6000 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #When the pixel size is not 8bits, this function can be used to choose 8bits form 10bits or 12bit for show image.
    GX_INT_H_BLANKING                 = 6001 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Horizontal blanking
    GX_INT_V_BLANKING                 = 6002 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Vertical blanking
    GX_STRING_USER_PASSWORD           = 6003 | GX_FEATURE_TYPE.GX_FEATURE_STRING | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # user password
    GX_STRING_VERIFY_PASSWORD         = 6004 | GX_FEATURE_TYPE.GX_FEATURE_STRING | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # verify password
    GX_BUFFER_USER_DATA               = 6005 | GX_FEATURE_TYPE.GX_FEATURE_BUFFER | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # user data
    GX_INT_GRAY_VALUE                 = 6006 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #ExpectedGrayValue_InqIsImplemented
    GX_ENUM_AA_LIGHT_ENVIRONMENT      = 6007 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Automatic function according to the external light conditions better for accommodation, see also GX_AA_LIGHT_ENVIRMENT_ENTRY
    GX_INT_AAROI_OFFSETX              = 6008 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #This value sets the X offset (left offset) for the rect of interest in pixels for 2A, i.e., the distance in pixels between the left side of the image area and the left side of the AAROI.
    GX_INT_AAROI_OFFSETY              = 6009 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #This value sets the Y offset (top offset) for the rect of interest for 2A, i.e., the distance in pixels between the top of the image area and the top of the AAROI.
    GX_INT_AAROI_WIDTH                = 6010 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #This value sets the width of the rect of interest in pixels for 2A.
    GX_INT_AAROI_HEIGHT               = 6011 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #This value sets the height of the rect of interest in pixels for 2A.
    GX_FLOAT_AUTO_GAIN_MIN            = 6012 | GX_FEATURE_TYPE.GX_FEATURE_FLOAT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Setting up automatic gain range of minimum. When the gain is set to auto mode, this function works.
    GX_FLOAT_AUTO_GAIN_MAX            = 6013 | GX_FEATURE_TYPE.GX_FEATURE_FLOAT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Setting up automatic gain range of maximum. When the gain is set to auto mode, this function works.
    GX_FLOAT_AUTO_EXPOSURE_TIME_MIN   = 6014 | GX_FEATURE_TYPE.GX_FEATURE_FLOAT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Setting up automatic shutter range of minimum. When the shutter is set to auto mode, this function works.
    GX_FLOAT_AUTO_EXPOSURE_TIME_MAX   = 6015 | GX_FEATURE_TYPE.GX_FEATURE_FLOAT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Setting up automatic shutter range of maximum. When the shutter is set to auto mode, this function works.
    GX_BUFFER_FRAME_INFORMATION       = 6016 | GX_FEATURE_TYPE.GX_FEATURE_BUFFER | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # FrameInformation
    GX_INT_CONTRAST_PARAM             = 6017 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Contrast parameter
    GX_FLOAT_GAMMA_PARAM              = 6018 | GX_FEATURE_TYPE.GX_FEATURE_FLOAT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Gamma parameter
    GX_INT_COLOR_CORRECTION_PARAM     = 6019 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Color correction coefficient
    GX_ENUM_IMAGE_GRAY_RAISE_SWITCH   = 6020 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Control ImageGrayRaise is valid, see also GX_IMAGE_GRAY_RAISE_SWITCH_ENTRY
    GX_ENUM_AWB_LAMP_HOUSE            = 6021 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Refers to the AWB working environment, see also GX_AWB_LAMP_HOUSE_ENTRY
    GX_INT_AWBROI_OFFSETX             = 6022 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #This value sets the X offset (left offset) for the rect of interest in pixels for Auto WhiteBalance
    GX_INT_AWBROI_OFFSETY             = 6023 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #This value sets the Y offset (top offset) for the rect of interest for Auto WhiteBalance
    GX_INT_AWBROI_WIDTH               = 6024 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #This value sets the width of the rect of interest in pixels for Auto WhiteBalance
    GX_INT_AWBROI_HEIGHT              = 6025 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #This value sets the height of the rect of interest in pixels for Auto WhiteBalance
    GX_ENUM_SHARPNESS_MODE            = 6026 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Sharpening mode, see also GX_SHARPNESS_MODE_ENTRY
    GX_FLOAT_SHARPNESS                = 6027 | GX_FEATURE_TYPE.GX_FEATURE_FLOAT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Sharpness

        #---------UserSetControl Section-------------------------
    GX_ENUM_USER_SET_SELECTOR         = 7000 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects the feature User Set to load, save or configure.
    GX_COMMAND_USER_SET_LOAD          = 7001 | GX_FEATURE_TYPE.GX_FEATURE_COMMAND | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Loads the User Set specified by UserSetSelector to the device and makes it active.
    GX_COMMAND_USER_SET_SAVE          = 7002 | GX_FEATURE_TYPE.GX_FEATURE_COMMAND | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Save the User Set specified by UserSetSelector to the non-volatile memory of the device.
    GX_ENUM_USER_SET_DEFAULT          = 7003 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects the feature User Set to load and make active by default when the device is reset.

        #---------Event Section-------------------------
    GX_ENUM_EVENT_SELECTOR             = 8000 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects which Event to signal to the host application.
    GX_ENUM_EVENT_NOTIFICATION         = 8001 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Activate or deactivate the notification to the host application of the occurrence of the selected Event.
    GX_INT_EVENT_EXPOSUREEND           = 8002 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Returns the unique identifier of the ExposureEnd type of Event.
    GX_INT_EVENT_EXPOSUREEND_TIMESTAMP = 8003 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Returns the Timestamp of the ExposureEnd Event.
    GX_INT_EVENT_EXPOSUREEND_FRAMEID   = 8004 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Returns the unique Identifier of the Frame (or image) that generated the ExposureEnd Event.
    GX_INT_EVENT_BLOCK_DISCARD         = 8005 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #This enumeration value indicates the BlockDiscard event ID.
    GX_INT_EVENT_BLOCK_DISCARD_TIMESTAMP = 8006 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Indicates the time stamp for the BlockDiscard event
    GX_INT_EVENT_OVERRUN                 = 8007 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # This enumeration value indicates the EventOverrun event ID.
    GX_INT_EVENT_OVERRUN_TIMESTAMP       = 8008 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Indicates the time stamp of the EventOverrun event
    GX_INT_EVENT_FRAMESTART_OVERTRIGGER  = 8009 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # This enumeration value indicates the FrameStartOverTrigger event ID.
    GX_INT_EVENT_FRAMESTART_OVERTRIGGER_TIMESTAMP = 8010 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Indicates the time stamp of the FrameStartOverTrigger event
    GX_INT_EVENT_BLOCK_NOT_EMPTY                  = 8011 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # This enumeration value indicates the BlockNotEmpty event.
    GX_INT_EVENT_BLOCK_NOT_EMPTY_TIMESTAMP        = 8012 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Indicates the time stamp of the BlockNotEmpty event
    GX_INT_EVENT_INTERNAL_ERROR                   = 8013 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # This enumeration value indicates the InternalError event.
    GX_INT_EVENT_INTERNAL_ERROR_TIMESTAMP         = 8014 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Indicates the time stamp of the InternalError event

        #---------LUT Section-------------------------
    GX_ENUM_LUT_SELECTOR             = 9000 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects which LUT to control.
    GX_BUFFER_LUT_VALUEALL           = 9001 | GX_FEATURE_TYPE.GX_FEATURE_BUFFER | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Accesses all the LUT coefficients in a single access without using individual LUTIndex.
    GX_BOOL_LUT_ENABLE               = 9002 | GX_FEATURE_TYPE.GX_FEATURE_BOOL | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Activates the selected LUT.
    GX_INT_LUT_INDEX                 = 9003 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Control the index (offset) of the coefficient to access in the selected LUT.
    GX_INT_LUT_VALUE                 = 9004 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Returns the Value at entry LUTIndex of the LUT selected by LUTSelector.

        #---------ChunkData Section-------------------------
    GX_BOOL_CHUNKMODE_ACTIVE         = 10001 | GX_FEATURE_TYPE.GX_FEATURE_BOOL | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Activates the inclusion of Chunk data in the payload of the image.
    GX_ENUM_CHUNK_SELECTOR           = 10002 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Selects which Chunk to enable or control.
    GX_BOOL_CHUNK_ENABLE             = 10003 | GX_FEATURE_TYPE.GX_FEATURE_BOOL | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Enables the inclusion of the selected Chunk data in the payload of the image.
    
        #---------Color Transformation Control-------------------------
    GX_ENUM_COLOR_TRANSFORMATION_MODE       = 11000 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Color conversion selection, see also GX_COLOR_TRANSFORMATION_MODE_ENTRY
    GX_BOOL_COLOR_TRANSFORMATION_ENABLE     = 11001 | GX_FEATURE_TYPE.GX_FEATURE_BOOL | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Activates the selected Color Transformation module.
    GX_ENUM_COLOR_TRANSFORMATION_VALUE_SELECTOR = 11002 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Selects the Gain factor or Offset of the Transformation matrix to access in the selected Color Transformation module.
    GX_FLOAT_COLOR_TRANSFORMATION_VALUE     = 11003 | GX_FEATURE_TYPE.GX_FEATURE_FLOAT| GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Represents the value of the selected Gain factor or Offset inside the Transformation matrix.

        #---------CounterAndTimerControl Section-------------------------
    GX_ENUM_TIMER_SELECTOR                  = 12000 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects which Counter to configure, Refer to GX_TIMER_SELECTOR_ENTRY
    GX_FLOAT_TIMER_DURATION                 = 12001 | GX_FEATURE_TYPE.GX_FEATURE_FLOAT| GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Sets the duration (in microseconds) of the Timer pulse.
    GX_FLOAT_TIMER_DELAY                    = 12002 | GX_FEATURE_TYPE.GX_FEATURE_FLOAT| GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Sets the duration (in microseconds) of the delay to apply at the reception of a trigger before starting the Timer.
    GX_ENUM_TIMER_TRIGGER_SOURCE            = 12003 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects the source of the trigger to start the Timer, Refer to GX_TIMER_TRIGGER_SOURCE_ENTRY
    GX_ENUM_COUNTER_SELECTOR                = 12004 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects which Counter to configure, Refer to GX_COUNTER_SELECTOR_ENTRY
    GX_ENUM_COUNTER_EVENT_SOURCE            = 12005 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Select the events that will be the source to increment the Counter, Refer to GX_COUNTER_EVENT_SOURCE_ENTRY
    GX_ENUM_COUNTER_RESET_SOURCE            = 12006 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects the signals that will be the source to reset the Counter, Refer to GX_COUNTER_RESET_SOURCE_ENTRY
    GX_ENUM_COUNTER_RESET_ACTIVATION        = 12007 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    #Selects the Activation mode of the Counter Reset Source signal, Refer to GX_COUNTER_RESET_ACTIVATION_ENTRY
    GX_COMMAND_COUNTER_RESET                = 12008 | GX_FEATURE_TYPE.GX_FEATURE_COMMAND | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_REMOTE_DEV    # Does a software reset of the selected Counter and starts it.

        #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #//
        # Local device layer(Device Feature)
        #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #//
    GX_DEV_INT_COMMAND_TIMEOUT     = 0 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DEV    # Indicates the current command timeout of the specific Link.
    GX_DEV_INT_COMMAND_RETRY_COUNT = 1 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DEV    # Command retry times

        #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #//
        # Flow layer(DataStream Feature)
        #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #    #//
    GX_DS_INT_ANNOUNCED_BUFFER_COUNT          = 0 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DS    #Number of Buffers declared
    GX_DS_INT_DELIVERED_FRAME_COUNT           = 1 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DS    #Number of received frames (including residual frames)
    GX_DS_INT_LOST_FRAME_COUNT                = 2 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DS    #Number of frames lost due to insufficient buffers
    GX_DS_INT_INCOMPLETE_FRAME_COUNT          = 3 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DS    #Number of residual frames received
    GX_DS_INT_DELIVERED_PACKET_COUNT          = 4 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DS    #Number of packets received
    GX_DS_INT_RESEND_PACKET_COUNT             = 5 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DS    #Number of retransmission packets
    GX_DS_INT_RESCUED_PACKED_COUNT            = 6 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DS    #Number of successful retransmitted packets
    GX_DS_INT_RESEND_COMMAND_COUNT            = 7 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DS    #Repeat command times
    GX_DS_INT_UNEXPECTED_PACKED_COUNT         = 8 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DS    #Exception packet number
    GX_DS_INT_MAX_PACKET_COUNT_IN_ONE_BLOCK   = 9 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DS    #Maximum number of retransmissions of data blocks
    GX_DS_INT_MAX_PACKET_COUNT_IN_ONE_COMMAND = 10 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DS    # Maximum number of packets contained in a retransmit command
    GX_DS_INT_RESEND_TIMEOUT                  = 11 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DS    # Retransmission timeout time
    GX_DS_INT_MAX_WAIT_PACKET_COUNT           = 12 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DS    # Maximum waiting packet number
    GX_DS_ENUM_RESEND_MODE                    = 13 | GX_FEATURE_TYPE.GX_FEATURE_ENUM | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DS    # Retransmission, see also GX_DS_RESEND_MODE_ENTRY
    GX_DS_INT_MISSING_BLOCKID_COUNT           = 14 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DS    # Missing number of BlockID
    GX_DS_INT_BLOCK_TIMEOUT                   = 15 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DS    # Data block timeout
    GX_DS_INT_STREAM_TRANSFER_SIZE            = 16 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DS    # size of transfer block
    GX_DS_INT_STREAM_TRANSFER_NUMBER_URB      = 17 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DS    # Number of data blocks transmitted
    GX_DS_INT_MAX_NUM_QUEUE_BUFFER            = 18 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DS    # Maximum Buffer Number of Collection Queues
    GX_DS_INT_PACKET_TIMEOUT                  = 19 | GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DS    # time of package timeout
    GX_DS_INT_SOCKET_BUFFER_SIZE     =  20|GX_FEATURE_TYPE.GX_FEATURE_INT | GX_FEATURE_LEVEL.GX_FEATURE_LEVEL_DS

GX_PIXEL_MONO           =       ( 0x01000000 )
GX_PIXEL_COLOR         =        ( 0x02000000 )

GX_PIXEL_8BIT          =        ( 0x00080000 )
GX_PIXEL_10BIT            =     ( 0x000A0000 )
GX_PIXEL_12BIT           =      ( 0x000C0000 )
GX_PIXEL_16BIT          =       ( 0x00100000 )
GX_PIXEL_24BIT          =       ( 0x00180000 )
GX_PIXEL_30BIT          =       ( 0x001E0000 )
GX_PIXEL_32BIT         =        ( 0x00200000 )
GX_PIXEL_36BIT          =       ( 0x00240000 )
GX_PIXEL_48BIT         =        ( 0x00300000 )
GX_PIXEL_64BIT       =          ( 0x00400000 )

class GX_PIXEL_FORMAT_ENTRY:
    GX_PIXEL_FORMAT_UNDEFINED          = (0),
    GX_PIXEL_FORMAT_MONO8              = (GX_PIXEL_MONO  | GX_PIXEL_8BIT  | 0x0001)    #0x1080001,
    GX_PIXEL_FORMAT_MONO8_SIGNED       = (GX_PIXEL_MONO  | GX_PIXEL_8BIT  | 0x0002)    #0x1080002,
    GX_PIXEL_FORMAT_MONO10             = (GX_PIXEL_MONO  | GX_PIXEL_16BIT | 0x0003)    #0x1100003,    
    GX_PIXEL_FORMAT_MONO12             = (GX_PIXEL_MONO  | GX_PIXEL_16BIT | 0x0005)    #0x1100005,    
    GX_PIXEL_FORMAT_MONO14             = (GX_PIXEL_MONO  | GX_PIXEL_16BIT | 0x0025)    #0x1100025,
    GX_PIXEL_FORMAT_MONO16             = (GX_PIXEL_MONO  | GX_PIXEL_16BIT | 0x0007)    #0x1100007,
    GX_PIXEL_FORMAT_BAYER_GR8          = (GX_PIXEL_MONO  | GX_PIXEL_8BIT  | 0x0008)    #0x1080008,               
    GX_PIXEL_FORMAT_BAYER_RG8          = (GX_PIXEL_MONO  | GX_PIXEL_8BIT  | 0x0009)    #0x1080009,                
    GX_PIXEL_FORMAT_BAYER_GB8          = (GX_PIXEL_MONO  | GX_PIXEL_8BIT  | 0x000A)    #0x108000A,
    GX_PIXEL_FORMAT_BAYER_BG8          = (GX_PIXEL_MONO  | GX_PIXEL_8BIT  | 0x000B)    #0x108000B,
    GX_PIXEL_FORMAT_BAYER_GR10         = (GX_PIXEL_MONO  | GX_PIXEL_16BIT | 0x000C)    #0x110000C,                
    GX_PIXEL_FORMAT_BAYER_RG10         = (GX_PIXEL_MONO  | GX_PIXEL_16BIT | 0x000D)    #0x110000D,
    GX_PIXEL_FORMAT_BAYER_GB10         = (GX_PIXEL_MONO  | GX_PIXEL_16BIT | 0x000E)    #0x110000E,
    GX_PIXEL_FORMAT_BAYER_BG10         = (GX_PIXEL_MONO  | GX_PIXEL_16BIT | 0x000F)    #0x110000F,
    GX_PIXEL_FORMAT_BAYER_GR12         = (GX_PIXEL_MONO  | GX_PIXEL_16BIT | 0x0010)    #0x1100010,              
    GX_PIXEL_FORMAT_BAYER_RG12         = (GX_PIXEL_MONO  | GX_PIXEL_16BIT | 0x0011)    #0x1100011,
    GX_PIXEL_FORMAT_BAYER_GB12         = (GX_PIXEL_MONO  | GX_PIXEL_16BIT | 0x0012)    #0x1100012,
    GX_PIXEL_FORMAT_BAYER_BG12         = (GX_PIXEL_MONO  | GX_PIXEL_16BIT | 0x0013)    #0x1100013,    
    GX_PIXEL_FORMAT_BAYER_GR16         = (GX_PIXEL_MONO  | GX_PIXEL_16BIT | 0x002E)    #0x110002E,                
    GX_PIXEL_FORMAT_BAYER_RG16         = (GX_PIXEL_MONO  | GX_PIXEL_16BIT | 0x002F)    #0x110002F,
    GX_PIXEL_FORMAT_BAYER_GB16         = (GX_PIXEL_MONO  | GX_PIXEL_16BIT | 0x0030)    #0x1100030,
    GX_PIXEL_FORMAT_BAYER_BG16         = (GX_PIXEL_MONO  | GX_PIXEL_16BIT | 0x0031)    #0x1100031,    
    GX_PIXEL_FORMAT_RGB8_PLANAR        = (GX_PIXEL_COLOR | GX_PIXEL_24BIT | 0x0021)    #0x2180021,
    GX_PIXEL_FORMAT_RGB10_PLANAR       = (GX_PIXEL_COLOR | GX_PIXEL_48BIT | 0x0022)    #0x2300022,
    GX_PIXEL_FORMAT_RGB12_PLANAR       = (GX_PIXEL_COLOR | GX_PIXEL_48BIT | 0x0023)    #0x2300023,
    GX_PIXEL_FORMAT_RGB16_PLANAR       = (GX_PIXEL_COLOR | GX_PIXEL_48BIT | 0x0024)    #0x2300024,



class DX_BAYER_CONVERT_TYPE:
	RAW2RGB_NEIGHBOUR  = 0   
	RAW2RGB_ADAPTIVE   = 1
	RAW2RGB_NEIGHBOUR3 = 2    



class  DX_PIXEL_COLOR_FILTER:
	NONE    = 0   
	BAYERRG = 1   
	BAYERGB = 2   
	BAYERGR = 3   
	BAYERBG = 4    
class GX_PIXEL_COLOR_FILTER_ENTRY:
    GX_COLOR_FILTER_NONE     = 0      # None
    GX_COLOR_FILTER_BAYER_RG = 1      # RG format
    GX_COLOR_FILTER_BAYER_GB = 2      # GB format
    GX_COLOR_FILTER_BAYER_GR = 3      # GR format
    GX_COLOR_FILTER_BAYER_BG = 4      # BG format







class GX_OPEN_PARAM(Structure):
    _fields_ = [
                 ("pszContent",     c_char_p),
                 ("openMode",       c_int),
                 ("accessMode",     c_int)
            ]

class GX_FRAME_STATUS_LIST:

    GX_FRAME_STATUS_SUCCESS             = 0     #Normal frame
    GX_FRAME_STATUS_INCOMPLETE          = -1      #Incomplete frame
    GX_FRAME_STATUS_INVALID_IMAGE_INFO  = -2       # Information Error Frame


class GX_FRAME_BUFFER(Structure):
    _fields_ = [
                ("nStatus",c_uint),
                ("pImgBuf", c_void_p),
                ("nWidth",c_uint),
                ("nHeight",c_uint),
                ("nPixelFormat",c_uint),
                ("nImgSize",c_uint),
                ("nFrameID",c_ulong),
                ("nTimestamp",c_ulong),
                ("nBufID",c_ulong),
                ("nOffsetX",c_uint),
                ("nOffsetY",c_uint),
                ("reserved",c_uint*16)
            ]



class GX_FRAME_DATA(Structure):
    _fields_ = [
                ("nStatus",c_uint),
                ("pImgBuf", c_void_p),
                ("nWidth",c_uint),
                ("nHeight",c_uint),
                ("nPixelFormat",c_uint),
                ("nImgSize",c_uint),
                ("nFrameID",c_ulong),
                ("nTimestamp",c_ulong),
                ("nOffsetX",c_uint),
                ("nOffsetY",c_uint),
                ("reserved",c_uint)
            ]






def wrap_func(lib, funcname, restype, argtypes):
    """Simplify wrapping ctypes functions"""
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func


class GalaxyCam():
    def __init__(self,libname,camindex):
        self.sdk = CDLL(libname)
        self.libc = CDLL("libc.so.6")
        self.m_handle = None

        #libc
        self._memcpy                     = wrap_func(self.libc, "memcpy",                   c_void_p,   [c_void_p, c_void_p, c_uint])
        self._malloc                     = wrap_func(self.libc, "malloc", POINTER(c_uint8), [c_int,])
        self._memset                     = wrap_func(self.libc, "memset", POINTER(c_uint8), [c_void_p,c_int,c_uint])

        #sdk
        self._GXInitLib = wrap_func(self.sdk,"GXInitLib",c_int,[])
        self._GXUpdateDeviceList = wrap_func(self.sdk,"GXUpdateDeviceList",c_int,[POINTER(c_uint),c_uint])
        self._GXOpenDevice = wrap_func(self.sdk,"GXOpenDevice",c_int,[POINTER(GX_OPEN_PARAM),c_void_p])
        self._GXOpenDeviceByIndex = wrap_func(self.sdk,"GXOpenDeviceByIndex",c_int,[c_uint,c_void_p])
        self._GXCloseDevice = wrap_func(self.sdk,"GXCloseDevice",c_int,[c_void_p])
        self._GXIsImplemented = wrap_func(self.sdk,"GXIsImplemented",c_int,[c_void_p,c_uint,POINTER(c_bool)])
        self._GXStreamOn = wrap_func(self.sdk,"GXStreamOn",c_int,[c_void_p])
        self._GXStreamOff = wrap_func(self.sdk,"GXStreamOff",c_int,[c_void_p])
        self._GXDQBuf = wrap_func(self.sdk,"GXDQBuf",c_int,[c_void_p,POINTER(GX_FRAME_BUFFER),c_uint])
        self._GXQBuf = wrap_func(self.sdk,"GXQBuf",c_int,[c_void_p,c_void_p])
        self._GXGetInt = wrap_func(self.sdk,"GXGetInt",c_int,[c_void_p,c_longlong,POINTER(c_longlong)])
        self._GXSendCommand = wrap_func(self.sdk,"GXSendCommand",c_int,[c_void_p,c_longlong])
        self._GXGetImage = wrap_func(self.sdk,"GXGetImage",c_int,[c_void_p,POINTER(GX_FRAME_DATA),c_uint])
        self._DxRaw8toRGB24 = wrap_func(self.sdk,"DxRaw8toRGB24",c_int,[c_void_p,c_void_p,c_uint,c_uint,c_int,c_int,c_bool])          

        self.camera_isOpen = False
        self.cam_index = camindex
        self.nDeviceNum = 0
        self.rgb_buf = self._malloc(1292*964*3)
        # self.pFrameBuffer = POINTER(GX_FRAME_BUFFER)
        
        # self.pFrameBuffer.pImgBuf= cast(self._malloc(1292*964),c_void_p)
        # # self.pFrameBuffer_pointer = byref(self.pFrameBuffer)
        self.stFrameData = GX_FRAME_DATA()
        self.stFrameData.pImgBuf= cast(self._malloc(1292*964),c_void_p)
        self.image = None




    def api_status(self,status):
        if status == API_STATUS_OK:
            return True
        else:
            return False

    def GXInitLib(self):
        status = self._GXInitLib()
        print("GXInitLib status:  ",status)
        return self.api_status(status)
    

    def GXUpdateDeviceList(self):
        nDeviceNum = c_uint(0)
        status = self._GXUpdateDeviceList(byref(nDeviceNum),1000)
        print("GXUpdateDeviceList status:    ",status,"   num:     ",nDeviceNum)
        self.nDeviceNum = nDeviceNum
        return nDeviceNum
    
    def GXOpenDevice(self):
        self.m_handle = c_void_p(None)
        stOpenParam = GX_OPEN_PARAM()
        stOpenParam.accessMode = GX_ACCESS_MODE.GX_ACCESS_EXCLUSIVE
        stOpenParam.openMode = GX_OPEN_MODE.GX_OPEN_SN
        stOpenParam.pszContent = c_char_p(bytes("GK0190120367", 'utf-8'))
        # stOpenParam.pszContent = 1

        status = self._GXOpenDevice(byref(stOpenParam),byref(self.m_handle))
        print("GXOpenDevice status:    ",status)
        return self.api_status(status)
    
    def GXOpenDeviceByIndex(self):
        # if c_uint(self.cam_index) > self.nDeviceNum:
        #     return False
        self.m_handle = c_void_p(None)
        status = self._GXOpenDeviceByIndex(self.cam_index,byref(self.m_handle))
        return self.api_status(status)

    
    def GXCloseDevice(self):
        status = self._GXCloseDevice(self.m_handle)
        self.m_handle = None
        print("GXCloseDevice status:      ",status)
        return self.api_status(status)

    def GXIsImplemented(self):
        bIsImplemented = c_bool(False)
        status = self._GXIsImplemented(self.m_handle,GX_FEATURE_ID.GX_FLOAT_GAIN,byref(bIsImplemented))
        print("GXIsImplemented status:    ",status)
        return self.api_status(status)


    def GXStreamOn(self):
        status = self._GXStreamOn(self.m_handle)
        print("GXStreamOn status:   ",status)
        return self.api_status(status)

    def GXStreamOff(self):
        status = self._GXStreamOff(self.m_handle)
        print("GXStreamOff status:   ",status)
        return self.api_status(status)

    def GXQBuf(self):
        status = self._GXQBuf(self.m_handle,byref(self.pFrameBuffer)) 

        return self.api_status(status)


    def GXDQBuf(self):
        self.GXGetInt()
        status = self._GXDQBuf(self.m_handle,byref(self.pFrameBuffer),1000)
        # buffer_contents_ = self.pFrameBuffer_pointer
        print("buffer_contents_.nWidth     ",self.pFrameBuffer.nWidth)
        image = None
        if self.api_status(status):
            
            print("self.pFrameBuffer.nStatus:     ",self.pFrameBuffer.nStatus)
            self.PixelFormatConvert()
            image = np.ctypeslib.as_array(self.rgb_buf, (964,1292,3 ))
            # print(image)

        self.GXQBuf()
            
        return image


    def DxRaw8toRGB24(self,pFrameBuffer):
        g_i64ColorFilter = GX_PIXEL_COLOR_FILTER_ENTRY.GX_COLOR_FILTER_NONE
        status = self._DxRaw8toRGB24(pFrameBuffer.pImgBuf,
        self.rgb_buf,
        pFrameBuffer.nWidth, 
        pFrameBuffer.nHeight,
        DX_BAYER_CONVERT_TYPE.RAW2RGB_NEIGHBOUR3,
        1,False)
        # print("DxRaw8toRGB24  status:    ",status)

        return self.api_status(status)



    def GXGetInt(self):
        nPayLoadSize = c_longlong(0)

        status = self._GXGetInt(self.m_handle,GX_FEATURE_ID.GX_INT_PAYLOAD_SIZE,byref(nPayLoadSize))
        print("GXGetInt status:       ",status," size:   ",nPayLoadSize)
        return nPayLoadSize

    def PixelFormatConvert(self):
        emStatus = GX_STATUS_LIST.GX_STATUS_SUCCESS
        emDXStatus = c_int(0)
        # print("stFrameData.nPixelFormat ==== ",self.stFrameData.nPixelFormat)
        if self.stFrameData.nPixelFormat == GX_PIXEL_FORMAT_ENTRY.GX_PIXEL_FORMAT_MONO8:
            pass
            # print("mono 8")
        elif self.stFrameData.nPixelFormat == GX_PIXEL_FORMAT_ENTRY.GX_PIXEL_FORMAT_MONO10  or self.stFrameData.nPixelFormat == GX_PIXEL_FORMAT_ENTRY.GX_PIXEL_FORMAT_MONO12:
            print("MONO10")

        elif (self.stFrameData.nPixelFormat == GX_PIXEL_FORMAT_ENTRY.GX_PIXEL_FORMAT_BAYER_GR8 or
        self.stFrameData.nPixelFormat == GX_PIXEL_FORMAT_ENTRY.GX_PIXEL_FORMAT_BAYER_RG8 or
        self.stFrameData.nPixelFormat == GX_PIXEL_FORMAT_ENTRY.GX_PIXEL_FORMAT_BAYER_GB8 or
        self.stFrameData.nPixelFormat == GX_PIXEL_FORMAT_ENTRY.GX_PIXEL_FORMAT_BAYER_BG8 ):
                # print("RG8")
                return self.DxRaw8toRGB24(self.stFrameData)


        elif (self.stFrameData.nPixelFormat == GX_PIXEL_FORMAT_ENTRY.GX_PIXEL_FORMAT_BAYER_GR10 or
        self.stFrameData.nPixelFormat == GX_PIXEL_FORMAT_ENTRY.GX_PIXEL_FORMAT_BAYER_RG10 or
        self.stFrameData.nPixelFormat == GX_PIXEL_FORMAT_ENTRY.GX_PIXEL_FORMAT_BAYER_GB10 or
        self.stFrameData.nPixelFormat == GX_PIXEL_FORMAT_ENTRY.GX_PIXEL_FORMAT_BAYER_BG10 or
        self.stFrameData.nPixelFormat == GX_PIXEL_FORMAT_ENTRY.GX_PIXEL_FORMAT_BAYER_GR12 or
        self.stFrameData.nPixelFormat == GX_PIXEL_FORMAT_ENTRY.GX_PIXEL_FORMAT_BAYER_RG12 or
        self.stFrameData.nPixelFormat == GX_PIXEL_FORMAT_ENTRY.GX_PIXEL_FORMAT_BAYER_GB12 or
        self.stFrameData.nPixelFormat == GX_PIXEL_FORMAT_ENTRY.GX_PIXEL_FORMAT_BAYER_GB12 
        ):
            print("RG10")


        else:
            print("other")











    def GXGetImage(self):
        
        self._memset(self.stFrameData.pImgBuf,0,1292*964)
        image = None
        status = self._GXGetImage(self.m_handle,byref(self.stFrameData),100)

        if self.PixelFormatConvert():
            image = np.ctypeslib.as_array(self.rgb_buf, ( 964,1292,3))            
        return image





    def GXSendCommand(self,cmd_id):
        status = self._GXSendCommand(self.m_handle,cmd_id)
        print("GXSendCommand  cmd:   ",cmd_id,"   status:   ",status)
        return self.api_status(status)



    def open(self):
        print("get in open..")
        if not self.GXInitLib():    
            return False
        if self.GXUpdateDeviceList() == 0:    
            return False
        if not self.GXOpenDeviceByIndex():  
            return False
        if not self.GXStreamOn():
            return False
        if not self.GXSendCommand(GX_FEATURE_ID.GX_COMMAND_ACQUISITION_START):
            return False

        self.camera_isOpen = True
        return True

    

    def close(self):
        self.camera_isOpen = False
        self.GXSendCommand(GX_FEATURE_ID.GX_COMMAND_ACQUISITION_STOP)
        self.GXStreamOff()
        self.GXCloseDevice()
        

    def save(self,fname,img):
        # image = np.ctypeslib.as_array(self.rgb_buf, (964,1292,3))
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imwrite(fname, img)

    def pop_frame(self):
       
        # status = self.GXDQBuf()
        # image = None
        
        image = self.GXGetImage()
        return image
    
    def start_grab(self):
        status = self.GXSendCommand(GX_FEATURE_ID.GX_COMMAND_ACQUISITION_START)
        return status
    def stop_grab(self):
        status = self.GXSendCommand(GX_FEATURE_ID.GX_COMMAND_ACQUISITION_STOP)
        return status


    def getCamIpStr(self):
        return ""
        # print("self.cam_init_state ============== ",self.cam_init_state)
        # if not self.cam_init_state:
        #     return ""

        # stIntvalue  = MVCC_INTVALUE()
        # stIntvalue = self.MV_CC_GetIntValue("GevCurrentIPAddress")
        # x = bin(stIntvalue.nCurValue)
        # ipstr = ""
        # for i in range(2,34,8):
        #     temp = x[i:i+8]
        #     ans = int(temp,2)
        #     ipstr = ipstr+str(ans)+"."
        # ipstr = ipstr[0:len(ipstr)-1]
        # return ipstr    

    def getCamDeviceID(self):
        return ""
        # if not self.cam_init_state:
        #     return ""
        # struStringValue = MVCC_STRINGVALUE()
        # struStringValue=self.MV_CC_GetStringValue("DeviceID")
        # # print(struStringValue.chCurValue)
        # # print(type(struStringValue.chCurValue))
        # return str(struStringValue.chCurValue,encoding = "utf-8")
