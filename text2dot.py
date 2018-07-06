import sys
from graph import detect_triplets, collect_objects_and_rels, generate_graph

# https://yandex.ru/images/search?text=%D0%BF%D0%BE%D0%B4%D0%BD%D1%8F%D1%82%D1%8C%20%D1%80%D1%83%D0%BA%D0%B8&isize=small&type=lineart&itype=png

def detect_node_shapes(a):
	pass

def main(file):
	lines = [ x.strip(" \n").strip(';') for x in open(file).readlines() ]
	triplets = detect_triplets(lines)
	triplets_dict = collect_objects_and_rels(triplets)
	node_shapes = detect_node_shapes(lines)
	
	return generate_graph(node_shapes, triplets_dict)
	
if __name__ == '__main__':
	try:
		print(main(sys.argv[1]))
	except FileNotFoundError:
		print('e')
	pass
