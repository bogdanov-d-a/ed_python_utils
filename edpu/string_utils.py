def removeprefix(str_, prefix):
    if str_.find(prefix) == 0:
        return str_[len(prefix):]
    return str_

def removesuffix(str_, suffix):
    if len(suffix) > len(str_):
        return str_
    str_suffix_pos = str_.find(suffix)
    if str_suffix_pos == len(str_) - len(suffix):
        return str_[:str_suffix_pos]
    return str_
