import json
import pickle
import os

def check2mkdir(file_path):
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

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


def save_json(save_data, output_path):
    print("[save_json] start : {}".format(output_path))
    check2mkdir(output_path)
    with open(output_path,'w+',encoding="utf-8") as f:
        for row_dic in save_data:
            try:
                jsondata=json.dumps(row_dic, ensure_ascii=False)
                f.write(jsondata + "\n")
            except Exception as e:
                print("[Exception] at {}:\n{}\n".format(row_dic, e))
                raise Exception("[save_json] 出现错误")
    print("[save_json] num = {}, open_path = {}".format(len(save_data), output_path))

def get_json(open_path):
    print("[get_json] start : {}".format(open_path))
    load_data = []
    i = 0
    with open(open_path, 'r', encoding="utf-8") as f:
        try:
            for line in f:
                load_data.append(json.loads(line))
                i += 1
        except Exception as e:
            print("[Exception] at line {}:\n{}\n".format(i, e))
            raise Exception("[get_json] 出现错误")
    print("[get_json] num = {}, open_path = {}".format(len(load_data), open_path))
    return load_data


def merge_json_files(file_paths,output_path):
    print("="*100)
    check2mkdir(output_path)
    result = []
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print("[warning] {} not exists".format(file_path))
            continue
        json_data = get_json(file_path)
        result.extend(json_data)
    save_json(result, output_path)
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


# if __name__ == '__main__':
#     test_path = "/home/qlh/data_pretrain/data/test2/test_funciton.py"
#     check2mkdir(test_path)
#     test_path = "/home/qlh/data_pretrain/data/test3"
#     check2mkdir(test_path)
#     test_path = "/home/qlh/data_pretrain/data/test4/"
#     check2mkdir(test_path)

