from text2dot import \
	wrap, \
	join, \
	pair, \
	triplet, \
	get_objects_and_rels, \
	collect_objects_and_rels, \
	fuzzy_triplets, \
	main

if __name__ == '__main__':
	print(main('testdata/in'))
	print(wrap())
	print(join())
	print(pair())
	print(triplet())
	print(get_objects_and_rels())
	print(collect_objects_and_rels(get_objects_and_rels()))
	print(fuzzy_triplets([('пирвет', 'тибе', 'привет'),
						  ('корвет', 'литит', 'кирвет'),
						  ('кювет', 'пропал', 'бювет'), ],
						 ['привет', 'корвет', 'кювет', 'бювет', ],
						 ['тебе', 'летит', 'пропан', ]))
