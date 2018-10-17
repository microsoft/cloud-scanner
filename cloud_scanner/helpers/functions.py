
def batch_list(items, batch_size):
    """Create batches from list of elements.

    :param items: List of all elements
    :param batch_size: Desired size of batches
    :return: Batches of list
    """
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]
