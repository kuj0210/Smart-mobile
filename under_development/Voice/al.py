import time

a = time.localtime()
print(a)
print(type(a.tm_hour))
print(type(a.tm_min))

#여기서 부터.
Alarm_On = True
al_H = 9 + 12
al_M = 9
flag = True

#current.tm_hour 는 시간 (0~23)
#current.tm_min 은 분 (0~59)
#a = time.localtime() 에서 현재의 날짜나 시간을 다 가져올 수 있음.
#print 변수 위에 작성을 해둬서 내용 참고 가능.
#미세한 설정을 하고 싶다면 그냥 사용 가능(ex:tm_wday 는 날짜 0~ 6 까지 월~일)
#참고 http://devanix.tistory.com/297
def alarm_Rpi(h,m):
    current = time.localtime()
    if current.tm_hour == al_H and current.tm_min == al_M:
        """
    and 0 < current.tm_sec < 30:
    and current.tm_wday == 3:
    """
        print("alarm on!")
        return False
    else:
        return True


#while문 안에서 돌지만 지속적으로 다른건 다 하고(while 안에 있는거.) 알람울리면 종료.
while(flag):
    time.sleep(1)
    print("no alarm")
    if Alarm_On == True:
        flag = alarm_Rpi(al_H,al_M)







