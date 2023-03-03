import time

def generate_ref():
    return f'ref_{time.strftime("%Y%m%d%H%M%S")}-{hex(int(time.time()))}'
