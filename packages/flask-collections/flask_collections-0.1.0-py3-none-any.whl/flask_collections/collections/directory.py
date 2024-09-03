import os
import yaml
from ..collection import (BaseCollection, CollectionEntry, FileCollectionEntry,
                          TemplateCollectionEntry, CollectionEntryNotFoundError)


class DirectoryCollection(BaseCollection):
    file_types = ('html', 'md')
    default_save_file_ext = "html"
    entry_cls = TemplateCollectionEntry

    @classmethod
    def matches_config(cls, config):
        return config.get("path") and os.path.isdir(config["path"])

    def __init__(self, app, name, path, **kwargs):
        super().__init__(app, name, **kwargs)
        self.path = path

    def _iter_entries(self):
        for filename in sorted(os.listdir(self.path)):
            yield self._create_entry(filename)

    def get(self, slug):
        filename = self.find_entry_filename(slug)
        if not filename:
            raise CollectionEntryNotFoundError()
        return self._create_entry(filename)
        
    def _create_entry(self, filename):
        return self.entry_cls.from_file(self, os.path.join(self.path, filename))

    def find_entry_filename(self, slug):
        for ext in self.file_types:
            filename = f"{slug}.{ext}"
            if os.path.isfile(os.path.join(self.path, filename)):
                return filename
            
    def save(self, slug_or_entry, props, content=None):
        if isinstance(slug_or_entry, FileCollectionEntry):
            filename = slug_or_entry.filename
        else:
            if isinstance(slug_or_entry, CollectionEntry):
                slug_or_entry = slug_or_entry.slug
            filename = os.path.join(self.path, f"{slug_or_entry}.{self.default_save_file_ext}")
        source = "---\n" + yaml.dump(props)
        if content:
            source += "\n---\n" + content
        with open(filename, "w") as f:
            f.write(source)
