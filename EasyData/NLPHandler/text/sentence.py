from string import punctuation as en_punctuation
from zhon.hanzi import punctuation as zh_punctuation
import warnings
import nltk
import pysbd
import re
import string
from typing import Tuple, Union
from .common import is_alphabet, is_chinese

DEFAULT_PUNCTUATIONS = ["。", "！", "!", ".", "？", "?", ",", "，", ";", "\n"]
ALL_PUNCTUATIONS = en_punctuation + zh_punctuation # 注意：不含有中文标点符号



# TODO: Need to hangle special punctuation like ... and .
# TODO: Can re.split work more elegently ?

def pad_mixed_language_by_space(sentence, language="mixed", split_puncs=True, space_chinese_char=False, punctuations: Union[list, str] = "default"):
    assert language in ["mixed", "english"]
    clean_para = ""
    if punctuations == "default":
        punctuations = set(DEFAULT_PUNCTUATIONS)
    elif punctuations == "all":
        punctuations = set(ALL_PUNCTUATIONS)
    else:
        punctuations = set() if not punctuations else punctuations
    seg_english = ""
    for char in sentence:
        # 中英文混合
        if language is "mixed":
            if not is_chinese(char):
                seg_english += char
            # 处理中文字符
            else:
                if seg_english:
                    # 分隔非汉字
                    clean_english = pad_mixed_language_by_space(seg_english, language="english", split_puncs=split_puncs)
                    seg_english = ""
                    clean_para = clean_para.strip() + " " + clean_english.strip() + " "

                if space_chinese_char:
                    # 分隔汉字
                    clean_para = clean_para.strip() + " " + char + " "
                else:
                    clean_para += char
        else:
            # 处理英文片段
            if split_puncs and char in punctuations:
                clean_para = clean_para.strip() + " " + char + " "
            else:
                clean_para += char
    if seg_english:
        # 分隔非汉字
        clean_english = pad_mixed_language_by_space(seg_english, language="english", split_puncs=split_puncs)
        seg_english = ""
        clean_para = clean_para.strip() + " " + clean_english.strip() + " "
    return clean_para

# ----------------------------------------------------------- #
# ----------------------------分句--------------------------- #
# ----------------------------------------------------------- #
def split_text(para, remain_split_char_way: Tuple[bool, str]="drop", split_char_list=DEFAULT_PUNCTUATIONS): 
    sents = []
    sent = ""
    if isinstance(remain_split_char_way, bool):
        remain_split_char_way = "left" if remain_split_char_way is True else "drop"
    elif isinstance(remain_split_char_way, str):
        assert remain_split_char_way in ["drop", "left", "space", "split"]

    for char in para:
        if char in split_char_list:
            if remain_split_char_way == "left":
                sent += char
            if remain_split_char_way == "space":
                sent = sent.rstrip() + " " +  char + " "            
            if sent:
                sents.append(sent)
            if remain_split_char_way == "split":
                sents.append(char)
            sent = ""
        else:
            sent += char
    if sent:
        sents.append(sent)
    return sents

def split_sentence_by_punctuation(sentence, remain_punc=True, punctuation=DEFAULT_PUNCTUATIONS):
    return split_text(sentence, remain_split_char_way=remain_punc, split_char_list=punctuation)


# ----------------------------------------------------------- #
# ----------------------------分句--------------------------- #
# ----------------------------------------------------------- #

class WiseClauseTokenizer(object):
    def __init__(self, flag="#"):
        self.seg = pysbd.Segmenter(language="en", clean=False)
        self.flag = flag

    def add_clause_flag(self, sentence):
        # tokens = re.split(r" ", sentence)
        tokens = sentence.replace(" ", "\t").split("\t")
        tagged_sent = nltk.pos_tag(tokens)
        sent_parsed = []
        for x, t in tagged_sent:
            if t in ["CC", "IN", "WRB", "LS"]:
                sent_parsed.append(self.flag + x)
            else:
                sent_parsed.append(x)
        return " ".join(sent_parsed)

    def cut4sent_simple(self, sentence):
        return self.seg.segment(sentence)

    def cut4sent_by_flag(self, para):
        split_set = [self.flag]
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
                while j < len(para) and para[j] not in split_set:
                    j += 1
                if j - i <= key_limit:
                    # print("test 3 ==",para[i:j])
                    continue
                # 将句子后面的 换行符和空格 也划入此句子内
                blank_idx = i+1
                # important!
                while blank_idx < len(para) and para[blank_idx] in ["\n", " "]:
                    blank_idx += 1
                text_sent = para[_s: blank_idx]
                text_sent = text_sent.replace(self.flag, "")
                if text_sent:
                    split_sents.append(text_sent)

                _s = blank_idx

        if _s != len(para):
            split_sents.append(para[_s:len(para)].replace(self.flag, ""))

        if len(split_sents) == 0:
            split_sents.append(para.replace(self.flag, ""))
        return split_sents

    def cut4sent_by_punctuation(self, para, level=1):
        if level == 1:
            split_set = set(['。', '！', '!', '.', '？', '?'])  # 句子
        elif level == 2:
            split_set = set(['。', '！', '!', '.', '？', '?', ',', ';']) # 子句
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
                    while j < len(para) and para[j] not in split_set:
                        j += 1
                    if j - i <= limit:
                        continue
                # 将句子后面的 换行符和空格 也划入此句子内
                blank_idx = i+1
                # important!
                while blank_idx < len(para) and para[blank_idx] in ["\n", " "]:
                    blank_idx += 1
                text_sent = para[_s: blank_idx]
                if text_sent:
                    split_sents.append(text_sent)

                _s = blank_idx

        if _s != len(para):
            split_sents.append(para[_s:len(para)])
        if len(split_sents) == 0:
            split_sents.append(para)

        return split_sents

    def tokenize(self, text, *argc, level=2, **argv):
        ss1 = self.cut4sent_simple(text)

        ss2 = []
        for s in ss1:
            s = self.add_clause_flag(s)  # 子句标志
            ss2.extend(self.cut4sent_by_punctuation(s, level=level))  # 使用标点符号划分粗子句

        ss3 = []
        for s in ss2:
            ss3.extend(self.cut4sent_by_flag(s))  # 使用标志划分细子句

        if len(text) != len("".join(ss3)):
            warnings.warn(f"'{self.flag}' in sentence is not recommend!")
        return ss3



# if __name__ == "__main__":
#     text = "there are 28 stations between hyderabad and bangalore \t\t  . how many second class tickets have to be printed , so that a passenger can travel from any station to any other station ?"
#     t = WiseClauseTokenizer().tokenize(text)
#     print(t)

#     text = "中文混合english,并且——含有符号"
#     clean_text = preprocess_string(text)
#     print(clean_text)
