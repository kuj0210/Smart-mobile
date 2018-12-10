from observer import *
import time as tm
import wave
import numpy as np
import scipy.io.wavfile as wav
from numpy.lib import stride_tricks
import pylab
import pyaudio
import prediction_simulation

class Vo(Observer):
    # 사용자의 요청 구분 예)목소리들려줘 노래들려줘 구분, 외부 참조내용 내부에서 구분할때도 사용할것
    NAME = 'VO'
    PUSHCODE_P1 = NAME+"목소리 들려줘"
    PUSHCODE_P2 = NAME+"노래 들려줘"
    #PUSHCODE_P3 = NAME+"-ob3"

    # 녹음시(주변 소리 크기가 울음인지 소음인지 구분없이 클때) 정보.
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 512
    RECORD_SECONDS = 5
    DEVICE_INDEX = -1
    WAVE_OUTPUT_FILENAME = "file.wav"
    Recode_Value = 1000

    # 시간체크용 변수
    Cry_Time_Strat = 0
    Cry_Time_End = 0
    Noise_Time_Start = 0
    Noise_Time_End = 0
    Cry_Check = False
    Noise_Check = False
    Msg_Check = False

    def __init__(self,Push):
        self.EV_PUSH = Vo.NAME+" 관측 푸쉬"
        self.RQ_PUSH = Vo.NAME+" 요청처리 메세지"
        self.reSet(Push)
        self.mPush = Push

    #오버라이딩, 요청처리기능 만약 하위 클래스가 처리하는게 없다면 False 반환
    def processRequest(self, PUSHCODE):
        # 넘어오는 코드별로 분류하여 행동처리 PUSHCODE == PUSHCODE_P1 이런식으로
        try:
            if (PUSHCODE == self.PUSHCODE_P1): # 목소리 재생
                print("request vo")
                file_path = "voice.wav"
                self.wav_play(file_path)
                print("play done")
                tm.sleep(1)
                return self.RQ_PUSH + PUSHCODE +"요청 종료."
            elif (PUSHCODE == self.PUSHCODE_P2): #노래 재생
                print("request vo")
                file_path = "music.wav"
                self.wav_play(file_path)
                print("play done")
                tm.sleep(1)
                return self.RQ_PUSH + PUSHCODE + "요청 종료."
            else:
                return False
        except:
            print("Vo - request 에러")
            print("Vo - porcessRequest 에러")
            return False

    # 오버라이딩, 관측 중 푸쉬해야하는 상황이 발생하면 정의해둔 메세지 리턴
    def detectEnvironment(self):
        res = False
        # 녹화 및 분석.
        try:
            if (True):
                # detection_flag = self.recode()
                if self.recode():
                   res = self.detection2()

            if (res == False):
                return False
            else:  # 필요시 elif등 사용할것
                return res

        except:
            print("Vo - detection 에러")
            print("Vo - detectEnvironment 에러")
            return False
        # 적당한 메서드를 호출해서 알람발생을 해야한다면 알람에 들어갈 메세지 리턴하게할것
        # 반드시 위에 상수를 참조하여 쓸 걸



    def wav_play(self, path):
        CHUNK = 1024
        wf = wave.open(path, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        data = wf.readframes(CHUNK)
        while data:
            stream.write(data)
            data = wf.readframes(CHUNK)

        stream.stop_stream()
        stream.close()
        p.terminate()

    #녹음 메소드
    def recode(self):
        #이전 코드에서 추가 부분
        #울음 및 소음에 시간제한을 위해 추가
        # 각각 3분으로 설정
        self.Cry_Time_End = tm.time()
        self.Noise_Time_End = tm.time()
        cry_c = self.Cry_Time_End - self.Cry_Time_Strat
        noise_c = self.Noise_Time_End - self.Noise_Time_Start

        '''
        print("현재 cry_c")
        print(cry_c)
        print("현재 noise_c")
        print(noise_c)
        '''
        #밑의 60 == 1분 단위가 전부 초단위.
        if self.Noise_Check == True:
            if noise_c > 60 * 3:
                self.Noise_Check = False

        if self.Cry_Check == True:
            if cry_c > 60 * 3:
                self.Cry_Check = False

        #여기서 부터 이전코드
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            input_device_index=self.DEVICE_INDEX,
            frames_per_buffer=self.CHUNK)
        frames = []

        data = stream.read(self.CHUNK, exception_on_overflow=False)
        check = pylab.fromstring(data, 'int16')
        if (sum(abs(check)) / len(check)) < self.Recode_Value:
            stream.stop_stream()
            stream.close()
            audio.terminate()

            #여기도 추가분
            if self.Cry_Check == True and self.Msg_check == False:
                msg = "아이가 울지 않아요."
                self.Msg_Check == True

            return False
        for i in range(1, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK, exception_on_overflow=False)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        waveFile = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        return True

    #판단 후 결과 판단 메소드.
    def detection2(self): #현재 사용.
        ans = prediction_simulation.main()
        result = "non msg"
        if ans == 1 and self.Cry_Check == False:
            result = "아이가 울고 있어요."
            self.Cry_Time_Strat = tm.time()
            self.Cry_Check = True
            self.Msg_Check = False
            print(result)
            #self.mPush.insertMSG('ALL', result)

        elif ans == 0 and self.Noise_Check == False:
            result = "주변에 소음이 나네요."
            self.Noise_Check = True
            self.Noise_Time_Start = tm.time()
            print(result)
            #self.mPush.insertMSG('ALL', result)

        else :
            return False

        return result

if __name__ == "__main__":
    vi=Vo(Observer)
    print("Running Vo")
    vi.run()