# Marcdata

[![PyPi Version](https://badge.fury.io/py/marcdata.svg)][pypi]
[![Build Status](http://img.shields.io/travis/seanredmond/py-marc-data.svg)][travis]

[travis]: http://travis-ci.org/seanredmond/py-marc-data
[pypi]: https://pypi.org/project/marcdata/

Load binary MARC files into a simple nested tuples (or nested dicts) data structure.

## Installation

    pip install marcdata
    
## Usage

Personally, I often have to parse MARC files just to get one piece of data. Marcdata parses binary MARC files into nested tuples and provides some methods to extract data.

Import the package:

    import marcdata
    
Read a file:

    marcdata.from_file("data.marc)
    
`from_file()` returns an iterator, so you probably want to do something like:

    for record in marcdata.from_file("data.marc"):
        # Do something with record...
        
The tuple for one record has two elements: the leader, and the fields. The leader consists of the [MARC leader values](https://www.loc.gov/marc/bibliographic/bdleader.html) unpacked into a tuple (excluding the first field, Record length). The fields are a tuple of tuples, one tuple for each field contained in the record.

Field tuples have the structure:

    (tag, ind1, ind2, subfield1 [,subfield2...])
    
Subfield tuples have the structure:

    (code, value)
    
A typical field tuple looks like:

    ('245', '1', '0', 
    ('a', 'Botanical materia medica and pharmacology;'), 
    ('b', 'drugs considered from a botanical, pharmaceutical, physiological, therapeutical and toxicological standpoint.'), 
    ('c', 'By S. H. Aurand.'))
    
That is, the tag is "245" (Title Statement), first indicator is "1" (Added entry), second indicator "0" (No nonfiling characters). There are three subfields, "a", "b", and "c" (Title, Remainder of title, and Statement of responsibility)

For [control fields](https://www.loc.gov/marc/bibliographic/bd00x.html), each indicator is `None` and the subfield tuple will have only one element with `None` as the code:

    ('003', None, None, (None, 'DLC'))
    
You can find a particular field by tag (and optionally also indicators):
	
    >>> marcdata.find(record, "245")
    >>> marcdata.find(record, "245", ind1="0")
    >>> marcdata.find(record, "245", ind2="1")
    >>> marcdata.find(record, "245", ind1="0", ind2="0")

`find()` will return a tuple of matching fields. 

To find subfields matching a field from a field:

    >>> title = marcdata.find(record, "245")[0]
    >>> marc_data.find_subf(title, "a")
    (('a', 'Botanical materia medica and pharmacology;'),)
    
Leave out the subfield code to get all subfields:

    marc_data.find_subf(title)
    
To retrieve the value of a control field:

    >>> identifier = marcdata.find(record, "003")[0]
    >>> marcdata.control_value(indentifier)
    'DLC'
    
`repr()` returns a text representation of the record in the traditional format, with empty indicators represented by "#" and subfields delimited with "\$":

    >>> print(marcdata.repr(marcdata.marc_tuple(REC1)))
    001         00000002
    003      DLC
    005      20040505165105.0
    008      800108s1899    ilu           000 0 eng
    010    ##$a   00000002
    035    ##$a(OCoLC)5853149
    040    ##$aDLC$cDSI$dDLC
    050    00$aRX671$b.A92
    100    1#$aAurand, Samuel Herbert,$d1854-
    245    10$aBotanical materia medica and pharmacology;$bdrugs considered from a botanical, pharmaceutical, physiological, therapeutical and toxicological standpoint.$cBy S. H. Aurand.
    260    ##$aChicago,$bP. H. Mallen Company,$c1899.
    300    ##$a406 p.$c24 cm.
    500    ##$aHomeopathic formulae.
    650    #0$aBotany, Medical.
    650    #0$aHomeopathy$xMateria medica and therapeutics.
    
### Utils

The `marcdata.utils` package provides some additional convenience methods.

    import marcdata.utils
    
Get the material type:

    >>> marcdata.utils.material_type(record)
    'BK'

This will return one of: "BK" (books), "CF" (computer files), "MP"
    (maps), "MU" (music), "CR" (continuing resource), "VM" (visual
    materials), "MX" (mixed materials)

You can get the [Fixed-Length Data Elements (008)](https://www.loc.gov/marc/bibliographic/bd008.html) unpacked as a tuple

    >>> marcdata.utils.fixed_length_tuple(record)
    ('800108', 's', '1899', '    ', 'ilu', ('    ', ' ', ' ', '    ', ' ', '0', '0', '0', ' ', '0', ' '), 'eng', ' ', ' ')
    
The sixth element of this tuple is a tuple specific to the material type of the record (positions 18-34 in the value of the 008 field)

The Fixed-Length Data Elements can also be retrieved as a dict:

    >>> marcdata.utils.fixed_length_dict(record)
    {'date_entered': '800108', 'type_of_date': 's', 'date1': '1899', 
    'date2': '    ', 'place_of_publication': 'ilu', 
    'illustrations': '    ', 'target_audience': ' ', 
    'form_of_item': ' ', 'nature_of_contents': '    ', 
    'government_publication': ' ', 'conference_publication': '0', 
    'festschrift': '0', 'index': '0', 'undefined': ' ', 
    'literary form': '0', 'biography': ' ', 'language': 'eng', 
    'modified_record': ' ', 'cataloging_source': ' '}

Note that rhe material-type-specific fields are simply part of the dict, so the dicts for different material types will have different keys.

Finally, you can retrieve the record as a dict:

    >>> marcdata.utils.marc_dict(record)
    
In the dict version, the keys are "leader" and the field tags present in the record

    >>> marcdata.utils.marc_dict(record).keys()
    dict_keys(['leader', '001', '003', '005', '008', '010', '035', '040', '050', '100', '245', '260', '300', '500', '650'])

The leader and Fixed-Length Data Elements are themselves unpacked into dicts.

For fields, the values from each pair is a tuple of dicts, with the multiple values of repeated fields grouped. In control fields the tuple will have a single member with the structure:

    '003': ({'type': 'control', 'value': 'DLC'},)
    
For variable fields the structure will be:
    
    '650': (
      {'type': 'variable', 'ind1': ' ', 'ind2': '0', 'subfields': {'a': 'Botany, Medical.'}}, 
      {'type': 'variable', 'ind1': ' ', 'ind2': '0', 'subfields': {'a': 'Homeopathy', 'x': 'Materia medica and therapeutics.'}}
    )  
    
## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/seanredmond/py-marc-data.

## License

The package is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).

