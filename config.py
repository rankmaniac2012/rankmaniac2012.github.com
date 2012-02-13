import os

numChildren = 6
maxDepth = 4
prob_parent = 0.5
prob_main = 0.9
prob_children = 1
prob_sibling = 0.6
sample_text_path = 'sample_book.txt'
images = ['images/' + img for img in os.listdir('images')]
template_path = 'template.html'
