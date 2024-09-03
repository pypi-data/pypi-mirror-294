from ..collection import BaseDataCollection
import csv
import json
import yaml
import os


class DataFileCollection(BaseDataCollection):
    @classmethod
    def matches_config(cls, config):
        return config.get("path") and os.path.isfile(config["path"]) and os.path.basename(config["path"]).split(".", 1)[1].lower() in getattr(cls, "file_exts", [])
    
    def __init__(self, app, name, path, **kwargs):
        super().__init__(app, name, **kwargs)
        self.path = path


class CSVCollection(DataFileCollection):
    file_exts = ("csv",)

    def __init__(self, app, name, path, csv_options=None, **kwargs):
        super().__init__(app, name, path, **kwargs)
        self.csv_options = csv_options or {}
    
    def _iter_entries(self):
        with open(self.path) as f:
            reader = csv.DictReader(f, **self.csv_options)
            for row in reader:
                 yield self.entry_cls.from_data(self, row)


class JSONCollection(DataFileCollection):
    file_exts = ("json",)
    
    def _iter_entries(self):
        with open(self.path) as f:
            for row in json.load(f):
                 yield self.entry_cls.from_data(self, row)


class YAMLCollection(DataFileCollection):
    file_exts = ("yaml", "yml")
    
    def _iter_entries(self):
        with open(self.path) as f:
            for row in yaml.safe_load(f):
                 yield self.entry_cls.from_data(self, row)
