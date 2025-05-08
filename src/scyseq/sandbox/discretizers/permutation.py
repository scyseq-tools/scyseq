MAX_W = 6 # 6! = 720 symbols which is already huge!
PERMUTATIONS = [list(itertools.permutations(list(range(k)))) for k in range(0, MAX_W+1)]

def permutation_coding(data, w, tau=1, array=False):
    """
    Permutation encoding due to Brandt and Pompe
    """
    global PERMUTATIONS, MAX_W
    if w > MAX_W:
        raise ValueError('w should be <= to %s' % str(MAX_W))
    modele = PERMUTATIONS[w]
    data = np.array(data)
    s = []
    N = len(data)

    for n in range(N-w*tau+1):
        tmp = data[n:n+w*tau:tau] # from:to:step
        # print tmp
        ind = tuple(np.argsort(tmp)) # increasing order
        s.append(modele.index(ind))

    if array:
        return np.array(s)
    else:
        return S.Sequence(s, math.factorial(w))

