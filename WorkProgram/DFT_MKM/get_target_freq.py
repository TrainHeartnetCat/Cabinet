import Freq_many

# 获得所需物种key，然后去freq的txt中提取
with open('species_and_energy.txt', encoding = 'utf8') as f:
	species_and_energy = f.readlines()

species = []
for i in species_and_energy:
	i = i.replace('\n','')
	i = i.split('\t')
	if i[0] == '':
		continue
	else:
		species.append(i[0])
print(species)
species.remove('slab_111')

print('')
print('{')
for i in species:
	print('"' + str(i) + '"' + ':' + str(Freq_many.frequency_dict[i]) + ',')
print('}')
