#!/usr/bin/python

DOCUMENTATION = '''
---
module: cisco_ucs_login
short_description: Login to a UCS Domain
version_added: "0.9.0.0"
description:
  - Logs in to a cisco UCS Domain
  - Executes the aaaLogin method provided by the UCS Manager

requirements: ['ucsmsdk']
author: "Swapnil Wagh(swwagh@cisco.com)"
'''

EXAMPLES = '''
- name: login to a UCS Domain
  hosts: 127.0.0.1
  connection: local
  tasks:
  - name: login to the server
    cisco_ucs_login:
      ip=192.168.1.1
      username=admin
      password=password
'''


def ucs_login(module):
    '''
    Fetches/Creates a server handle.

    Arguments:
        module: AnsibleModule

    Returns:
        (server(UcsHandle), results(dict), error(bool))

    '''
    ansible = module.params
    results = {}

    server, results, err = _login(ip=ansible["ip"],
                                  username=ansible["username"],
                                  password=ansible["password"],
                                  port=ansible["port"],
                                  secure=ansible["secure"],
                                  proxy=ansible["proxy"])
    return server, results, err


def _login(ip, username, password, port=None, secure=None, proxy=None):
    from ucsmsdk.ucshandle import UcsHandle
    results = {}
    try:
        server = UcsHandle(ip, username, password, port, secure, proxy)
        server.login()
    except Exception as e:
        results["msg"] = str(e)
        return server, results, True

    results["msg"] = "login succeded"
    results["changed"] = False
    return server, results, False


def main():
    from ansible.module_utils.basic import AnsibleModule
    module = AnsibleModule(
        argument_spec=dict(
            ip=dict(required=True, type='str'),
            username=dict(required=False, default="admin", type='str'),
            password=dict(required=True, type='str'),
            port=dict(required=False, default=None),
            secure=dict(required=False, default=None),
            proxy=dict(required=False, default=None)
        ),
        supports_check_mode=True
    )

    server, results, err = ucs_login(module)
    if err:
        module.fail_json(**results)
    module.exit_json(**results)


if __name__ == '__main__':
    main()
