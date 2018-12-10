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
    PUSHCODE_P1 = NAME+"노래"
    PUSHCODE_P2 = NAME+"목소리"
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
    
    Cry_Value_V = 50
    Cry_Value_B = 35
    Sound_Value = 45
    Sick_Value = 80
    Hungry_Value = 65
    Sleepy_Value = 50
    Vo_Noise_Start = 0
    Vo_Noise_End = 0
    Vo_Cry_Start = 0
    Vo_Cry_End = 0
    
    def __init__(self,Push):
        self.EV_PUSH = Vo.NAME+" 관측 푸쉬"
        self.RQ_PUSH = Vo.NAME+" 요청처리 메세지"
        self.reSet(Push)
        self.mPush = Push
        self.setStatToAnotherForImage()
        

    #오버라이딩, 요청처리기능 만약 하위 클래스가 처리하는게 없다면 False 반환
    def processRequest(self, PUSHCODE):
        # 넘어오는 코드별로 분류하여 행동처리 PUSHCODE == PUSHCODE_P1 이런식으로
        try:
            if (PUSHCODE == self.PUSHCODE_P1): # 노래 재생
                print("request vo")
                file_path = "music.wav"
                self.wav_play(file_path)
                print("play done")
                tm.sleep(1)
                #here
                # return self.RQ_PUSH + PUSHCODE +" 요청 종료."
                return "노래 재생이 종료됬어요"
            elif (PUSHCODE == self.PUSHCODE_P2): #목소리 재생
                print("request vo")
                file_path = "voice.wav"
                self.wav_play(file_path)
                print("play done")
                tm.sleep(1)
                #here
                # return self.RQ_PUSH + PUSHCODE + " 요청 종료."
                return "목소리 재생이 종료됬어요"
            else:
                return False
        except:
            print("Vo - request 에러")
            print("Vo - porcessRequest 에러")
            return False

    # 오버라이딩, 관측 중 푸쉬해야하는 상황이 발생하면 정의해둔 메세지 리턴
    def detectEnvironment(self):
        res = False

        # 록 부분. 각각 5분.
        if self.Noise_Check == True:
            self.Vo_Noise_End = tm.time()
        if self.Vo_Noise_End - self.Vo_Noise_Start > 300:
            self.Noise_Check = False

        if self.Cry_Check == True:
            self.Vo_Cry_End = tm.time()
        if self.Vo_Noise_End - self.Vo_Noise_Start > 300:
            self.Cry_Check = False
        
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
        #예외처리
        except:
            print("Vo - detection 에러")
            print("Vo - detectEnvironment 에러")
            return False
        # 적당한 메서드를 호출해서 알람발생을 해야한다면 알람에 들어갈 메세지 리턴하게할것
        # 반드시 위에 상수를 참조하여 쓸 걸

    #음성, 노래 파일 실행 메소드.
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

    #현 녹음 파일을 단시간 푸리에 변환(STFT) 하기 위한 메소드
    def stft(self, sig, frameSize, overlapFac=0.5, window=np.hanning):
        win = window(frameSize)
        hopSize = int(frameSize - np.floor(overlapFac * frameSize))
        samples = np.append(np.zeros(int(np.floor(frameSize / 2.0))), sig)
        cols = np.ceil((len(samples) - frameSize) / float(hopSize)) + 1
        samples = np.append(samples, np.zeros(frameSize))

        frames = stride_tricks.as_strided(samples, shape=(int(cols), frameSize),
                                          strides=(samples.strides[0] * hopSize, samples.strides[0])).copy()
        frames *= win

        return np.fft.rfft(frames)

    #주파수, 음향을 얻기 위한 메소드
    def logscale_spec(self, spec, sr=44100, factor=20.):
        timebins, freqbins = np.shape(spec)

        scale = np.linspace(0, 1, freqbins) ** factor
        scale *= (freqbins - 1) / max(scale)
        scale = np.unique(np.round(scale))

        newspec = np.complex128(np.zeros([timebins, len(scale)]))
        for i in range(0, len(scale)):
            if i == len(scale) - 1:
                newspec[:, i] = np.sum(spec[:, int(scale[i]):], axis=1)
            else:
                newspec[:, i] = np.sum(spec[:, int(scale[i]):int(scale[i + 1])], axis=1)

        allfreqs = np.abs(np.fft.fftfreq(freqbins * 2, 1. / sr)[:freqbins + 1])
        freqs = []
        for i in range(0, len(scale)):
            if i == len(scale) - 1:
                freqs += [np.mean(allfreqs[int(scale[i]):])]
            else:
                freqs += [np.mean(allfreqs[int(scale[i]):int(scale[i + 1])])]

        return newspec, freqs

    #울음 분석 및 분류. 울음이 발견되면 15초 동안 정지.
    def detection2(self):
        samplerate, samples = wav.read(self.WAVE_OUTPUT_FILENAME)
        binsize = 2 ** 10

        s = self.stft(samples, binsize)
        sshow, freq = self.logscale_spec(s, sr=samplerate, factor=1.0)

        ims = 20. * np.log10(np.abs(sshow) / 10e-6)
        timebins, freqbins = np.shape(ims)

        time = ((timebins * len(samples) / timebins) + (0.5 * binsize)) / samplerate
        timei = ((len(samples) / timebins) + (0.5 * binsize)) / samplerate
        timei /= 2

        maxnum = 0
        fr25 = 0
        tmp = 0
        fullcount = 0

        for i in range(timebins):
            for j in range(freqbins):
                if i == 0:
                    if freq[j] < 2500:
                        tmp = j
                if ims[i][j] < 200:
                    ims[i][j] = 0
                else:
                    maxnum += 1
                    fullcount += ims[i][j]

        ti = 0
        maxval = 0
        maxnum2500 = 0
        fullcount2500 = 0
        t_if = True
        tcheck = 0
        for i in range(timebins):
            for j in range(0, tmp + 1):
                if maxval < ims[i][j]:
                    maxval = ims[i][j]
                    ti = i
                if ims[i][j] >= 210:
                    maxnum2500 += 1
                    fullcount2500 += ims[i][j]
                    if t_if != i:
                        t_if = i
                        tcheck += 1

        cry_bindo = tcheck / timebins * 100
        cry_volum = maxnum2500 / timebins * 100

        result = 0
        if cry_volum > self.Cry_Value_V and cry_bindo > self.Cry_Value_B:
            result = "울고 있어요."
            if self.Cry_Check == True:
                return False
            self.Cry_Check = True
            self.Vo_Cry_Start = tm.time()
        else:
            if self.Noise_Check == True:
                return False
            self.Noise_Check = True
            self.Vo_Noise_Start = tm.time()
            return "주변 소음이 나네요."

        if cry_volum > self.Sick_Value:
            result = "아파서 " + result
        elif cry_volum > self.Hungry_Value:
            result = "배고파서 " + result
        elif cry_volum > self.Sleepy_Value:
            result = "졸려서 " + result
        else:
            result = "왜 우는지 모르겠어요 "

        print(result)
        #self.mPush.insertMSG('ALL', "아이가 %s" % result)
        print("Vo sleep")
        tm.sleep(3)

        return result

if __name__ == "__main__":
    vi=Vo(Observer)
    print("Running Vo")
    vi.run()