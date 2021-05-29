import os
import sys
from datetime import datetime
import random
import json
import fasttext
import time


#model_id = '6'


#train_files = ['0th_fold.json', '3th_fold.json', '4th_fold.json']
#test_files = ['1th_fold.json']
#valid_files = ['2th_fold.json']

def mdoel_build(train_files,test_files,valid_files, model_id,seq_range):
    out_dict = {}
    out_dict['filtered'] = {}
    out_dict['full'] = {}
    out_dict['model_name'] = 'fasttext_{}'.format(model_id)
    out_dict['full']['validiation'] = []
    out_dict['filtered']['validiation'] = []
    file_size = {}
    size = '1M'
    for isfiltered in [True,False]:
        if isfiltered:
            tf = 'fast_train_{}_token_len_50.txt'.format(model_id)
            sf = 'fast_select_{}_token_len_50.txt'.format(model_id)
            vf = 'fast_valid_{}_token_len_50.txt'.format(model_id)
        else:
            tf = 'fast_train_{}.txt'.format(model_id)
            sf = 'fast_select_{}.txt'.format(model_id)
            vf = 'fast_valid_{}.txt'.format(model_id)
        print ('iffiltered: ',isfiltered)
        print(tf,sf,vf)
        out_file = open(tf, 'w')
        select_file = open(sf, 'w')
        valid_file = open(vf, 'w')
        data_c = 0
        for fold_n in train_files:
            infile = open(fold_n,'r')
            for row in infile:
                row = json.loads(row.strip())
                label = row['label']
                content = row['content']
                features = row['features']
                if isfiltered:
                    if len(features) > int(seq_range[0]) and len(features) <= int(seq_range[1]):
                        output = ' '.join([label,content])+'\n'
                        a=out_file.write(output)
                        data_c+=1
                else:
                    output = ' '.join([label, content]) + '\n'
                    a = out_file.write(output)
                    data_c+=1
            infile.close()
        out_file.close()
        file_size[tf] = data_c
        data_c = 0
        for fold_n in test_files:
            infile = open(fold_n,'r')
            for row in infile:
                row = json.loads(row.strip())
                label = row['label']
                content = row['content']
                features = row['features']
                if isfiltered:
                    if len(features) > int(seq_range[0]) and len(features) <= int(seq_range[1]):
                        output = ' '.join([label,content])+'\n'
                        a=select_file.write(output)
                        data_c+=1
                else:
                    output = ' '.join([label, content]) + '\n'
                    a = select_file.write(output)
                    data_c+=1
            infile.close()
        select_file.close()
        file_size[sf] = data_c
        data_c = 0
        for fold_n in valid_files:
            infile = open(fold_n,'r')
            for row in infile:
                row = json.loads(row.strip())
                label = row['label']
                content = row['content']
                features = row['features']
                if isfiltered:
                    if len(features) > int(seq_range[0]) and len(features) <= int(seq_range[1]):
                        output = ' '.join([label,content])+'\n'
                        a=valid_file.write(output)
                        data_c += 1
                else:
                    output = ' '.join([label, content]) + '\n'
                    a = valid_file.write(output)
                    data_c += 1
            infile.close()
        valid_file.close()
        file_size[vf] = data_c
        for model_i in [0,1]:
            params = dict(input=tf)
            initial_time = time.time()
            if model_i ==0:
                out_model_id = model_id
                selecting = sf
                validating = vf
            else:
                out_model_id = '-'.join([model_id, '1'])
                selecting = vf
                validating = sf
            params.update(dict(
                autotuneValidationFile=selecting,
                autotuneModelSize=size,
            ))
            model = fasttext.train_supervised(**params)
            score = model.test(validating)
            time_consum = time.time() - initial_time
            if isfiltered:
                save_model_name = 'model_token_filtered/fasttext_model{}.ftz'.format(out_model_id)
                out_dict['filtered']['validiation'].append({'test_file':selecting,'valid_file':validating,'model_name':save_model_name,'valid_score':score,'valid_sample_size':file_size[validating],'model_build_time':time_consum})
            else:
                save_model_name = 'model_token_full/fasttext_model{}.ftz'.format(out_model_id)
                out_dict['full']['validiation'].append({'test_file':selecting,'valid_file':validating,'model_name':save_model_name,'valid_score':score,'valid_sample_size':file_size[validating],'model_build_time':time_consum})
            model.save_model(save_model_name)
    print(out_dict)
    return out_dict

if __name__=='__main__':
    #train_files,test_files,valid_files, model_id,seq_range
    train_files = sys.argv[1].split(',')
    test_files = sys.argv[2].split(',')
    valid_files = sys.argv[3].split(',')
    model_id = sys.argv[4]
    seq_range = sys.argv[5].split(',')
    mdoel_build(train_files, test_files, valid_files, model_id, seq_range)
