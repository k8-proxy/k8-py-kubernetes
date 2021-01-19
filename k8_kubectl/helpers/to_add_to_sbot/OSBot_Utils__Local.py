import warnings


def ignore_warning__unclosed_ssl():
    warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")

def lower(target : str):
    if target:
        return target.lower()
    return ""