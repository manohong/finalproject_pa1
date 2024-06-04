import time

class Timer:
    def __init__(self):
        self.start_time = 0
        self.paused_time = 0
        self.running = False
        self.paused = False

    def start(self):
        if not self.running:
            self.start_time = time.time()
            self.running = True
            self.paused = False

    def pause(self):
        if self.running and not self.paused:
            self.paused_time = time.time() - self.start_time
            self.paused = True

    def resume(self):
        if self.running and self.paused:
            self.start_time = time.time() - self.paused_time
            self.paused = False

    def stop(self):
        if self.running:
            self.running = False
            self.paused = False

    def get_elapsed_time(self):
        if self.running:
            if self.paused:
                return self.paused_time
            else:
                return time.time() - self.start_time
        return 0

