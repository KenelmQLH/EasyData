def BatchGenerator(data: list, batch_size: int):
    batch_num = int(len(data)/batch_size)
    if len(data) % batch_size != 0:
        batch_num += 1
    for idx in range(batch_num):
        batch_start = idx*batch_size
        batch_end = min((idx+1)*batch_size, len(data))
        yield data[batch_start:batch_end]