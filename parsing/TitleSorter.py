
def get_highest_title_keys(titles):
    for prefix in ['e', 'k', 'd', 'c', 'b']:
        keys_with_prefix = []
        for title in titles:
            if title[0] == prefix:
                keys_with_prefix.append(title)

        if len(keys_with_prefix) > 0:
            return keys_with_prefix

    return []