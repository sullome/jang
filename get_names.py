#!/usr/bin/python
from html.parser import HTMLParser
from urllib.request import urlopen

class MolomoParser(HTMLParser):
    CONTENT = False
    SPAN = False
    RESULT = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and attrs == [('class', 'content')]:
            self.CONTENT = True
        elif tag == 'span':
            self.SPAN = True

    def handle_endtag(self, tag):
        if tag == 'div' and self.CONTENT:
            self.CONTENT = False
        elif tag == 'span':
            self.SPAN = False

    def handle_data(self, data):
        if self.CONTENT and self.SPAN:
            self.RESULT += '\n{},'.format(data)

def from_molomo(nat):
    page = urlopen('http://www.molomo.ru/inquiry/{}_male.html'.format(nat))
    page = page.read().decode('utf-8')
    parser = MolomoParser()
    parser.feed(page)
    print(parser.RESULT)

if __name__ == '__main__':
    from_molomo('spanish')
