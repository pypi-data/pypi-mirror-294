# Jinja-Frontmatter

Utilities to handle frontmatters in Jinja templates

## Installation

    pip install jinja-frontmatter

## Remove frontmatter from templates

```python
from jinja2 import Environment, PackageLoader
from jinja_frontmatter import RemoveFrontmatterLoader, get_template_frontmatter
import yaml

env = Environment(loader=RemoveFrontmatterLoader(PackageLoader(__name__, 'templates')))
frontmatter = get_template_frontmatter(env, "template.html") # frontmatter as text
frontmatter = get_template_frontmatter(env, "template.html", loads=yaml.safe_load) # frontmatter as yaml
```

## Access YAML frontmatters in templates

```python
from jinja2 import Environment, PackageLoader
from jinja_frontmatter import YAMLFrontmatterExtension

env = Environment(loader=PackageLoader(__name__, 'templates'))
env.add_extension(YAMLFrontmatterExtension)
```

In your template:

```
---
foo: bar
---
{{ frontmatter.foo }}
```
