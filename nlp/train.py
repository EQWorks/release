import os
import sys
from datetime import datetime
import random
import json

import fasttext

DIR = os.path.abspath('')
DATA_DIR = os.path.join(DIR, 'data')


def train(tf, vf, size='1M', auto=True):
    now = datetime.now().strftime('%Y%m%d%H%M')
    meta = f'{size.lower()}-{now}' if auto else now
    m = os.path.join(DIR, f'commits-{meta}.bin')
    params = dict(input=tf)
    if auto:
        # auto-tuned model through supervised learning
        # and hyper-parameters autotuned through validation file
        params.update(dict(
            autotuneValidationFile=vf,
            autotuneModelSize=size,
        ))
    model = fasttext.train_supervised(**params)
    model.save_model(m)
    return m


def split_train_valid():
    tf_path = os.path.join(DATA_DIR, 'train.txt')
    vf_path = os.path.join(DATA_DIR, 'new_valid.txt')

    with open(tf_path, 'w') as tf, open(vf_path, 'w') as vf:
        for label in os.scandir(os.path.join(DATA_DIR, 'labels')):
            if not label.path.endswith('.txt'):
                continue

            with open(label.path) as f:
                lines = f.readlines()
                random.shuffle(lines)  # shuffle list of lines in-place
                split = len(lines) // 5  # 20/80 split
                tf.writelines(lines[split:])  # 80
                vf.writelines(lines[:split])  # 20

    return tf_path, vf_path


def threshold_test(m, threshold=0.9):
    count = 0
    below = 0
    sf = os.path.join(DATA_DIR, 'snoke')
    ff = os.path.join(DATA_DIR, 'firstorder')
    model = fasttext.load_model(m)

    with open(sf) as snoke, open(ff) as fo:
        for commit in snoke:
            count += 1
            label, score = model.predict(commit.strip().lower())
            if score < threshold:
                below += 1

        for commit in fo:
            count += 1
            label, score = model.predict(commit.strip().lower())
            if score < threshold:
                below += 1

    return below / count


def compare(m, ref_m, vf, ref_vf, threshold=0.9):
    # load previous model for reference
    ref = fasttext.load_model(ref_m)
    ref_score = ref.test(ref_vf)[1]
    ref_below = threshold_test(ref_m, threshold)
    # train new model
    model = fasttext.load_model(m)
    size = round(os.stat(m).st_size / 1024 / 1024, 3)  # in mega-bytes
    score = model.test(vf)[1]
    score2 = model.test(ref_vf)[1]
    below = threshold_test(m, threshold)
    meta = dict(
        model=m.split('/')[-1],
        size=size,
        score=score,
        score2=score2,
        ref_score=ref_score,
        threshold=threshold,
        below=below,
        ref_below=ref_below,
    )
    # compare
    if score > ref_score and score2 > ref_score and below <= ref_below:
        return True, meta

    return False, meta


if __name__ == '__main__':
    # load previous model for reference
    bin_dir = os.path.join(DIR, '..', 'bin')
    ref_vf = os.path.join(DATA_DIR, 'valid.txt')
    ref_m = os.path.join(bin_dir, 'commits.bin')
    ref = fasttext.load_model(ref_m)
    ref_score = ref.test(ref_vf)[1]
    # train new model
    tf, vf = split_train_valid()
    m = train(tf, vf)
    # compare new model
    better, meta = compare(m, ref_m, vf, ref_vf)
    print(better, meta)

    if not better:
        sys.exit(1)

    # persist new valid.txt and commits.bin
    os.replace(vf, ref_vf)
    os.replace(m, ref_m)
    os.remove(m)
    with open(os.path.join(bin_dir, 'meta.json'), 'w') as fp:
        json.dump(meta, fp, indent=2)
