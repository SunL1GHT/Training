import cv2

def cosine(xA,yA):
    L1 = 225
    L2 = 175
    L3 = 9
    c2 = (L1**2 + (L2+L3)**2 - (xA**2+yA**2)) / (2*L1*(L2+L3))
    fai = (xA**2 + yA**2 +L1**2-(L1+L3)**2) / (2*L1*(xA**2+yA**2)**0.5)



