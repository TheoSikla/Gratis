import re
import platform

try:
    re.search(r'\bWindows\b', platform.platform()).group()
    platform_type = "Windows"
    transform = "1000x600"
    path_escape = "/"
except AttributeError:
    try:
        re.search(r'\bLinux\b', platform.platform()).group()
        platform_type = "Linux"
        transform = "1100x600"
        path_escape = "/"
    except AttributeError:
        try:
            re.search(r'\bDarwin\b', platform.platform()).group()
            platform_type = "OSX"
            transform = "1000x600"
            path_escape = "/"
        except AttributeError:
            platform_type = "Unknown"
            transform = "1000x600"
            path_escape = "/"
