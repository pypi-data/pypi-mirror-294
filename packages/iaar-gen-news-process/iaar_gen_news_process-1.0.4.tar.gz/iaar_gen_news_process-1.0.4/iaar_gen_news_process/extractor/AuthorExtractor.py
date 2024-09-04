import re

from iaar_gen_news_process.defaults import AUTHOR_PATTERN, AUTHOR_PATTERN_END, AUTHOR_DISTURB
from lxml.html import HtmlElement

from iaar_gen_news_process.utils import config


class AuthorExtractor:
    def __init__(self):
        self.author_pattern = AUTHOR_PATTERN
        self.defaults_end = AUTHOR_PATTERN_END
        self.author_disturb = AUTHOR_DISTURB

    def extractor(self, element: HtmlElement, author_xpath=''):
        author_xpath = author_xpath or config.get('author', {}).get('xpath')
        if author_xpath:
            author = ''.join(element.xpath(author_xpath))
            return author
        text = ''.join(element.xpath('.//text()'))
        for pattern in self.author_pattern:
            author_obj = re.search(pattern + self.defaults_end, text)
            if author_obj:
                author = author_obj.group(1)
                if author not in self.author_disturb:
                    return author
        return ''
