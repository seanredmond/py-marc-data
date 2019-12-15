from itertools import groupby
from marcdata import *

LDR_FIELDS = ("record_status", "type_of_record", "bibliographic_level",
              "type_of_control", "character_encoding_scheme",
              "indicator_count", "subfield_code_count",
              "base_address_of_data", "encoding_level",
              "descriptive_cataloging_form",
              "multipart_resource_record_level",
              "length_of_length_of_field_portion",
              "length_of_starting_character_position_portion",
              "length_of_implication_defined_portion", "undefined")

MD_FIELDS = {
    "BK": ("illustrations", "target_audience", "form_of_item",
           "nature_of_contents", "government_publication",
           "conference_publication", "festschrift", "index", "undefined",
           "literary form", "biography"),
    "CF": ("undefined", "target_audience", "form_of_item", "undefined2",
           "type_of_computer_file", "undefined3", "government_publication",
           "undefined4"),
    "MP": ("relief", "projection", "undefined",
           "type_of_cartographic_material", "undefined2",
           "government_publication", "form_of_item", "undefined3", "index",
           "undefined4", "special_format_characteristics"),
    "MU": ("form_of_composition", "format_of_music", "music_parts",
           "target_audience", "form_of_item", "accompanyingd_ matter",
           "literary_text_for_sound_recordings", "undefined",
           "transposition_and_arrangement", "undefined2"),
    "CR": ("frequency", "regularity", "undefined",
           "type_of_continuing_resource", "form_of_original_item",
           "form_of_item", "nature_of_entire_work", "nature_of_contents",
           "government_publication", "conference_publication", "undefined2",
           "original_alphabet_or_script_of_title", "entry_convention"),
    "VM": ("running_time_for_motion_pictures_and_videorecordings",
           "undefined", "target_audience", "undefined2",
           "government_publication", "form_of_item", "undefined3",
           "type_of_visual_material", "technique"),
    "MX": ("Undefined", "form_of_item", "undefined2")
    }


def fixed_length_tuple(rec):
    """ Unpack the 008 field of a record (arg1) into a tuple.

    Unpacks the Fixed-Length Data Elements fields (008) of a record
    into a tuple containing the values of the separate fields.

    The sixth element in the tuple containing the fields appropriate
    to the material configuration of the record (positions 18-34) in
    the field value.

    """
    
    f = control_value([fld for fld in rec[1] if fld[0] == "008"][0])
    return (f[0:6], f[6], f[7:11], f[11:15], f[15:18],
            __material_desc(material_type(rec), f[18:35]), f[35:38],
            f[38], f[39])


def fixed_length_dict(rec):
    """ Unpack the 008 field of a record (arg1) into a dict. """
    
    f = control_value([fld for fld in rec[1] if fld[0] == "008"][0])
    return {**{"date_entered": f[0:6],
               "type_of_date": f[6],
               "date1": f[7:11],
               "date2": f[11:15],
               "place_of_publication": f[15:18]},
            **__material_desc_dict(material_type(rec), f[18:35]),
            **{"language": f[35:38],
               "modified_record": f[38],
               "cataloging_source": f[39]}}
    

def marc_dict(marc):
    """ Create nested dicts out of the nested tuples. """
    return {**{"leader" :__leader_dict(marc[0])},
            **dict([(m[0], __field_dict(m[1])) for m in
                    groupby(marc[1], key=lambda k: k[0])]),
            # Overwrite the default 008 dict with specialized version
            **{"008": (__control_dict(fixed_length_dict(marc)),)}}


def material_type(rec):
    """Determine material type for record (arg1). 
    
    Returns: 
    A string, one of BK (books), CF (computer files), MP
    (maps), MU (music), CR (continuing resource), VM (visual
    materials), MX (mixed materials)

    """

    l = rec[0]
    
    # Book: Leader/06 (Type of record) contains code a (Language
    # material) or t (Manuscript language material) and Leader/07
    # (Bibliographic level) contains code a (Monographic component
    # part), c (Collection), d (Subunit), or m (Monograph)
    if l[1] in ("a", "t") and l[2] in ("a", "c", "d", "m"):
        return "BK"

    # Computer File: Leader/06 (Type of record) contains code m
    if l[1] == "m":
        return "CF"

    # Map: Leader/06 (Type of record) contains code e (Cartographic
    # material) or f (Manuscript cartographic material)
    if l[1] in ("e", "f"):
        return "MP"

    # Music: Leader/06 (Type of record) contains code c (Notated
    # music), d (Manuscript notated music), i (Nonmusical sound
    # recording), or j (Musical sound recording)
    if l[1] in ("c", "d", "i", "j"):
        return "MU"

    # Continuing resources: Leader/06 (Type of record) contains code a
    # (Language material) and Leader/07 contains code b (Serial
    # component part), i (Integrating resource), or code s (Serial)
    if l[1] == "a" and l[2] in ("b", "i", "s"):
        return "CR"

    # Visual materials: Leader/06 (Type of record) contains code g
    # (Projected medium), code k (Two-dimensional nonprojectable
    # graphic, code o (Kit), or code r (Three-dimensional artifact or
    # naturally occurring object)
    if l[1] in ("g", "k", "o", "r"):
        return "VM"

    # Mixed materials: Leader/06 (Type of record) contains code p
    # (Mixed material)
    if l[1] == "p":
        return "MX"

    raise ValueError


def __leader_dict(l):
    """ A dict representation of the leader. """
    return dict(zip(LDR_FIELDS, l))



def __material_desc(m, d):
    """ Unpack positions 18-34 into material specific data structure. """ 
    return {"BK": __material_bk, "CF": __material_cf, "MP": __material_mp,
            "MU": __material_mu, "CR": __material_cr, "VM": __material_vm,
            "MX": __material_mx}[m](d)


def __material_bk(d):
    """ Fixed length data fields for books. """
    return (d[0:4], d[4], d[5], d[6:10], d[10], d[11], d[12], d[13],
            d[14], d[15], d[16])


def __material_cf(d):
    """ Fixed length data fields for computer files. """
    return (d[0:4], d[4], d[5], d[6:8], d[8], d[9], d[10], d[11:])


def __material_mp(d):
    """ Fixed length data fields for maps. """
    return (d[0:4], d[4:6], d[6], d[7], d[8:10], d[10], d[11], d[12],
            d[13], d[14], d[15:])


def __material_mu(d):
    """ Fixed length data fields for music. """
    return (d[0:2], d[2], d[3], d[4], d[5], d[6:12], d[12:14], d[14],
            d[15], d[16])


def __material_cr(d):
    """ Fixed length data fields for continuing resources. """
    return (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7:10], d[10],
            d[11], d[12:15], d[15], d[16])


def __material_vm(d):
    """ Fixed length data fields for visual materials. """
    return (d[0:3], d[3], d[4], d[5:10], d[10], d[11], d[12:15],
            d[15], d[16])


def __material_mx(d):
    """ Fixed length data fields for mixed materials. """
    return (d[0:5], d[6], d[7:])


def __control_dict(v):
    """ Wrap a control field value in a dict. """
    return {"type": "control", "value": v}
    

def __subfield_dict(marc_subfield):
    """ Create appropriate dict for values in a control or variable field. """
    if marc_subfield[3][0] is None:
        return __control_dict(marc_subfield[3][1])
    return {"type": "variable",
            "ind1": marc_subfield[1],
            "ind2": marc_subfield[2],
            "subfields": dict(marc_subfield[3:])}


def __field_dict(marc_field):
    """ Create a tuple of dicts for fields. """
    return tuple([__subfield_dict(f) for f in marc_field])


def __material_desc_dict(m, d):
    """ Unpack positions 18-34 into material specific dict. """ 
    return dict(zip(MD_FIELDS[m],
                    {"BK": __material_bk, "CF": __material_cf,
                     "MP": __material_mp, "MU": __material_mu,
                     "CR": __material_cr, "VM": __material_vm,
                     "MX": __material_mx}[m](d)))
