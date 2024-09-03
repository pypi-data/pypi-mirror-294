from jinja2 import BaseLoader
from jinja2.ext import Extension
import yaml


class RemoveFrontmatterLoader(BaseLoader):
    def __init__(self, loader):
        self.loader = loader

    def get_source(self, environment, template):
        source, filename, uptodate = self.loader.get_source(environment, template)
        if not getattr(environment, "keep_frontmatter", False):
            source = extract_frontmatter(source)[0]
        return source, filename, uptodate
    
    def list_templates(self):
        return self.loader.list_templates()


class YAMLFrontmatterExtension(Extension):
    """Jinja extension to access YAML frontmatters in templates
    """
    def preprocess(self, source, name, filename=None):
        source, frontmatter = extract_frontmatter(source, loads=yaml.safe_load)
        varname = getattr(self.environment, "frontmatter_varname", "frontmatter")
        return "{%% set %s = %r -%%}\n%s" % (varname, frontmatter, source)


def get_template_frontmatter(env, filename, loads=None):
    env.keep_frontmatter = True
    source = env.loader.get_source(env, filename)[0]
    env.keep_frontmatter = False
    return extract_frontmatter(source, loads=loads)[1]


def extract_frontmatter(source, loads=None):
    if source.startswith("---\n"):
        frontmatter_end = source.find("\n---\n", 4)
        if frontmatter_end == -1:
            frontmatter = source[4:]
            source = ""
        else:
            frontmatter = source[4:frontmatter_end]
            source = source[frontmatter_end + 5:]
        if loads:
            frontmatter = loads(frontmatter)
        return source, frontmatter
    return source, None
