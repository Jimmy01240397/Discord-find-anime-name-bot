import sys
import time

class Stopwatch:

    # Construct self and start it running.
    def __init__(self):
        self._creationTime = time.time()  # Creation time
        self._endTime = 0

    def stop(self):
        self._endTime = time.time()

    def start(self):
        if self._creationTime == 0:
            self._creationTime = time.time()  # Creation time
        else:
            self._creationTime = time.time() - self._endTime + self._creationTime

        self._endTime = 0

    def reset(self):
        self._creationTime = 0  # Creation time
        self._endTime = 0
    
    def restart(self):
        self._creationTime = time.time()  # Creation time
        self._endTime = 0

    # Return the elapsed time since creation of self, in seconds.
    def time(self):
        if self._creationTime == 0:
            return 0
        elif self._endTime == 0:
            return time.time() - self._creationTime
        else:
            return self._endTime - self._creationTime

