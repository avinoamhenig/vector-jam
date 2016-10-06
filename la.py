import math
import cmath

def matrixMul(a, b):
	if not isinstance(a[0], list): a = [[x] for x in a]
	if not isinstance(b[0], list): b = [[x] for x in b]
	if len(a[0]) != len(b):
		raise Exception("Dimensions don't match!")

	result = []
	for row in a:
		new_row = []
		for col in range(len(b[0])):
			s = 0
			for row_i in range(len(b)):
				s += b[row_i][col] * row[row_i]
			new_row.append(s)
		result.append(new_row)
	return result

def scalarMul(s, v):
	return [s*x for x in v]

def eigenvals(m1, m2, m3, m4):
	a = 1
	b = -(m1 + m4)
	c = m1*m4 - m2*m3
	term = b**2 - 4*a*c
	sqrt = cmath.sqrt if term < 0 else math.sqrt
	return (
		(-b + sqrt(term)) / (2*a),
		(-b - sqrt(term)) / (2*a)
	)

def eigen(m1, m2, m3, m4):
	ev1, ev2 = eigenvals(m1, m2, m3, m4)
	return (
		(ev1, ev2),
		[] if isinstance(ev1, complex) else [
			[1, (m1-ev1)/-m2],
			[1, (m1-ev2)/-m2]
		]
	)

def normalize(v):
	norm = math.sqrt(v[0]**2 + v[1]**2)
	return [x/norm for x in v]
