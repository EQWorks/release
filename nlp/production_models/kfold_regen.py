import json
base_path = '/Users/stevenlu/Documents/GitHub/release/nlp/data/k_fold'
embedded_path = '/Users/stevenlu/Documents/GitHub/release/nlp/data/k_fold_embedded'
out_path = '/Users/stevenlu/Documents/GitHub/release/nlp/data/k_fold_regen3'

fold_names = ['0th_fold', '1th_fold', '2th_fold', '3th_fold', '4th_fold']

embedded_type = '_base_-3_-2_-1'

for label_n in fold_names:
    k_file = open('{}/{}.json'.format(base_path, label_n.lower()),'r')
    fold_data = []
    for row in k_file:
        row= json.loads(row.strip())
        a= row.pop('features', None)
        fold_data.append(row)
    k_file.close()
    embedded_file = open('{}/{}{}.jsonl'.format(embedded_path, label_n.lower(),embedded_type),'r')
    out_file = open('{}/{}.json'.format(out_path, label_n.lower()),'w')
    i = 0
    for row in embedded_file:
        row = json.loads(row.strip())
        fold_data[i]['features']= row['features']
        out_file.write(json.dumps(fold_data[i])+'\n')
        i+=1
    out_file.close()
    embedded_file.close()

