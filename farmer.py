import random
from config import *

class Page(object):
    def __init__(self, pageId):
        self.pageId = pageId
        self.children = []
        self.childrenId = []
        self.parent = 0
        self.parentId = 0
        self.depth = 0

    def registerPage(self, pageDict):
        pageDict[len(pageDict)] = self

    def produceChildren(self,numChildren, pageDict):
        pageIndex = len(pageDict)
        for i in range(numChildren):
            child = Page(pageIndex)
            child.depth = self.depth + 1
            child.parent = self
            child.parentId = self.pageId
            self.children.append(child)
            self.childrenId.append(child.pageId)
            child.registerPage(pageDict)
            pageIndex = pageIndex + 1

    def cascadeChildren(self, numChildren, depth, pageDict):
        self.produceChildren(numChildren, pageDict)
        if depth <= 1:
            pass
        else:
            for child in self.children:
                child.cascadeChildren(numChildren, depth-1, pageDict)
    
    def display(self):
        print "PageId: %d, Depth: %d, Children: %r" % (self.pageId, self.depth, self.childrenId)

    def displayAll(self):
        self.display()
        for child in self.children:
            child.displayAll()


def makeLinkToSibling(page, probability, links):
    childrenId = page.childrenId
    for i in range(len(childrenId)):
        for j in range(len(childrenId)):
            if i == j:
                pass
            elif randBoolean(probability):
                addLink(childrenId[i],childrenId[j], links)
            else:
                pass


def makeLinkToParent(page, probability, links):
    if randBoolean(probability):
        addLink(page.pageId, page.parentId, links)
    else:
        pass


def makeLinkToChildren(page, prob, links):
    for childId in page.childrenId:
        if randBoolean(prob):
            addLink(page.pageId, childId, links)
        else:
            pass


def makeLinkToMainPage(main, me, probability, links):
    mainId = main.pageId
    myId = me.pageId
    if randBoolean(probability):
        addLink(myId, mainId, links)
    else:
        pass


def addLink(linkFrom,linkTo, links):
    if linkFrom not in links:
        links[linkFrom] = set()
    links[linkFrom].add(linkTo)

def randBoolean(probability):
    num = random.random()
    if (num < probability):
        return True
    else:
        return False


def generate_links(mainPage, pageDict, prob_children, prob_sibling, prob_parent, prob_main, links):
    for i, page in pageDict.items():
        makeLinkToParent(page, prob_parent, links)
        makeLinkToMainPage(mainPage, page,prob_main, links)
        makeLinkToSibling(page, prob_sibling, links)
        makeLinkToChildren(page, prob_children, links)


def display_links(links):
    for i, v in links.items():
        print "%d -> %r" % (i, v)


def create_tree():
    #numChildren, maxDepth, prob_parent, prob_main, prob_children, prob_sibling):
    ##########################
    ## Initialization and parameter setup
    ##########################
    pageDict = dict()   ## Dictionary to store all pages
    links = dict()      ## Dictionary to store all links

    ## Set our parameters for tree structure
    #numChildren = 3     ## number of children for a page
    #maxDepth = 3       ## maximum depth

    ## Set our parameters for links
    #prob_parent = 1    ## probability of link to its parent
    #prob_main = 1      ## probability of link to the main page
    #prob_children = 1  ## probability of link to its children
    #prob_sibling = 1   ## probability of links among siblings

    #########################
    ##  generate pages and links
    #########################
    ## Generate the starting page and register it to our dictionary
    mainPage = Page(0)
    mainPage.registerPage(pageDict)

    ## Recursively generate childrens for maxDepth 
    ## Begin with mainPage
    mainPage.cascadeChildren(numChildren, maxDepth, pageDict)

    ## Generate links among the pages and store it at links
    for i in xrange(0, numChildren*maxDepth):
        links[i] = set()
    generate_links(mainPage, pageDict, prob_children, prob_sibling, prob_parent, prob_main, links)
    return links, pageDict
