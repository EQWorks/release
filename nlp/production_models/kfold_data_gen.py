import json
import random

content_path = '/Users/stevenlu/Documents/GitHub/release/nlp/data/labels'
embedded_path = '/Users/stevenlu/Documents/GitHub/release/nlp/data/embedded'
k_fold_path = '/Users/stevenlu/Documents/GitHub/release/nlp/data/k_fold'

label_names = ['Added', 'Changed', 'Deprecated', 'Fixed', 'Removed', 'Security']

k = 5

k_fold_l = {}

for k_i in range(0,k):
    k_fold_l[k_i] = []

#label_names = ['Security','Changed']


for label_n in label_names:
    input_l = []
    label = '__label__{}'.format(label_n)
    embedded_file = open('{}/{}.jsonl'.format(embedded_path, label_n.lower()),'r')
    for row in embedded_file:
        row = json.loads(row.strip())
        row['label'] = label
        input_l.append(row)
    embedded_file.close()
    file_i = 0
    content_file = open('{}/{}_content.txt'.format(content_path, label_n.lower()), 'r')
    for row in content_file:
        input_l[file_i]['content'] = row.strip()
        file_i+=1
    content_file.close()
    random.shuffle(input_l)
    chunk_size = int(file_i/k)
    for k_i in range(0, k):
        inital_i = k_i * chunk_size
        if k_i == k-1:
            k_fold_l[k_i] += input_l[inital_i:]
        else:
            end_i = (k_i+1)*chunk_size
            k_fold_l[k_i] += input_l[inital_i:end_i]




for k_i in range(0,k):
    k_file = open('{}/{}th_fold.json'.format(k_fold_path,k_i),'w')
    out_l = k_fold_l[k_i]
    random.shuffle(out_l)
    for record in out_l:
        record = json.dumps(record)
        k_file.write(record+'\n')
    k_file.close()


