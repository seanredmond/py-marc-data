LDR_LEN = 19
LDR_FIELDS = ("record_status", "type_of_record", "bibliographic_level",
              "type_of_control", "character_encoding_scheme",
              "indicator_count", "subfield_code_count",
              "base_address_of_data", "encoding_level",
              "descriptive_cataloging_form",
              "multipart_resource_record_level",
              "length_of_length_of_field_portion",
              "length_of_starting_character_position_portion",
              "length_of_implication_defined_portion", "undefined")

def marc_list(d):
    ldr = leader(d[0:LDR_LEN].decode())
    # drc = directory(d[LDR_LEN:ldr["base_address_of_data"]-5].decode())
    vf = variable_fields(
        directory(d[LDR_LEN:ldr[7]-5].decode()),
        d[ldr[7]-5:])
    return (ldr, vf)


def leader(d):
    return (d[0], d[1], d[2], d[3], d[4], int(d[5]), int(d[6]),
            int(d[7:12]), d[12], d[13], d[14], int(d[15]), int(d[16]),
            int(d[17]), int(d[18]))


def leader_dict(l):
    return dict(zip(LDR_FIELDS, l))


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
        return ((subfields(tag, data),) + variable_fields(d[1:], f))
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

def control_value(f):
    return f[3][1]


def fixed_length_tuple(rec):
    f = control_value([fld for fld in rec[1] if fld[0] == "008"][0])
    return (f[0:6], f[6], f[7:11], f[11:15], f[15:18],
            material_desc(material_type(rec), f[18:35]), f[35:38],
            f[38], f[39])


def material_desc(m, d):
    return {"BK": material_bk, "CF": material_cf, "MP": material_mp,
            "MU": material_mu, "CR": material_cr, "VM": material_vm, "MX": material_mx}[m](d)


def material_bk(d):
    return (d[0:4], d[4], d[5], d[6:10], d[10], d[11], d[12], d[13],
            d[14], d[15], d[16])


def material_cf(d):
    return (d[0:4], d[4], d[5], d[6:8], d[8], d[9], d[10], d[11:])


def material_mp(d):
    return (d[0:4], d[4:6], d[6], d[7], d[8:10], d[10], d[11], d[12],
            d[13], d[14], d[15:])


def material_mu(d):
    return (d[0:2], d[2], d[3], d[4], d[5], d[6:12], d[12:14], d[14],
            d[15], d[16])


def material_cr(d):
    return (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7:10], d[10],
            d[11], d[12:15], d[15], d[16])


def material_vm(d):
    return (d[0:3], d[3], d[4], d[5:10], d[10], d[11], d[12:15],
            d[15], d[16])


def material_mx(d):
    return (d[0:5], d[6], d[7:])


def material_type(rec):
    """ Determine material type from leader values."""

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


def find(d, tag, **kwargs):
    return find_ind(
        find_ind(
            tuple([f for f in d[1] if f[0] == tag]),
            kwargs.get("ind1"), 1),
        kwargs.get("ind2"), 2)


def find_subf(d, code=None):
    if code is None:
        return d[3:]

    return tuple([s for s in d[3:] if s[0] == code])


def find_ind(d, ind, pos):
    if ind is None:
        return d

    return tuple([f for f in d if f[pos] == ind])


def from_file(f):
    with open (f, "rb") as file:
        t = True
        while t:
            try:
                rec = file.read(int(file.read(5)) - 5)
                yield marc_list(rec)
            except ValueError:
                break


def repr_indicators(f):
    return "".join(["#" if i == " " else i for i in f[1:3]])


def repr_field(f):
    if f[1] is None and f[2] is None:
        return "{}      {}".format(f[0], f[3][1])

    return "{}    {}{}".format(
        f[0], repr_indicators(f),
        "".join(["${}{}".format(s[0], s[1]) for s in f[3:]]))


def repr(d):
    return "\n".join([repr_field(f) for f in d[1]])


def test_file(f, t):
    for r in from_file(f):
        f008 = [v for v in r[1] if v[0] == "008"][0]
        if material_type(r) == t:
            print(r)
            break
