import os
import yaml
import markdown
from flask import url_for, abort
from markupsafe import Markup


class MissingCollectionEntryLayoutError(Exception):
    pass


class CollectionEntry:
    @classmethod
    def from_data(cls, collection, data):
        slug = data.pop(getattr(collection, "slug_attr", "slug"))
        props = dict(data)
        content_attr = getattr(collection, "content_attr", None)
        if content_attr and content_attr != "content":
            props["content"] = props.pop(content_attr, None)
        return cls(collection, slug, **props)
    
    def __init__(self, collection, slug, content=None, layout=None, **props):
        self.collection = collection
        self.slug = slug
        self.content = content
        self.layout = layout
        self.props = props

    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, value):
        self._content = value

    @property
    def url(self):
        return url_for(self.collection.endpoint, slug=self.slug)

    def __getitem__(self, name):
        return self.props[name]
    
    def render(self):
        layout = self.layout
        if layout is None or layout is True:
            layout = self.collection.layout
        if not layout:
            return self.content or ""
        tpl = self.collection.app.jinja_env.get_template(layout)
        return tpl.render(entry=self)
    
    def update(self, content, props):
        if self.collection.save_entry(self, content, props):
            self.content = content
            self.props = props


class MarkdownCollectionEntryMixin:
    @property
    def content(self):
        content = self._content
        if self.is_markdown:
            return Markup(markdown.markdown(content))
        return content
    
    @content.setter
    def content(self, value):
        self._content = value
    

class MarkdownCollectionEntry(MarkdownCollectionEntryMixin, CollectionEntry):
    is_markdown = True


class FileCollectionEntry(MarkdownCollectionEntryMixin, CollectionEntry):
    @classmethod
    def read_frontmattered_file(cls, filename):
        slug = os.path.basename(filename).split(".", 1)[0]
        with open(filename) as f:
            content, frontmatter = parse_frontmatter(f.read())
        props = yaml.safe_load(frontmatter) if frontmatter else {}
        return slug, content, props
    
    @classmethod
    def from_file(cls, collection, filename):
        slug, content, props = cls.read_frontmattered_file(filename)
        return cls(collection, slug, filename, content, **props)
    
    def __init__(self, collection, slug, filename, content=None, **props):
        super().__init__(collection, slug, content, **props)
        self.filename = filename
        self.is_markdown = self.filename.endswith('.md')


class TemplateCollectionEntry(FileCollectionEntry):
    @property
    def content(self):
        ctx = dict(self.props, entry=self)
        content = self.template.render(**ctx)
        if self.is_markdown:
            content = markdown.markdown(content)
        return Markup(content)
    
    @content.setter
    def content(self, value):
        self._content = value
        self.template = self.collection.app.jinja_env.from_string(self._content)
    

class CollectionEntryNotFoundError(Exception):
    pass


class BaseCollection:
    @classmethod
    def matches_config(cls, config):
        return False

    def __init__(self, app, name, url=None, url_rule=None, endpoint=None, layout=None, **config):
        self.app = app
        self.name = name
        if url is False:
            self.url = None
            self.url_rule = None
            self.endpoint = None
        else:
            self.url = url or f"/{name}"
            self.url_rule = url_rule or f"{self.url.lstrip('/')}/<path:slug>"
            self.endpoint = endpoint or f"collections.{name}"
        self.layout = layout
        self.config = config

    def iter_entries(self, slice=None):
        entries = self._iter_entries()
        if slice:
            return entries[slice]
        return entries

    def _iter_entries(self):
        raise NotImplementedError()
    
    def get(self, slug):
        for entry in self.iter_entries():
            if entry.slug == slug:
                return entry
        raise CollectionEntryNotFoundError()
    
    def get_or_404(self, slug):
        try:
            return self.get(slug)
        except CollectionEntryNotFoundError:
            abort(404)
            
    def save(self, slug_or_entry, props, content=None):
        raise NotImplementedError()
            
    def remove(self, slug_or_entry):
        raise NotImplementedError()
    
    def register(self, app):
        if self.url_rule is None:
            raise Exception("cannot register collection without urls")
        app.add_url_rule(self.url_rule, self.endpoint, lambda slug: self.get_or_404(slug).render())

    def __iter__(self):
        return self.iter_entries()
    
    def __len__(self):
        return len(list(self.iter_entries()))
    
    def page(self, page, per_page=25):
        return self.iter_entries(slice(page * per_page, None, per_page))

    def __getitem__(self, slug):
        if isinstance(slug, slice):
            return self.iter_entries(slug)
        return self.get(slug)
            

class BaseDataCollection(BaseCollection):
    entry_cls = CollectionEntry

    def __init__(self, app, name, slug_attr="slug", content_attr="content", **kwargs):
        super().__init__(app, name, **kwargs)
        self.slug_attr = slug_attr
        self.content_attr = content_attr


class DataCollection(BaseDataCollection):
    @classmethod
    def matches_config(cls, config):
        return isinstance(config.get("entries"), list)
    
    def __init__(self, app, name, entries, **kwargs):
        super().__init__(app, name, **kwargs)
        self.entries = entries

    def _iter_entries(self):
        for obj in self.entries:
            yield self.entry_cls.from_data(self, obj)


def parse_frontmatter(source):
    if source.startswith("---\n"):
        frontmatter_end = source.find("\n---\n", 3)
        if frontmatter_end == -1:
            frontmatter = source[3:]
            source = ""
        else:
            frontmatter = source[3:frontmatter_end]
            source = source[frontmatter_end + 5:]
        return source, frontmatter
    return source, None