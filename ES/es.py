# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : es.py
# @Software: PyCharm


"""
es 引擎相关
"""

from elasticsearch import Elasticsearch

es = Elasticsearch("http://47.111.69.97:9200/")


class ES(object):
    """
    es 对象
    """

    def __init__(self, index_name: str):
        self.es = es
        self.index_name = index_name

    def get_doc(self, uid):
        return self.es.get(index=self.index_name, id=uid)

    def insert_one(self, doc: dict):
        self.es.index(index=self.index_name, body=doc)

    def insert_array(self, docs: list):
        for doc in docs:
            self.es.index(index=self.index_name, body=doc)

    def search(self, query, count: int = 30, fields=None):
        fields = fields if fields else ["title", 'pub_date']
        dsl = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": fields
                },
                'wildcard': {
                    'content': {
                        'value': '*' + query + '*'
                    }
                }
            },
            "highlight": {
                "fields": {
                    "title": {}
                }
            }
        }
        match_data = self.es.search(index=self.index_name, body=dsl, size=count)
        print('>>>>>>>>>>', match_data)
        return match_data

    def _search(self, query: dict, count: int = 20, fields=None):  # count: 返回的数据大小
        results = []
        # params = {
        #     'size': count
        # }
        match_data = self.search(query, count, fields)
        for hit in match_data['hits']['hits']:
            results.append(hit['_source'])
        return results

    def create_index(self):
        if self.es.indices.exists(index=self.index_name) is True:
            self.es.indices.delete(index=self.index_name)
        self.es.indices.create(index=self.index_name, ignore=400)

    def delete_index(self):
        try:
            self.es.indices.delete(index=self.index_name)
        except:
            pass

