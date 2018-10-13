import time as tm
import wave
import numpy as np
import scipy.io.wavfile as wav
from numpy.lib import stride_tricks
import pylab
import pyaudio


class Vo():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 512
    RECORD_SECONDS = 5
    DEVICE_INDEX = -1
    WAVE_OUTPUT_FILENAME = "file.wav"
    Recode_Value = 1500

    Cry_Value_V = 50
    Cry_Value_B = 35
    Sick_Value = 80
    Hungry_Value = 65
    Sleepy_Value = 50

    def __init__(self):
        #self.reSet(Push)
        po = pyaudio.PyAudio()
        for index in range(po.get_device_count()):
            desc = po.get_device_info_by_index(index)
            if desc["name"] == "USB Audio Device":
                self.DEVICE_INDEX = index
                break
            


    def run(self):
        print("running vo")
        while (True):
            try:
                if (True):
                    detection_flag = self.recode()
                    if detection_flag:
                        self.detection2()
            except:
                print("Vo - detection 에러")
                continue



                    
    def wav_play(self,path):
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
        print("recode...")
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
        print("recode done")
        return True

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
        #print("cry_volum : ", cry_volum)
        #print("cry_bindo : ", cry_bindo)
        #print("timebins : ",timebins)
        #print("tcheck : ", tcheck)
        #print("maxnum2500 : ", maxnum2500)
        
        if cry_volum > self.Cry_Value_V and cry_bindo > self.Cry_Value_B:
            result = "울고 있어요."
        else:
            print("dont cry")
            return "don't cry"

        if cry_volum > self.Sick_Value:
            result = "아파서 " + result
        elif cry_volum > self.Hungry_Value:
            result = "배고파서 " + result
        elif cry_volum > self.Sleepy_Value:
            result = "졸려서 " + result
        else:
            result = "왜 우는지 모르겠어요 "

        #self.mPush.insertMSG('ALL', "아이가 %s" % result)
        #print("Vo sleep")
        #tm.sleep(1500)
        print(result)

        return result
    
vo = Vo()
vo.run()