LDR_LEN = 19


class InvalidMarcError(Exception):
    pass


def from_file(f):
    """ Parse MARC file into tuples.

    Parameters:
    arg1 Name of the MARC file to be parsed.

    Returns:
    An iteratorof tuples, each representing a single MARC record.
    """
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


def marc_tuple(d):
    """Parse a MARC record into a tuple.

    Parameters:

    arg1 a binary string containing a MARC record, minus
    the first five bytes containing the record length

    Returns:

    A tuple representing the MARC record.

    The returned value will be a one tuple containing the leader data
    and another containing the fields. The leader contains fifteen
    values from the standar MARC leader, minus the first field, record
    length. The values tuple contains one tuple for each field.

    Each field tuple is a tuple containing the tag, the two indicators
    and a tuple of sub-fields. Each sub-field tuple consists of a
    subfield code and the code value.

    For control fields, both of the indicators will be None and there
    will be on subfield, with None as the subfield code.

    """

    ldr = __leader(d[0:LDR_LEN].decode())
    vf = __variable_fields(
        __directory(d[LDR_LEN:ldr[7]-5].decode()), d[ldr[7]-5:])
    return (ldr, vf)


def control_value(f):
    """ Return the value of a control field (arg1). """
    return f[3][1]


def find(d, tag, **kwargs):
    """ Find all the fields matching the tag and optional indicators

    Parameters:

    arg1: data tuple (as returned by marc_tuple())
    arg2: the tag to be matched. Should always be a three-character string

    Keyword arguments:

    ind1 -- Value of first indicator
    ind2 -- Value of second indicator
    """
    return __find_ind(
        __find_ind(
            tuple([f for f in d[1] if f[0] == tag]),
            kwargs.get("ind1"), 1),
        kwargs.get("ind2"), 2)


def find_subf(d, code=None):
    """ Return subfields in arg1 or subfields in arg1 matching code arg2.

    Parameters:

    arg1: The field tuple to be searched
    arg2: The subfield field code to be searched for. If ommitted or None,
    all subfields will be returned

    Returns:
    A tuple of subfield tuples (empty if no matches)
    """
    if code is None:
        return d[3:]

    return tuple([s for s in d[3:] if s[0] == code])


def repr(d):
    """ A string representation of record arg1. """
    return "\n".join([__repr_field(f) for f in d[1]])


def __leader(d):
    """ Unpack the leader into its separate values. """
    return (d[0], d[1], d[2], d[3], d[4], int(d[5]), int(d[6]),
            int(d[7:12]), d[12], d[13], d[14], int(d[15]), int(d[16]),
            int(d[17]), int(d[18]))


def __directory(d):
    """ Recursively unpack the directory data into tuples. """
    if len(d) < 12:
        return ()

    return ((d[0:3], int(d[3:7]), int(d[7:12])),) + __directory(d[12:])


def __variable_fields(d, f):
    """ Unpack variable field data into tuples. """
    if len(d) < 1:
        return ()

    try:
        tag = d[0][0]
        data = f[d[0][2]:d[0][2] + d[0][1]-1]
        return ((__subfields(tag, data),) + __variable_fields(d[1:], f))
    except IndexError:
        raise InvalidMarcError(
            "Could not parse {} field at position {}".format(d[0][0], d[0][2]))


def __subfields(t, d):
    """ Unpack subfield data into tuples. """

    # Remove extra trailing subfield delimiters, if neccessary, before
    # splitting into subfields
    subf = d.rstrip(b"\x1f").split(b"\x1f")

    # No subfields means it's a control field, with no indicators and
    # no subfield code
    if len(subf) == 1:
        return (t, None, None, (None, d.decode()))

    return (t, chr(subf[0][0]), chr(subf[0][1])) + \
        tuple([(chr(s[0]), s[1:].decode()) for s in subf[1:]])


def __find_ind(d, ind, pos):
    """ Return fields from arg1 with value arg2 in indicator position arg3
    (1 or 2).
    """
    if ind is None:
        return d

    return tuple([f for f in d if f[pos] == ind])


def __repr_indicators(f):
    """ String representation of an indicator (replace spaces with '#'). """
    return "".join(["#" if i == " " else i for i in f[1:3]])


def __repr_field(f):
    """ String representation a single field. """
    if f[1] is None and f[2] is None:
        return "{}      {}".format(f[0], f[3][1])

    return "{}    {}{}".format(
        f[0], __repr_indicators(f),
        "".join(["${}{}".format(s[0], s[1]) for s in f[3:]]))
