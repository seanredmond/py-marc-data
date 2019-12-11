import marcdata
import pytest
from tests.marc_records import *


def test_leader():
    print(marcdata.marc_list(REC1))

    marc = marcdata.marc_list(REC1)
    ldr = marc[0]
    assert ldr == ("c", "a", "m", " ", "a", 2, 2, 205, "1", " ", " ",
                   4, 5, 0, 0)


def test_leader_dict():
    marc = marcdata.marc_list(REC1)
    ldr = marcdata.leader_dict(marc[0])

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


def test_control_value():
    marc = marcdata.marc_list(REC1)
    f008 = marc[1][3]
    assert marcdata.control_value(f008) == \
        "800108s1899    ilu           000 0 eng  "


def test_fixed_length_tuple():
    marc = marcdata.marc_list(REC1)
    print(marcdata.fixed_length_tuple(marc))
    assert marcdata.fixed_length_tuple(marc) == \
        ("800108", "s", "1899", "    ", "ilu",
         ("    ", " ", " ", "    ", " ", "0", "0", "0", " ", "0", " "),
         "eng", " ", " ")


def test_mixed_materials():
    marc = marcdata.marc_list(REC_MX)
    assert marcdata.material_type(marc) == "MX"
    assert marcdata.fixed_length_tuple(marc) == \
        ("000724", "i", "1980", "2005", "xxu",
         ("     ", " ", "          "), "eng", " ", " ")


