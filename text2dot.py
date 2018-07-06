from nltk.tokenize import WordPunctTokenizer
import sys

wpt = WordPunctTokenizer()

PUNKT = list(".,:;-")

# https://yandex.ru/images/search?text=%D0%BF%D0%BE%D0%B4%D0%BD%D1%8F%D1%82%D1%8C%20%D1%80%D1%83%D0%BA%D0%B8&isize=small&type=lineart&itype=png

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
	rez = "\\n".join(rez).replace(" )", ")").replace("( ", "(")
	return rez

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
			if len(triplet) == 3:
				rez += [triplet]
			elif len(triplet) == 2:
				rez += [(triplet[0], '', triplet[1])]
			else:
				pass
	return rez

def get_objects_and_rels(line='Поворот в другую сторону;Не повернулся;Подать звуковой сигнал, ожидание;Объект ушел;Робот стоит на месте, определяет положение в пространстве(начальное состояние);Робот находится в выделенно области'):
	parts = line.split(';')
	if len(parts) == 2:
		return [pair(parts)]
	elif len(parts) == 3:
		return [triplet(parts)]
	else:
		return long(parts)

def compare(S1, S2):
	ngrams = [S1[i:i + 3] for i in range(len(S1))]
	count = 0
	for ngram in ngrams:
		count += S2.count(ngram)

	try:
		rez = count / max(len(S1), len(S2)) > 0.65
	except ZeroDivisionError:
		rez = 0
	return rez

def fuzzy_unique(_list):
	def fuzzy_compare(X, y):
		for x in X:
			if compare(x, y):
				return True
		return False

	rez = []
	for y in _list:
		if not fuzzy_compare(rez, y):
			rez += [y]
	return rez

def fuzzy_triplets(triplets, objects, rels):
	def fuzzy_find(_item, _list):
		for i in _list:
			if compare(i, _item):
				return i
		return _item
	
	rez = []
	for s, r, o  in triplets:
		s1 = fuzzy_find(s, objects) 
		o1 = fuzzy_find(o, objects)
		r1 = fuzzy_find(r, rels)
		rez += [(s1, r1, o1)]
	return rez

def cross_check(triplets_dict):
	dO, dR = {}, {}
	O = [ x[0] for x in triplets_dict ] + [ x[2] for x in triplets_dict ]
	R = [ x[1] for x in triplets_dict ]
	for o in O:
		for r in R:
			if compare(o, r):
				try:
					dR[o] += 1 
				except KeyError:
					dR[o] = 1 
	for r in R:
		for r in R:
			if compare(o, r):
				try:
					dO[r] += 1 
				except KeyError:
					dO[r] = 1
					
	to_del = []
	for i in dO.keys():
		for s, r, o in triplets_dict:
			if r == i:
				print("Wrong triplet found:", s, r, o, file=sys.stderr)
				to_del += [(s, r, o)] 
	for i in dR.keys():
		for s, r, o in triplets_dict:
			if s == i or o == i:
				print("Wrong triplet found:", s, r, o, file=sys.stderr) 
				to_del += [(s, r, o)] 
	
	for i in to_del:
		triplets_dict.pop(i)
		
	return triplets_dict 
	
def make_dict(triplets=[('a', 'r1', 'b'), ('a', 'r1', 'b'), ('b', 'r2', 'c'), ('b', 'r2', 'c'), ('c', 'r3', 'd')]):
	rez = {}
	for triplet in triplets:
		try:
			rez[triplet] += 1
		except KeyError:
			rez[triplet] = 1
	return rez

def collect_objects_and_rels(triplets=[('a', 'r1', 'b'), ('b', 'r2', 'c'), ('c', 'r3', 'd')]):
	objects = []
	rels = []
	objects = fuzzy_unique([ x[0] for x in triplets ] + [ x[2] for x in triplets ])
	rels = fuzzy_unique([ x[1] for x in triplets ])
	triplets = fuzzy_triplets(triplets, objects, rels) 
	triplets_dict = make_dict(triplets)
	triplets_dict = cross_check(triplets_dict) 
	
	return triplets_dict


def main(file):
	lines = [ x.strip(" \n").strip(';') for x in open(file).readlines() ]
	triplets = []
	for line in lines:
		triplets += get_objects_and_rels(line)
	triplets_dict = collect_objects_and_rels(triplets)
	print("digraph g {\n\trankdir = LR\n")
	for triplet in triplets_dict:
		s, r, o = triplet
		w = triplets_dict[triplet]
		print('\t"%s" -> "%s" [label="%s", penwidth="%s"]' % (wrap(s), wrap(o), wrap(r), w))
	print("}")
	
if __name__ == '__main__':
	try:
		main(sys.argv[1])
	except FileNotFoundError:
		print('e')
	pass
