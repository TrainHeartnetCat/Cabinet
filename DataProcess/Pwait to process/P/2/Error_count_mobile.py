import os


input_error = r'./error.txt'

species_list = ['C', 'C-H', 'C-O', 'C-OH', 'CH', 'CH-H', 'CH-O', 'CH-OH', 'CH2', 'CH2-H', 'CH2-O', 'CH2-OH', 'CH2O', 'CH2O-H', 'CH2OH', 'CH3', 'CH3-H', 'CH3-O', 'CH3-OH', 'CH3O', 'CH3O-H', 'CH3OH', 'CHO', 'CHO-H', 'CHO-O', 'CHOH', 'CO', 'CO-H', 'CO-O', 'CO-OH', 'COH', 'COO-H', 'COOH', 'H', 'H-CH2O', 'H-CH2OH', 'H-CHO', 'H-CHOH', 'H-CO', 'H-COH', 'H-COO', 'HCOO', 'O', 'O-H', 'OH']

with open(input_error, encoding = 'utf-8') as f:
	content = f.readlines()

work = []
for i in content:
	i = eval(i)
	work.append(i)

for i in work:
	print(i[0])