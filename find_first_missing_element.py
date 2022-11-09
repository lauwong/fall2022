##################################################
##  Problem 3.4. Find order
##################################################

# Given a list of positive integers and the starting integer s, return x such that x is the smallest value greater than
# or equal to s that's not present in the list

def binary_search(arr, val):

    p1 = 0
    p2 = len(arr) - 1

    while p1 <= p2:
        n = (p1 + p2) // 2
        if arr[n] == val:
            return n
        elif arr[n] < val:
            p1 = n+1
        else:
            p2 = n-1
    return None


def find_first_missing_element(arr, s):
    '''
    Inputs: 
        arr        (list(int)) | List of sorted, unique positive integer order id's
        s          (int)       | Positive integer
    Output: 
        -          (int)       | The smallest integer greater than or equal to s that's not present in arr
    '''
    ##################
    # YOUR CODE HERE #
    ################## 
    try:
        if not min(arr) <= s <= max(arr):
            return s
    except:
        return s

    s_idx = binary_search(arr, s)

    if s_idx is None:
        return s

    p1 = s_idx
    p2 = len(arr) - 1

    while p2 - p1 > 1:
        n = (p1 + p2) // 2
        if arr[n] > n - p1 + arr[p1]:
            p2 = n-1
        else:
            p1 = n
    
    if arr[p2] - arr[p1] == 1:
        return arr[p2] + 1
    else:
        return arr[p1] + 1