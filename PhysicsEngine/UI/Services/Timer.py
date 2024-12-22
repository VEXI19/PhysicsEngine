from PyQt5 import QtCore


class TimeLine(QtCore.QObject):
    """
    TimeLine class is a custom class that emits a signal frameChanged(int) every interval.

    Attributes:
        frameChanged (pyqtSignal): signal emitted every interval
        _startFrame (int): start frame of the timeline
        _endFrame (int): end frame of the timeline
        _loop_count (int): number of loops to repeat the timeline
        _timer (QTimer): timer to emit signal
        _counter (int): current frame number
        _loop_counter (int): current loop number
        interval (int): interval between frames
        paused (bool): pause flag
    """
    frameChanged = QtCore.pyqtSignal(int)

    def __init__(self, interval: int = 50, loop_count: int = 1, parent: QtCore.QObject = None):
        """
        Constructor of TimeLine class

        Args:
            interval (int): interval between frames
            loop_count (int): number of loops to repeat the timeline
            parent (QObject): parent object
        """
        super(TimeLine, self).__init__(parent)
        self._startFrame = 0
        self._endFrame = 0
        self._loop_count = loop_count
        self._timer = QtCore.QTimer(self, timeout=self.on_timeout)
        self._counter = 0
        self._loop_counter = 0
        self.interval = interval
        self.paused = False  # Pause flag

    def on_timeout(self) -> None:
        """
        Slot function to emit frameChanged signal
        """

        if not self.paused:
            if self._startFrame <= self._counter < self._endFrame:
                self.frameChanged.emit(self._counter)
                self._counter += 1
            else:
                self._counter = 0
                self._loop_counter += 1
                if self._loop_count > 0 and self._loop_counter >= self._loop_count:
                    self._timer.stop()

    @property
    def loop_count(self) -> int:
        """
        Returns number of loops to repeat the timeline

        Returns:
            int: number of loops to repeat the timeline
        """
        return self._loop_count

    @loop_count.setter
    def loop_count(self, value: int) -> None:
        """
        Sets number of loops to repeat the timeline

        Args:
            value (int): number of loops to repeat the timeline
        """

        self._loop_count = value

    @property
    def interval(self) -> int:
        """
        Returns interval between frames

        Returns:
            int: interval between frames
        """

        return self._timer.interval()

    @interval.setter
    def interval(self, value: int) -> None:
        """
        Sets interval between frames

        Args:
            value (int): interval between frames
        """

        self._timer.setInterval(value)

    def set_frame_range(self, start_frame: int, end_frame: int) -> None:
        """
        Sets start and end frame of the timeline

        Args:
            start_frame (int): start frame
            end_frame (int): end frame
        """

        self._startFrame = start_frame
        self._endFrame = end_frame

    @QtCore.pyqtSlot()
    def start(self) -> None:
        """
        Starts the timeline
        """

        self._counter = 0
        self._loop_counter = 0
        self._timer.start()

    def pause(self) -> None:
        """
        Pauses the timeline
        """

        self.paused = True
        self._timer.stop()

    def resume(self) -> None:
        """
        Resumes the timeline
        """

        self.paused = False
        self._timer.start()

