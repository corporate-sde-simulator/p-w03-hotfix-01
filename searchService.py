"""
====================================================================
 JIRA: PLATFORM-2870 — Fix Binary Search Off-by-One in Search Service
====================================================================
 Priority: P1 | Sprint: Sprint 25 | Points: 2
 Reporter: Search Team (automated tests)
 Labels: algorithms, python, production, search

 DESCRIPTION:
 The binary search in our sorted inventory lookup returns wrong results
 for edge cases: first element, last element, and single-element arrays.
 The boundary condition causes infinite loop on arrays of length 1.

 FAILING TEST LOG:
 ─────────────────
 FAIL: test_first_element — expected index 0, got -1
 FAIL: test_single_element — timeout (infinite loop)
 PASS: test_middle_element
 FAIL: test_not_found — expected -1, got 3
 
 SLACK — #search-team:
 @dev: "The binary search has off-by-one. Check the while condition
        and the right boundary initialization."

 ACCEPTANCE CRITERIA:
 - [ ] Returns correct index for all positions (first, middle, last)
 - [ ] Returns -1 for elements not in array
 - [ ] No infinite loop on edge cases (empty array, single element)
 - [ ] All 6 test assertions pass
====================================================================
"""

def binary_search(arr, target):
    """Binary search on a sorted array. Returns index or -1."""
    if not arr:
        return -1

    left = 0
    right = len(arr)  # BUG: Should be len(arr) - 1

    while left < right:  # BUG: Should be left <= right (misses single element)
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1  # This can make right < left with the wrong init

    return -1


# ─── Tests ──────────────────────────────────────
if __name__ == '__main__':
    data = [1, 3, 5, 7, 9, 11, 13, 15]

    assert binary_search(data, 1) == 0, "FAIL: first element"
    assert binary_search(data, 15) == 7, "FAIL: last element"
    assert binary_search(data, 7) == 3, "FAIL: middle element"
    assert binary_search(data, 6) == -1, "FAIL: not found"
    assert binary_search([42], 42) == 0, "FAIL: single element"
    assert binary_search([], 5) == -1, "FAIL: empty array"
    print("All tests passed!")
