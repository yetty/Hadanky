#/usr/bin/python
#-*- coding:utf-8 -*-

import sys, os, re, locale

locale.setlocale(locale.LC_ALL, "")

DATA_DIR = './data/'
categories = []

class Output:
    out = ''
    categories = []

    def getTemplate(self, name):
        return open(DATA_DIR+name+'.tex').read()

    def createLink(self, string):
        return string.replace(" ", "_")

    def __init__(self,categories):
        self.categories = categories

        out = open(DATA_DIR+'template.tex').read()
        out = out.replace("%CONTENT%", self.getContent())
        out = out.replace("%SOLUTIONS%", self.getSolutions())

        self.out = out

    def getContent(self):
        ret = ''
        template = self.getTemplate('category')

        for category in self.categories:
            cret = template.replace("%NAME%", category.name)
            cret = cret.replace("%ITEMS%", self.getItems(category))
            ret = ret+cret

        return ret

    def getItems(self, category):
        ret = ''
        template = self.getTemplate('item')

        for item in category.get():
            iret = template.replace("%NAME%", item.data["name"])
            iret = iret.replace("%LINK%", self.createLink(item.data["name"]))
            iret = iret.replace("%DIFF%", str(item.data["diff"]))
            iret = iret.replace("%TEXT%", item.data["text"])

            if item.data["bad"]:
                iret = iret.replace("%HBAD%", "")
                iret = iret.replace("%BAD%", item.data["bad"])

            if item.data["help"]:
                iret = iret.replace("%HHELP%", "")
                iret = iret.replace("%HELP%", item.data["help"])

            ret = ret+iret

        return ret

    def getSolutions(self):
        return self.getTemplate('solutions').replace("%CONTENT%", self.getSCategories())

    def getSCategories(self):
        ret = ''
        template = self.getTemplate('scategory')

        for category in self.categories:
            cret = template.replace("%NAME%", category.name)
            cret = cret.replace("%ITEMS%", self.getSItems(category))
            ret = ret+cret

        return ret

    def getSItems(self, category):
        ret = ''
        template = self.getTemplate('sitem')

        for item in category.get():
            iret = template.replace("%NAME%", item.data["name"])
            iret = iret.replace("%LINK%", self.createLink(item.data["name"]))
            iret = iret.replace("%SOLUTION%", item.data["solution"])
            ret = ret+iret

        return ret


    def get(self):
        return self.out

class Category:
    name = ''
    puzzles = []

    def __init__(self, name):
        self.name = name
        self.puzzles = []

    def __repr__(self):
        return "<"+self.name+": \n\t"+str(self.puzzles)+">\n"

    def append(self, puzzle):
        self.puzzles.append(puzzle)

    def get(self):
        self.puzzles.sort(key=lambda puzzle: puzzle.data['name'], cmp=locale.strcoll)
        return self.puzzles



class Puzzle:
    data = {}

    def __init__(self, fileContent):
        self.data = {'name' : '', 'diff' : 0, 'text' : '', 'bad' : '', 'help' : '', 'solution' : '', 'story' : ''}
        self.parseFile(fileContent)

    def __repr__(self):
        return self.data['name']

    def parseFile(self, fileContent):
        lines = []
        for line in fileContent:
            line = line.strip()
            if line:
                lines.append(line)

        self.data['name'] = lines[0]
        lines.pop(0)

        self.data['diff'] = int(re.search("([0-9]+).+[%]", lines[0]).group(1))
        lines.pop(0)

        for line in lines:
            rkey = re.search("\%([A-Z]+)\%", line)

            if rkey:
                key = rkey.group(1).lower()
            else:
                self.data[key] = self.data[key]+line+"\n\n"


if __name__=="__main__":
    for dir in os.listdir(DATA_DIR):
        if os.path.isdir(DATA_DIR+dir):
            category = Category(dir)

            for file in os.listdir(DATA_DIR+dir):
                filePath = DATA_DIR+dir+'/'+file

                try:
                    if os.path.isfile(filePath) and file.split('.')[1]=="tex":
                        content = open(filePath)
                        category.append(Puzzle(content))
                except:
                    pass

            categories.append(category)

    categories.sort(key=lambda category: category.name, cmp=locale.strcoll)

    for category in categories:
        print category.get()

    save = open('./out/hadanky.tex', 'w')
    save.write(Output(categories).get())
