def bellman_ford(Adj, w, s):
    INF = float('inf')
    d = {u:INF for u in Adj}
    parent = {u:None for u in Adj}
    d[s], parent[s] = 0, s

    V = len(Adj)
    for _ in range(V-1):
        for u in Adj:
            for v in Adj[u]:
                if d[u] + w[(u, v)] < d[v]:
                    d[v] = d[u] + w[(u, v)]
                    parent[v] = u
    
    for u in Adj:
        for v in Adj[u]:
            if d[v] > d[u] + w[(u,v)]:
                return None
    
    return d, parent

def find_start_times(constraints):
    """Find the start times that follows the provided constraints.
    Args:
        constraints(List[Tuple[str, str, int]]): A list of tuples
            `(a, b, t)` where `a` and `b` are strings that contain
            variable names such that `a - b <= t`.
    
    Returns:
        A Python dictionary where keys are variables and values are
        their correct assignments.
        `None` if it is not possible.
    """

    # Your code here!
    edges = {}
    weights = {}

    for a, b, t in constraints:
        if b in edges:
            edges[b].append(a)
        else:
            edges[b] = [a]
        
        if not a in edges:
            edges[a] = []
        
        weights[(b,a)] = t

    edges['super'] = list(edges.keys())
    
    for node in edges:
        weights[('super', node)] = 0

    # print(constraints, edges, weights)

    out = bellman_ford(edges, weights, 'super')

    if out is None:
        return None

    return out[0]