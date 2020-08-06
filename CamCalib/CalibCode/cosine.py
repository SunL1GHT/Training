import math
import numpy as np

# Input: expects Nx3 matrix of points
# Returns R,t
# R = 3x3 rotation matrix
# t = 3x1 column vector

def rigid_transform_3D(A, B):
    assert len(A) == len(B)

    N = A.shape[0]  # total points

    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)

    # centre the points
    AA = A - np.tile(centroid_A, (N, 1))
    BB = B - np.tile(centroid_B, (N, 1))

    H = np.matmul(np.transpose(AA),BB)

    U, S, Vt = np.linalg.svd(H)

    R = np.matmul(Vt.T, U.T)

    # special reflection case
    if np.linalg.det(R) < 0:
        print("Reflection detected")
        Vt[2, :] *= -1
        R = np.matmul(Vt.T,U.T)

    t = -np.matmul(R, centroid_A) + centroid_B
    # err = B - np.matmul(A,R.T) - t.reshape([1, 3])
    return R, t



def cosine(usrcamx,usrcamy,HandSyatemFlag): # 参数分别为目标位置的目标位置，机械臂左右手系标志，默认为右手
    # 将输入的目标位置(相机位置)的用户坐标值转为世界坐标值
    usrp = np.array([[46.5356, 17.6832],
                     [64.5361, 17.6166],
                     [72.0898, 23.2969],
                     [72.0890, 36.5419],
                     [81.9393, 53.4010],
                     [81.9378, 86.5455],
                     [90.9304, 92.1731],
                     [98.4165, 97.9386],
                     [40.6375, 97.9341],
                     [40.4441, 56.5775]], dtype=np.float)
    usrp_temp = np.zeros((10, 1))
    usrp = np.hstack((usrp, usrp_temp))
    print(usrp)

    wrdp = np.array([[161.2493, 126.3738],
                     [179.1858, 124.8577],
                     [187.1906, 129.8824],
                     [188.3042, 143.0805],
                     [199.5379, 159.0511],
                     [202.3249, 192.0782],
                     [211.7591, 196.9293],
                     [219.7038, 202.0446],
                     [162.1292, 206.9011],
                     [158.4571, 165.7074]], dtype=np.float)
    wrdp_temp = np.zeros((10, 1))
    wrdp = np.hstack((wrdp, wrdp_temp))
    print(wrdp)

    r, t = rigid_transform_3D(usrp, wrdp)
    # testu = np.array([37.8825,12.0431,0])
    # testw = np.matmul(testu, r.T) + t.reshape([1, 3])
    # print('testw:', testw)

    usrcam = np.array([usrcamx,usrcamy,0],dtype=np.float64)
    wrdcam = np.matmul(usrcam, r.T) + t.reshape([1, 3])

    print('wrdcam[0]:',wrdcam[0])
    print('wrdcam[0][0]:',wrdcam[0][0])

    # 由余弦定理求出J1的关节角度值
    L1 = 225
    L2 = 175
    L3 = 90
    alpha = math.atan2(wrdcam[0][1],wrdcam[0][0])
    fai = math.acos((wrdcam[0][0]**2 + wrdcam[0][1]**2 + L1**2 - (L1+L3)**2) / (2*L1*(wrdcam[0][0]**2+wrdcam[0][1]**2)**0.5))
    if HandSyatemFlag == 1:
        J1_angle = alpha - fai
    else:
        J1_angle = alpha + fai

    print('alpha',alpha,math.degrees(alpha))
    print('fai',fai,math.degrees(fai))
    print('J1',J1_angle,math.degrees(J1_angle))

    # 根据相似三角形推出相机的世界坐标位置
    wrdtoolx = (L2*wrdcam[0][0]+L1*L3*math.sin(J1_angle)) / (L2+L3)
    wrdtooly = (L2*wrdcam[0][1]+L1*L3*math.cos(J1_angle)) / (L2+L3)
    return wrdtoolx,wrdtooly

if __name__=='__main__':

    # x,y = cosine(83.36344691388528,124.22368156695669,0)
    x, y = cosine(23.805516807623047, 114.53304900030075,0)
    print('x,y:',x,y)