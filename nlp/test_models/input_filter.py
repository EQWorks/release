import json

infile = open('0th_fold.json','r')

long_c = 0

short_c = 0

long_sampe = []

for row in infile:
    row = json.loads(row.strip())
    content = row['content']
    feature = row['features']
    if len(feature) > 20:
        long_c+=1
        long_sampe.append(row)
    else:
        short_c+=1



sample_i = 5

remain_w = 0

total_len = len(long_sampe[sample_i]['features'])

full_token = []

remain_tokens = []

#for sample in long_sampe:

for token_d in long_sampe[sample_i]['features']:
    full_token.append(token_d['token'])
    if token_d['token'] in ['.',',',';','?','!']:
        remain_tokens.append(token_d['token'])
    elif len(token_d['token']) > 1 and '##' not in token_d['token'] and not token_d['token'].isnumeric():
        remain_tokens.append(token_d['token'])
    elif '##' in token_d['token'] and len(token_d['token']) >=4 and not token_d['token'].replace('##','').isnumeric():
        remain_tokens.append(token_d['token'])


print (len(full_token), full_token)

print (len(remain_tokens), remain_tokens)
