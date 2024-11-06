import datetime

def log_info(*messages):
    current_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    message_content = " ".join(str(msg) for msg in messages)
    print(f"[{current_time}][Info] {message_content}")