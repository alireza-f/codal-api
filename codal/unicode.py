from scrapy.exporters import JsonItemExporter


class JsonUnicode(JsonItemExporter):
    """Override constructor of JsonItemExporter for persian alphabet"""
    def __init__(self, file, **kwargs):
        super().__init__(file, ensure_ascii=False, **kwargs)
