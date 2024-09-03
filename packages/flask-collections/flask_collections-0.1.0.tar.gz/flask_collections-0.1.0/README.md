# Flask-Collections

Static collections for Flask. Inspired by [Jekyll collections](https://jekyllrb.com/docs/collections/).

## Installation

    pip install flask-collections

## Usage

```python
from flask import Flask
from flask_collections import Collections

app = Flask(__name__)
collections = Collections(app)
```

## Creating collections