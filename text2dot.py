from nltk.tokenize import WordPunctTokenizer
wpt = WordPunctTokenizer()

PUNKT = list(".,:;-")

def join(tokens = ['очень', 'длинная', 'строка', ',', 'с', 'пробелами', ',', 'и', 'знаками', 'препинания']):
	rez = []
	for i in range(len(tokens)):
		token = tokens[i]
		if token in PUNKT:
			rez[-1] += token
		else:
			rez += [token]
	return rez

def wrap(_str = "очень длинная строка,с пробелами, и знаками препинания"):
	_len = 0
	rez = ""
	for token in join(wpt.tokenize(_str)):
		_len += len(token)
		rez += " " + token
		if _len > 20:
			rez += "\n"
			_len = 0
	return rez.strip()

if __name__ == '__main__':
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
