LDR_LEN = 19


class InvalidMarcError(Exception):
    pass


def marc_tuple(d):
    ldr = leader(d[0:LDR_LEN].decode())
    vf = variable_fields(
        directory(d[LDR_LEN:ldr[7]-5].decode()),
        d[ldr[7]-5:])
    return (ldr, vf)


def leader(d):
    return (d[0], d[1], d[2], d[3], d[4], int(d[5]), int(d[6]),
            int(d[7:12]), d[12], d[13], d[14], int(d[15]), int(d[16]),
            int(d[17]), int(d[18]))


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
    except IndexError:
        raise InvalidMarcError("Could not parse {} field at position {}".format(d[0][0], d[0][2]))


def subfields(t, d):
    # Remove extra trailing subfield delimiters, if neccessary, before
    # splitting into subfields
    subf = d.rstrip(b"\x1f").split(b"\x1f")

    # No subfields means it's a control field, with no indicators and
    # no subfield code
    if len(subf) == 1:
        return (t, None, None, (None, d.decode()))

    return (t, chr(subf[0][0]), chr(subf[0][1])) + \
        tuple([(chr(s[0]), s[1:].decode()) for s in subf[1:]])


def control_value(f):
    return f[3][1]


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
    with open(f, "rb") as file:
        offset = 0
        while 1:
            try:
                reclen = int(file.read(5))
                rec = file.read(reclen - 5)
                yield marc_tuple(rec)
                offset += reclen
            except InvalidMarcError as e:
                raise InvalidMarcError(
                    e.args[0] + " at file offset {}".format(offset))
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
