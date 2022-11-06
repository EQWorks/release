## Data preparation
1. Raw data: https://github.com/EQWorks/release/tree/master/nlp/data/labels
2. Execute kfold_data_gen.py
    * This will randomly separate each label’s content into 5 folds.
3. Execute kfold_train_data.py
    *Strip label from each fold file, prepare content for Bert embedding
4. In case of switching to another Bert pre-trained model and want k-fold remain the same, execute the kfild_regen.py

## Bert embedding generation
1. Clone Bert from Github: https://github.com/google-research/bert
2. Download one of the pre-trained models
3. Set up environment path to the model
    * Example: export BERT_BASE_DIR=/Users/stevenlu/Downloads/bert-master/uncased_L-12_H-768_A-12
4. Execute script
    * Example: 
python3 extract_features.py \
--input_file=/Users/stevenlu/Documents/GitHub/release/nlp/data/k_fold_content/4th_fold_content.txt \
--output_file=/Users/stevenlu/Documents/GitHub/release/nlp/data/k_fold_embedded/4th_fold_base_-3_-2_-1.jsonl \
 --vocab_file=$BERT_BASE_DIR/vocab.txt \
 --bert_config_file=$BERT_BASE_DIR/bert_config.json \
 --init_checkpoint=$BERT_BASE_DIR/bert_model.ckpt \
 --layers=-10,-11,-12 \
 --max_seq_length=128 \
 --batch_size=8

## Model execution on ec2
1. Initial the cluster and prepare for the model training
    * ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-20201026 - ami-0885b1f6bd170450c
    * sudo apt-get update
    * sudo apt-get -y install python3-pip
    * sudo apt install python3-testresources
    * sudo pip3 install --upgrade tensorflow
    * sudo apt install awscli
2. Configure your AWS
3. Copy script and k-fold files from s3: s3://eq-miner/test2/release_label/
4. Create a model output folder
5. sudo pip3 install fasttext (if your building fasttext model)
6. Execute the script
    * Execute embedding_wrap.py/embedding_wrap2.py/embedding_wrap_lstm.py
    * This will train the model and generate testing result
      * embedding_wrap: Multi-head self-attention without location encoding
      * embedding_wrap2: Multi-head self-attention with location encoding
      * embedding_wrap_lstm: Bi-directional LSTM
    * Input example:
      * embedding_wrap/embedding_wrap2: python3 embedding_wrap_lstm.py 768 50 100 1th_fold.json:1684,2th_fold.json:1684,3th_fold.json:1684 4th_fold.json:1691 model7 0,50 0th_fold.json:1684 0.0001 50
      * embedding_wrap_lstm: python3 embedding_wrap_lstm.py 768 50 100 0th_fold.json:1684,1th_fold.json:1684,2th_fold.json:1684 3th_fold.json:1684 model1 0,50 4th_fold.json:1691 0.00008 50
    * Example of output:
      * {'filtered': {'mold_build_time': 5105.467138528824, 'sample_length': 4595, 'validiation': [{'test_file': ['0th_fold.json:1691'], 'valid_file': ['3th_fold.json:1684'], 'model_name': '47-0.9978-0.0171.hdf5', 'valid_score': [0.7473069429397583, 0.8219354748725891], 'test_score': [0.7553659081459045, 0.8098001480102539], 'valid_sample_size': 1550}, {'test_file': ['3th_fold.json:1684'], 'valid_file': ['0th_fold.json:1691'], 'model_name': '46-0.9965-0.0207.hdf5', 'valid_score': [0.7761548161506653, 0.8052868843078613], 'test_score': [0.7688340544700623, 0.8225806355476379], 'valid_sample_size': 1551}]}, 'restricted': {'mold_build_time': 3495.59513258934, 'sample_length': 5059, 'validiation': [{'test_file': ['0th_fold.json:1691'], 'valid_file': ['3th_fold.json:1684'], 'model_name': '46-0.9937-0.0317.hdf5', 'valid_score': [0.8246729373931885, 0.8105700612068176], 'test_score': [0.813213050365448, 0.801068902015686], 'valid_sample_size': 1684}, {'test_file': ['3th_fold.json:1684'], 'valid_file': ['0th_fold.json:1691'], 'model_name': '16-0.9302-0.2405.hdf5', 'valid_score': [0.5546706318855286, 0.7897862195968628], 'test_score': [0.5412384867668152, 0.8141329884529114], 'valid_sample_size': 1684}]}, 'model_name': 'transB_8'}
7. Execute fasttext
    * Install fasttext
    * Execute fasttext_kfold.py

## T-test
1. Gather result accuracy to a list
2. Execute t_tests.py
