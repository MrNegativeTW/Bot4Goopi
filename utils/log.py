import datetime

class LogUtils:
    @staticmethod
    def log(level, *messages):
        timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        log_message = f"[{timestamp}][{level}] " + " ".join(map(str, messages))
        print(log_message)

    @staticmethod
    def log_info(*messages):
        LogUtils.log("INFO", *messages)

    @staticmethod
    def log_warn(*messages):
        LogUtils.log("WARN", *messages)

    @staticmethod
    def log_err(*messages):
        LogUtils.log("ERR", *messages)
