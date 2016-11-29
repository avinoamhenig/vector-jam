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
        if self.numCols != b.numRows:
            raise Exception("Matrix dimensions do not match for multiplication")
        result = []
        for row in self.rows():
            new_row = []
            for col in b.cols():
                s = 0
                for i in range(len(col)):
                    s += row[i] * col[i]
                new_row.append(s)
            result.append(new_row)
        return result[0][0] if self.numRows == 1 and b.numCols == 1 else Matrix(result)

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

    def __repr__(self):
        s = ""
        for row in self.rows():
            for x in row:
                s += str(x) + '\t'
            s += '\n'
        return s[:-1]

    def __add__(self, b):
        if not isinstance(b, self.__class__):
            raise Exception("Cannot add "
                    + str(type(self)) + " and "
                    + str(type(b)) + ".")
        if b.numRows != self.numRows or b.numCols != self.numCols:
            raise Exception("Matrix dimensions do not match for addition")

        ar = self.rows()
        br = b.rows()
        result = []
        for r in range(self.numRows):
            result.append([])
            for c in range(self.numCols):
                result[r].append(ar[r][c] + br[r][c])
        return Matrix(result)

    def tensor(self, b):
        result = []
        rowIndex = 0
        for row in self.rows():
            result += [[] for _ in range(b.numRows)]
            for x in row:
                multiplied = (x * b).rows()
                for i in range(b.numRows):
                    result[rowIndex + i] += multiplied[i]
            rowIndex += b.numRows
        return Matrix(result)

    def norm(self, comp = False):
        s = 0
        for x in self.vals():
            s += abs(x)**2
        return (cmath if comp else math).sqrt(s)

    def normalize(self, comp = False):
        norm = self.norm(comp)
        return ((norm if norm == 0 else 1/norm) *
                Matrix.identity(self.numRows)) * self

    def transpose(self):
        return Matrix(self.cols())

    def conjugate(self, comp = False):
        if comp:
            return Matrix([[z.conjugate() for z in row] for row in self.rows()])
        else:
            return self

    def adjoint(self, comp = False):
        return self.transpose().conjugate(comp)

    def isHermitian(self, comp = False):
        return self == self.adjoint(comp)

    def isUnitary(self, accuracy=.0001):
        if self.numRows != self.numCols: return False
        identity_matrix = Matrix.identity(2)
        product = self * self.adjoint()
        rounded = Matrix([
            # round to 1 if v close
            [1 if abs(1-x) < accuracy else x for x in row]
            for row in product.rows()
        ])
        return rounded == identity_matrix

    def eigenvals(self, comp = False):
        if self.numRows != 2 or self.numCols != 2:
            raise Exception("Can only find eigenvalues of a 2x2 matrix")
        m1, m2 = self.rows()[0]
        m3, m4 = self.rows()[1]
        a = 1
        b = -(m1 + m4)
        c = m1*m4 - m2*m3
        term = b**2 - 4*a*c
        sqrt = cmath.sqrt if comp or term < 0 else math.sqrt
        return (
            (-b + sqrt(term)) / (2*a),
            (-b - sqrt(term)) / (2*a)
        )

    def eigenvector(self, ev, comp = False):
        a, b, c, d = self.vals()
        if d - ev != 0:
            return Matrix([[1], [-c/(d-ev)]]).normalize(comp)
        elif b != 0:
            return Matrix([[1], [(a-ev)/-b]]).normalize(comp)
        elif a - ev != 0:
            return Matrix([[-b/(a-ev)], [1]]).normalize(comp)
        elif c != 0:
            return Matrix([[(d-ev)/-c], [1]]).normalize(comp)
        else:
            return Matrix([[0], [0]])

    def eigen(self, comp = False):
        ev1, ev2 = self.eigenvals(comp)
        return (
            (ev1, ev2),
            [ Matrix([[0], [0]]),
                Matrix([[0], [0]])
            ] if (not comp) and isinstance(ev1, complex) else [
                self.eigenvector(ev1, comp),
                self.eigenvector(ev2, comp)
            ]
        )

    def innerProduct(self, b):
        return b.adjoint() * self
