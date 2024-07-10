import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta


class TimedRotatingFileHandlerWithCleanup(TimedRotatingFileHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def doRollover(self):
        super().doRollover()
        self.cleanup_old_logs()

    def cleanup_old_logs(self):
        now = datetime.now()
        for filename in os.listdir(self.baseFilename.rsplit(".", 1)[0]):
            filepath = os.path.join(self.baseFilename.rsplit(".", 1)[0], filename)
            if os.path.isfile(filepath):
                file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                if now - file_time > timedelta(days=7):
                    os.remove(filepath)
                    print(f"Deleted old log file: {filepath}")
