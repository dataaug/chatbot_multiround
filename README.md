# 多轮对话机器人
### 该仓库提供训练数据，训练代码，推断代码以及可交互的网页
### 多轮中文聊天机器人，采用GPT2进行微调，清洗聊天数据110w+，采用语义相似度和文本jaccard相似度过滤回话。

## 推断代码 （快速开始）
训练好的模型暂不开源， 将训练后的模型后存入cache，执行以下命令
```bash
cd chat_web
python3 chat.py
```
即可和聊天机器人交互


## 对话网页
改自项目：https://github.com/sylviapap/chatbot 
对话网页可以提供更友好的AI，运行这部分代码可以快速部署AI聊天机器人服务
首先，开启flask服务

```bash
cd flask_chat
export FLASK_APP=chat_server
nohup flask run --host=0.0.0.0 -p 5000 > flask.log 2>&1 &
```
点开 chat_web/index.html就可以看到可交互网页了
如果需要公网访问架设的聊天服务，请将 index.js 中相关ip改为你的服务器ip

## 训练数据
清洗自 https://github.com/yangjianxin1/GPT2-chitchat 中的100w聊天语料，以及 https://github.com/codemayq/chinese_chatbot_corpus 中的贴吧及电视剧对白语料，仅保留3段以上的对话。请前往 [百度网盘]() 密码:？？ 下载解压后存入data文件夹下

## 训练代码
改自huggingface源码 https://github.com/huggingface/transformers/blob/master/examples/pytorch/language-modeling/run_clm.py
```bash
python3 run_clm.py \
    --model_name_or_path uer/gpt2-distil-chinese-cluecorpussmall  \
    --train_file data/merge_train.txt \
    --do_train \
    --do_eval \
    --output_dir cache/new \
    --overwrite_output_dir
```


## 技术细节
采用GPT-2训练，训练数据格式如下
```
[CLS]天气真不错[SEP]你也很不错[SEP]你真会夸人[SEP]过奖了[SEP]
[CLS]你好啊[SEP]你好[SEP]吃了[SEP]那我们一起出去玩吧[SEP]
```
推断过程根据用户输入采样30条回应（topp采样），这个回应将通过roberta模型与用户发言进行语义排序，希望选择语义相似度最高的句子。
与此同时，计算用户发言和候选语句jaccard相似度，将语义相似度 + （1 - jaccard相似分）就得到机器回复的排序。选择最高排序结果返回。

TODO： 完善依赖，测试环境

