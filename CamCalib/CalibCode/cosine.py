import cv2
import math
import numpy as np

def cosine(usrA,mtx,dist,HandSyatemFlag): # 参数分别为目标位置的目标位置，内参矩阵，畸变系数，以及机械臂左右手系标志，默认为右手
    # 将输入的目标位置(相机位置)的用户坐标值转为世界坐标值
    usrp = []
    wrdp = []
    ret,rvec,tvec,_ = cv2.solvePnPRansac(usrp, wrdp, mtx, dist)
    rMat = np.zeros((3, 3), dtype=np.float64)
    cv2.Rodrigues(rvec, rMat)
    invR = np.asmatrix(rMat).I
    WrdA = np.dot(invR, usrA - np.asmatrix(tvec))

    # 由余弦定理求出J1的关节角度值
    L1 = 225
    L2 = 175
    L3 = 9
    alpha = math.atan2(WrdA[1],WrdA[0])
    fai = math.acos((usrA[0]**2 + usrA[1]**2 + L1**2 - (L1+L3)**2) / (2*L1*(usrA[0]**2+usrA[1]**2)**0.5))
    if HandSyatemFlag == 1:
        J1_angle = alpha - fai
    else:
        J1_angle = alpha + fai
    print(math.degrees(J1_angle))

    # 根据相似三角形推出相机的世界坐标位置
    WrdxB = (L2*WrdA[0]+L1*L3*math.sin(J1_angle))/(L2+L3)
    WrdyB = (L2*WrdA[1]+L1*L3*math.cos(J1_angle))/(L2+L3)
    return WrdxB,WrdyB
