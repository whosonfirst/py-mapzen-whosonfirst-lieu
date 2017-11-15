import json

def crawl(paths):

    for path in paths:
        
        fh = open(path, "r")
        
        for ln in fh:
            
            ln = ln.strip()
            data = json.loads(ln)
            yield data

            # yield idx.prepare_report_bulk(data)
