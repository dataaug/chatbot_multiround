from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
import torch
import requests
import copy
import re


class Semantic_sort():
    def __init__(self) -> None:
        # 存储所有句子的句向量 queries
        self.tokenizer = AutoTokenizer.from_pretrained(
            'hfl/chinese-roberta-wwm-ext')
        self.model = AutoModelForSequenceClassification.from_pretrained(
            'hfl/chinese-roberta-wwm-ext') #.cuda()
        self.model.eval()

    def get_tokens(self, lines):  # 输入句子列表 输出CLS token 列表
        inputs = self.tokenizer(lines, return_tensors="pt", truncation=True,
                                padding='max_length', max_length=40) #.to('cuda')
        outputs = self.model(**inputs, output_hidden_states=True)
        last_hidden = outputs[1][-1]  # hidden states的最后一层输出
        cls_token = last_hidden[:, 0, :]
        return cls_token

    def mask_sents(self, key_word='', sents=[]):
        assert key_word, sents
        for i, sent in enumerate(sents):
            sent = re.sub('|'.join(key_word.split(' ')), '[MASK]', sent)
            sents[i] = sent

        return sents

    def sem_sort(self, keyword='', sentences=[], mask=False):
        assert keyword, sentences

        recalls = sentences

        tmp = copy.deepcopy(recalls)  # 暂存 以便不展现mask后结果
        if mask:
            recalls = self.mask_sents(keyword, recalls)
        print('keyword', keyword)
        print('recalls', recalls)
        # 同时传入keyword和句子 避免两次前传播
        with torch.no_grad():
            queries = self.get_tokens([keyword] + recalls)
            key = queries[0]
            queries = queries[1:]

            cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
            cos_sim = cos(queries, key.unsqueeze(0))

            cos_sim = [float(x) for x in cos_sim]

            sent_score = list(zip(tmp, cos_sim))
        # sent_score.sort(key=lambda x: x[0], reverse=True)
        return sent_score


if __name__ == '__main__':
    sem_sorter = Semantic_sort()
    res = sem_sorter.sem_sort('电视', ['老电视', '新电视', '电视柜'])
    print(res)
