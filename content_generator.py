import os
import re
import random

from jinja2 import Template


def id_to_word(cnt, book, min_length=3, max_length=15):
    keywords = set()
    while len(keywords) < cnt:
        print len(keywords)
        line = book.readline()
        if line is None:
            break
        words = line.split(' ')
        for word in words:
            word = re.sub(r"[^a-zA-Z]", "", word).lower()
            if len(word) in xrange(min_length, max_length+1):
                keywords.add(word)
    keywords = list(keywords)
    random.shuffle(keywords)
    return ["index"] + keywords


def generate_url(node, keywords, create_folder_at=None):
    path = []
    curr = node
    while curr:
        path.append(keywords[curr.pageId])
        curr = curr.parent
    path.reverse()
    path[-1] += ".html"
    if create_folder_at:
        folder_path = os.path.join(create_folder_at, *path[0:-1])
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    return '/'.join(path)


def generate_content(images, links, keyword, boost_num, book, min_content_length, climb):
    # pick some content
    start_idx = random.randint(0, len(book) - min_content_length - 1)
    words = book[start_idx:start_idx+min_content_length+1].split()
    # boost keywords
    for _ in xrange(0, boost_num):
        words.insert(random.randint(0, len(words)-1), keyword)
    # insert pictures
    for img in images:
        if random.random() > 0.5:
            idx = random.randint(0, len(words) - 1)
            img_name = ' ' + img.split('/')[-1].replace('-',' ') 
            words.insert(idx, "<img src='%s%s' title='%s' alt='%s' />" % (climb, img, keyword + img_name, keyword + img_name))

    # insert links
    for link in links:
        idx = random.randint(0, len(words) - 1)
        words.insert(idx, "<a href='%s'>" % link)
        words.insert(idx+2, "</a>")
    for _ in xrange(1,5):
        idx = random.randint(0, len(words) - 1)
        words.insert(idx, "<br /><br />")
    return ' '.join(words)


def generate_site(tree, page_dict, sample_text_path, images,
                  template_path,
                  output_path='.',
                  keyword='rankmaniac 2012'):

    print 1
    with open(sample_text_path) as txt:
        words = id_to_word(len(tree), txt)

    print 2
    # create urls and folders
    urls = {}
    for node_id, parent_ids in tree.items():
        urls[node_id] = generate_url(page_dict[node_id], words,
                                     output_path)
    print 3

    # create content
    with open(template_path) as f:
        template = Template(f.read())
    print 4

    for node_id, parent_ids in tree.items():
        depth = page_dict[node_id].depth
        climb = "".join(["../"]*depth)
        links = [climb + urls[parent] for parent in parent_ids]
        main_url = climb + "index.html"
        if main_url in links:
            links.remove(main_url)
            links.append("/")
        text = re.sub(r"[^a-zA-Z0-9\.\s\']", "", open(sample_text_path).read())
        content = generate_content(images, links, keyword, 30, text, 10000, climb)
        f = file(urls[node_id], 'w')
        f.write(template.render(content=content, title=f.name.split('.')[-2], climb=climb, links=links))

import farmer

def run():
    import config
    print "creating tree"
    t, page_dict = farmer.create_tree()
    print "created tree"
    generate_site(t, page_dict, config.sample_text_path,
                  config.images,
                  config.template_path)

run()

