'''
    7.16 工业相机调试
'''
import numpy as np
import glob
import cv2

def calibrate():
    # 设置寻找亚像素角点的参数，采用的停止准则是最大迭代次数30和最大误差容限0.001
    criteria = (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.001)
    # 获取标定板角点的位置
    objp = np.zeros((Nx_cor * Ny_cor, 3), np.float32)
    objp[:, :2] = np.mgrid[0:Nx_cor*5:5, 0:Ny_cor*5:5].T.reshape(-1, 2)  # 将世界坐标系建在标定板上，所有点的Z坐标全部为0，所以只需要赋值x和y

    obj_points = []  # 存储3D点
    img_points = []  # 存储2D点

    images = sorted(glob.glob("../Calibsource/calib1.jpg"))
    # cv2.imshow('img',cv2.imread(images[0]))
    # cv2.waitKey(0)
    # images = cv2.imread('../Calibsource/calib*.jpg')
    for fname in images:
        # print(fname)
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
    # global mtx, dist, rvecs, tvecs
    global mtx,dist
    # 标定
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

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
    np.savez('../Calibresult/calibrate.npz', mtx=mtx, dist=dist[0:4])

# 得到相机的外参矩阵
def Transfer():
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((Nx_cor * Ny_cor, 3), np.float32)
    objp[:, :2] = np.mgrid[0:Nx_cor * 30:30, 0:Ny_cor * 30:30].T.reshape(-1, 2)

    print("外参标定时采用的内参矩阵为:\n",mtx)
    # 载入固定标定图
    images = glob.glob('../Calibsource/T.jpg')  # 选择需要标定的图片
    if len(images) == 0:
        print('No Test Picture can be loading!')
        exit()
    img = cv2.imread(images[0])
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # 灰度处理
    ret, corners = cv2.findChessboardCorners(gray, (Nx_cor, Ny_cor), None)  # 寻找角点
    print(ret)
    global rmtx,tmtx
    if ret:
        imgp = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), criteria)
        ret, rmtx, tmtx, inliers = cv2.solvePnPRansac(objp, imgp, mtx, dist)
        print('像素原点:',imgp[0][0])
        print('用户原点:',cameraToWorld(mtx,rmtx,tmtx,imgp[0][0])[0][0])
    print("-----------------------------------------------------")
    print(rmtx)
    # return rmtx,tmtx
    # np.savez('../Calibresult/Transfer.npz', rmtx = rmtx, tmtx = tmtx)

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
    pt[0][0] = worldPtPlaneReproject[0][0]
    pt[1][0] = worldPtPlaneReproject[1][0]
    pt[2][0] = 0  # 世界坐标系的Z轴坐标，一般设定为0
    worldpt.append(pt.T.tolist())
    # worldpt.append(pt.T())
    # print('worldpt:',worldpt)
    return worldpt

# 检测所截取图片中工件的圆心的像素坐标，并转换成世界坐标，最后返回图片编号，进入下一次循环
def DetectCircle( i, matrix, Rmatrix, tmatrix):
    # 载入图片
    image = glob.glob('../Calibresult/Circle%d.jpg' % i)
    if len(image) == 0:
        print('No Detect Picture can be loading!')
        exit()
    img = cv2.imread(image[0])

    imgroi = img[154:661, 299:965]  # roi [y,x]
    imgGray = cv2.cvtColor(imgroi, cv2.COLOR_BGR2GRAY)

    # 取工件圆心，采用contour算法实现
    ret, binary = cv2.threshold(imgGray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # print('contours:',contours)
    # print('hierarchy:',hierarchy)
    # print(np.size(contours))

    find = False # 是否检测到圆的标志,False--->未检测到圆，True--->检测到圆
    Rx = 0
    Ry = 0
    Cx = 0
    Cy = 0
    angle = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        # 工件大圆检测
        if 1000 < area < 500000:
            cv2.drawContours(imgroi, cnt, -1, (255, 30, 255), 2)  # 绘制外轮廓
            # peri = cv2.arcLength(cnt, True)
            # print('工件的周长是:', peri)
            (Cx, Cy), radius = cv2.minEnclosingCircle(cnt)
            Xcenter = (int(Cx), int(Cy))
            Sx = Cx + 299
            Sy = Cy + 154
            circle_point = np.array([Sx, Sy], dtype=np.float32)
            radius = int(radius)
            cv2.circle(imgroi, Xcenter, radius, (255, 0, 0), 2)
            # print("工件中心为：", Xcenter)
            find = True

        # 工件小圆检测
        if 100 < area < 1000:
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
            # print("圆心坐标为:", Ycenter)
            cv2.line(imgroi, (int(Cx), int(Cy)), (int(Rx), int(Ry)), (0, 255, 0), 2)
            a=np.array([int(Rx-Cx),int(Ry-Cy)])
            b = np.array([int(Cx),0])
            cosangle = a.dot(b)/(np.linalg.norm(a)*np.linalg.norm(b))
            angle = np.arccos(cosangle) * 57.3
            if Cy < Ry:
                angle = 360 - angle
            cv2.putText(imgroi, '{}'.format(angle), Ycenter, cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)

    if find:
        print('圆心检测成功!')
        cv2.imwrite('../Calibresult/detectedCircle%d.jpg'%i, imgroi)
        print('Save detectCircle%d.jpg'%i)
        print('圆心坐标为:', circle_point)
        print('圆心对应世界坐标为:', cameraToWorld(matrix, Rmatrix, tmatrix, circle_point)[0][0])
        print('图片detectedCircle%d中工件角度为:'%i, angle)
        print("-----------------------------------------------------")
        i += 1
        return i

    else:
        print('圆心检测失败!')
        print("-----------------------------------------------------")
        return i

if __name__ == '__main__':
    # 全局变量
    Nx_cor = 20  # 横向
    Ny_cor = 16  # 竖向

    rmtx = []
    tmtx = []

    # 标定，获取内参，同一相机内参矩阵固定
    try:
        npzfile = np.load('../Calibresult/calibrate.npz')
        mtx = npzfile['mtx']
        dist = npzfile['dist']
    except IOError:
        print("重新标定相机...")
        calibrate()

    # # 二次标定,获取相机-标定板外参
    # try:
    #     npzfile1 = np.load('../Calibresult/Transfer.npz')
    #     rmtx = npzfile1['rmtx']
    #     tmtx = npzfile1['tmtx']
    # except IOError:
    #     print("重新标定外参...")
    #     Transfer()

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)    # 载入视频
    cap.set(3,1280)
    cap.set(4,720)
    count = 1    # 图片编号初始化
    Tflag = 0
    # 按一下空格，打印此刻图片的圆心像素坐标转换成世界坐标
    # 最后按esc ord:27可以退出循环
    print('请按空格键获取外参...')
    while True:
        isCaptured, frame = cap.read()
        # print(frame.shape)
        cv2.imshow('frame', frame)
        k = cv2.waitKey(1)
        if k == ord(' '):
            print(Tflag)
            # 每次开机都要对外参进行校正
            if Tflag == 0:
                cv2.imwrite("../Calibsource/T.jpg", frame)
                print("开始标定外参...")
                Transfer()
                Tflag += 1
            else:
                print(rmtx)
                # 保存关键帧
                cv2.imwrite("../Calibresult/Circle%d.jpg" % count, frame)
                print('Save Circle%d.jpg' % count)
                # 检测圆心世界坐标值
                count = DetectCircle( count,mtx,rmtx,tmtx)
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
