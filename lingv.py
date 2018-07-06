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
	rez = "\\n".join(rez).replace(" )", ")").replace("( ", "(").strip()
	return rez

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

