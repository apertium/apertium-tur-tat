#!/usr/bin/python3
# coding=utf-8
# -*- encoding: utf-8 -*-

import sys, codecs, copy, re;

sys.stdin  = codecs.getreader('utf-8')(sys.stdin);
sys.stdout = codecs.getwriter('utf-8')(sys.stdout);
sys.stderr = codecs.getwriter('utf-8')(sys.stderr);

# Example input:
#
# абориген [aborigen] yerli аборт [abort] kürtaj
# абрикос [abrikos] kayısı абруй [abruy] otorite,  yüz su­yu, abruy абруйлы [abruylı] otoriteli абруйсыз [abruysız] otoritesiz абсолют [absol'ut] 1. mutlak ha­kikat; Hakk; 2. mutlaka
# мазлум [mazlum] mazlum
# абайлау [abaylau] 1. dikkatli ol­mak; 2. sezmek, farkına varmak

skipped = 0;

def cleanTrad(s): #{
	out = s.strip();
	out = out.replace(u'­', ''); # this is '­' (U+00AD) not space
	netejedor = re.compile(u'^ *;? *[0-9]+\.');
	out = netejedor.sub(u'', out);
	netejedor = re.compile(u' [❖O<] *$');
	out = netejedor.sub(u'', out);
	netejedor = re.compile(u'^;');
	out = netejedor.sub(u'', out); 
	netejedor = re.compile(u'<'); # костыргыч [kostırgıç] kusturu< 
	out = netejedor.sub(u'', out);
	netejedor = re.compile(u'^\[.*\] '); # беришле [berişle] [<ber+işle] tek düze, monoton
	out = netejedor.sub(u'', out);
	
	return out;
#}

def cleanLine(s): #{

	out = s;
	out = out.replace('{kimse)', '(kimse)');
	# бәйрәм ит- [beyrem it-] bayram etmek <> бәйрәм котлы булсын [beyrem kotlı bulsın] bayramınız kutlu olsun
	out = out.replace('<>', '');  

	return out;
#}

lineno = 0; 					# Total number of lines in the source file
dixlines = 0; 					# Number out lines we're going to output in .dix format
cyr = re.compile(u'[Ё-ӿ]', re.UNICODE); 	# A regular expression to test if a character is Cyrillic or not.
logfile = open(sys.argv[1] + ".log", 'w+'); 	# The log file 

print '<dictionary>'; 
print '  <alphabet/>';
print '  <sdefs>';
print '    <sdef n="unk"   c="Unknown part of speech"/>';
print '  </sdefs>';
print '  <section id="unchecked" type="standard">';

for line in file(sys.argv[1]).readlines(): #{
	lineno += 1;
	line = cleanLine(line.decode('utf-8'));
	# Skip lines: 
	#   without '['
	#   with unbalanced '[ ]'
	#   with unbalanced '( )'
	#   with '{'
	#   where the first character is not cyrillic
	if line.count('[') < 1 or (line.count('[') != line.count(']')) or (line.count('(') != line.count(')')) or line.count('{') > 0 or cyr.match(line[0]) == None: #{
		skipped = skipped + 1;
		print >> sys.stderr, line;
		continue;
	#}

	i = 0; 			# The current (char) index of the line
	c = line[i]; 		# The current character we are processing
	isCyr = False; 		# Is the current character cyrillic ? 
	lindex = 0; 		# The current entry we are scanning for
	tindex = 1; 		# The current translation we are scanning
	state = 0; 		# Where we are in the entry (0 = scanning cyrillic, 1 = scanning [], 2 scanning latin)
	line_words = {}; 	# A list of the Tatar (cyrillic) headwords, may contain words with ',' = two headwords in one
	current_lemma = ''; 	# The current headword (cyrillic) that we are processing

	while c != '\n': #{
		# If the current character is cyrillic and we aren't in the final state
		if cyr.match(c) != None and state != 2: #{
			isCyr = True;
			current_lemma = current_lemma + c;
			state = 0;
		# If the current character is in [, -] and we are in the initial state
		elif (c == ',' or c == ' ' or c == '-') and state == 0: #{
			isCyr = True;
			current_lemma = current_lemma + c;
			state = 0;
		# If the current character is not cyrillic and it is '('
		elif cyr.match(c) == None and c == u'(': #{
			# Skip until ')', e.g. discard the contents of parentheses
			while c != u')': #{
				i = i + 1;
				c = line[i];
			#}
		# If the current character is cyrillic and we are in the final state
		elif cyr.match(c) != None and state == 2: #{
			current_lemma = '';
			current_lemma = current_lemma + c;
			lindex += 1;
			state = 0;
		# IF the current character is not cyrillic, we are in the initial state and the character is '['
		elif cyr.match(c) == None and state == 0 and c == u'[': #{
			# We have read a headword, this is the pronunciation, we want to discard it, and then
			#   move onto the translations
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
		# If the current character is not cyrillic and we are in the final state
		elif cyr.match(c) == None and state == 2: #{
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
	print >>logfile, '    <!--' , line.strip() , '-->';
	words = line_words.keys();
	words.sort();
	dixout = '';

	# For each of the headwords we have found (which may contain >1 word separated by ',')
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
