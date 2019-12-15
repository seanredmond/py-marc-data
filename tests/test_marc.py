import marcdata
import marcdata.utils
import pytest
from tests.marc_records import *


def test_leader():
    print(marcdata.marc_tuple(REC1))

    marc = marcdata.marc_tuple(REC1)
    ldr = marc[0]
    assert ldr == ("c", "a", "m", " ", "a", 2, 2, 205, "1", " ", " ",
                   4, 5, 0, 0)


def test_control_value():
    marc = marcdata.marc_tuple(REC1)
    f008 = marc[1][3]
    assert marcdata.control_value(f008) == \
        "800108s1899    ilu           000 0 eng  "


def test_find():
    marc = marcdata.marc_tuple(REC1)
    assert marcdata.find(marc, "010") == \
        (("010", " ", " ", ("a", "   00000002 ")),)


def test_find_multiple():
    marc = marcdata.marc_tuple(REC1)
    assert len(marcdata.find(marc, "650")) == 2


def test_find_none():
    marc = marcdata.marc_tuple(REC1)
    assert marcdata.find(marc, "XYZ") == ()


def test_find_with_indicators():
    marc = marcdata.marc_tuple(REC1)
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
    marc = marcdata.marc_tuple(REC1)
    title = marcdata.find(marc, "245")[0]
    assert len(marcdata.find_subf(title)) == 3
    assert marcdata.find_subf(title, "a") == \
        (("a", "Botanical materia medica and pharmacology;"),)
    assert marcdata.find_subf(title, "c") == \
        (("c", "By S. H. Aurand."),)
    assert marcdata.find_subf(title, "z") == ()


def test_bad_record():
    # tests/bad_record.utf8 is a malformed record
    with pytest.raises(marcdata.marcdata.InvalidMarcError):
        marc = marcdata.from_file("tests/bad_record.utf8")
        next(marc)
