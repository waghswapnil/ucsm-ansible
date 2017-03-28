!/usr/bin/python

DOCUMENTATION = '''
---
module: cisco_ucs_logout
short_description: Logout of a UCS Domain
version_added: "0.9.0.0"
description:
  - Logs out of a cisco UCS Domain
  - Executes the aaaLogout method provided by the UCS Manager

requirements: ['ucsmsdk']
author: "Swapnil Wagh(swwagh@cisco.com)"
'''

EXAMPLES = '''
- name: login to a UCS Domain
  hosts: 127.0.0.1
  connection: local
  tasks:
  - name: logout from the server
    cisco_ucs_logout:
      server=frozen_server_handle
'''


def ucs_logout(module):
    results = {}
    results['changed'] = False

    ucs = module.params.get('server')
    if ucs:
        ucs.logout()
        return results, False

    results["msg"] = "server is a required parameter"
    return results, True


def main():
    from ansible.module_utils.basic import AnsibleModule
    module = AnsibleModule(
        argument_spec=dict(
            server=dict(required=True)
        ),
        supports_check_mode=True
    )

    results, err = ucs_logout(module)
    if err:
        module.fail_json(**results)
    module.exit_json(**results)


if __name__ == '__main__':
    main()
