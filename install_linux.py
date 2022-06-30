import os

def install_linux_mint(os_release):
    if os_release['VERSION_ID'].strip('"') == '20.3':
        print('OS identified as Linux Mint 20.3')
        command = 'apt install -y'
        needed_packages = ['python3-pyqt5']
        for package in needed_packages:
            command = f'{command} {package}'
        print('Install nessesary packages ...')
        print(f'Running command: {command}')
        cmd_out = os.popen(command)
        print(cmd_out.read())

print('Starting install process ...')
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

