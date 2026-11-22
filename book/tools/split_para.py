"""Split one over-long paragraph at the sentence boundary nearest its middle.
Usage: python3 tools/split_para.py FILE LINE [LINE ...]  (1-based; process from the bottom up).
Reread the result: the split point is mechanical."""
import re, sys
path=sys.argv[1]; lines=open(path,encoding='utf-8').read().split('\n')
for n in sorted(map(int,sys.argv[2:]),reverse=True):
    t=lines[n-1]
    cuts=[m.end() for m in re.finditer(r'[.!?)]["”)]?\s+(?=[A-Z*`(])', t)]
    if not cuts: continue
    mid=len(t)/2; c=min(cuts,key=lambda x:abs(x-mid))
    lines[n-1]=t[:c].rstrip()+'\n\n'+t[c:].lstrip()
open(path,'w',encoding='utf-8').write('\n'.join(lines))
