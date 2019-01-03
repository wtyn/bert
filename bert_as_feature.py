# coding=utf-8

import tensorflow as tf
import tokenization, modeling
import os

os.environ["CUDA_VISIBLE_DEVICES"] = '2'

# 配置文件
data_root = 'weight/chinese_L-12_H-768_A-12/'
bert_config_file = data_root + 'bert_config.json'
bert_config = modeling.BertConfig.from_json_file(bert_config_file)
init_check_point = data_root + 'bert_model.ckpt'
bert_vocab_file = data_root + 'vocab.txt'
bert_vocab_En_file = 'weight/uncased_L-12_H-768_A-12/vocab.txt'

# test
token = tokenization.CharTokenizer(vocab_file=bert_vocab_file)
split_tokens = token.tokenize('龘,Jack,请回答1988')
word_ids = token.convert_tokens_to_ids(split_tokens)
word_mask = [1] * len(word_ids)
word_segment_ids = [0] * len(word_ids)

# graph
input_ids = tf.placeholder(tf.int32, shape=[None, None], name='input_ids')
input_mask = tf.placeholder(tf.int32, shape=[None, None], name='input_masks')
segment_ids = tf.placeholder(tf.int32, shape=[None, None], name='segment_ids')

# 初始化BERT
model = modeling.BertModel(
    config=bert_config,
    is_training=False,
    input_ids=input_ids,
    input_mask=input_mask,
    token_type_ids=segment_ids,
    use_one_hot_embeddings=False)

# 加载bert模型
tvars = tf.trainable_variables()
(assignment, initialized_variable_names) = modeling.get_assignment_map_from_checkpoint(tvars, init_check_point)

# 获取最后一层和倒数第二层。
encoder_last_layer = model.get_sequence_output()
encoder_last2_layer = model.all_encoder_layers[-2]

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    token = tokenization.CharTokenizer(vocab_file=bert_vocab_file)
    basic_token = tokenization.BasicTokenizer()
    full_token = tokenization.FullTokenizer(vocab_file=bert_vocab_En_file)
    query = u'Jack,请回答1988, UNwant\u00E9d,running'
    # split_tokens = basic_token.tokenize(query)
    split_tokens = full_token.tokenize(u"UNwant\u00E9d,running")
    split_tokens = token.tokenize(query)
    word_ids = token.convert_tokens_to_ids(split_tokens)
    word_mask = [1] * len(word_ids)
    word_segment_ids = [0] * len(word_ids)
    fd = {input_ids: [word_ids], input_mask: [word_mask], segment_ids: [word_segment_ids]}
    last, last2 = sess.run([encoder_last_layer, encoder_last_layer], feed_dict=fd)
    print('last shape:{}, last2 shape: {}'.format(last.shape, last2.shape))
    pass
