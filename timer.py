import time

QUESTION_TIME_LIMIT = 30

def get_time_remaining(start_time):
    elapsed = time.time() - start_time
    return max(0, QUESTION_TIME_LIMIT - elapsed)

def get_time_bonus(start_time):
    elapsed = time.time() - start_time
    if elapsed <= 10:
        return 1.5
    elif elapsed <= 20:
        return 1.0
    else:
        return 0.5

def is_time_up(start_time):
    return time.time() - start_time >= QUESTION_TIME_LIMIT
