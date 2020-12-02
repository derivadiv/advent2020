readfilename = 'input1.txt'

def readfile(filename):
    nums = []
    with open(filename, 'r') as f:
        for line in f:
            num = int(line.strip())
            nums.append(num)
    return nums

def part1(filename):
    nums = readfile(filename)
    pairs = set()
    for i in range(len(nums)):
        pair = 2020 - nums[i]
        if pair in pairs:
            return (pair, 2020-pair, pair*(2020-pair))
        pairs.add(nums[i])

def part2(filename):
    nums = readfile(filename)
    diffs = [2020 - k for k in nums]
    for i in range(len(nums)):
        newsum = diffs[i]
        pairs = set()
        for j in range(len(nums)):
            if i != j:
                pair = newsum - nums[j]
                if pair in pairs:
                    return (pair, newsum-pair, 2020-newsum, pair*(newsum-pair)*(2020-newsum))
                pairs.add(nums[j])
                
print(part2(readfilename))
