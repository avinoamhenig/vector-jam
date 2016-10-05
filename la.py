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
