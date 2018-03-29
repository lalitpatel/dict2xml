## dict-2-xml
Converts a Python dictionary to a valid XML string. Supports attributes and CDATA.

### Usage
```python
from dict2xml import Dict2XML

book = {
    '@attributes': {
        'type': 'fiction'
    },
    '@text': 1984
}
print(Dict2XML('book', book).to_xml_string(xml_declaration=False))
# <book type="fiction">1984</book>
```

### Examples

```python
books_empty = {}
# <books/>
```
#### Attributes can be added to any node by having a `@attributes` key in the dict
```python
books_attributes = {
    '@attributes': {
        'type': 'fiction',
        'year': 2011,
        'bestsellers': True
    }
}
```
```xml
<books type="fiction" year="2011" bestsellers="true"/>
```
#### XML with text nodes
Text modes can be added to any node by directly assigning the value or by having a `@text` (or `@cdata`) key in the dict
```python
books_value = 1984  # or
books_value = {
    '@text': 1984
}
```
```xml
<books>1984</books>
```
#### XML with attributes and text nodes
```python
books_attributes = {
    '@attributes': {
        'type': 'fiction'
    },
    '@text': 1984
}
```
```xml
<books type="fiction">1984</books>
```
#### XML with child node
```python
books_child = {
    '@attributes': {
        'type': 'fiction'
    },
    'book': 1984
}
```
```xml
<books type="fiction">
<book>1984</book>
</books>
```
#### XML with mutliple children of same kind
```python
books_children = {
    '@attributes': {
        'type': 'fiction'
    },
    'book': ['1984', 'Foundation', 'Stranger in a Strange Land']
}
```
```xml
<books type="fiction">
<book>1984</book>
<book>Foundation</book>
<book>Stranger in a Strange Land</book>
</books>
```
#### Simple dict with no attributes
A text node can be wrapped in CDATA by having a `@cdata` key in the dict
```python
books_with_out_attributes = {
    'book': [
        {
            'title': '1984',
            'isbn': 973534,
        },
        {
            'title': {'@cdata': 'Foundation'},
            'price': '$15.61',
            'isbn': 573234,
        },
        {
            'title': {'@cdata': 'Stranger in a Strange Land'},
            'price': '$18.00',
            'isbn': 341232
        }
    ]
}
```
```xml
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
```
#### Complex example with many different data types. 
```python
from collections import OrderedDict
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
            'isbn': 972132L,
        },
        {
            '@attributes': {
                'author': 'Isaac Asimov',
                'available': False
            },
            'title': {'@cdata': 'Foundation'},
            'price': '$15.61',
            'isbn': 5735232L,
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
            'isbn': 3412332L
        }
    ]
})
```
```xml
<books type="fiction">
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
```
