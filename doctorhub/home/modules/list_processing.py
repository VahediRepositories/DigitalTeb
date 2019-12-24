def list_to_sublists_of_size_n(any_list=[], n=1):
    l = [any_list[i * n:(i + 1) * n] for i in range((len(any_list) + n - 1) // n)]
    for item in l:
        item.reverse()
    return l
