#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import logging
from collections import OrderedDict
from pprint import pprint

from lxml import etree

__version__ = '0.1'
version = __version__

logger = logging.getLogger("xml2dict")


class XML2Dict(object):
    """
    Converts a Python dictionary to XML using the lxml.etree library
    For more info on see: http://lxml.de/tutorial.html
    """
    _xml = None

    def __init__(self, xml, ns_clean=True):
        parser = etree.XMLParser(ns_clean=ns_clean, remove_blank_text=True)
        self._xml = etree.XML(xml, parser)

    def to_dict(self, ordered_dict=False):
        return self._convert(self._xml, ordered_dict)

    def get_etree_object(self):
        return self._xml

    def _convert(self, node, ordered_dict=False):
        logger.debug("Parent Tag {} {}".format(node.tag, self._to_string(node)))
        xml_dict = OrderedDict() if ordered_dict else {}

        # add attributes and text nodes
        if len(node.attrib):
            xml_dict['@attributes'] = node.attrib
        if node.text:
            xml_dict['@text'] = node.text

        # add children if any
        if len(node):
            for child in node:
                if child.tag not in xml_dict:
                    # assume there will be more than one of a given child node
                    xml_dict[child.tag] = []
                xml_dict[child.tag].append(self._convert(child, ordered_dict))

            # flatten the arrays
            # print(xml_dict.items())
            for key, value in xml_dict.items():
                if type(value) == list and len(value) == 1:
                    # print("{}: {}".format(key, value))
                    xml_dict[key] = value[0]

        # flatten the dict if it just has the @text key
        if len(xml_dict) == 1 and '@text' in xml_dict:
            xml_dict = xml_dict['@text']

        return xml_dict

    @staticmethod
    def _to_string(node):
        """
        Helper method to pretty print xml nodes
        :param node: etree XML Node to be printed.
        :return: string
        """
        return etree.tostring(node, xml_declaration=False, pretty_print=True, encoding='UTF-8', method='xml')



books = OrderedDict({
    '@attributes': {
        'type': 'fiction'
    },
    'book': [
        {
            '@attributes': {
                'author': 'George Orwell',
                'available': None
            },
            'title': '1984',
            'isbn': 973523442132L,
        },
        {
            '@attributes': {
                'author': 'Isaac Asimov',
                'available': False
            },
            'title': {'@cdata': 'Foundation'},
            'price': '$15.61',
            'isbn': 57352342132L,
        },
        {
            '@attributes': {
                'author': 'Robert A Heinlein',
                'available': True
            },
            'title': {'@cdata': 'Stranger in a Strange Land'},
            'price': {
                '@attributes': {
                    'discount': '10%'
                },
                '@text': '$18.00'
            },
            'isbn': 341232132L
        }
    ]
})

books = """<books type="fiction">
  <book available="" author="George Orwell">
    <isbn>973523442132</isbn>
    <title>1984</title>
  </book>
  <book available="false" author="Isaac Asimov">
    <price>$15.61</price>
    <isbn>57352342132</isbn>
    <title><![CDATA[Foundation]]></title>
  </book>
  <book available="true" author="Robert A Heinlein">
    <price discount="10%">$18.00</price>
    <isbn>341232132</isbn>
    <title><![CDATA[Stranger in a Strange Land]]></title>
  </book>
</books>
"""

if __name__ == "__main__":
    pprint(XML2Dict(books).to_dict(ordered_dict=True))
