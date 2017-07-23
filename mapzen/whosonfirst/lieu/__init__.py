import json

def parse_feature_id(f):

    fid = f.get("id", None)

    if not fid:
        return None, None, Exception("Missing id property")

    try:
        source, id = fid.split("#")
        return source, id, None
    except Exception, e:
        return None, None, e

def to_string(f):

    src, id, err = parse_feature_id(f)

    if err != None:
        logging.warning(err)
        return ""

    props = f["properties"]
    geom = f["geometry"]
    coords = geom["coordinates"]

    name = props.get("name", None)

    if not name:
        name = props.get("wof:name")

    housenumber = props["addr:housenumber"]
    street = props["addr:street"]

    addr_full = props.get("addr:full", None)

    label = [
        "[%s] %s" % (src, id),
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

