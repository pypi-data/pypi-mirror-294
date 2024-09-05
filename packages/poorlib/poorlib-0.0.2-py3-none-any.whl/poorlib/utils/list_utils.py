"""Generator function for helping iteration of list by split the list"""
def split_list(items: list, batch=10000):
    total_list = len(items)
    if total_list > 0 and total_list%batch == 0:
        total_batch = total_list // batch
    else:
        total_batch = total_list // batch + 1

    for x in range(total_batch):
        yield items[batch * x:batch * (x + 1)]