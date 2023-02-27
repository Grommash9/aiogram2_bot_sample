import os.path
import os
import subprocess
import sys
from typing import List
from os.path import dirname, abspath

parent_path = dirname(dirname(abspath(__file__)))

repository_name = os.path.basename(dirname(dirname(abspath(__file__))))


for package in os.listdir(parent_path):
    if os.path.isdir(os.path.join(parent_path, package)) \
            and os.path.exists(os.path.join(parent_path, package, '__main__.py')):
        if package == 'bot_app':
            file_name = repository_name
        else:
            file_name = package

        sys_reload_result = subprocess.run(['systemctl', 'daemon-reload'], capture_output=True)
        print(sys_reload_result.stdout.decode() + sys_reload_result.stderr.decode())
        for commands in ['restart', 'status']:
            run_service_result = subprocess.run(['systemctl', commands, f"{file_name}.service"], capture_output=True)
            print(run_service_result.stdout.decode() + run_service_result.stderr.decode())
        print(f"{file_name} restart done")


