LDR_LEN = 19

def marc_list(d):
    ldr = leader(d[0:LDR_LEN].decode())
    # drc = directory(d[LDR_LEN:ldr["base_address_of_data"]-5].decode())
    vf = variable_fields(
        directory(d[LDR_LEN:ldr["base_address_of_data"]-5].decode()),
        d[ldr["base_address_of_data"]-5:])
    return {"leader": ldr, "variable_fields": vf}


def leader(d):
    return {
        "record_status": d[0],
        "type_of_record": d[1],
        "bibliographic_level": d[2],
        "type_of_control": d[3],
        "character_encoding_scheme": d[4],
        "indicator_count": int(d[5]),
        "subfield_code_count": int(d[6]),
        "base_address_of_data": int(d[7:12]),
        "encoding_level": d[12],
        "descriptive_cataloging_form": d[13],
        "multipart_resource_record_level": d[14],
        "length_of_length_of_field_portion": int(d[15]),
        "length_of_starting_character_position_portion": int(d[16]),
        "length_of_implication_defined_portion": int(d[17])
    }


def directory(d):
    if len(d) < 12:
        return ()

    tag = d[0:3]
    length = int(d[3:7])
    start = int(d[7:12])
    return ((tag, length, start),) + directory(d[12:])

def variable_fields(d, f):
    if len(d) < 1:
        return ()

    try:
        tag = d[0][0]
        data = f[d[0][2]:d[0][2] + d[0][1]-1]
        return (subfields(tag, data),) + variable_fields(d[1:], f)
    except IndexError as e:
        print("{0} {1} {0}".format("-"*10, "variable_fields"))
        print(d)
        print(f)
        raise e
    


def subfields(t, d):
    subf = d.split(b"\x1f")
    if len(subf) == 1:
        return (t, None, None, (None, d.decode()))
    try:
        return (t, chr(subf[0][0]), chr(subf[0][1])) + \
            tuple([(chr(s[0]), s[1:].decode()) for s in subf[1:]])
    except IndexError as e:
        # This handles an error seen in a LOC file where a control
        # field has a stray subfield delimiter (\x1f) at the end,
        # i.e. "  00038361\x1f\x1e"
        return subfields(t, d.strip(b"\x1f"))



def from_file(f):
    with open (f, "rb") as file:
        t = True
        while t:
            try:
                rec = file.read(int(file.read(5)) - 5)
                yield marc_list(rec)
            except ValueError:
                break
        
