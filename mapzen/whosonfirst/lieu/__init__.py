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

def crawl(parts, **kwargs):

    for path in parts:

        fh = open(path, "r")

        for ln in fh:

            try:
                data = json.loads(ln)
                yield data["is_dupe"], data["object"], data.get("same_as", []), None
            except Exception, e:
                yield None, None, None, e

