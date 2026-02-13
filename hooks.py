# https://github.com/squidfunk/mkdocs-material/discussions/4969#discussioncomment-7290363
from datetime import datetime


def on_config(config, **kwargs):
    config.copyright = config.copyright.format(year=datetime.now().year)
