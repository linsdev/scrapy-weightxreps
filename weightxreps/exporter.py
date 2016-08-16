# -*- coding: utf-8 -*-

from scrapy.conf import settings
from scrapy.contrib.exporter import CsvItemExporter


class CSVitemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        kwargs['fields_to_export'] = settings.getlist('EXPORT_FIELDS')
        kwargs['encoding'] = settings.get('EXPORT_ENCODING', 'utf-8')
        super(CSVitemExporter, self).__init__(*args, **kwargs)
