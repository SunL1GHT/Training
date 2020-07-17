import cv2
import numpy as np
import glob

def calibrate():
    # 设置寻找亚像素角点的参数，采用的停止准则是最大迭代次数30和最大误差容限0.001
    criteria = (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.001)
    # 获取标定板角点的位置
    objp = np.zeros((Nx_cor * Ny_cor, 3), np.float32)
    objp[:, :2] = np.mgrid[0:Nx_cor*30:30, 0:Ny_cor*30:30].T.reshape(-1, 2)  # 将世界坐标系建在标定板上，所有点的Z坐标全部为0，所以只需要赋值x和y

    obj_points = []  # 存储3D点
    img_points = []  # 存储2D点

    images = sorted(glob.glob("./Calibsource/calib*.jpg"))
    for fname in images:
        print(fname)
        img = cv2.imread(fname)
        cv2.imshow('img',img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (Nx_cor, Ny_cor), None)
        print(ret)
        if ret:
            corners = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), criteria)  # 在原角点的基础上寻找亚像素角点
            obj_points.append(objp)
            img_points.append(corners)

            cv2.drawChessboardCorners(img, (Nx_cor, Ny_cor), corners, ret)  # OpenCV的绘制函数一般无返回值
            cv2.imshow('img', img)
            cv2.waitKey(800)
    print('共计',len(img_points),'张图片')
    global mtx, dist
    # 标定
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

    print('objp:',obj_points[0][0])    # 图片编号0的
    print('imgp:',img_points[0][0][0])

    # print('rvecs:',rvecs[0])
    # print('tvces:',tvecs[0])
    print('conversedIMGP:',cameraToWorld(mtx,rvecs[0],tvecs[0],img_points[0][0][0]))


    # 衡量误差
    # 使用cv2.projectPoints()，计算三维点到二维图像的投影，
    # 然后计算反投影得到的点与图像上检测到的点的误差，最后计算一个对于所有标定图像的平均误差，这个值就是反投影误差。
    # 重投影误差是用估计的内在矩阵和外在矩阵重新投影的3D点与通过某些图像处理技术（例如棋盘图案的角落）检测到的2D图像点之间的误差（例如欧几里德距离）。
    tot_error = 0
    for i in range(len(obj_points)):
        img_points2, _ = cv2.projectPoints(obj_points[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(img_points[i], img_points2, cv2.NORM_L2) / len(img_points2)
        tot_error += error
    print("重投影误差:", tot_error / len(obj_points))
    print("-----------------------------------------------------")
    np.savez('D:/Users/Desktop/CamCalib/Calibresult/calibrate.npz', mtx=mtx, dist=dist[0:4])

# 得到相机的外参矩阵
def Transfer():
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((Nx_cor * Ny_cor, 3), np.float32)
    objp[:, :2] = np.mgrid[0:Nx_cor * 30:30, 0:Ny_cor * 30:30].T.reshape(-1, 2)

    print("外参标定时采用的内参矩阵为:\n",mtx)
    # 载入固定标定图
    images = glob.glob('./Calibsource/T3.jpg')  # 选择需要标定的图片
    if len(images) == 0:
        print('No Test Picture can be loading!')
        exit()
    img = cv2.imread(images[0])
    gray  = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # 灰度处理
    ret, corners = cv2.findChessboardCorners(gray, (Nx_cor, Ny_cor), None)  # 寻找角点

    global rmtx,tmtx
    if ret:
        imgp = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), criteria) # 亚像素点
        ret, rmtx, tmtx, inliers = cv2.solvePnPRansac(objp, imgp, mtx, dist)

    print('imgp:',imgp[0])
    print('world:',cameraToWorld(mtx,rmtx,tmtx,imgp[0][0]))

    # print('rmtx:\n',rmtx)
    # print('tmtx:\n',tmtx)
    print("-----------------------------------------------------")
    np.savez('D:/Users/Desktop/CamCalib/Calibresult/Transfer.npz', rmtx = rmtx, tmtx = tmtx)

# 霍夫圆检测算法
# def detect_circles():
#     # 载入图片
#     images = glob.glob('./Calibsource/Circle.jpg')
#     if len(images) == 0:
#         print('No Detect Picture can be loading!')
#         exit()
#     image = cv2.imread(images[0])
#     # 取工件圆心，采用霍夫圆变换实现
#     dst = cv2.pyrMeanShiftFiltering(image,10,100)  # 边缘保留滤波
#     Gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
#     binary = cv2.adaptiveThreshold(Gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 20)
#     circles = cv2.HoughCircles(binary,cv2.HOUGH_GRADIENT,1,1,param1=30,param2=30,minRadius=0,maxRadius=0)  #method:基于梯度  dp:步长
#     # print(circles[0][0][0])
#     circles = np.uint16(np.around(circles))
#     for i in circles[0,:]:
#         if i[2] < 20:
#             cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)  # 画圆
#             cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 2)  # 画圆心
#             # print((i[0], i[1]))
#             circle_point = np.array([i[0],i[1]],dtype=np.float32)
#     cv2.imshow("circles",image)
#     cv2.waitKey(1000)
#     cv2.imwrite('./Calibresult/detectedCircle.jpg',image)
#     return circle_point

def detect_circles():
    # 载入图片
    images = glob.glob('./Calibsource/Circle5.jpg')
    if len(images) == 0:
        print('No Detect Picture can be loading!')
        exit()
    img = cv2.imread(images[0])

    # Imageroi = img[213:631, 404:852] # roi [y,x]
    Imageroi = img[:, :]  # roi [y,x]
    imgGray = cv2.cvtColor(Imageroi, cv2.COLOR_BGR2GRAY)

    # 取工件圆心，采用contour算法实现
    ret, binary = cv2.threshold(imgGray, 70, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        # print(area)
        if 500 < area < 800:
            # print('圆的面积:', area)
            cv2.drawContours(Imageroi, cnt, -1, (255, 0, 255), 2)  # 绘制外轮廓
            peri = cv2.arcLength(cnt, True)
            # print('圆的周长:',peri)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            # print('拐点坐标:',approx)
            # print('圆的拐点个数:',len(approx))
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(Imageroi, (x, y), (x + w, y + h), (0, 255, 0), 3)
            # Rx = x + w / 2 + 404
            # Ry = y + h / 2 + 213
            Rx = x + w / 2
            Ry = y + h / 2
            # print("圆心坐标:", Rx, Ry)
            circle_point = np.array([Rx, Ry], dtype=np.float32)
    cv2.imwrite('./Calibresult/detectedCircle.jpg', Imageroi)
    # cv2.imshow("Detected", Imageroi)
    return circle_point

def cameraToWorld(cameraMatrix, r, t, imgPoints):
    invK = np.asmatrix(cameraMatrix).I
    rMat = np.zeros((3, 3), dtype=np.float64)
    cv2.Rodrigues(r, rMat)
    # print('rMat=', rMat)
    # 计算 invR * T
    invR = np.asmatrix(rMat).I  # 3*3
    # print('invR=', invR)
    transPlaneToCam = np.dot(invR, np.asmatrix(t))  # 3*3 dot 3*1 = 3*1
    # print('transPlaneToCam=', transPlaneToCam)
    worldpt = []
    coords = np.zeros((3, 1), dtype=np.float64)
    coords[0][0] = imgPoints[0]
    coords[1][0] = imgPoints[1]
    coords[2][0] = 1.0

    worldPtCam = np.dot(invK, coords)  # 3*3 dot 3*1 = 3*1
    # print('worldPtCam=', worldPtCam)
    # [x,y,1] * invR
    worldPtPlane = np.dot(invR, worldPtCam)  # 3*3 dot 3*1 = 3*1
    # print('worldPtPlane=', worldPtPlane)
    # zc
    scale = transPlaneToCam[2][0] / worldPtPlane[2][0]
    # print("scale: ", scale)
    # zc * [x,y,1] * invR
    scale_worldPtPlane = np.multiply(scale, worldPtPlane)
    # print("scale_worldPtPlane: ", scale_worldPtPlane)
    # [X,Y,Z]=zc*[x,y,1]*invR - invR*T
    worldPtPlaneReproject = np.asmatrix(scale_worldPtPlane) - np.asmatrix(transPlaneToCam)  # 3*1 dot 1*3 = 3*3
    # print("worldPtPlaneReproject: ", worldPtPlaneReproject)
    pt = np.zeros((3, 1), dtype=np.float64)

    # 转为SCARA适合的笛卡尔右手坐标系
    pt[0][0] = worldPtPlaneReproject[1][0]
    pt[1][0] = worldPtPlaneReproject[0][0]
    pt[2][0] = 0  # 世界坐标系的Z轴坐标，一般设定为0
    worldpt.append(pt.T.tolist())
    # print('worldpt:',worldpt)
    return worldpt

if __name__ == '__main__':
    # 全局变量
    Nx_cor = 8  # 横向
    Ny_cor = 6  # 竖向
    # flag = 0 # 标志位，指示是否检测到圆心

    # 标定，获取内参，同一相机内参矩阵固定
    try:
        npzfile = np.load('D:/Users/Desktop/CamCalib/Calibresult/calibrate.npz')
        mtx = npzfile['mtx']
        dist = npzfile['dist']
    except IOError:
        print("重新标定相机...")
        calibrate()

    # 获取外参
    try:
        npzfile1 = np.load('D:/Users/Desktop/CamCalib/Calibresult/Transfer.npz')
        rmtx = npzfile1['rmtx']
        tmtx = npzfile1['tmtx']
    except IOError:
        print("重新标定外参...")
        Transfer()

    imgp = detect_circles()
    # print(imgp[0])
    print('圆心像素坐标值为:',imgp)
    print('转化成世界坐标值为:',cameraToWorld(mtx,rmtx,tmtx,imgp)[0][0])


    cv2.destroyAllWindows()