# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import shutil

import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
from scrapy.http import Request
from scrapy.utils.python import to_bytes
import hashlib
from scrapy.exceptions import NotConfigured, IgnoreRequest
from scrapy.utils.request import referer_str


class FileException(Exception):
    """General media error exception"""


class ScrapyPicPipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):
    image_dir = ""

    def get_media_requests(self, item, info):
        self.image_dir = item["image_dir"]
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    # def file_path(self, request, response=None, info=None):
    #     def _warn():
    #         from scrapy.exceptions import ScrapyDeprecationWarning
    #         import warnings
    #         warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
    #                       'please use file_path(request, response=None, info=None) instead',
    #                       category=ScrapyDeprecationWarning, stacklevel=1)
    #
    #     if not isinstance(request, Request):
    #         _warn()
    #         url = request
    #     else:
    #         url = request.url
    #
    #     if not hasattr(self.file_key, '_base'):
    #         _warn()
    #         return self.file_key(url)
    #     elif not hasattr(self.image_key, '_base'):
    #         _warn()
    #         return self.image_key(url)
    #
    #     image_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
    #     return 'full/%s/%s.jpg' % (self.image_dir, image_guid)
    #
    # def thumb_path(self, request, thumb_id, response=None, info=None):
    #     def _warn():
    #         from scrapy.exceptions import ScrapyDeprecationWarning
    #         import warnings
    #         warnings.warn('ImagesPipeline.thumb_key(url) method is deprecated, please use '
    #                       'thumb_path(request, thumb_id, response=None, info=None) instead',
    #                       category=ScrapyDeprecationWarning, stacklevel=1)
    #
    #     if not isinstance(request, Request):
    #         _warn()
    #         url = request
    #     else:
    #         url = request.url
    #
    #     if not hasattr(self.thumb_key, '_base'):
    #         _warn()
    #         return self.thumb_key(url, thumb_id)
    #
    #     thumb_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
    #     return 'thumbs/%s/%s/%s.jpg' % (thumb_id, self.image_dir, thumb_guid)

    def item_completed(self, results, item, info):
        settings = get_project_settings()
        storage = settings.get('IMAGES_STORE')
        if not os.path.exists(os.path.join(storage, "full/%s" % item["image_dir"])):
            os.makedirs(os.path.join(storage, "full/%s" % item["image_dir"]))
        file_paths = [
            {
                "origin_path": x['path'],
                "next_path": x['path'].replace("full", "full/%s" % item["image_dir"])
            }
            for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no files")
        for i in file_paths:
            origin_path = os.path.join(storage, i.get("origin_path", ""))
            next_path = os.path.join(storage, i.get("next_path", ""))
            try:
                shutil.move(origin_path, next_path)
            except Exception as exc:
                print exc.message
                pass
        item['image_paths'] = file_paths
        return item
