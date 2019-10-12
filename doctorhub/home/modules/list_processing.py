def list_to_sublists_of_size_n(any_list=[], n=1):
    return [any_list[i * n:(i + 1) * n] for i in range((len(any_list) + n - 1) // n)]
