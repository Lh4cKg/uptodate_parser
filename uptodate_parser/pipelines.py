# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class UptodateParserPipeline:
    def process_item(self, item, spider):
        breakpoint()
        return item


class UptodateHtmlFilePipeline:

    def process_item(self, item, spider):
        breakpoint()
        print(f'Item: {item}')
