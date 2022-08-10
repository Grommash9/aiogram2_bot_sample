import os
import subprocess
import sys
from typing import List

systemctl_files_path = '/etc/systemd/system'


class File:
    abs_path = str()
    file_name = str()

    def __init__(self, abs_path, file_name):
        self.abs_path = abs_path
        self.file_name = file_name


def get_service_files() -> List[File]:
    service_files_list = [File(os.path.join(os.getcwd(), files), files) for files in os.listdir(os.getcwd()) if files.endswith('.service')]
    if len(service_files_list) > 0:
        return service_files_list
    print('There is no any service file in this folder, maybe you are already add it?')
    return sys.exit(1)


for file in get_service_files():
    try:
        os.replace(file.abs_path, os.path.join(systemctl_files_path, file.file_name))
        print(f"{file.file_name} replacing success")
    except Exception as e:
        print(f'There is an error {e} while moving the {file.file_name} file, sorry for what')

    sys_reload_result = subprocess.run(['systemctl', 'daemon-reload'], capture_output=True)
    print(sys_reload_result.stdout.decode() + sys_reload_result.stderr.decode())
    for commands in ['enable', 'start', 'status']:
        run_service_result = subprocess.run(['systemctl', commands, file.file_name], capture_output=True)
        print(run_service_result.stdout.decode() + run_service_result.stderr.decode())
    print(f"{file.file_name} install done")
