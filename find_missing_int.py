##################################################
##  Problem 3.c. Find the Missing Number 2
##################################################

# Given n integers in the range [0,N] where n <= N, find an integer
# in the range [0,N] that is missing. If there are multiple missing numbers,
# return any of them. There is at least one number in the range that is missing.


def find_missing_int(arr, N):
    '''
    Inputs:
        arr     (list(int)) | List of unsorted, unique positive integer order id's
        N       (int)       | A positive integer larger than len(arr)
    Output:
        -       (int)       | An integer in the range [0,N] not present in arr
    '''

    n = len(arr)

    daa = [False] * (n+1)

    for elt in arr:
        if elt <= n:
            daa[elt] = True
    
    for i in range(len(daa)):
        if not daa[i]:
            return i



