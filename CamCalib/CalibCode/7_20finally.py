"""
    参考自CalibPhoto文档，加入坐标系绘制
"""
import cv2
import numpy as np
import glob

def calibrate():
    criteria = (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.0001)
    objp = np.zeros((Nx_cor * Ny_cor, 3), np.float32)
    objp[:, :2] = np.mgrid[0:Nx_cor*5:5, 0:Ny_cor*5:5].T.reshape(-1, 2)
    obj_points = []
    img_points = []
    images = sorted(glob.glob("../Calibsource/calib*.jpg"))

    for fname in images:
        img = cv2.imread(fname)
        cv2.imshow('img',img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (Nx_cor, Ny_cor), None)
        print(ret)
        if ret:
            corners = cv2.cornerSubPix(gray, corners, (5, 5), (1, 1), criteria)
            obj_points.append(objp)
            img_points.append(corners)
            cv2.drawChessboardCorners(img, (Nx_cor, Ny_cor), corners, ret)
            cv2.imshow('img', img)
            cv2.waitKey(500)
    
    print('共计',len(img_points),'张图片')
    global mtx, dist
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)
    np.savez('../Calibresult/calibrate.npz', mtx=mtx, dist=dist[0:4])

def draw_axis(img, corners, imgpts):
        corners = corners.astype(np.int32)
        imgpts = imgpts.astype(np.int32)
        corner = tuple(corners[0].ravel())
        img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
        cv2.putText(img, "x", tuple(imgpts[0].ravel()), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
        cv2.putText(img, "y", tuple(imgpts[1].ravel()), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
        cv2.putText(img, "z", tuple(imgpts[2].ravel()), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return img

def Transfer():
    # 绘制坐标系
    axis_axis = np.float32([[20,0,0], [0,20,0], [0,0,-20]]).reshape(-1,3)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.0001)
    objp = np.zeros((Nx_cor * Ny_cor, 3), np.float32)
    objp[:, :2] = np.mgrid[0:Nx_cor * 5:5, 0:Ny_cor * 5:5].T.reshape(-1, 2)
    images = glob.glob('../Calibsource/T.jpg')
    if len(images) == 0:
        print('No Test Picture can be loading!')
        exit()
    img = cv2.imread(images[0])

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ret, corners = cv2.findChessboardCorners(binary, (Nx_cor, Ny_cor), None)

    global rmtx,tmtx
    if ret:
        imgp_temp = cv2.cornerSubPix(gray, corners, (5, 5), (1, 1), criteria) # 亚像素点
        if imgp_temp[0][0][0] < imgp_temp[1][0][0]:# 判断是否按照由左到右的顺序
            imgp = imgp_temp
        else:
            imgp = np.flipud(imgp_temp)

        ret, rmtx, tmtx, inliers = cv2.solvePnPRansac(objp, imgp, mtx, dist)
        # project 3D points to image plane
        imgpts, jac = cv2.projectPoints(axis_axis, rmtx, tmtx, mtx, dist)
        img = draw_axis(img, imgp, imgpts)
        cv2.imshow('img',img)
        cv2.waitKey(2000)
        cv2.imwrite('../Calibresult/gesture.png', img)

    print('imgp:',imgp[0])
    print('world:',cameraToWorld(mtx,rmtx,tmtx,imgp[0][0]))
    print("-----------------------------------------------------")
    np.savez('../Calibresult/Transfer.npz', rmtx = rmtx, tmtx = tmtx)

def DetectCircle(matrix, Rmatrix, tmatrix):
    image = glob.glob('../Calibsource/111.jpg')
    if len(image) == 0:
        print('No Detect Picture can be loading!')
        exit()
    img = cv2.imread(image[0])
    imgroi = img[0:960, 320:1280]  # roi [y,x]

    imgGray = cv2.cvtColor(imgroi, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(imgGray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # Cx = 0
    # Cy = 0
    find = False # 是否检测到圆的标志,False--->未检测到圆，True--->检测到圆
   
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # 工件大圆检测
        if 10000 < area < 50000:
            cv2.drawContours(imgroi, cnt, -1, (255, 30, 255), 2)  # 绘制外轮廓
            # peri = cv2.arcLength(cnt, True)
            # print('工件的周长是:', peri)
            (Cx, Cy), radius = cv2.minEnclosingCircle(cnt)
            Xcenter = (int(Cx), int(Cy))
            Sx = Cx + 320
            Sy = Cy
            circle_point = np.array([Sx, Sy], dtype=np.float32)
            radius = int(radius)
            cv2.circle(imgroi, Xcenter, radius, (255, 0, 0), 2)
            print("大圆中心坐标为：", Xcenter)
            find = True

        # 工件小圆检测
        if 300 < area < 1000:
            cv2.drawContours(imgroi, cnt, -1, (255, 0, 255), 2)  # 绘制外轮廓
            peri = cv2.arcLength(cnt, True)
            # print('圆的周长:',peri)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            # print('拐点坐标:',approx)
            # print('圆的拐点个数为:',len(approx))
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgroi, (x, y), (x + w, y + h), (0, 255, 0), 3)
            Rx = x + w / 2
            Ry = y + h / 2
            Ycenter = (int(Rx), int(Ry))
            print("小圆中心坐标为:", Ycenter)
            cv2.line(imgroi, (int(Cx), int(Cy)), (int(Rx), int(Ry)), (0, 255, 0), 2)
            a = np.array([int(Rx - Cx), int(Ry - Cy)])
            b = np.array([int(Cx), 0])
            cosangle = a.dot(b) / (np.linalg.norm(a) * np.linalg.norm(b))
            angle = np.arccos(cosangle) * 57.3
            if Cy < Ry:
                angle = 360 - angle
            cv2.putText(imgroi, '{}'.format(angle), Ycenter, cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)

    if find:
        print('圆心检测成功!')
        cv2.imwrite('../Calibresult/detectedCircle.jpg', imgroi)
        print('圆心坐标为:', circle_point)
        print('圆心对应世界坐标为:', cameraToWorld(matrix, Rmatrix, tmatrix, circle_point)[0][0])
        print(type(cameraToWorld(matrix, Rmatrix, tmatrix, circle_point)[0][0]))
        print(type(angle))
        print("-----------------------------------------------------")
    else:
        print('圆心检测失败!')
        print("-----------------------------------------------------")

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
    # worldpt.append(pt.T.tolist())
    worldpt.append(pt.T)
    return worldpt

if __name__ == '__main__':
    # 全局变量
    Nx_cor = 19  # 横向
    Ny_cor = 15  # 竖向

    # 标定，获取内参，同一相机内参矩阵固定
    try:
        npzfile = np.load('../Calibresult/calibrate.npz')
        mtx = npzfile['mtx']
        dist = npzfile['dist']
    except IOError:
        print("重新标定相机...")
        calibrate()

    # 获取外参
    try:
        npzfile1 = np.load('../Calibresult/Transfer.npz')
        rmtx = npzfile1['rmtx']
        tmtx = npzfile1['tmtx']
    except IOError:
        print("重新标定外参...")
        Transfer()

    DetectCircle(mtx, rmtx, tmtx)

    cv2.destroyAllWindows()