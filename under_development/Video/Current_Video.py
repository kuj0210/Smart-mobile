import numpy as np
import cv2
import time

cap = cv2.VideoCapture('test2.mp4') #웹켐쓸거면인자 0 , 영상파일 열거면 이름 넣을것
fgbg = cv2.createBackgroundSubtractorMOG2()

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


A = []
x = 1
y = 1
f = 0
o = 0
rx = 0  #세이프티존 왼쪽상단점 x좌표
ry = 0  #세이프티존 왼쪽상단점 y좌표
w = 0   #세이프티존 너비
h = 0   #세이프티존 높이
sf = 5  #세이프티존 생성시 기준프레임
of = 1  #관측 프레임
sz_size = 100   #세이프티존 사이즈%
prevTime = time.time()

#존이탈 검사 함수
def out(mx, my) :
    if mx > rx and mx < rx + w and my > ry  and my < ry + h :
        return 0
    else :
        return 1


while (1):
    curTime = time.time()
    t = curTime - prevTime

    f = f + 1

    #관측프레임 설정
    if f != sf :
        if f%of != 0 and o == 0 :
            continue
        if f%5 != 0 :
            continue

    #영상처리
    ret, frame = cap.read()
    frgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret2, thr = cv2.threshold(frgray, 127, 255, 0)
    kernel = np.ones((3, 3), np.float32) / 25
    dst = cv2.filter2D(frgray, -1, kernel)
    edges = cv2.Canny(dst, 50, 100)
    _, contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #moment이용 무게중심을 구함
    max_area = 0;
    ci = 0
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if (area > max_area):
            max_area = area
            ci = i
    contours = contours[ci]
    mmt = cv2.moments(contours)
    if mmt['m00'] != 0 :
        mx = int(mmt['m10']/mmt['m00'])
        my = int(mmt['m01']/mmt['m00'])

    #세이프티존 생성
    if f == sf :
        for i in range(0,width):
            for j in range(0,height):
                if edges[j,i] == 0:
                    edges[j,i] = 255
                else :
                    edges[j,i] = 0
                    A.append([i, j])
        B = np.array(A)
        rx, ry, w, h = cv2.boundingRect(B)

        # 세이프티존 크기 설정
        tmp_rx = rx
        tmp_ry = ry
        rx = tmp_rx + int((100 - sz_size) / 200 * w)
        ry = tmp_ry + int((100 - sz_size) / 200 * h)
        w = sz_size / 100 * w
        h = sz_size / 100 * h


    #존이탈 검사
    if out(mx, my) == 1 :
        o = o + 1
    else :
        o = 0
    if o > 30 :
        print("존이탈!!!!")
        o = 0

    if f > sf:
        cv2.rectangle(frame, (int(mx), int(my)), (int(mx), int(my)), (0, 0, 255), 8)
        cv2.rectangle(frame, (int(rx), int(ry) ), (int(rx+w), int(ry+h)), (0, 0, 255), 3)

    cv2.imshow('fgmask', frame)
    #cv2.imshow('frame', fgmask)
    #cv2.imshow('dst2', dst2)
    cv2.imshow('EDGES', edges)


    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


print(A)
cap.release()
cv2.destroyAllWindows()
