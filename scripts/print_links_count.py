import ast
p='run_pipeline.py'
src=open(p,'r',encoding='utf-8').read()
tree=ast.parse(src)
links=[]
for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if getattr(t,'id',None)=='article_links' and isinstance(node.value,(ast.List,ast.Tuple)):
                for elt in node.value.elts:
                    if isinstance(elt,ast.Constant) and isinstance(elt.value,str):
                        links.append(elt.value)
print('found', len(links))
for i,l in enumerate(links[:50],1):
    print(i, l)
