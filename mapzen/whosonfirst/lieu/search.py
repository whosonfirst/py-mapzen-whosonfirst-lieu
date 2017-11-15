import mapzen.whosonfirst.elasticsearch

class index(mapzen.whosonfirst.elasticsearch.index):

    def __init__(self, **kwargs):

        mapzen.whosonfirst.elasticsearch.index.__init__(self, **kwargs)

        self.index = 'lieu'
        self.doctype = 'lieu'
        
    def prepare_report(self, report):

        body = self.prepare_json(report)

        return {
            'index': self.index,
            'doc_type': self.doctype,
            'body': body
        }

    # https://stackoverflow.com/questions/20288770/how-to-use-bulk-api-to-store-the-keywords-in-es-by-using-python

    def prepare_report_bulk(self, report):
       
        body = self.prepare_json(report)

        return {
            # '_id': id,
            '_index': self.index,
            '_type': self.doctype,
            '_source': body
        }

    def prepare_json(self, report):

        data = copy.deepcopy(report)
        return data

class search(mapzen.whosonfirst.elasticsearch.search):

    def __init__(self, **kwargs):

        mapzen.whosonfirst.elasticsearch.query.__init__(self, **kwargs)
