class TwoDSegmentTree(object):
    
    def __init__(self, rectangle):
        self.rectangle = rectangle
        self.n = len(self.rectangle)
        self.m = len(self.rectangle[0])
        dim = max(self.n, self.m)
        self.tree = [None for _ in range(dim * dim * 4)]
        self.lazy = [False for _ in range(dim * dim * 4)]
        self.construct(0, 0, 0, self.n-1, self.m-1)
        
    def construct(self, index, row_1, col_1, row_2, col_2):
        if row_1 > row_2 or col_1 > col_2:
            return
        if row_1 == row_2 and col_1 == col_2:
            self.tree[index] = self.rectangle[row_1][col_1]
            return
        row_m = row_1 + (row_2 - row_1) // 2
        col_m = col_1 + (col_2 - col_1) // 2
        self.construct(4 * index + 1, row_1, col_1, row_m, col_m)
        self.construct(4 * index + 2, row_1, col_m + 1, row_m, col_2)
        self.construct(4 * index + 3, row_m + 1, col_1, row_2, col_m)
        self.construct(4 * index + 4, row_m + 1, col_m + 1, row_2, col_2)
        self.tree[index] = None

    def point_update(self, row, col, value):
        pass

    def range_update(self, index, row_1, col_1, row_2, col_2, i_1, j_1, i_2, j_2, value):
        if row_1 > row_2 or col_1 > col_2:
            return
        if i_1 > row_2 or i_2 < row_1:
            return
        if j_2 < col_1 or j_1 > col_2:
            return
        if row_1 != row_2 or col_1 != col_2:
            self.push(index)
        if i_1 <= row_1 and row_2 <= i_2 and j_1 <= col_1 and col_2 <= j_2:
            self.tree[index] = value
            self.lazy[index] = True
            if row_1 == row_2 and col_1 == col_2:
                self.lazy[index] = False
            return
        row_m = row_1 + (row_2 - row_1) // 2
        col_m = col_1 + (col_2 - col_1) // 2
        self.range_update(4 * index + 1, row_1, col_1, row_m, col_m, i_1, j_1, i_2, j_2, value)
        self.range_update(4 * index + 2, row_1, col_m + 1, row_m, col_2, i_1, j_1, i_2, j_2, value)
        self.range_update(4 * index + 3, row_m + 1, col_1, row_2, col_m, i_1, j_1, i_2, j_2, value)
        self.range_update(4 * index + 4, row_m + 1, col_m + 1, row_2, col_2, i_1, j_1, i_2, j_2, value)
        
    def push(self, index):
        if not self.lazy[index]:
            return
        assert self.tree[index] is not None
        self.tree[4 * index + 1] = self.tree[index]
        self.tree[4 * index + 2] = self.tree[index]
        self.tree[4 * index + 3] = self.tree[index]
        self.tree[4 * index + 4] = self.tree[index]
        self.lazy[4 * index + 1] = self.lazy[4 * index + 2] = self.lazy[4 * index + 3] = self.lazy[4 * index + 4] = True
        self.lazy[index] = False
        return

    def point_query(self, index, row_1, col_1, row_2, col_2, i, j):
        if row_1 > row_2 or col_1 > col_2:
            return None
        if i < row_1 or i > row_2 or j < col_1 or j > col_2:
            return None
        if row_1 == row_2 == i and col_1 == col_2 == j:
            return self.tree[index]
        self.push(index)
        row_m = row_1 + (row_2 - row_1) // 2
        col_m = col_1 + (col_2 - col_1) // 2
        if row_1 <= i <= row_m and col_1 <= j <= col_m:
            return self.point_query(4 * index + 1, row_1, col_1, row_m, col_m, i, j)
        elif row_1 <= i <= row_m and col_m + 1 <= j <= col_2:
            return self.point_query(4 * index + 2, row_1, col_m + 1, row_m, col_2, i, j)
        elif row_m + 1 <= i <= row_2 and col_1 <= j <= col_m:
            return self.point_query(4 * index + 3, row_m + 1, col_1, row_2, col_m, i, j)
        elif row_m + 1 <= i <= row_2 and col_m + 1 <= j <= col_2:
            return self.point_query(4 * index + 4, row_m + 1, col_m + 1, row_2, col_2, i, j)
        raise Exception
    
    def range_query(self, index, row_1, col_1, row_2, col_2, i_1, j_1, i_2, j_2):
        pass
