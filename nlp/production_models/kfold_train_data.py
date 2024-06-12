import json
base_path = '/Users/stevenlu/Documents/GitHub/release/nlp/data/k_fold'
content_path = '/Users/stevenlu/Documents/GitHub/release/nlp/data/k_fold_content'

fold_names = ['0th_fold', '1th_fold', '2th_fold', '3th_fold', '4th_fold']

for label_n in fold_names:
    k_file_path = '{}/{}.json'.format(base_path, label_n.lower())
    label = '__label__{}'.format(label_n)
    label_len = len(label)
    k_content_file = open('{}/{}_content.txt'.format(content_path, label_n.lower()),'w')
    k_fiile = open(k_file_path, 'r')
    for row in k_fiile:
        row = json.loads(row.strip())
        content = row['content']
        k_content_file.write(content+'\n')
    k_content_file.close()
    k_fiile.close()


