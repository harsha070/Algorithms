class MergeSortTree(object):
    
    def __init__(self, a):
        self.a = a
        self.n = len(a)
        self.tree = [None for _ in range(4 * self.n)]
        self.construct(0, 0, self.n - 1)
        self.INT_MAX = 1000000000
    
    def construct(self, index, start, end):
        if start == end:
            self.tree[index] = [self.a[start]]
            return
        if start > end:
            return
        mid = (start + end) // 2
        self.construct(2 * index + 1, start, mid)
        self.construct(2 * index + 2, mid + 1, end)
        
        self.tree[index] = self.merge(self.tree[2 * index + 1], self.tree[2 * index + 2])
        return
    
    @staticmethod
    def merge(a, b):
        n = len(a)
        m = len(b)
        i = 0
        j = 0
        c = []
        while len(c) < n + m:
            if i == n:
                c.append(b[j])
                j += 1
            elif j == m:
                c.append(a[i])
                i += 1
            elif a[i] <= b[j]:
                c.append(a[i])
                i += 1
            else:
                c.append(b[j])
                j += 1
        return c
    
    def search(self, a, x):
        left = 0
        right = len(a) - 1
        if x < a[left]:
            return a[left]
        if x > a[right]:
            return self.INT_MAX
        while left < right:
            mid = (left + right) // 2
            if a[mid] < x:
                left = mid + 1
            else:
                right = mid
        return a[left]
    
    def point_update(self, index, start, end, i, value):
        if i > end or i < start:
            return
        if start == end:
            self.tree[index] = value
            return
        mid = (start + end) // 2
        if i <= mid:
            self.point_update(2 * index + 1, start, mid, i, value)
        else:
            self.point_update(2 * index + 2, mid + 1, end, i, value)
        self.tree[index] = self.merge(self.tree[2 * index + 1], self.tree[2 * index + 2])
        return
    
    def range_update(self, index, start, end, i, j, value):
        pass
    
    def point_query(self, index):
        return self.range_query(0, 0, self.n - 1, index, index)
    
    def range_query(self, index, start, end, i, j, value):
        # return tree, max-sum-left, max-sum-right, sum
        if i > end or j < start:
            return None
        if i <= start and end <= j:
            return self.search(self.tree[index], value)
        mid = (start + end) // 2
        l_tree = self.range_query(2 * index + 1, start, mid, i, j, value)
        r_tree = self.range_query(2 * index + 2, mid + 1, end, i, j, value)
        tree = min(l_tree, r_tree)
        return tree
