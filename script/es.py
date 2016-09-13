#coding:utf-8
import elasticsearch
import datetime,time

class ES(object):
    @classmethod
    def connect_host(cls):
        hosts=[{"host": "10.117.26.137","port": 9200}]
        es = elasticsearch.Elasticsearch(
            hosts,
            sniff_on_start=True,
            sniff_on_connection_fail=True,
            sniffer_timeout=600
        )
        return es
def es_query():
    es = ES.connect_host()
    d1=datetime.datetime.now()
    d2 =d1 - datetime.timedelta(days=1)
    start_time="%s000" % int(time.mktime(d2.timetuple()))
    end_time="%s000" % int(time.mktime(d1.timetuple()))

    q_body={
        "query":
        {
            "filtered":
            {
                "query":
                {
                    "query_string":
                    {
                        "query": "(dbgroup: \"bbsdb\" OR  dbgroup: \"wwwdb\") AND lock_time: >0.3",
                    }
                },
            "filter":
            {
                "bool":
                {
                    "must":
                    [
                        {
                            "range":
                            {
                                "@timestamp":
                                {
                                    "gte": start_time,
                                    "lte": end_time,
                                    "format": "epoch_millis"
                                }
                            }
                        }
                    ],
                "must_not": []
                }
            }
        }
    },
    "size": 9999,
    "sort":
    [
        {
            "@timestamp":
            {
                "order": "desc",
                "unmapped_type": "boolean"
            }
        }
    ],
    "fields":
    [
        "_source"
    ]
         }
    res = es.search(body=q_body)
    ret = []
    print "%-25s%-15s%-18s%+15s%+15s%+15s%+10s  %-200s" % ('Time','user','clientip','lock_time','query_time','rows_examined','rows_sent','sqlcmd')
    for hit in res["hits"]["hits"]:
        value = {}
        src = hit["_source"]
        if src:
            print "%-25s%-15s%-18s%+15s%+15s%+15s%+10s  %-200s" % (src['@timestamp'],src['user'],src['clientip'],src['lock_time'],src['query_time'],src['rows_examined'],src['rows_sent'],src['sqlcmd']) 

es_query()
