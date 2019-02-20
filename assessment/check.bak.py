def knapsack(w, d, **kwargs):
    if not kwargs:
        return knapsack(w, d, n=len(d))

    num = kwargs["n"]

    if w < 0:
        return float("-inf")
    if num == 0:
        return 0

    ans = max(knapsack(w - d[num], d, n=num - 1), knapsack(w, d, n=num - 1))


d = (
    {"w": 850, "p": 400},
    {"w": 300, "p": 150},
    {"w": 500, "p": 150},
    {"w": 200, "p": 120}
)
