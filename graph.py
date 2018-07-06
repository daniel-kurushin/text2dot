import sys

from lingv import *


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



def generate_graph(node_shapes, triplets_dict):
	out = "digraph g {\n\trankdir = LR\n"
	for triplet in triplets_dict:
		s, r, o = triplet
		w = triplets_dict[triplet]
		out += '\t"%s" -> "%s" [label="%s", penwidth="%s"]\n' % (wrap(s), wrap(o), wrap(r), w)
		
	out += "}\n"
	return out


def detect_triplets(lines):
	triplets = []
	for line in lines:
		triplets += get_objects_and_rels(line)
	
	return triplets
