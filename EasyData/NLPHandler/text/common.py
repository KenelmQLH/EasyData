def is_number(uchar):
        """判断一个unicode是否是数字"""
        if u'\u0030' <= uchar <= u'\u0039':
            return True
        else:
            return False

def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):
        return True
    else:
        return False

def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if u'\u4e00' <= uchar <= u'\u9fa5':
        return True
    else:
        return False

# c.isalnum()
# c.isspace()
# set(string.punctuation): 
