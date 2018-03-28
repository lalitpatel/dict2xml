#!/usr/bin/env python
# coding: utf-8

"""
Converts a Python dictionary valid XML string.
"""

from __future__ import unicode_literals

import datetime
import logging
from types import NoneType

from lxml import etree

__version__ = '0.1'
version = __version__

logger = logging.getLogger("v2")


def to_string(root, encoding='UTF-8', pretty_print=True, xml_declaration=False):
    return etree.tostring(root, method='xml', xml_declaration=xml_declaration, pretty_print=pretty_print,
                          encoding=encoding)


def create_xml(root_name, dictionary, encoding='UTF-8', pretty_print=True, xml_declaration=False, force_cdata=False):
    xml_root = etree.Element(root_name)
    convert(xml_root, dictionary, force_cdata=force_cdata)
    logger.debug(to_string(xml_root, encoding=encoding, pretty_print=pretty_print, xml_declaration=xml_declaration))
    return to_string(xml_root, encoding=encoding, pretty_print=pretty_print, xml_declaration=xml_declaration)


def convert(node, value, force_cdata=False):
    logger.debug("{} {}".format(node.tag, to_string(node)))
    logger.debug(value)
    if isinstance(value, dict):
        if '@attributes' in value:
            logger.debug("Found @attributes")
            attributes = value.pop('@attributes')
            for key in attributes.keys():
                attributes[key] = serialize_value(attributes[key])
            node.attrib.update(attributes)
        if '@value' in value:
            logger.debug("Found @value")
            if force_cdata:
                node.text = etree.CDATA(serialize_value(value.pop('@value')))
            else:
                node.text = serialize_value(value.pop('@value'))
        if '@cdata' in value:
            logger.debug("Found @cdata")
            node.text = etree.CDATA(serialize_value(value.pop('@cdata')))
        for key, val in value.items():
            logger.debug('Creating sub node ' + key)
            sub_node = etree.SubElement(node, key)
            convert(sub_node, val, force_cdata)
    elif isinstance(value, list):
        logger.debug("Value is an array of len {}".format(len(value)))
        tag = node.tag
        parent = node.getparent()
        # remove the current code as we will recreate a array of nodes below
        parent.remove(node)
        for val in value:
            sub_node = etree.SubElement(parent, tag)
            logger.debug("{} {}".format(sub_node.tag, to_string(sub_node)))
            logger.debug(val)
            convert(sub_node, val, force_cdata)
    else:
        if force_cdata:
            node.text = etree.CDATA(serialize_value(value))
        else:
            node.text = serialize_value(value)


def serialize_value(val):
    """Returns the santizized value for to be used in XML"""
    # if type(val).__name__ not in ('str', 'unicode','int', 'long','float','bool', 'NoneType'):
    #     ValueError('Do not know how to serialize the value of type {}'.format(type(val).__name__))
    if type(val) == bool:
        return 'true' if val else 'false'
    if type(val) == NoneType:
        return ''
    if type(val) == datetime.datetime:
        return val.isoformat()
    return str(val)


books_empty = {}
# <books/>

books_value = 1984  # or
books_value = {
    '@value': 1984
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
    '@value': 1984
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

books = {
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
                '@value': '$18.00'
            },
            'isbn': 341232132L
        }
    ]
}
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
    print create_xml('books_empty', books_empty)
    print create_xml('books_value', books_value)
    print create_xml('books_attributes', books_attributes)
    print create_xml('books_attributes_value', books_attributes_value)
    print create_xml('books_child', books_child)
    print create_xml('books_children', books_children)
    print create_xml('books_with_out_attributes', books_with_out_attributes)
    print create_xml('books_with_out_attributes', books_with_out_attributes)
    print create_xml('books', books, force_cdata=True)
