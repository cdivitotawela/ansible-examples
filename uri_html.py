#!/usr/bin/python
#coding: utf-8 -*-

# (c) 2019 Chaminda Divitotawela <cdivitotawela@gmail.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from ansible.module_utils.basic import *

DOCUMENTATION = '''
module: uri_html
version_added: 2.7
short_description: Collect html page from url and parse values with xpath
'''



def main():

    ERROR = ''

    # Verify requests module available
    try:
        import requests
    except ImportError:
        ERROR = 'Python package requests is required'

    # Verify lxml module available
    try:
        from lxml import html
    except:
        ERROR = 'Python package lxml is required'

    module = AnsibleModule(
        argument_spec=dict(
            url=dict(required=True),
            xpath=dict(required=True),
            mode=dict(required=True, type='str', choices=['extract','present'])
        )
    )

    if not ERROR == '':
        module.fail_json(msg={'error': ERROR})

    url = module.params['url']
    xpath = module.params['xpath']

    try:
        page = requests.get(url)
        tree = html.fromstring(page.content)
        output = tree.xpath(xpath)[0]
        response={"output": output}
        module.exit_json(changed=False, result=response)
    except Exception as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()