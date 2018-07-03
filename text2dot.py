from nltk.tokenize import WordPunctTokenizer
wpt = WordPunctTokenizer()

PUNKT = list(".,:;-")

def join(tokens=['очень', 'длинная', 'строка', ',', 'с', 'пробелами', ',', 'и', 'знаками', 'препинания']):
	rez = []
	for i in range(len(tokens)):
		token = tokens[i]
		if token in PUNKT:
			rez[-1] += token
		else:
			rez += [token]
	return rez

def wrap(_str="очень длинная строка,с пробелами, и знаками препинания"):
	_len = 0
	rez = []
	is_first_word = True
	for token in join(wpt.tokenize(_str)):
		_len += len(token)
		
		if is_first_word:
			rez = [token]
			is_first_word = False
		elif _len < 20:
			rez[-1] += " %s" % token
		else:
			rez += [token]
			_len = 0
	return "\n".join(rez)

def pair(parts=['a', 'b']):
	return (parts[0], '', parts[1])

def triplet(parts=['a', 'r', 'b']):
	return (parts[0], parts[1], parts[2])

def long(parts=['a', 'r1', 'b', 'r2', 'c', 'r3', 'd']):
	n = 0
	rez = []
	while 1:
		triplet = tuple(parts[n:n + 3])
		n += 2
		if not triplet:
			break
		else:
			rez += [triplet]
	return rez

def get_objects_and_rels(line='Поворот в другую сторону;Не повернулся;Подать звуковой сигнал, ожидание;Объект ушел;Робот стоит на месте, определяет положение в пространстве(начальное состояние);Робот находится в выделенно области'):
	parts = line.split(';')
	if len(parts) == 2:
		return [pair(parts)]
	elif len(parts) == 3:
		return [triplet(parts)]
	else:
		return long(parts)

def fuzzy_unique(_list):
	def fuzzy_compare(X, y):
		def compare(S1, S2):
			ngrams = [S1[i:i + 3] for i in range(len(S1))]
			count = 0
			for ngram in ngrams:
				count += S2.count(ngram)

			return count / max(len(S1), len(S2)) > 0.65

		for x in X:
			if compare(x, y):
				return True
		return False

	rez = []
	for y in _list:
		if not fuzzy_compare(rez, y):
			rez += [y]
	return rez

def fuzzy_triplets(triples, objects, rels):
	return triples

def collect_objects_and_rels(triplets=[('a', 'r1', 'b'), ('b', 'r2', 'c'), ('c', 'r3', 'd')]):
	objects = []
	rels = []
	objects = fuzzy_unique([ x[0] for x in triplets ] + [ x[2] for x in triplets ])
	rels = fuzzy_unique([ x[1] for x in triplets ])
	triplets = fuzzy_triplets(triplets, objects, rels) 
	
	return objects, rels


def generate():
	import sys
	lines = [ _.strip(" \n").strip(';') for _ in open(sys.argv[1]).readlines() ]
	print("digraph g {\n\trankdir = LR\n")
	for line in lines:
		try:
			_from, _to, _rel = [ wrap(_.strip()) for _ in line.split(";") ]
			print('\t"%s" -> "%s" [label="%s"]' % (_from, _to, _rel))
		except ValueError:
			try:
				_from, _to = [ wrap(_.strip()) for _ in line.split(";") ]
				print('\t"%s" -> "%s"' % (_from, _to))
			except ValueError:
				pass
	print("}")
	
if __name__ == '__main__':
	pass
