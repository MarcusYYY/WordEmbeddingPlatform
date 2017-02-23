import re,numpy,nltk,os


path = 'r52-train-stemmed.txt'
with open(path,'r') as file:
	read_data = file.read()
file.closed

tab_text = read_data.split('\n')
labels = {}
for tuple_ in tab_text:
	tab = tuple_.split('	')[0]
	text = tuple_.split('	')[1]
	if tab not in labels:
		texts = []
		texts.append(text)
		labels[tab] = texts
	else:
		labels[tab].append(text)

count = 0
for label,txt in labels.iteritems():
	if not os.path.exists(label):
		os.makedirs(label)
	for item in txt:
		file_name = str(count)
		fpath = os.path.join(label,file_name)
		count = count + 1
		f = open(fpath,'w')
		f.write(item)
	
