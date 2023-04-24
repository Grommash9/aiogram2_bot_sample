import os.path
import os
import subprocess
import sys
from typing import List
from os.path import dirname, abspath

parent_path = dirname(dirname(abspath(__file__)))

repository_name = os.path.basename(dirname(dirname(abspath(__file__))))

if not os.path.exists(os.path.join(parent_path, 'env')):
    subprocess.run(['sudo apt-get install python3.10-dev default-libmysqlclient-dev build-essential'], capture_output=True, shell=True)
    print('venv creating started')
    venv_creation_result = subprocess.run(['python3', '-m', 'venv', 'env'], capture_output=True, cwd='..')
    print(venv_creation_result.stdout.decode() + venv_creation_result.stderr.decode())
    print('=' * 70)
    print('pip installation')
    venv_activate_path = '../env/bin/python'
    requirements_path = '../requirements.txt'
    result = subprocess.run([venv_activate_path, '-m', 'pip', 'install', '-r', requirements_path], capture_output=True)
    print(result.stdout.decode() + result.stderr.decode())
    print('=' * 70)


if not os.path.exists(os.path.join(parent_path, '.env')):
    print('cant find .env file! creating it from .env.sample!')
    if not os.path.exists(os.path.join(parent_path, '.env.sample')):
        print('.env.sample file does not exists!')
        sys.exit(-1)
    with open(os.path.join(parent_path, '.env'), 'w') as new_env_file:
        new_env_file.write(open(os.path.join(parent_path, '.env.sample'), 'r').read())
    if os.path.exists(os.path.join(parent_path, '.env')):
        print('.env file created!')
    else:
        print('cant create .env file!')
        sys.exit(-1)

for package in os.listdir(parent_path):
    if os.path.isdir(os.path.join(parent_path, package)) \
            and os.path.exists(os.path.join(parent_path, package, '__main__.py')):
        if package == 'bot_app':
            file_name = repository_name
        elif package == 'api_application':
            file_name = f"{repository_name}_api"
        else:
            file_name = package
        with open(f'{file_name}.service', 'w') as new_service_file:
            new_service_file.write("[Unit]\n"
                                   f"Description={file_name} service\n"
                                   "After=syslog.target\n"
                                   "After=network.target\n\n\n"

                                   "[Service]\n"
                                   "Type=simple\n"
                                   "User=root\n"
                                   f"WorkingDirectory={parent_path}\n"
                                   f"ExecStart={os.path.join(parent_path, 'env', 'bin', 'python3')} -m {package}\n"
                                   "RestartSec=10\n"
                                   "Restart=on-failure\n\n\n"

                                   f"StandardOutput=append:{os.path.join(parent_path, 'log_output.log')}\n"
                                   f"StandardError=append:{os.path.join(parent_path, 'log_error.log')}\n\n\n"

                                   "[Install]\n"
                                   "WantedBy=multi-user.target")
        print(f'{file_name}.service has been created!')


systemctl_files_path = '/etc/systemd/system'


class File:
    abs_path = str()
    file_name = str()

    def __init__(self, abs_path, file_name):
        self.abs_path = abs_path
        self.file_name = file_name


def get_service_files() -> List[File]:
    service_files_list = [File(os.path.join(os.getcwd(), files), files) for files in os.listdir(os.getcwd()) if
                          files.endswith('.service')]
    if len(service_files_list) > 0:
        return service_files_list
    print('There is no any service file in this folder, maybe you are already add it?')
    return sys.exit(1)


for file in get_service_files():
    if os.path.exists(os.path.join(systemctl_files_path, file.file_name)):
        print(f"{os.path.join(systemctl_files_path, file.file_name)} already exists and will be skipped for now")
        continue
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
