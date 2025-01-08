import numpy as np
settings = ['local', 'ew', 'eu']
HOST_DIR = './HOSTS/'

#Large Machines
local_sizes = [3, 4, 5]
EW_EU_sizes = [3,4,5]
prefix = 'large_'

# #Small Machines
# local_sizes = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 26, 28, 30]
# EW_EU_sizes = [3, 6, 10, 20]
# prefix = ''

ip_dict = {}
#Read the Ip addresses from each file into a dict
for setting in settings:
    with open('{}{}{}.example'.format(HOST_DIR, prefix, setting), mode='r') as f:
        content = f.readlines()
    ip_dict[setting] = [x.strip() for x in content]

#Write the local files
for size in local_sizes:
    with open('{}{}{}_{}.example'.format(HOST_DIR, prefix,'local', size), mode='w') as f:
        for ip in ip_dict['local'][:size]:
            f.write(ip+'\n')

#Write the east west and europe files
for size in EW_EU_sizes:
    for setting in ['ew', 'eu']:
        with open('{}{}{}_{}.example'.format(HOST_DIR, prefix, setting, size), mode='w') as f:
            for ip in ip_dict['local'][:int(np.ceil(size/2))]:
                f.write(ip+'\n')
            for ip in ip_dict[setting][:int(size/2)]:
                f.write(ip+'\n')

#Make the HOSTS_ALL file for house keeping
with open(prefix+'HOSTS_ALL.example', mode='w') as f:
    for setting in settings:
        for ip in ip_dict[setting]:
            f.write(ip+'\n')