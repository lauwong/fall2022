def dfs(Adj, s, parent = None, order = None):
    if parent is None:
        parent = [None for v in Adj]
        order = []
        parent[s] = s
    for v in Adj[s]:
        if parent[v] is None:
            parent[v] = s
            dfs(Adj, v, parent, order)
    order.append(s)
    return parent, order

def full_dfs(Adj):
    parent = [None for v in Adj]
    order = []
    for v in range(len(Adj)):
        if parent[v] is None:
            parent[v] = v
            dfs(Adj, v, parent, order)
    return parent, order

def reverse_graph(Adj):
    reverse_adj = [[] for _ in range(len(Adj))]
    for u in range(len(Adj)):
        for v in Adj[u]:
            if reverse_adj[v]:
                reverse_adj[v].append(u)
            else:
                reverse_adj[v] = [u]
    return reverse_adj

def find_meeting_point(Adj):
    '''
    inputs:
        Adj - an adjacency list such as [[1,2], [2], []]
    return a meeting point or None if no meeting points exist
    '''
    reverse = reverse_graph(Adj)
    _,  full_order = full_dfs(reverse)
    _, check_order = dfs(reverse, full_order[-1])
    if check_order == full_order:
        return full_order[-1]
    else:
        print(full_order, check_order)