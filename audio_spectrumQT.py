import numpy as np
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget
from scipy.fftpack import fft
from scipy.io import wavfile
import sys


class AudioStream(object):
    def __init__(self, wav_file_path):
        # pyqtgraph stuff
        pg.setConfigOptions(antialias=True)
        self.traces = dict()
        self.app = QtWidgets.QApplication(sys.argv)
        self.win = GraphicsLayoutWidget(title='Spectrum Analyzer')

        self.win.setGeometry(5, 115, 1910, 1070)

        wf_xlabels = [(0, '0'), (2048, '2048'), (4096, '4096')]
        wf_xaxis = pg.AxisItem(orientation='bottom')
        wf_xaxis.setTicks([wf_xlabels])

        wf_ylabels = [(0, '0'), (127, '128'), (255, '255')]
        wf_yaxis = pg.AxisItem(orientation='left')
        wf_yaxis.setTicks([wf_ylabels])

        sp_xlabels = [
            (np.log10(10), '10'), (np.log10(100), '100'),
            (np.log10(1000), '1000'), (np.log10(22050), '22050')
        ]
        sp_xaxis = pg.AxisItem(orientation='bottom')
        sp_xaxis.setTicks([sp_xlabels])

        self.waveform = self.win.addPlot(
            title='WAVEFORM', row=1, col=1, axisItems={'bottom': wf_xaxis, 'left': wf_yaxis},
        )
        self.spectrum = self.win.addPlot(
            title='SPECTRUM', row=2, col=1, axisItems={'bottom': sp_xaxis},
        )

        # Read .wav file
        wave_data = wavfile.read(wav_file_path)
        self.wav_data = wave_data[1][:, 0]  # Use only the first channel if stereo

        self.CHUNK = 1024  # Adjust the chunk size as needed
        self.x = np.arange(0, self.CHUNK, 1)
        self.f = np.linspace(0, wave_data[0], self.CHUNK)

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            self.app.exec()

    def set_plotdata(self, name, data_x, data_y):
        if name in self.traces:
            self.traces[name].setData(data_x, data_y)
        else:
            if name == 'waveform':
                self.traces[name] = self.waveform.plot(pen='c', width=3)
                self.waveform.setYRange(0, 255, padding=0)
                self.waveform.setXRange(0, self.CHUNK, padding=0.005)
            if name == 'spectrum':
                self.traces[name] = self.spectrum.plot(pen='m', width=3)
                self.spectrum.setLogMode(x=True, y=True)
                self.spectrum.setYRange(-4, 0, padding=0)
                self.spectrum.setXRange(
                    np.log10(20), np.log10(self.f[-1]), padding=0.005)

    # def update(self):
    #     if len(self.wav_data) >= self.CHUNK:
    #         wf_data = self.wav_data[:self.CHUNK]
    #         self.wav_data = self.wav_data[self.CHUNK:]

    #         wf_data = np.array(wf_data, dtype='int32') + 128
    #         self.set_plotdata(name='waveform', data_x=self.x, data_y=wf_data)

    #         sp_data = fft(np.array(wf_data, dtype='int32') - 128)
    #         sp_data = np.abs(sp_data[:int(self.CHUNK / 2)]) * 2 / (128 * self.CHUNK)
    #         self.set_plotdata(name='spectrum', data_x=self.f, data_y=sp_data)
    def update(self):
        if len(self.wav_data) >= self.CHUNK:
            wf_data = self.wav_data[:self.CHUNK]
            self.wav_data = self.wav_data[self.CHUNK:]

            wf_data = np.array(wf_data, dtype='int32') + 128
            self.set_plotdata(name='waveform', data_x=self.x, data_y=wf_data)

            sp_data = fft(np.array(wf_data, dtype='int32') - 128)
            sp_data = np.abs(sp_data[:int(self.CHUNK / 2)]) * 2 / (128 * self.CHUNK)
            self.set_plotdata(name='spectrum', data_x=self.f[:int(self.CHUNK / 2)], data_y=sp_data)


    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)
        self.start()


if __name__ == '__main__':
    wav_file_path = r"C:\Users\rajka\Downloads\Sunflower-(Spider-Man_-Into-the-Spider-Verse)(PagalWorld).wav"
    audio_app = AudioStream(wav_file_path)
    audio_app.animation()
