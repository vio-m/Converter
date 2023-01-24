import re

def url_is_valid(str):
    regex = ("^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$")
    p = re.compile(regex)
    if (str == None):
        return False
    if (re.search(p, str)):
        return True
    else:
        return False