from loguru import logger

current_session = None

is_someone_using = False

def get_current_session():
    global current_session
    return current_session

def set_current_session(session):
    global current_session
    current_session = session

def someone_using():
    global is_someone_using
    return is_someone_using

def set_someone_using(bool):
    global is_someone_using
    is_someone_using = bool