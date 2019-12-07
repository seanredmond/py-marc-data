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
