#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import logging
from collections import OrderedDict
from types import NoneType

import datetime
from lxml import etree

__version__ = '0.1'
version = __version__

logger = logging.getLogger("dict2xml")


class Dict2XML(object):
    """
    Converts a Python dictionary to XML using the lxml.etree library
    For more info on see: http://lxml.de/tutorial.html
    """
    _xml = None

    def __init__(self, root_node_name, dictionary, force_cdata=False):
        """
        Converts a Python dictionary to XML using the lxml.etree library
        :param root_node_name: name of the root node
        :param dictionary: instance of a dict object that needs to be converted
        :param force_cdata: if true, all the text nodes will be wrapped in <!CDATA[[ ]]>
        """
        self._xml = etree.Element(root_node_name)
        self._convert(self._xml, dictionary, force_cdata=force_cdata)

    def to_xml_string(self, encoding='UTF-8', pretty_print=True, xml_declaration=True):
        """
        Convert the etree object into string
        :param encoding: specify the encoding for the XML String. Default 'UTF-8'
        :param pretty_print: pretty print the XML wth indentation. Default True
        :param xml_declaration: Print the XML Declaration tag in the output. Default True
        :return: XML string
        """
        return etree.tostring(self._xml, xml_declaration=xml_declaration, pretty_print=pretty_print,
                              encoding=encoding, method='xml')

    def get_etree_object(self):
        return self._xml

    def _convert(self, node, value, force_cdata=False):
        """
        Recursively traverse the dictionary to convert it to a XML
        :param node: the parent XML node
        :param value: value of the Node
        :param force_cdata: if true, all the text nodes will be wrapped in <!CDATA[[ ]]>
        :return: None
        """
        logger.debug("Parent Tag {} {}".format(node.tag, self._to_string(node)))
        logger.debug("Value {}".format(value))
        if isinstance(value, dict):
            if '@attributes' in value:
                logger.debug("Found @attributes")
                attributes = value.pop('@attributes')
                for key in attributes.keys():
                    attributes[key] = self._serialize_value(attributes[key])
                node.attrib.update(attributes)
            if '@text' in value:
                logger.debug("Found @text")
                if force_cdata:
                    node.text = etree.CDATA(self._serialize_value(value.pop('@text')))
                else:
                    node.text = self._serialize_value(value.pop('@text'))
            if '@cdata' in value:
                logger.debug("Found @cdata")
                node.text = etree.CDATA(self._serialize_value(value.pop('@cdata')))
            for key, val in value.items():
                logger.debug('Creating sub node ' + key)
                sub_node = etree.SubElement(node, key)
                self._convert(sub_node, val, force_cdata)
        elif isinstance(value, list):
            # array of nodes
            tag = node.tag
            parent = node.getparent()  # remove the current code as we will recreate a array of nodes below
            parent.remove(node)
            for val in value:
                sub_node = etree.SubElement(parent, tag)
                self._convert(sub_node, val, force_cdata)
        else:
            # text node
            if force_cdata:
                node.text = etree.CDATA(self._serialize_value(value))
            else:
                node.text = self._serialize_value(value)

    @staticmethod
    def _to_string(node):
        """
        Helper method to pretty print xml nodes
        :param node: etree XML Node to be printed.
        :return: string
        """
        return etree.tostring(node, xml_declaration=False, pretty_print=True, encoding='UTF-8', method='xml')

    @staticmethod
    def _serialize_value(value):
        """Returns the serlialized value for to be used in XML"""
        # if type(val).__name__ not in ('str', 'unicode','int', 'long','float','bool', 'NoneType'):
        #     ValueError('Do not know how to serialize the value of type {}'.format(type(val).__name__))
        if type(value) == bool:
            return 'true' if value else 'false'
        if type(value) == NoneType:
            return ''
        if type(value) == datetime.datetime:
            return value.isoformat()
        return str(value)


books_empty = {}
# <books/>

books_value = 1984  # or
books_value = {
    '@text': 1984
}
"""
<books>1984</books>
"""

# Attributes: Attributes can be added to any node by having a @attributes key in the array
books_attributes = {
    '@attributes': {
        'type': 'fiction',
        'year': 2011,
        'bestsellers': True
    }
}
"""
<books type="fiction" year="2011" bestsellers="true"/>
"""

books_attributes_value = {
    '@attributes': {
        'type': 'fiction'
    },
    '@text': 1984
}
"""
<books type="fiction">1984</books>
"""

books_child = {
    '@attributes': {
        'type': 'fiction'
    },
    'book': 1984
}
"""
<books type="fiction">
<book>1984</book>
</books>
"""

books_children = {
    '@attributes': {
        'type': 'fiction'
    },
    'book': ['1984', 'Foundation', 'Stranger in a Strange Land']
}
"""
<books type="fiction">
<book>1984</book>
<book>Foundation</book>
<book>Stranger in a Strange Land</book>
</books>
"""

books_with_out_attributes = {
    'book': [
        {
            'title': '1984',
            'isbn': 973523442132L,
        },
        {
            'title': {'@cdata': 'Foundation'},
            'price': '$15.61',
            'isbn': 57352342132L,
        },
        {
            'title': {'@cdata': 'Stranger in a Strange Land'},
            'price': '$18.00',
            'isbn': 341232132L
        }
    ]
}
"""
<books>
  <book>
    <isbn>973523442132</isbn>
    <title>1984</title>
  </book>
  <book>
    <price>$15.61</price>
    <isbn>57352342132</isbn>
    <title><![CDATA[Foundation]]></title>
  </book>
  <book>
    <price>$18.00</price>
    <isbn>341232132</isbn>
    <title><![CDATA[Stranger in a Strange Land]]></title>
  </book>
</books>
"""

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

"""<books type="fiction">
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
    print Dict2XML('books_empty', books_empty).to_xml_string()
    print Dict2XML('books_value', books_value).to_xml_string()
    print Dict2XML('books_attributes', books_attributes).to_xml_string()
    print Dict2XML('books_attributes_value', books_attributes_value).to_xml_string()
    print Dict2XML('books_child', books_child).to_xml_string()
    print Dict2XML('books_children', books_children).to_xml_string()
    print Dict2XML('books_with_out_attributes', books_with_out_attributes).to_xml_string()
    print Dict2XML('books_with_out_attributes', books_with_out_attributes).to_xml_string()
    print Dict2XML('books', books, force_cdata=True).to_xml_string()
