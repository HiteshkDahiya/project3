print("Enter entries for matrix:")
matrix = []
for i in range(2):
    list = []
    for j in range(3):
        x = int(input("Enter a number:"))
        list.append(x)
    matrix.append(list)

print("matrix:")
for row in matrix:
    print(row)

print("transpose Matrix:")
transposed_matrix = []
a = len(matrix)
b = len(matrix[0])
for j in range(b):
    rows = []
    for i in range(a):
        rows.append(matrix[i][j])
    transposed_matrix.append(rows)

for row in transposed_matrix:
    print(row)

