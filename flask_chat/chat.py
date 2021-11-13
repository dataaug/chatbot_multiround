# coding=utf-8
from datetime import datetime
from elasticsearch import Elasticsearch
import os
import jieba
import re
import sys
import json
import sys
from transformers import pipeline, set_seed
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch.nn as nn
import torch
import requests
from semantic_sort import Semantic_sort


class Generator():
    def __init__(self) -> None:
        # set_seed(42)
        model_cache = "../cache/checkpoint-download"
        self.tokenizer = AutoTokenizer.from_pretrained(model_cache)
        self.model = AutoModelForCausalLM.from_pretrained(model_cache)# .cuda() 暂不用显卡
        self.semantic = Semantic_sort().sem_sort

    def cal_jaccard(self, text1, text2):
        text1 = set(text1)
        text2 = set(text2)
        same = text1.intersection(text2)
        return float(len(same))/(len(text1)+len(text2)-len(same))

    # 生成
    def generate(self, key_word, FIN = '', SIN = ''): # TODO 使用行业信息
        def cut_SEP(input_ids):
            return input_ids[:,:-1]

        # set seed to reproduce results. Feel free to change the seed though to get different results
        with torch.no_grad():
            input_ids = self.tokenizer.encode('[SEP]'.join(key_word), return_tensors='pt')# .cuda()
            print('输入:', self.tokenizer.decode(input_ids[0]), input_ids[0])
            # input_ids = cut_SEP(input_ids)
            print('输入:', self.tokenizer.decode(input_ids[0]))
            input_record = self.tokenizer.decode(input_ids[0])

            # torch.manual_seed(2)
            num_return_sequences = 30
            # activate sampling and deactivate top_k by setting top_k sampling to 0

            sample_output = self.model.generate(
                input_ids, 
                do_sample=True, 
                max_length=len(input_record) + 30, 
                top_k=0,
                top_p=0.92,
                num_return_sequences=num_return_sequences,
                # eos_token_id = 101
                # temperature=0.7
            )

            seqs = []
            len_prefix = len(input_record) 
            print('input_record',input_record)
            print(len_prefix)
            print("Output:\n" + 100 * '-')
            for i in range(num_return_sequences):
                res = self.tokenizer.decode(sample_output[i], skip_special_tokens=False)
                print(res)
                res = res[len_prefix:]
                print(res)
                print(re.findall('(.*?)\[SEP\]',res))
                try:
                    seqs.append(re.findall('(.*?)\[SEP\]',res)[0])
                except:
                    print('输出出现异常:')
                    print(res)
                    pass
                # print(res)
            seqs = list(set(seqs))
            seqs = self.semantic(key_word[-1], seqs)
            # seqs = [x for x in seqs if self.cal_jaccard(key_word[-1], x[0]) < 0.8]
            seqs = [[x[0], x[1] + (1 - self.cal_jaccard(key_word[-1], x[0]))] for x in seqs]
            seqs.sort(key = lambda x: x[1], reverse = True)
            print(seqs)
            seqs = [re.sub(' ','',x[0]) for x in seqs]
            seqs = [seqs[0]]
            print(seqs)
        return list(set(seqs))





if __name__ == '__main__':
    engine = Generator()
    sents = []
    while True: 
        key_word = input("发言:")
        sents.append(key_word)
        res = engine.generate(sents)
        if '[CLS]' in res[0]:
            print('无言以对......')
            sents = []
        else:
            sents.append(res[0])
            print(res)
