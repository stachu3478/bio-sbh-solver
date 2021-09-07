class LevenshteinDistance:
    def compute(self, string1, string2):
        if (string1 == string2):
            return 0
        if (string1 == ''):
            return len(string2)
        if (string2 == ''):
            return len(string1)

        n = len(string1)
        m = len(string2)
        d = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

        # initialize the top and right of the table to 0, 1, 2, ...
        d[0] = [y for y in range(n + 1)]
        for x in range(m + 1):
            d[x][0] = x

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                cost = 0
                if (string2[j - 1] != string1[i - 1]):
                    cost = 1
                min1 = d[i - 1][j] + 1
                min2 = d[i][j - 1] + 1
                min3 = d[i - 1][j - 1] + cost
                d[i][j] = min(min1, min2, min3)
        return d[n][m]

LevenshteinDistance.compute = staticmethod(LevenshteinDistance.compute)