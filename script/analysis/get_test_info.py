import os
import pandas as pd

test_type_dict = {'Multi':'', 'Single':'_single'}
networks_lst = os.popen("cat ../../data/networks.txt").read().split()
methods_lst = os.popen("cat ../../data/implementation_list.txt").read().split()

def init_info(obj):
    obj['Network'] = '-'
    obj['Method'] = '-'
    obj['Setup'] = '-'
    obj['Loading time'] = '-'
    obj['Preprocessing time'] = '-'
    obj['Walking time'] = '-'
    obj['Training time'] = '-'
    obj['Total time'] = '-'
    obj['Total time in second'] = '-'
    obj['Maximum resident size'] = '-'
    return obj

def format_time(t):
    t = t.split(':')
    t[-1] = "%.2f"%float(t[-1])
    for i in range(2): # pop zero hr/min
        if float(t[0]) == 0:
            t.pop(0)
    # pad with zeros
    if len(t) > 1:
        t[-1] = f'{t[-1]:0>5}'
        if len(t) > 2:
            t[-2] = f'{t[-2]:0>2}'
    return ':'.join(t)

def t_tot_sec(t):
    t_sec = 0
    t = list(map(float, t.split(':')))
    for i,j in enumerate(reversed(t)):
        t_sec += j * pow(60, i)
    return f'{t_sec:.2f}'

def read_stat(fp, method):
    info = init_info({})
    try:
        with open(fp, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('Took'):
                    if line.endswith('load graph'):
                        info['Loading time'] = format_time(line.split(' ')[1])
                    elif line.endswith('pre-compute transition probabilities'):
                        info['Preprocessing time'] = format_time(line.split(' ')[1])
                    elif line.endswith('generate walks'):
                        info['Walking time'] = format_time(line.split(' ')[1])
                    elif line.endswith('train embeddings'):
                        info['Training time'] = format_time(line.split(' ')[1])
                if line.startswith('Elapsed (wall clock) time'):
                    info['Total time'] = format_time(line.split(' ')[-1])
                    info['Total time in second'] = t_tot_sec(line.split(' ')[-1])
                if line.startswith('Maximum resident set size (kbytes)'):
                    val = int(line.split(' ')[-1])
                    if val > 1024:
                        val /= 1024
                        unit = 'MB'
                    if val > 1024:
                        val /= 1024
                        unit = 'GB'
                    info['Maximum resident size'] = '%.1f%s'%(val, unit)
    except FileNotFoundError:
        print("Missing test info file: %s"%fp)
    info['Method'] = method
    return info

df = init_info(pd.DataFrame())
for network in networks_lst:
    print('Start collecting testing info for %s'%repr(network))

    for test_type_name, test_type in test_type_dict.items():

        for method in methods_lst:
            stat = read_stat(f"../../result/stat/{method}/{network}{test_type}.txt", method)
            stat['Network'] = network
            stat['Setup'] = test_type_name
            df = df.append(stat, ignore_index=True)

df.to_csv(f"../../result/stat_summary.tsv", sep='\t', index=False)

