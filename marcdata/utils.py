from marcdata import *

def fixed_length_tuple(rec):
    f = control_value([fld for fld in rec[1] if fld[0] == "008"][0])
    return (f[0:6], f[6], f[7:11], f[11:15], f[15:18],
            material_desc(material_type(rec), f[18:35]), f[35:38],
            f[38], f[39])


def material_desc(m, d):
    return {"BK": material_bk, "CF": material_cf, "MP": material_mp,
            "MU": material_mu, "CR": material_cr, "VM": material_vm,
            "MX": material_mx}[m](d)


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
