import os


def gcd(m,n):
    if n == 0:
        return m
    else:
        rest = m%n
        return gcd(n, rest)

def binary_search(vals, i, j, key):
    if i > j:
        return None
    else:
        k = int((i+j)/2)
        if vals[k] == key:
            return k
        elif vals[k] > key:
            return binary_search(vals, i, k-1, key)
        elif vals[k] < key:
            return binary_search(vals, k+1, j, key)


def total_file_size(path):
    tot_size = 0
    for thing in os.listdir(path):
        sub_path = path+"/"+thing
        if os.path.isdir(sub_path):
            tot_size += total_file_size(sub_path)
        else:
            #try:
            tot_size += os.path.getsize(sub_path)
            #except:
            #    print(sub_path, "not found")
    return tot_size


def format_size(size):
    prefixes = ["", "K", "M", "G", "T", "P"]
    tens = 0
    while size > 1000:
        size /= 1000
        tens += 1
    return f"{round(size, 2)} {prefixes[tens]}B"

print("GCD:", gcd(1300, 40))
print("Binary search:", binary_search([1,2,3,4,5,6,7,8,9], 2, 6, 6))



print("Size:", format_size(total_file_size("/home/hd/kode")))
