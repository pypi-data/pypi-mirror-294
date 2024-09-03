import warnings


__version__ = 0.9

IP = '127.0.0.1'
GROUP = "238.3.2.2"
try:
    with open("/etc/product", "r") as file:
        for line in file:
            key, value = line.split("=", 1)
            if key == "MCAST_GROUP":
                GROUP = value.strip()
                break
except FileNotFoundError:
    def formatwarning(message, category, *args, **kwargs):
        return f"{category.__name__}: [W] {message}\n"
    warnings.formatwarning = formatwarning
    warnings.warn("Remote mode is activated. Please, set your ip and multicast group properly to use!", category=UserWarning)
    
    
