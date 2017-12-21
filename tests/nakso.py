from konlpy.tag import Twitter

twt = Twitter()

a = '구름과자 위를 걷는 거야, 불확실한 삶을 살아간 다는 건. 자유한국당 홍준표 대표 섬유산업 시장에 국회의자 때리기'

b = twt.pos(a)
print(b)
_nouns = twt.nouns(a)[:]

_indx = 0
ancbuf =''
prevanc = ''
complexity = 0
for c in b:
    sp = a.find(c[0], _indx)
    if c[1] in ['Suffix', 'Noun']:
        if sp == _indx and sp != 0:
            complexity += 1
            print(prevanc + ' str ' + c[0] + ' pos ' + str(sp) + ' is next of noun/suff, complexity ' + str(complexity))
            prevanc += c[0]
        else:
            if complexity > 0:
                print(prevanc)
            prevanc = c[0]
            complexity = 0

    else:
        if complexity > 0:
            print(prevanc)
        prevanc = ''
        complexity = 0
    _indx = sp + len(c[0])
