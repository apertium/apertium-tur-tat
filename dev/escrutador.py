#!/usr/bin/python3
# coding=utf-8
# -*- encoding: utf-8 -*-

import sys, codecs, copy, re;

sys.stdin  = codecs.getreader('utf-8')(sys.stdin);
sys.stdout = codecs.getwriter('utf-8')(sys.stdout);
sys.stderr = codecs.getwriter('utf-8')(sys.stderr);

skipped = 0;

def cleanTrad(s): #{
	out = s.strip();
	out = out.replace(u'­', ''); # this is '­' (U+00AD) not space
	netejedor = re.compile(u'^ *[0-9]+\.');
	out = netejedor.sub(u'', out);
	netejedor = re.compile(u' [❖O] *$');
	out = netejedor.sub(u'', out);
	netejedor = re.compile(u'^;');
	out = netejedor.sub(u'', out);
	
	return out;
	
#}
def cleanLine(s): #{

	out = s;
	out = out.replace('{kimse)', '(kimse)');

	return out;
#}
lineno = 0;
dixlines = 0;
cyr = re.compile(u'[Ё-ӿ]', re.UNICODE);
logfile = open(sys.argv[1] + ".log", 'w+');
print '<dictionary>';
print '  <section id="unchecked" type="standard">';
for line in file(sys.argv[1]).readlines(): #{
	lineno += 1;
	# мазлум [mazlum] mazlum
	line = cleanLine(line.decode('utf-8'));
	# Skip lines without []
	if line.count('[') < 1 or (line.count('[') != line.count(']')) or (line.count('(') != line.count(')')) or line.count('{') > 0: #{
		skipped = skipped + 1;
		print >> sys.stderr, line;
		continue;
	#}

	if cyr.match(line[0]) == None: #{
		skipped = skipped + 1;
		print >> sys.stderr, line;
		continue;
	#}
	
	# абориген [aborigen] yerli аборт [abort] kürtaj
	# абрикос [abrikos] kayısı абруй [abruy] otorite,  yüz su­yu, abruy абруйлы [abruylı] otoriteli абруйсыз [abruysız] otoritesiz абсолют [absol'ut] 1. mutlak ha­kikat; Hakk; 2. mutlaka
	
	i = 0;
	c = line[i];
	isCyr = False;
	lindex = 0; # The current entry we are scanning for
	tindex = 1; # The current translation we are scanning
	state = 0; # Where we are in the entry (0 = scanning cyrillic, 1 = scanning [], 2 scanning latin)
	line_words = {};
	current_lemma = '';

	while c != '\n': #{
		if cyr.match(c) != None and state != 2: #{
			isCyr = True;
			current_lemma = current_lemma + c;
			state = 0;
		elif (c == ',' or c == ' ' or c == '-') and state == 0: #{
			isCyr = True;
			current_lemma = current_lemma + c;
			state = 0;
		elif cyr.match(c) == None and c == u'(': #{
			while c != u')': #{
				i = i + 1;
				c = line[i];
			#}
		elif cyr.match(c) != None and state == 2: #{
			current_lemma = '';
			current_lemma = current_lemma + c;
			lindex += 1;
			state = 0;
		elif cyr.match(c) == None and state == 0 and c == u'[': #{
			state = 1;
			line_words[current_lemma] = {};	
			while c != u']': #{
				i = i + 1;
				if i < len(line): #{
					c = line[i];
				else: #{
					break;
				#}
			#}
			state = 2;
		elif cyr.match(c) == None and state == 2: #{
			# абайлау [abaylau] 1. dikkatli ol­mak; 2. sezmek, farkına varmak
			if c == ';': #{
				tindex = tindex + 1;	
			#}
			if tindex not in line_words[current_lemma]: #{
				line_words[current_lemma][tindex] = '';
			#}
			line_words[current_lemma][tindex] += c;
		elif (c == ' ' or c == '-') and state == 2: #{
			isCyr = True;
			line_words[current_lemma][tindex] += c;
		#}
		#print isCyr , c;
		i = i + 1;
		if i < len(line): #{
			c = line[i];
		else: #{
			break;
		#}
		isCyr = False;
	#}
	#print line_words;
	print '    <!--' , line.strip() , '-->';
	words = line_words.keys();
	words.sort();
	dixout = '';
	for word in words: #{
		for s in line_words[word]: #{
			swords = [word];
			if word.count(',') > 0: #{
				swords = word.split(',');
			#}	
			for sw in swords: #{
				tr = cleanTrad(line_words[word][s].strip());
				if tr == '': #{
					continue;
				#}
				ii = 0;
				xword = sw.strip().replace(' ', '<b/>'); # xmlword
				if tr.count(',') > 0: #{
					for w in tr.split(','): #{
						if w == '': #{
							continue;
						#}
						ii += 1;
						print >>logfile, '+' , lineno, lindex , sw, s , ii , w.strip(); 
						xw = w.strip().replace(' ', '<b/>');
						dixline = '    <e><p><l>' + xw + '<s n="unk"/></l><r>' + xword + '<s n="unk"/></r></p></e>\n';
						dixout = dixout + dixline;
					#}
	
				else: #{
					print >>logfile, '+' , lineno, lindex , sw, s , ii , tr; 
					xtr = tr.strip().replace(' ', '<b/>');
					dixout = dixout + '    <e><p><l>' + xtr + '<s n="unk"/></l><r>' + xword + '<s n="unk"/></r></p></e>\n';
				#}
			#}
		#}
	#}
	print dixout;
	dixlines = dixlines + dixout.count('<e>');
#}
logfile.close();
print '  </section>';
print '  <!--';
print '       Пропущеные строки:', skipped , ''.join(str((100.0-(float(skipped)/float(lineno)*100.0)))[0:6]);
print '       Строки:', dixlines;
print '  -->';
print '</dictionary>'
