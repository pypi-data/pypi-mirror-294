import re

from .defaults import DEFAULT_NOISE_XPATH, ARTICLE_XPATH
from .exceptions import NoContentException
from .extractor import AuthorExtractor, TimeExtractor, TitleExtractor, MetaExtractor, ContentExtractor, ListExtractor
from .utils import pre_parse, remove_noise_node, config, html2element, normalize_text, fix_html

__version__ = "0.0.1"
__author__ = "Gie"


class GeneralNewsExtractor:
    def extract(self,
                html,
                title_xpath='',
                author_xpath='',
                publish_time_xpath='',
                host='',
                body_xpath='',
                content_xpath_list=ARTICLE_XPATH,
                normalize=False,
                noise_node_list=DEFAULT_NOISE_XPATH,
                with_body_html=False,
                use_visiable_info=False):

        # 对 HTML 进行预处理可能会破坏 HTML 原有的结构，导致根据原始 HTML 编写的 XPath 不可用
        # 因此，如果指定了 title_xpath/author_xpath/publish_time_xpath，那么需要先提取再进行
        # 预处理
        html = fix_html(html)
        if normalize:
            normal_html = normalize_text(html)
        else:
            normal_html = html
        element = html2element(normal_html)
        meta_content = MetaExtractor().extract(element)
        title = TitleExtractor().extract(element, title_xpath=title_xpath)
        publish_time = TimeExtractor().extractor(element, publish_time_xpath=publish_time_xpath)
        author = AuthorExtractor().extractor(element, author_xpath=author_xpath)
        element = pre_parse(element)
        remove_noise_node(element, noise_node_list)
        content = ContentExtractor().extract(element,
                                             host=host,
                                             with_body_html=with_body_html,
                                             body_xpath=body_xpath,
                                             use_visiable_info=use_visiable_info)
        if not content:
            raise NoContentException('无法提取正文！')
        # while len(content) > 3:
        #     if content[0][1]['score'] > content[1][1]['score'] * 1.3:
        #         content.pop(0)
        #         continue
        #     break


        result = {'title': title,
                  'author': author,
                  'publish_time': publish_time,
                  'content': content[0][1]['text'],
                  'images': content[0][1]['images'],
                  'images_desc': content[0][1]['images_desc'],
                  'meta': meta_content
                  }
        if content_xpath_list:
            for content_xpath in content_xpath_list:
                content_desc = element.xpath(content_xpath)
                if content_desc:
                    content_desc = content_desc[0].xpath('string(.)')
                    content_desc = re.sub('[\\r\\t ]', '', content_desc)
                    if len(content_desc) > len(result['content']):
                        result['content'] = content_desc
                        break

        if with_body_html or config.get('with_body_html', False):
            result['body_html'] = content[0][1]['body_html']
        return result


class ListPageExtractor:
    def extract(self, html, feature):
        normalize_html = normalize_text(html)
        element = html2element(normalize_html)
        extractor = ListExtractor()
        return extractor.extract(element, feature)

