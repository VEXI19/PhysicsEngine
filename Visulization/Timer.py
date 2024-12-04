from PyQt5 import QtCore


class TimeLine(QtCore.QObject):
    frameChanged = QtCore.pyqtSignal(int)

    def __init__(self, interval=50, loopCount=1, parent=None):
        super(TimeLine, self).__init__(parent)
        self._startFrame = 0
        self._endFrame = 0
        self._loopCount = loopCount
        self._timer = QtCore.QTimer(self, timeout=self.on_timeout)
        self._counter = 0
        self._loop_counter = 0
        self.setInterval(interval)
        self.paused = False  # Pause flag

    def on_timeout(self):
        if not self.paused:
            if self._startFrame <= self._counter < self._endFrame:
                self.frameChanged.emit(self._counter)
                self._counter += 1
            else:
                self._counter = 0
                self._loop_counter += 1
                if self._loopCount > 0 and self._loop_counter >= self._loopCount:
                    self._timer.stop()

    def setLoopCount(self, loopCount):
        self._loopCount = loopCount

    def loopCount(self):
        return self._loopCount

    def setInterval(self, interval):
        self._timer.setInterval(interval)

    def interval(self):
        return self._timer.interval()

    def setFrameRange(self, startFrame, endFrame):
        self._startFrame = startFrame
        self._endFrame = endFrame

    @QtCore.pyqtSlot()
    def start(self):
        self._counter = 0
        self._loop_counter = 0
        self._timer.start()

    def pause(self):
        self.paused = True
        self._timer.stop()

    def resume(self):
        self.paused = False
        self._timer.start()

