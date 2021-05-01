def dictify(item):

    if isinstance(item, dict):
        for k, v in item.items():
            item[k] = dictify(v)
        return item
    elif isinstance(item, (list, tuple)):
        # assuming the item in list won't be dictionaries
        return  { k:i for i , k in enumerate(item)}
    
