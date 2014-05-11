from flask import url_for
from functools import partial

import re

def format_images(post, recipe_id):
    r = re.compile('\[img=([a-zA-Z0-9]*)\]')
    repl = partial(match_replace, recipe_id=recipe_id)
    out = r.sub(repl, post)
    return out

def match_replace(match, recipe_id):
    return '<div class="recipe-img"><img src="' + url_for('show_photo', recipe_id=recipe_id, tag=match.group(1)) + '" /></div>'
