import cv2
import numpy as np
import matplotlib.pyplot as plt

pos = np.array([
        [10,    50],
        [12,    49],
        [11,    52],
        [13,    52.2],
        [12.9,  50]], np.float32)

'''
它有3个输入参数，
dynam_params：状态空间的维数，这里为2；
measure_param：测量值的维数，这里也为2;
control_params：控制向量的维数，默认为0。由于这里该模型中并没有控制变量，因此也为0。
'''
kalman = cv2.KalmanFilter(2,2)

kalman.measurementMatrix = np.array([[1,0],[0,1]],np.float32)
kalman.transitionMatrix = np.array([[1,0],[0,1]], np.float32)
kalman.processNoiseCov = np.array([[1,0],[0,1]], np.float32) * 1e-3
kalman.measurementNoiseCov = np.array([[1,0],[0,1]], np.float32) * 0.01
'''
kalman.measurementNoiseCov为测量系统的协方差矩阵，方差越小，预测结果越接近测量值，
kalman.processNoiseCov为模型系统的噪声，噪声越大，预测结果越不稳定，越容易接近模型系统预测值，且单步变化越大，相反，若噪声小，则预测结果与上个计算结果相差不大。
'''

kalman.statePre = np.array([[6],[6]],np.float32)

for i in range(len(pos)):
    mes = np.reshape(pos[i,:],(2,1))

    x = kalman.correct(mes)

    y = kalman.predict()
    print (kalman.statePost[0],kalman.statePost[1])
    print (kalman.statePre[0],kalman.statePre[1])
    print ('measurement:\t',mes[0],mes[1])
    print ('correct:\t',x[0],x[1])
    print ('predict:\t',y[0],y[1])
    print ('='*30)

# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
#
# frame = np.zeros((800, 800, 3), np.uint8)
# last_mes = current_mes = np.array((2, 1), np.float32)
# last_pre = current_pre = np.array((2, 1), np.float32)
#
#
# def mousemove(event, x, y, s, p):
#     global frame, current_mes, mes, last_mes, current_pre, last_pre
#     last_pre = current_pre
#     last_mes = current_mes
#     current_mes = np.array([[np.float32(x)], [np.float32(y)]])
#
#     kalman.correct(current_mes)
#     current_pre = kalman.predict()
#
#     lmx, lmy = last_mes[0], last_mes[1]
#     lpx, lpy = last_pre[0], last_pre[1]
#     cmx, cmy = current_mes[0], current_mes[1]
#     cpx, cpy = current_pre[0], current_pre[1]
#     cv2.line(frame, (lmx, lmy), (cmx, cmy), (0, 200, 0))
#     cv2.line(frame, (lpx, lpy), (cpx, cpy), (0, 0, 200))
#
#
# cv2.namedWindow("Kalman")
# cv2.setMouseCallback("Kalman", mousemove)
# kalman = cv2.KalmanFilter(4, 2)
# kalman.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
# kalman.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
# kalman.processNoiseCov = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32) * 0.003
# kalman.measurementNoiseCov = np.array([[1, 0], [0, 1]], np.float32) * 1
#
# while True:
#     cv2.imshow('Kalman', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cv2.destroyAllWindows()

### 由于pip安装导致，使用sudo apt install libopencv-dev python3-opencv

# import cv2
# import numpy as np
#
# # 创建一个空帧，定义(700, 700, 3)画图区域
# frame = np.zeros((700, 700, 3), np.uint8)
#
# # 初始化测量坐标和鼠标运动预测的数组
# last_measurement = current_measurement = np.array((2, 1), np.float32)
# last_prediction = current_prediction = np.zeros((2, 1), np.float32)
#
# # 定义鼠标回调函数，用来绘制跟踪结果
# def mousemove(event, x, y, s, p):
#     global frame, current_measurement, measurements, last_measurement, current_prediction, last_prediction
#     last_prediction = current_prediction # 把当前预测存储为上一次预测
#     last_measurement = current_measurement # 把当前测量存储为上一次测量
#     current_measurement = np.array([[np.float32(x)], [np.float32(y)]]) # 当前测量
#     kalman.correct(current_measurement) # 用当前测量来校正卡尔曼滤波器
#     current_prediction = kalman.predict() # 计算卡尔曼预测值，作为当前预测
#
#     lmx, lmy = last_measurement[0], last_measurement[1] # 上一次测量坐标
#     cmx, cmy = current_measurement[0], current_measurement[1] # 当前测量坐标
#     lpx, lpy = last_prediction[0], last_prediction[1] # 上一次预测坐标
#     cpx, cpy = current_prediction[0], current_prediction[1] # 当前预测坐标
#
#     # 绘制从上一次测量到当前测量以及从上一次预测到当前预测的两条线
#     cv2.line(frame, (lmx, lmy), (cmx, cmy), (255, 0, 0)) # 蓝色线为测量值
#     cv2.line(frame, (lpx, lpy), (cpx, cpy), (255, 0, 255)) # 粉色线为预测值
#
# # 窗口初始化
# cv2.namedWindow("kalman_tracker")
#
# # opencv采用setMouseCallback函数处理鼠标事件，具体事件必须由回调（事件）函数的第一个参数来处理，该参数确定触发事件的类型（点击、移动等）
# cv2.setMouseCallback("kalman_tracker", mousemove)
#
# kalman = cv2.KalmanFilter(4, 2) # 4：状态数，包括（x，y，dx，dy）坐标及速度（每次移动的距离）；2：观测量，能看到的是坐标值
# kalman.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32) # 系统测量矩阵
# kalman.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32) # 状态转移矩阵
# kalman.processNoiseCov = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)*0.003 # 系统过程噪声协方差
# kalman.measurementNoiseCov = np.array([[1,0],[0,1]], np.float32) * 1
#
# while True:
#     cv2.imshow("kalman_tracker", frame)
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'):
#         break
# cv2.destroyAllWindows()



### 一维卡尔曼
# import numpy as np
# import matplotlib.pyplot as plt
#
#
# class kalman_filter:
#     def __init__(self, Q, R):
#         self.Q = Q
#         self.R = R
#
#         self.P_k_k1 = 1
#         self.Kg = 0
#         self.P_k1_k1 = 1
#         self.x_k_k1 = 0
#         self.ADC_OLD_Value = 0
#         self.Z_k = 0
#         self.kalman_adc_old = 0
#
#     def kalman(self, ADC_Value):
#
#         self.Z_k = ADC_Value
#
#         if (abs(self.kalman_adc_old - ADC_Value) >= 60):
#             self.x_k1_k1 = ADC_Value * 0.382 + self.kalman_adc_old * 0.618
#         else:
#             self.x_k1_k1 = self.kalman_adc_old;
#
#         self.x_k_k1 = self.x_k1_k1
#         self.P_k_k1 = self.P_k1_k1 + self.Q
#
#         self.Kg = self.P_k_k1 / (self.P_k_k1 + self.R)
#
#         kalman_adc = self.x_k_k1 + self.Kg * (self.Z_k - self.kalman_adc_old)
#         self.P_k1_k1 = (1 - self.Kg) * self.P_k_k1
#         self.P_k_k1 = self.P_k1_k1
#
#         self.kalman_adc_old = kalman_adc
#
#         return kalman_adc
#
#
# if __name__ == '__main__':
#     kalman_filter = kalman_filter(0.001, 0.1)
#     a = [100] * 200
#     array = np.array(a)
#
#     s = np.random.normal(0, 15, 200)
#     # print(s)
#     test_array = array + s
#     adc = []
#     for i in range(200):
#         adc.append(kalman_filter.kalman(test_array[i]))
#
#     print(adc[199])
#     plt.plot(adc)
#     plt.plot(array)
#     plt.plot(test_array) # 噪声
#     plt.show()

