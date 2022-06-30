#!/usr/bin/env python3
import os
import pathlib

def install_linux_mint(os_release):
    if os_release['VERSION_ID'].strip('"') == '20.3':
        print('OS identified as Linux Mint 20.3')
        commands = ['apt update']
        install_command = 'apt install -y'
        needed_packages = ['python3-pyqt5']
        for package in needed_packages:
            install_command = f'{install_command} {package}'
        commands.append(install_command)
        for command in commands:
            print(f'Running command: {command}')
            cmd_out = os.popen(command)
            print(cmd_out.read())
        answer = input('Do you want to install a system alias for ocLogfileAnalyzer? (Y/n): ')
        if answer.lower() != 'y' or answer.lower() != '':
            path = f'{os.path.abspath(__file__).strip(__file__.split("/")[len(__file__.split("/"))-1])}main.py'
            found = False
            with open(f'{pathlib.Path.home()}/.bashrc', 'r') as reader:
                for line in reader.readlines():
                    if 'alias ocLogfileAnalyzer=' in line:
                        found = True
                        break
            if not found:
                with open(f'{pathlib.Path.home()}/.bashrc', 'a') as writer:
                    writer.write("alias ocLogfileAnalyzer='/usr/bin/python3 "+path+"'")
                print(f'Alias ocLogfileAnalyzer written to {pathlib.Path.home()}/.bashrc')
                print('Please restart your shell or reload .bashrc by typing <source ~/.bashrc> and start the app ocLogfileAnalyzer by typing <ocLogfileAnalyzer>')
            else:
                print(f'Alias ocLogfileAnalyzer found in {pathlib.Path.home()}/.bash. Stop writing aliases')

print('Identifying OS')

with open('/etc/os-release', 'r') as reader:
    os_release_read = reader.readlines()

os_release = {}
for line in os_release_read:
    line = line.strip('\n').split('=')
    os_release[line[0]] = line[1]

if os_release['NAME']  != ' ':
    if os_release['NAME'].lower() != 'linux mint':
        install_linux_mint(os_release)

