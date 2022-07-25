import json
import pickle
import os
import warnings

def check2mkdir(file_path):
    "note: file_path must be like path/to/dir/filename"
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def read_json(open_path):
    load_data = json.load(open(open_path, 'r', encoding='utf-8'))
    print("[read_json] num = {}, open_path = {}".format(len(load_data), open_path))
    return load_data

def write_json(save_data, output_path):
    check2mkdir(output_path)
    with open(output_path, 'w+', encoding="utf-8") as f:
        f.write(json.dumps(save_data, indent=4, ensure_ascii=False))
    print("[write_json] num = {}, save_path = {}".format(len(save_data), output_path))


def save_pkl(save_data, output_path):
    check2mkdir(output_path)
    output = open(output_path, 'wb')
    pickle.dump(save_data, output)
    output.close()
    print("[save_pkl] num = {}, save_path = {}".format(len(save_data), output_path))

def get_pkl(open_path):
    pkl_file = open(open_path, 'rb')
    load_data = pickle.load(pkl_file)
    pkl_file.close()
    print("[get_pkl] num = {}, open_path = {}".format(len(load_data), open_path))
    return load_data

def read_line_json(open_path, error_handler="raise"):
    print("[read_line_json] start : {}".format(open_path))
    load_data = []
    i = 0
    with open(open_path, 'r', encoding="utf-8") as f:
        try:
            for line in f:
                load_data.append(json.loads(line))
                i += 1
        except Exception as e:
            if error_handler == "ignore":
                warnings.warn("[Warning] at line {}:\n{}\n".format(i, e))
            else:
                print("[Exception] at line {}:\n{}\n".format(i, e))
                raise Exception("[read_line_json] 出现错误")
    print("[read_line_json] num = {}, open_path = {}".format(len(load_data), open_path))
    return load_data

def write_line_json(save_data, output_path):
    print("[write_line_json] start : {}".format(output_path))
    check2mkdir(output_path)
    with open(output_path,'w+',encoding="utf-8") as f:
        for row_dic in save_data:
            try:
                jsondata=json.dumps(row_dic, ensure_ascii=False)
                f.write(jsondata + "\n")
            except Exception as e:
                print("[Exception] at {}:\n{}\n".format(row_dic, e))
                raise Exception("[write_line_json] 出现错误")
    print("[write_line_json] num = {}, open_path = {}".format(len(save_data), output_path))



def merge_json_files(file_paths, output_path, line_format=True):
    print("="*100)
    check2mkdir(output_path)
    
    result = []
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print("[warning] {} not exists".format(file_path))
            continue
        if line_format is True:
            json_data = read_line_json(file_path)
        else:
            json_data = read_json(file_path)
        result.extend(json_data)
    if line_format is True:
        write_line_json(result, output_path)
    else:
        write_json(result, output_path)
    
    print("="*100)
    print("[merge_json_files] finish merge => {}".format(output_path))

def merge_pkl_files(file_paths,output_path,datatype='List'):
    if datatype != 'List':
        return None
    
    print("="*100)
    check2mkdir(output_path)
    all_data = []
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print("[warning] {} not exists".format(file_path))
            continue
        pkl_data = get_pkl(file_path)
        all_data.extend(pkl_data)
    save_pkl(all_data, output_path)
    print("="*100)
    print("[merge_pkl_files] finish merge => {}".format(output_path))
