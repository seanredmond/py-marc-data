import marcdata
import pytest
from tests.marc_records import *


def test_leader():
    print(marcdata.marc_list(REC1))
    marc = marcdata.marc_list(REC1)["leader"]

    assert marc["record_status"] == "c"
    assert marc["type_of_record"] == "a"
    assert marc["bibliographic_level"] == "m"
    assert marc["type_of_control"] == " "
    assert marc["character_encoding_scheme"] == "a"
    assert marc["indicator_count"] == 2
    assert marc["subfield_code_count"] == 2
    assert marc["base_address_of_data"] == 205
    assert marc["encoding_level"] == "1"
    assert marc["descriptive_cataloging_form"] == " "
    assert marc["multipart_resource_record_level"] == " "
    assert marc["length_of_length_of_field_portion"] == 4
    assert marc["length_of_starting_character_position_portion"] == 5
    assert marc["length_of_implication_defined_portion"] == 0

    assert 1 == 2
