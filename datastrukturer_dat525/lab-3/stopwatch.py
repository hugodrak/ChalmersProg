import time

class Stopwatch:
    """Measures the time that a given piece of code takes."""

    _start: float

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset the elapsed time to 0."""

        self._start = time.perf_counter()

    def elapsed_time(self):
        """Returns the elapsed time in seconds."""

        now = time.perf_counter()
        return now - self._start

    def finished(self, task):
        """Prints a timing report and resets the elapsed time to 0."""

        print("%s took %.2f seconds." % (task, self.elapsed_time()))
        self.reset()
