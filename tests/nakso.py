from konlpy.tag import Twitter
from textrkr_test import TextRank

twt = Twitter()

a = '문재인 대선캠프에서 치어리더를 맡았던 박기량의 키는 매우 크다. 176cm 정도 하는 것 같다. 2018년 11월 11일엔 빼빼로를 받을 수 있을까? 불가능한 것으로 알려져 있다.'

b = twt.pos(a)
print(b)
cc = TextRank(a)
_nouns = twt.nouns(a)[:]

_indx = 0
ancbuf =''
prevanc = ''
complexity = 0
for c in b:
    sp = a.find(c[0], _indx)
    if c[1] in ['Suffix', 'Noun']:
        if sp == _indx and len(prevanc) > 0:
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
        prevanc = c[0]
        complexity = 0
    _indx = sp + len(c[0])

for ff in cc.sentences:
    print(ff.nouns)