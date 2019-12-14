import marcdata
import marcdata.utils
import pytest
from tests.marc_records import *


def test_leader_dict():
    marc = marcdata.marc_list(REC1)
    ldr = marcdata.utils.leader_dict(marc[0])

    assert ldr["record_status"] == "c"
    assert ldr["type_of_record"] == "a"
    assert ldr["bibliographic_level"] == "m"
    assert ldr["type_of_control"] == " "
    assert ldr["character_encoding_scheme"] == "a"
    assert ldr["indicator_count"] == 2
    assert ldr["subfield_code_count"] == 2
    assert ldr["base_address_of_data"] == 205
    assert ldr["encoding_level"] == "1"
    assert ldr["descriptive_cataloging_form"] == " "
    assert ldr["multipart_resource_record_level"] == " "
    assert ldr["length_of_length_of_field_portion"] == 4
    assert ldr["length_of_starting_character_position_portion"] == 5
    assert ldr["length_of_implication_defined_portion"] == 0


def test_fixed_length_tuple():
    marc = marcdata.marc_list(REC1)
    assert marcdata.utils.fixed_length_tuple(marc) == \
        ("800108", "s", "1899", "    ", "ilu",
         ("    ", " ", " ", "    ", " ", "0", "0", "0", " ", "0", " "),
         "eng", " ", " ")

def test_map():
    marc = marcdata.marc_list(REC_MP)
    assert marcdata.utils.material_type(marc) == "MP"
    assert marcdata.utils.fixed_length_tuple(marc) == \
        ("940812", "m", "1898", "1906", "pau",
         ("    ", "  ", " ", "e", "  ", " ", " ", " ", " ", " ", "  "),
         "eng", " ", " ")


def test_computer_file():
    marc = marcdata.marc_list(REC_CF)
    assert marcdata.utils.material_type(marc) == "CF"
    assert marcdata.utils.fixed_length_tuple(marc) == \
        ("000110", "s", "2000", "    ", "ohu",
         ("    ", "f", " ", "  ", "m", " ", " ", "      "),
         "eng", " ", " ")


def test_music():
    marc = marcdata.marc_list(REC_MU)
    assert marcdata.utils.material_type(marc) == "MU"
    assert marcdata.utils.fixed_length_tuple(marc) == \
        ("000824", "s", "1998", "    ", "nyu",
         ("pp", "n", " ", " ", " ", "      ", "  ", " ", " ", " "),
         "   ", " ", "d")


def test_continuing_resource():
    marc = marcdata.marc_list(REC_CR)
    assert marcdata.utils.material_type(marc) == "CR"
    assert marcdata.utils.fixed_length_tuple(marc) == \
        ("940906", "u", "1994", "9999", "dcu",
         ("u", "u", " ", " ", " ", " ", " ",
          "   ", " ", "0", "   ", " ", "0"), "eng", " ", " ")


def test_visual_materials():
    marc = marcdata.marc_list(REC_VM)
    assert marcdata.utils.material_type(marc) == "VM"
    assert marcdata.utils.fixed_length_tuple(marc) == \
        ("991028", "s", "    ", "    ", "xxu",
         ("   ", " ", " ", "     ", " ", " ", "   ", "v", "|"),
         "eng", " ", " ")


def test_mixed_materials():
    marc = marcdata.marc_list(REC_MX)
    assert marcdata.utils.material_type(marc) == "MX"
    assert marcdata.utils.fixed_length_tuple(marc) == \
        ("000724", "i", "1980", "2005", "xxu",
         ("     ", " ", "          "), "eng", " ", " ")


def test_marc_dict():
    md = marcdata.utils.marc_dict(marcdata.marc_list(REC1))

    # Control field has one value
    assert len(md["003"]) == 1
    assert md["003"][0]["type"] == "control"
    assert md["003"][0]["value"] == "DLC"

    # The 650 field has two values
    assert len(md["650"]) == 2

    # The second 650 has two subfields
    assert md["650"][1]["type"] == "variable"
    assert md["650"][1]["ind1"] == " "
    assert md["650"][1]["ind2"] == "0"
    assert len(md["650"][1]["subfields"]) == 2
    assert md["650"][1]["subfields"]["a"] == "Homeopathy"
    assert md["650"][1]["subfields"]["x"] == "Materia medica and therapeutics."
