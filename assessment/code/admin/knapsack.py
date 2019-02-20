def knapsack(load_weight, object_dict, **kwargs):
    if not kwargs:
        return knapsack(load_weight, object_dict, n=len(object_dict))

    n = kwargs["n"]

    if load_weight < 0:
        return float("-inf")

    if n == 0:
        return 0

    take_num = knapsack(
        load_weight=load_weight - object_dict[n - 1]["weight"],
        object_dict=object_dict,
        n=n - 1
    ) + object_dict[n - 1]["price"]

    do_not_take_num = knapsack(
        load_weight=load_weight,
        object_dict=object_dict,
        n=n - 1
    )

    return max(take_num, do_not_take_num)