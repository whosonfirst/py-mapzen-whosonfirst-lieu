import mapzen.whosonfirst.elasticsearch
import hashlib
import copy
import json

class index(mapzen.whosonfirst.elasticsearch.index):

    def __init__(self, **kwargs):

        mapzen.whosonfirst.elasticsearch.index.__init__(self, **kwargs)

    def prepare_report_bulk(self, report):

        rows = []

        str_report = json.dumps(report)

        hash = hashlib.md5()
        hash.update(str_report)
        
        hash_report = hash.hexdigest()

        candidates = [
            report["object"]
        ]

        for o in report.get("same_as", []):
            candidates.append(o["object"])

        for o in report.get("possibly_same_as", []):
            candidates.append(o["object"])
        
        for o in candidates:

            source = copy.deepcopy(o)
            source["properties"]["lieu:hash"] = hash_report

            row = {
                "_id": o["properties"]["lieu:guid"],
                "_index": "lieu",
                "_type": "record",
                "_source": source
            }

            rows.append(row)

        # https://github.com/openvenues/lieu#output-format

        is_dupe = report["is_dupe"]
        principal = report["object"]
        
        principal_id = principal["properties"]["lieu:guid"]

        for rel in ("same_as", "possibly_same_as"):

            for o in report.get(rel, []):

                other = o["object"]
                other_id = other["properties"]["lieu:guid"]
                
                source = copy.deepcopy(o)
                del(source["object"])

                source["lieu:principal"] = principal_id
                source["lieu:other"] = other_id
                source["lieu:rel"] = rel
                source["lieu:hash"] = hash_report
                source["is_dupe"] = is_dupe
            
                row = {
                    # "_id": ""			# just let ES do this
                    "_index": "lieu",
                    "_type": "rollup",
                    "_source": source
                }

                rows.append(row)

        for row in rows:
            yield row

class search(mapzen.whosonfirst.elasticsearch.search):

    def __init__(self, **kwargs):

        mapzen.whosonfirst.elasticsearch.query.__init__(self, **kwargs)
