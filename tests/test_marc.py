import marcdata
import marcdata.utils
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


def test_find():
    marc = marcdata.marc_list(REC1)
    assert marcdata.find(marc, "010") == \
        (("010", " ", " ", ("a", "   00000002 ")),)


def test_find_multiple():
    marc = marcdata.marc_list(REC1)
    assert len(marcdata.find(marc, "650")) == 2


def test_find_none():
    marc = marcdata.marc_list(REC1)
    assert marcdata.find(marc, "XYZ") == ()


def test_find_with_indicators():
    marc = marcdata.marc_list(REC1)
    title = (("245", "1", "0",
              ("a", "Botanical materia medica and pharmacology;"),
              ("b", "drugs considered from a botanical, pharmaceutical, physiological, therapeutical and toxicological standpoint."),
              ("c", "By S. H. Aurand.")),)
    assert marcdata.find(marc, "245", ind1="x") == ()
    assert marcdata.find(marc, "245", ind1="1") == title

    assert marcdata.find(marc, "245", ind2="x") == ()
    assert marcdata.find(marc, "245", ind2="0") == title

    assert marcdata.find(marc, "245", ind1="1", ind2="x") == ()
    assert marcdata.find(marc, "245", ind1="1", ind2="0") == title


def test_subfields():
    marc = marcdata.marc_list(REC1)
    title = marcdata.find(marc, "245")[0]
    assert len(marcdata.find_subf(title)) == 3
    assert marcdata.find_subf(title, "a") == \
        (("a", "Botanical materia medica and pharmacology;"),)
    assert marcdata.find_subf(title, "c") == \
        (("c", "By S. H. Aurand."),)
    assert marcdata.find_subf(title, "z") == ()


#def test_2():
#    marc = marcdata.marc_list(REC_02)
#    assert marcdata.material_type(marc) == "MP"


def test_bad_record():
    # tests/bad_record.utf8 is a malformed record
    with pytest.raises(marcdata.marcdata.InvalidMarcError):
        marc = marcdata.from_file("tests/bad_record.utf8")
        next(marc)
