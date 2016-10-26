import math
import cmath

class Matrix:
    def __init__(self, rows):
        self.m = rows
        self.numRows = len(rows)
        self.numCols = len(rows[0])

    def identity(dim):
        return Matrix([
            [1 if c == r else 0 for c in range(dim)]
            for r in range(dim)
        ])

    def rows(self):
        return self.m

    def cols(self):
        return [[row[i] for row in self.m] for i in range(self.numCols)]

    def vals(self):
        return [x for row in self.m for x in row]

    def isColVector(self):
        return self.numCols == 0

    def isRowVector(self):
        return self.numRows == 0

    def mul(self, b):
        if self.numCols != b.numRows: raise Exception("Dimensions do not match")
        result = []
        for row in self.rows():
            new_row = []
            for col in b.cols():
                s = 0
                for i in range(len(col)):
                    s += row[i] * col[i]
                new_row.append(s)
            result.append(new_row)
        return Matrix(result)

    def scalarMul(self, s):
        return Matrix([[s*x for x in row] for row in self.rows()])

    def __mul__(self, b):
        if not isinstance(b, self.__class__): return self.scalarMul(b)
        else: return self.mul(b)
    def __rmul__(self, a):
        if not isinstance(a, self.__class__): return self.scalarMul(a)
        else: return a.mul(self)

    def __eq__(self, b):
        return isinstance(b, self.__class__) and self.rows() == b.rows()
    def __ne__(self, b):
        return not self.__eq__(b)

    def norm(self):
        s = 0
        for x in self.vals():
            s += x**2
        return math.sqrt(s)

    def normalize(self):
        norm = self.norm()
        return (1/norm * Matrix.identity(self.numRows)) * self

    def transpose(self):
        return Matrix(self.cols())

    def conjugate(self):
        # TODO actually implement conjugate
        return self

    def adjoint(self):
        return self.transpose().conjugate()

    def isHermitian(self):
        return self == self.adjoint()

    def isUnitary(self, accuracy=.0001):
        if self.numRows != self.numCols: return False
        identity_matrix = Matrix.identity(2)
        product = self * self.adjoint()
        rounded = Matrix([
            # round to 1 if v close
            [1 if abs(1-x) < accuracy else x for x in row] for row in product.rows()
        ])
        return rounded == identity_matrix

    def eigenvals(self):
        if self.numRows != 2 or self.numCols != 2:
            raise Exception("Can only find eigenvalues of a 2x2 matrix")
        m1, m2 = self.rows()[0]
        m3, m4 = self.rows()[1]
        a = 1
        b = -(m1 + m4)
        c = m1*m4 - m2*m3
        term = b**2 - 4*a*c
        sqrt = cmath.sqrt if term < 0 else math.sqrt
        return (
            (-b + sqrt(term)) / (2*a),
            (-b - sqrt(term)) / (2*a)
        )

    def eigen(self):
        ev1, ev2 = self.eigenvals()
        m1, m2 = self.rows()[0]
        return (
            (ev1, ev2),
            [] if isinstance(ev1, complex) else [
                Matrix([[1], [(m1-ev1)/-m2]]),
                Matrix([[1], [(m1-ev2)/-m2]])
            ]
        )
