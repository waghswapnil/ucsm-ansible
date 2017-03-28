#!/usr/bin/python

DOCUMENTATION = '''
---
module: cisco_ucs_server_power.py
short_description:
version_added:
description:

Input Params:

    state:
        description: Used to create or delete the local user
        choices: ["present", "absent"]
        default: "present"
        required: False

ucsmsdk apis:

requirements: ['ucsmsdk', 'ucsm_apis']
author: "Swapnil Wagh(swwagh@cisco.com)"
'''

EXAMPLES = '''
- name: power on a server
  cisco_ucs_user:
    state: "present"
    ip: "192.168.1.1"
    username: "admin"
    password: "password"
'''


def login(module):
    ansible = module.params
    ucsm = ansible.get('ucsm')
    if ucsm:
        return ucsm

    from ucsmsdk.ucshandle import UcsHandle
    results = {}
    try:
        ucsm = UcsHandle(ip=ansible["ip"],
                         username=ansible["username"],
                         password=ansible["password"],
                         port=ansible["port"],
                         secure=ansible["secure"],
                         proxy=ansible["proxy"])
        ucsm.login()
    except Exception as e:
        results["msg"] = str(e)
        module.fail_json(**results)
    return ucsm


def logout(module, handle):
    ansible = module.params
    ucsm = ansible.get('ucsm')
    if ucsm:
        # we used a pre-existing handle from another task.
        # do not logout
        return False

    if handle:
        handle.logout()
        return True
    return False


def setup(ucsm, module):

    from ucsm_apis.server.power import server_power_on
    from ucsm_apis.server.power import server_power_off
    from ucsm_apis.server.power import server_power_get

    results = {}
    err = False
    match = False

    ansible = module.params
    power_state = ansible.get("power_state")
    chassis_id = ansible.get("chassis_id")
    blade_id = ansible.get("blade_id")
    rack_id = ansible.get("rack_id")

    try:
        current_state = server_power_get(ucsm,
                                         chassis_id=chassis_id,
                                         blade_id=blade_id,
                                         rack_id=rack_id)
        if current_state == power_state:
            match = True

        if power_state == "on":
            if module.check_mode or match:
                results["changed"] = not match
                return results, False

            server_power_on(ucsm, chassis_id=chassis_id, blade_id=blade_id,
                            rack_id=rack_id)
        elif power_state == "off":
            server_power_off(ucsm, chassis_id=chassis_id, blade_id=blade_id,
                             rack_id=rack_id)
        results["changed"] = True
    except Exception as e:
        err = True
        results["msg"] = str(e)
        results["changed"] = False
        ucsm.logout()
        raise

    return results, err


def main():
    from ansible.module_utils.basic import AnsibleModule
    module = AnsibleModule(
        argument_spec=dict(
            chassis_id=dict(required=False, default=0, type='int'),
            blade_id=dict(required=False, default=0, type='int'),
            rack_id=dict(required=False, default=0, type='int'),
            power_state=dict(required=True,
                             choices=["on", "off"], type='str'),

            # UcsHandle
            ucsm=dict(required=False, type='dict'),

            # UCS Domain credentials
            ip=dict(required=False, type='str'),
            username=dict(required=False, default="admin", type='str'),
            password=dict(required=False, type='str'),
            port=dict(required=False, default=None),
            secure=dict(required=False, default=None),
            proxy=dict(required=False, default=None)
        ),
        supports_check_mode=True
    )

    ucsm = login(module)
    results, err = setup(ucsm, module)
    logout(module, ucsm)
    if err:
        module.fail_json(**results)
    module.exit_json(**results)


if __name__ == '__main__':
    main()
