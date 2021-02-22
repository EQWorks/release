from prod_model_transformer import mdoel_build
from embedded_valid import mdoel_valid
import os
import sys

def model_write(embedd_dim,sentence_len,neuron_size,train_files,test_files, model_name,seq_range,valid_date_files,lr):
    out_dict = {}
    out_dict['filtered'] = {}
    out_dict['restricted'] = {}
    out_dict['model_name'] = model_name
    #res models
    res_model = '{}_restricted'.format(model_name)
    os.mkdir(res_model)
    res_model_build_time,res_sample_l= mdoel_build(embedd_dim,sentence_len,neuron_size,train_files,test_files,res_model, res_model,seq_range,False,lr)
    res_model_name1, res_valid_score1, res_test_score1,res_valid_l1 = mdoel_valid(embedd_dim, sentence_len, test_files, valid_date_files, res_model, seq_range,False)
    out_dict['restricted']['mold_build_time'] = res_model_build_time
    out_dict['restricted']['sample_length'] = res_sample_l
    out_dict['restricted']['validiation'] = []
    out_dict['restricted']['validiation'].append({'test_file':test_files,'valid_file':valid_date_files,'model_name':res_model_name1,'valid_score':res_valid_score1,'test_score':res_test_score1,'valid_sample_size':res_valid_l1})
    res_model_name2, res_valid_score2, res_test_score2,res_valid_l2 = mdoel_valid(embedd_dim, sentence_len, valid_date_files,test_files, res_model, seq_range,False)
    out_dict['restricted']['validiation'].append({'test_file':valid_date_files,'valid_file':test_files,'model_name':res_model_name2,'valid_score':res_valid_score2,'test_score':res_test_score2,'valid_sample_size':res_valid_l2})
    #filtered_model
    filtered_model = '{}_filtered'.format(model_name)
    os.mkdir(filtered_model)
    filtered_model_build_time,filter_sample_l= mdoel_build(embedd_dim,sentence_len,neuron_size,train_files,test_files,filtered_model, filtered_model,seq_range,True,lr)
    filtered_model_name1, filter_valid_score1, filter_test_score1,valid_l1 = mdoel_valid(embedd_dim, sentence_len, test_files, valid_date_files, filtered_model, seq_range,True)
    out_dict['filtered']['mold_build_time'] = filtered_model_build_time
    out_dict['filtered']['sample_length'] = filter_sample_l
    out_dict['filtered']['validiation'] = []
    out_dict['filtered']['validiation'].append({'test_file':test_files,'valid_file':valid_date_files,'model_name':filtered_model_name1,'valid_score':filter_valid_score1,'test_score':filter_test_score1,'valid_sample_size':valid_l1})
    filtered_model_name2, filter_valid_score2, filter_test_score2,valid_l2 = mdoel_valid(embedd_dim, sentence_len, valid_date_files,test_files, filtered_model, seq_range,True)
    out_dict['filtered']['validiation'].append({'test_file':valid_date_files,'valid_file':test_files,'model_name':filtered_model_name2,'valid_score':filter_valid_score2,'test_score':filter_test_score2,'valid_sample_size':valid_l2})

    print(out_dict)
    return out_dict

if __name__=='__main__':
    #embedd_dim,sentence_len,neuron_size,train_files,test_files, model_name,seq_range,valid_date_files,lr
    embedd_dim = int(sys.argv[1])
    sentence_len = int(sys.argv[2])
    neuron_size = int(sys.argv[3])
    train_files = sys.argv[4].split(',')
    test_files = sys.argv[5].split(',')
    model_name = sys.argv[6]
    seq_range = sys.argv[7].split(',')
    valid_date_files = sys.argv[8].split(',')
    lr = float(sys.argv[9])
    #python3 embedding_wrap_lstm.py 768 50 100 1th_fold.json:1684,2th_fold.json:1684,3th_fold.json:1684 4th_fold.json:1691 model7 0,50 0th_fold.json:1684 0.0001 50
    model_write(embedd_dim, sentence_len, neuron_size, train_files, test_files, model_name, seq_range,valid_date_files, lr)

