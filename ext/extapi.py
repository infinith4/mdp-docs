#
# Kenozooid - software stack to support different capabilities of dive
# computers.
#
# Copyright (C) 2009 by Artur Wroblewski <wrobell@pld-linux.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# 2011: heavily modified by us for use with MDP

import os.path
from docutils import nodes

def api_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Role `:api:` bridges generated API documentation by tool like EpyDoc
    with Sphinx Python Documentation Generator.

    Other tools, other than EpyDoc, can be easily supported as well.

    First generate the documentation to be referenced, i.e. with EpyDoc::

        $ mkdir -p doc/_build/html/api
        $ epydoc -o doc/_build/html/api ...

    Next step is to generate documentation with Sphinx::

        $ sphinx-build doc doc/_build/html

    """
    basedir = inliner.document.settings.env.config.extapi_epydoc_path
    prefix = os.path.abspath(basedir)
    if not os.path.exists(prefix):
        inliner.document.settings.env.app.info('Warning: '
                                               'epydoc API not found '
                                               'in %s'%prefix)
    exists = lambda f: os.path.exists(os.path.join(prefix, f))
    link_prefix = inliner.document.settings.env.config.extapi_link_prefix
    
    # assume module is referenced
    name = '%s' % text
    uri = '%s/%s-module.html' % (link_prefix, text)
    file = '%s/%s-module.html' % (prefix, text)
    chunks = text.split('.')

    # if not module, then a class
    if not exists(file):
        name = text.split('.')[-1]
        uri = '%s/%s-class.html' % (link_prefix, text)
        file = '%s/%s-class.html' % (prefix, text)

    # if not a class, then function or class method 
    if not exists(file):
        method = chunks[-1]
        fprefix = '.'.join(chunks[:-1])
        # assume function is referenced
        file = '%s/%s-module.html' % (prefix, fprefix)
        if exists(file):
            uri = '%s/%s-module.html#%s' % (link_prefix, fprefix, method)
        else:
            # class method is references
            file = '%s/%s-class.html' % (prefix, fprefix)
            if exists(file):
                name = '.'.join(chunks[-2:]) # name should be Class.method
                uri = '%s/%s-class.html#%s' % (link_prefix, fprefix, method)

    if exists(file):
        node = nodes.reference(rawtext, name, refuri=uri, **options)
    else:
        # cannot find reference, then just inline the text
        node = nodes.literal(rawtext, text)

    return [node], []


def setup(app):
    app.add_role('api', api_role)
    app.add_config_value('extapi_epydoc_path', '', 'env')
    app.add_config_value('extapi_link_prefix', '', 'env')
