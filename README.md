# 多轮对话机器人
### 提供训练数据，训练代码，推断代码以及可交互的网页

## 推断代码
下载训练了10轮的模型， [百度网盘]() 密码:？？， 解压后存入cache，执行以下命令
```bash
cd chat_web
python3 chat.py
```
即可和聊天机器人交互


## 训练数据
清洗自 https://github.com/yangjianxin1/GPT2-chitchat 中的100w聊天语料，以及 https://github.com/codemayq/chinese_chatbot_corpus 中的贴吧及电视剧对白语料，仅保留3段以上的对话。请前往 [百度网盘]() 密码:？？ 下载解压后存入data文件夹下

## 训练代码
改自huggingface源码 
```bash
python3 run_clm.py \
    --model_name_or_path uer/gpt2-distil-chinese-cluecorpussmall  \
    --train_file data/merge_train.txt \
    --do_train \
    --do_eval \
    --output_dir cache/new \
    --overwrite_output_dir
```

## 对话网页
来自项目： 


TODO： 完善文档， 完善flask搭建（本地搭建），完善依赖

