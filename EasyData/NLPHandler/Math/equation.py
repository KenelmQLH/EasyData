# -*- encoding:utf-8 -*-
import re
from .common import COMMON_NUM_PATTERN

def infix_to_postfix(expression):
    st = list()
    res = list()
    priority = {"+": 0, "-": 0, "*": 1, "/": 1, "^": 2}
    for e in expression:
        if e in ["(", "["]:
            st.append(e)
        elif e == ")":
            c = st.pop()
            while c != "(":
                res.append(c)
                c = st.pop()
        elif e == "]":
            c = st.pop()
            while c != "[":
                res.append(c)
                c = st.pop()
        elif e in priority:
            while len(st) > 0 and st[-1] not in ["(", "["] and priority[e] <= priority[st[-1]]:
                res.append(st.pop())
            st.append(e)
        else:
            res.append(e)
    while len(st) > 0:
        res.append(st.pop())
    return res

def postfix_to_prefix(post_equ, check=False):
    op_list = set(["+", "-", "*", "/", "^"])
    stack = []
    for elem in post_equ:
        sub_stack = []
        if elem not in op_list:
            sub_stack.append(elem)
            stack.append(sub_stack)
        else:
            if len(stack) >= 2:
                opnds = reversed([stack.pop() for i in range(2)])
                sub_stack.append(elem)
                for opnd in opnds:
                    sub_stack.extend(opnd)
                stack.append(sub_stack)
    if check and len(stack) != 1:
        pre_equ = None
    else:
        pre_equ = stack.pop()
    return pre_equ

def post_solver(post_equ):
    op_list = set(['+', '-', '/', '*', '^'])
    status = True
    stack = []
    for elem in post_equ:
        if elem in op_list:
            if len(stack) >= 2:
                op = elem
                opnd2 = stack.pop()
                opnd1 = stack.pop()
                if op == '+':
                    answer = opnd1 + opnd2
                elif op == '-':
                    answer = opnd1 - opnd2
                elif op == '*':
                    answer = opnd1 * opnd2
                elif op == '/':
                    answer = opnd1 / opnd2
                elif op == '^':
                    answer = opnd1 ** opnd2
                else:
                    status = False
                    break
                stack.append(answer)
            else:
                status = False
                break
        else:
            elem = float(elem)
            stack.append(elem)
    if status and len(stack) == 1:
        answer = stack.pop()
    else:
        answer = None
        status = False
    return status, answer


def number_map(equ, num_list):
    num_equ = []
    for token in equ:
        if "temp_" in token:
            token = num_list[ord(token[-1]) - ord('a')]
        elif token == "PI":
            token = 3.14
        num_equ.append(token)
    return num_equ


def eval_num_list(str_num_list):
    num_list = list()
    for item in str_num_list:
        if item[-1] == "%":
            num_list.append(float(item[:-1]) / 100)
        else:
            num_list.append(eval(item))
    return num_list


def replace_num_with_tag(text, pattern=COMMON_NUM_PATTERN, tag="[NUM]"):
    return re.sub(pattern, tag, text)

def pad_num_with_space(text, pattern=COMMON_NUM_PATTERN):
    return re.sub(pattern, r" \1 ", text)


def extract_num(text, pattern=COMMON_NUM_PATTERN):
    nums = re.findall(pattern, text)
    return nums


from copy import deepcopy

def transfer_num(data):
    pattern = re.compile(r"\d*\(\d+/\d+\)\d*|\d+\.\d+%?|\d+%?")
    n_data = list()
    for d in data:
        nums = []
        input_seq = []
        seg = d["segmented_text"].strip().split(" ")
        equations = d["equation"][2:]

        n_num = 0
        for s in seg:
            pos = re.search(pattern, s)
            if pos and pos.start() == 0:
                nums.append(s[pos.start(): pos.end()])
                input_seq.append(f"num{str(n_num)}")
                n_num += 1
                if pos.end() < len(s):
                    input_seq.append(s[pos.end():])
            else:
                input_seq.append(s)

        nums_fraction = []
        for num in nums:
            if re.search(r"\d*\(\d+/\d+\)\d*", num):
                nums_fraction.append(num)
        nums_fraction = sorted(nums_fraction, key=lambda x: len(x), reverse=True)

        # seg the equation and tag the num
        def seg_and_tag(st):
            res = []
            for n in nums_fraction:
                if n in st:
                    p_start = st.find(n)
                    p_end = p_start + len(n)
                    if p_start > 0:
                        res += seg_and_tag(st[:p_start])
                    if n in nums:
                        res.append(f"num{str(nums.index(n))}")

                        res.append(n)
                    if p_end < len(st):
                        res += seg_and_tag(st[p_end:])
                    return res
            pos_st = re.search(r"\d+\.\d+%?|\d+%?", st)
            if pos_st:
                p_start = pos_st.start()
                p_end = pos_st.end()
                if p_start > 0:
                    res += seg_and_tag(st[:p_start])
                st_num = st[p_start:p_end]
                if st_num in nums:
                    res.append(f"num{str(nums.index(st_num))}")
                else:
                    res.append(st_num)
                if p_end < len(st):
                    res += seg_and_tag(st[p_end:])
                return res
            for ss in st:
                res.append(ss)
            return res

        out_seq = seg_and_tag(equations) # 中序表达式
        postfix = infix_to_postfix(out_seq)
        f_nums = eval_num_list(nums)
        n_d = deepcopy(d)
        n_d['id'] = d['id']
        n_d['equation'] = d['equation']

        n_d['text'] = ' '.join(input_seq)
        n_d['equation_infix_template'] = ' '.join(out_seq)  # ['x', '='] + 
        n_d['equation_post_template'] = ' '.join(postfix)  # ['x', '='] + 
        n_d['num_list'] = f_nums

        n_data.append(n_d)
        if post_solver(number_map(postfix, f_nums)) is None:
            print(d['id'])
    return n_data
