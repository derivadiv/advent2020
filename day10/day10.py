def parseAndGetNums(filename):
    nums = []
    with open(filename, 'r') as f:
        for line in f:
            nums.append(int(line.strip()))
    return nums

def getDiffs(nums):
    nums = sorted([0] + nums + [max(nums) + 3])
    onediffs = 0
    threediffs = 0
    for i in range(len(nums)-1):
        diff = nums[i+1] - nums[i]
        if diff == 1:
            onediffs += 1
        elif diff == 3:
            threediffs += 1
    return (onediffs, threediffs)

def run(filename):
    nums = parseAndGetNums(filename)
    return getDiffs(nums)

# print(run('testinput1.txt'))
# print(run('testinput2.txt'))
# print(run('input10.txt'))

# part 2: DP given final num?
# reaches max(nums) + 3 IFF it reaches max(nums)

# cache: start num = key, number of paths from there = value
# I attempted many smarter solutions, but none worked as well as
# this dumb solution with a cache.
def pathsreaching(nums, reach, cache, start):
    if start == reach:
        return 1
    if start > reach:
        return 0
    if start in cache:
        return cache[start]
    p = 0
    if (start + 1) in nums[:3]:
        p += pathsreaching(nums[1:], reach, cache, start + 1)
    if (start + 2) in nums[:3]:
        ind = nums.index(start + 2)
        p += pathsreaching(nums[ind + 1:], reach, cache, start + 2)
    if (start + 3) in nums[:3]:
        ind = nums.index(start + 3)
        p += pathsreaching(nums[ind + 1:], reach, cache, start + 3)
    cache[start] = p
    return p

def run2(filename):
    nums = parseAndGetNums(filename)
    nums = sorted(nums)
    reach = max(nums)
    # clear cache each run
    cache2 = {}
    return pathsreaching(nums, reach, cache2, 0)

print(run2('testinput1.txt'))
print(run2('testinput2.txt'))
print(run2('input10.txt'))
