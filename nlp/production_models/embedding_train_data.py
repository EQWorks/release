import sys

base_path = '/Users/stevenlu/Documents/GitHub/release/nlp/data/labels'


label_names = ['Added', 'Changed', 'Deprecated', 'Fixed', 'Removed', 'Security']

#label_names = ['Added']



for label_n in label_names:
    label_file_path = '{}/{}.txt'.format(base_path, label_n.lower())
    label = '__label__{}'.format(label_n)
    label_len = len(label)
    label_content_file = open('{}/{}_content.txt'.format(base_path, label_n.lower()),'w')
    label_fiile = open(label_file_path, 'r')
    for row in label_fiile:
        row = row.strip()
        content = row[label_len + 1:]
        label_content_file.write(content+'\n')
    label_content_file.close()
    label_fiile.close()


