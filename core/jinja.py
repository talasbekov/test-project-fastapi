import tempfile
import jinja2

templates_dir = tempfile.gettempdir()
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir))
