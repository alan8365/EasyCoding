def hello_world():
    import os
    import subprocess
    from django.conf import settings
    # return subprocess.check_output(['uname', '-a'])
    return subprocess.check_output(['mount'], stderr=subprocess.STDOUT)