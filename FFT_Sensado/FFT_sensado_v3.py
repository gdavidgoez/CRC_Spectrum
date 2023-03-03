#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FFT_sensado_v3
# Author: David Góez
# GNU Radio version: 3.8.2.0


from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import eng_notation
from gnuradio import qtgui
import sip
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import uhd
import time
from gnuradio.fft import logpwrfft
from gnuradio.qtgui import Range, RangeWidget
import threading

from gnuradio import qtgui
import numpy as np
class FFT_sensado_v3GRC(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "FFT_sensado_v3")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FFT_sensado_v3")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "FFT_sensado_v3GRC")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.variable_function = variable_function = 0
        self.samp_rate = samp_rate = 56e6
        self.nfft = nfft = 4096
        self.Frecuencia = Frecuencia = 100e6
        self.Average = Average = 0.07

        self.frec_val = self.Frecuencia
        self.tFrecuencia = self.Frecuencia
        self.fscan = 3900000000
        self.step = 56e6   # Aquí se establece el paso de muestreo para el escaneo dinámico
        ##################################################
        # Blocks
        ##################################################
        self.blocks_probe = blocks.probe_signal_vf(4096)
        self._Frecuencia_tool_bar = Qt.QToolBar(self)
        self._Frecuencia_tool_bar.addWidget(Qt.QLabel('Frecuencia' + ": "))
        self._Frecuencia_line_edit = Qt.QLineEdit(str(self.Frecuencia))
        self._Frecuencia_tool_bar.addWidget(self._Frecuencia_line_edit)
        self._Frecuencia_line_edit.returnPressed.connect(
            lambda: self.set_Frecuencia(eng_notation.str_to_num(str(self._Frecuencia_line_edit.text()))))
        self.top_grid_layout.addWidget(self._Frecuencia_tool_bar)
        self._Average_range = Range(0.001, 1, 0.001, 0.07, 200)
        self._Average_win = RangeWidget(self._Average_range, self.set_Average, 'Average', "counter_slider", float)
        self.top_grid_layout.addWidget(self._Average_win)
        def _variable_function_probe():
            ##########################################################################
            # Trabajar aquí
            ###########################################################################
            while True:

                val = self.blocks_probe.level()
                sint = np.array(val)
                if np.std(sint) != 0:
                    Umbral = np.mean(sint) + (np.max(sint) - np.mean(sint)) / 2.0
                    s = np.where(sint > Umbral, 1, -1)
                    print(np.where(s == 1))
                    if self.frec_val > self.fscan:
                        self.frec_val = self.Fstart
                    self.frec_val = self.frec_val + self.step
                    self.set_Frecuencia(self.frec_val)
                    print(self.frec_val)
                try:
                    self.set_variable_function(val)
                except AttributeError:
                    pass
                time.sleep(2)
                #time.sleep(1.0 / (10))
        _variable_function_thread = threading.Thread(target=_variable_function_probe)
        _variable_function_thread.daemon = True
        _variable_function_thread.start()

        self.uhd_usrp_source_0_0 = uhd.usrp_source(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0_0.set_center_freq(Frecuencia, 0)
        self.uhd_usrp_source_0_0.set_gain(38, 0)
        self.uhd_usrp_source_0_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0_0.set_bandwidth(56000000, 0)
        self.uhd_usrp_source_0_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0_0.set_time_unknown_pps(uhd.time_spec())
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            nfft,
            0,
            1.0,
            "x-Axis",
            "y-Axis",
            "",
            1 # Number of inputs
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0.set_y_axis(-140, 10)
        self.qtgui_vector_sink_f_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0.enable_grid(False)
        self.qtgui_vector_sink_f_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_win)
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
            sample_rate=samp_rate,
            fft_size=nfft,
            ref_scale=2,
            frame_rate=30,
            avg_alpha=Average,
            average=True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_probe, 0))
        self.connect((self.logpwrfft_x_0, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.logpwrfft_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "FFT_sensado_v3GRC")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_variable_function(self):
        return self.variable_function

    def set_variable_function(self, variable_function):
        self.variable_function = variable_function

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)
        self.uhd_usrp_source_0_0.set_samp_rate(self.samp_rate)

    def get_nfft(self):
        return self.nfft

    def set_nfft(self, nfft):
        self.nfft = nfft

    def get_Frecuencia(self):
        return self.Frecuencia

    def set_Frecuencia(self, Frecuencia):
        self.Frecuencia = Frecuencia
        Qt.QMetaObject.invokeMethod(self._Frecuencia_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.Frecuencia)))
        self.uhd_usrp_source_0_0.set_center_freq(self.Frecuencia, 0)

    def get_Average(self):
        return self.Average

    def set_Average(self, Average):
        self.Average = Average
        self.logpwrfft_x_0.set_avg_alpha(self.Average)





def main(top_block_cls=FFT_sensado_v3GRC, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
