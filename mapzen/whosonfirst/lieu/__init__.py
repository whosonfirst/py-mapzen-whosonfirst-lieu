import json
import machinetag.common

def parse_feature_id(f):

    fid = f.get("id", None)

    if not fid:
        return None, None, None, Exception("Missing id property")

    mt = machinetag.common.from_string(fid)

    if not mt.is_machinetag():
        return None, None, None, Exception("Invalid source ID")

    return mt.namespace(), mt.predicate(), mt.value(), None

def to_string(f):

    prefix, key, id, err = parse_feature_id(f)

    if err != None:
        logging.warning(err)
        return ""

    props = f["properties"]
    geom = f["geometry"]
    coords = geom["coordinates"]

    name = props.get("name", "MISSING name")

    if not name:
        name = props.get("wof:name", "MISSING name")

    housenumber = props.get("addr:housenumber", "MISSING addr:housenumber")
    street = props.get("addr:street", "MISSING addr:street")

    addr_full = props.get("addr:full", "MISSING addr:full")

    label = [
        "[%s:%s=%s]" % (prefix, key, id),
        name,
        "%s %s" % (housenumber, street),
        "%s" % ",".join(map(str, coords)),
    ]

    if addr_full:
        label.append(" (%s)" % addr_full)

    label = "\t".join(label)
    return label

def crawl(parts, **kwargs):

    for path in parts:

        fh = open(path, "r")

        for ln in fh:

            try:
                data = json.loads(ln)
                yield data["is_dupe"], data["object"], data.get("same_as", []), None
            except Exception, e:
                yield None, None, None, e

