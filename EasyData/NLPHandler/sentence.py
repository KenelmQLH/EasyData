import nltk
import pysbd
seg = pysbd.Segmenter(language="en", clean=False)


def add_clause_flag(sentence, flag="#"):
    tokens = sentence.split()
    tagged_sent = nltk.pos_tag(tokens)
    sent_parsed = []
    for x, t in tagged_sent:
        if t in ["CC", "IN", "WRB","LS"]:
            sent_parsed.append( flag+x )
        else:
            sent_parsed.append(x)
    return " ".join(sent_parsed)

def cut_sent_by_key(para):
    split_set = ["#"]
    split_sents = []
    _s = 0

    key_limit = 18
    for i in range(len(para)):
      if i <= 40:
        continue
      if len(para) - i <= 40:
        break
      if para[i] in split_set:
        # 仅仅划分长句子
        # if i - _s <= key_limit: 
          # 误打误撞：如果当前关键词距离 上次分句较短，而且距离下一个 关键词的距离也很短， 那么跳过（选用下一个词语）
          # 原理： 合理分割词 后面一般不会 立马 有迷惑性的短语介词等。
        j = i+1
        while j<len(para) and para[j] not in split_set:
          j+=1
        if j -i <= key_limit:
          # print("test 3 ==",para[i:j])
          continue
        # 将句子后面的 换行符和空格 也划入此句子内
        blank_idx = i+1
        while blank_idx < len(para) and para[ blank_idx ] in ["\n"," "]: # important!
          blank_idx +=1
        text_sent = para[_s: blank_idx]
        text_sent = text_sent.replace("#", "")
        if text_sent:
          split_sents.append(text_sent)
        
        _s = blank_idx

    if _s != len(para):
      split_sents.append(para[_s:len(para)].replace("#", ""))
    
    if len(split_sents) == 0: 
      split_sents.append(para.replace("#", ""))
    return split_sents

def cut_sent_by_punctuation(para, level=1):
    if level == 1:
      split_set = set(['。', '！', '!', '.', '？', '?']) # 句子
    elif level == 2:
      split_set = set(['。', '！', '!', '.', '？', '?', ',', ';']) # 修改2.12, 句子片段： 加入',' , ';'
    else:
      raise KeyError("Illegal leval of cut_sent !")
    split_sents = []
    _s = 0
    limit = 15
    for i in range(len(para)):
      if para[i] in split_set:
        # 仅仅划分长句子
        if i - _s <= limit:
          continue
        else:
          j = i+1
          while j<len(para) and para[j] not  in split_set:
            j+=1
          if j -i <=limit:
            continue
        # 将句子后面的 换行符和空格 也划入此句子内
        blank_idx = i+1
        while blank_idx < len(para) and para[ blank_idx ] in ["\n"," "]: # important!
          blank_idx +=1
        text_sent = para[_s: blank_idx]
        if text_sent:
          split_sents.append(text_sent)
        
        _s = blank_idx

    if _s != len(para):
      split_sents.append(para[_s:len(para)])
    if len(split_sents) == 0:
      split_sents.append(para)
    
    return split_sents


def cut_sent(text, *argc, level=2, **argv):
  ss1 = seg.segment(text)
  
  ss2 = []
  for s in ss1:
    s = add_clause_flag(s, flag="#") # 子句标志
    ss2.extend(cut_sent_by_punctuation(s, level=level)) # 使用标点符号划分粗子句
  
  ss3 = []
  for s in ss2:
    ss3.extend(cut_sent_by_key(s)) # 使用标志划分细子句
  
  wrong_num = []
  if len(text) != len("".join(ss3)):
    wrong_num.append(len(text) - len("".join(ss3)))
  return ss3

# if __name__ == "__main__":
#   text = "there are 28 stations between hyderabad and bangalore . how many second class tickets have to be printed , so that a passenger can travel from any station to any other station ?"
#   t = cut_sent(text)
#   print(t)