def TwoSum(nums, target):
    memo = []
    nums_len = len(nums)
    for i in range(nums_len):
        if nums[i] not in memo:
            for j in range(i + 1, nums_len):
                if nums[i] + nums[j] == target:
                    return [i, j]
            memo += [i]
    return []


if __name__ == "__main__":
    
    # Base Case
    nums = [2, 7, 11, 15]
    target = 9
    print("Expected: [0, 1]\n Answer: " + str(TwoSum(nums, target)))
    
    # Negative Numbers
    nums = [-2, -7, 11, 15]
    target = 9
    print("Expected: [0, 2]\n Answer: " + str(TwoSum(nums, target)))
    
    # Zero Target
    nums = [1, 2, 3, -1]
    target = 0
    print("Expected: [0, 3]\n Answer: " + str(TwoSum(nums, target)))
    
    # Large Numbers
    nums = [1000000, 2000000, 3000000, 4000000]
    target = 5000000
    print("Expected: [0, 3]\n Answer: " + str(TwoSum(nums, target)))
    
    # No Solution
    nums = [1, 2, 3, 4, 5]
    target = 10
    print("Expected: []\n Answer: " + str(TwoSum(nums, target)))
    
    # Duplicate Elements
    nums = [3, 2, 3]
    target = 6
    print("Expected: [0, 2]\n Answer: " + str(TwoSum(nums, target)))
    
    # Empty Array
    nums = []
    target = 5
    print("Expected: []\n Answer: " + str(TwoSum(nums, target)))
    