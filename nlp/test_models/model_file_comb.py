from itertools import combinations
file_l = ['0th_fold','1th_fold','2th_fold','3th_fold','4th_fold']
out_list = list(combinations(file_l, 3))


for fold_c in out_list:
    print(','.join(fold_c))