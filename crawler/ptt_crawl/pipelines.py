# -*- coding: utf-8 -*-
import pymongo
from scrapy.conf import settings
import datetime
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MongoDBPipeline:
    def open_spider(self, spider):
        """
        pyMongo initialize
        """
        client = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
        tdb = client[settings['MONGODB_DB']]
        self.cur_article = tdb[settings['MONGODB_DB_ARTICLE']]
        self.cur_user = tdb[settings['MONGODB_DB_USER']]
        self.cur_logs = tdb[settings['MONGODB_DB_LOGS']]
        self.start_time = datetime.datetime.now()

    def process_item(self, item, spider):
        """
        save data into DB.
        """

        # self.cur_article
        if self.cur_article.find({'url': item['url']}).count() == 0:
            self.cur_article.insert(dict(item))
        else:
            self.cur_article.update({'url': item['url']}, dict(item))

        # self.cur_user
        # article
        tar = self.cur_user.find_one({'id': item['author']})
        if not tar:
            # author not in db
            val = {
                'id': item['author'],
                'ip': [item['ip_author']],
                'data': [{'board': item['board'], 'text': item['text'], 'tag': None, 'url': item['url'],
                          'title': item['title']}],
                'tags': 0
            }
            self.cur_user.insert(val)
        else:
            # author in db
            val = dict(tar)
            if not item['ip_author'] in val['ip']:
                val['ip'].append(item['ip_author'])
            if not item['text'] in [data['text'] for data in val['data']]:
                val['data'].append({'board': item['board'], 'text': item['text'], 'tag': None, 'url': item['url'],
                                    'title': item['title']})
            self.cur_user.update({'id': item['author']}, val)

        # comment
        tag_dict = {'推': 1, '噓': -1, '→': 0}
        for com in item['comment']:
            tar = self.cur_user.find_one({'id': com['user']})
            if not tar:
                # user not in db
                val = {
                    'id': com['user'],
                    'ip': [com['ip']] if com['ip'] else [],
                    'data': [
                        {'board': item['board'], 'text': com['text'], 'tag': tag_dict[com['tag']], 'url': item['url'],
                         'title': item['title']}],
                    'tags': tag_dict[com['tag']]
                }
                self.cur_user.insert(val)
            else:
                # user in db
                val = dict(tar)
                if com['ip'] and not com['ip'] in val['ip']:
                    val['ip'].append(com['ip'])
                if not com['text'] in [data['text'] for data in val['data']]:
                    val['data'].append(
                        {'board': item['board'], 'text': com['text'], 'tag': tag_dict[com['tag']], 'url': item['url'],
                         'title': item['title']})
                    val['tags'] += tag_dict[com['tag']]
                self.cur_user.update({'id': com['user']}, val)
        return item

    def close_spider(self, spider):
        end_time = datetime.datetime.now()
        val = {
            'start_time': self.start_time,
            'end_time': end_time
        }
        self.cur_logs.insert(val)

