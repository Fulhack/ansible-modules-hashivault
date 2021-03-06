#!/usr/bin/env python
DOCUMENTATION = '''
---
module: hashivault_init
version_added: "2.2.0"
short_description: Hashicorp Vault init enable module
description:
    - Module to init Hashicorp Vault.
options:
    url:
        description:
            - url for vault
        default: to environment variable VAULT_ADDR
    verify:
        description:
            - verify TLS certificate
        default: to environment variable VAULT_SKIP_VERIFY
    authtype:
        description:
            - "authentication type to use: token, userpass, github, ldap"
        default: token
    token:
        description:
            - token for vault
        default: to environment variable VAULT_TOKEN
    username:
        description:
            - username to login to vault.
    password:
        description:
            - password to login to vault.
    secret_shares:
        description:
            - specifies the number of shares to split the master key into.
        default: 5
    secret_threshold:
        description:
            - specifies the number of shares required to reconstruct the master key.
        default: 3
    pgp_keys:
        description:
            - specifies an array of PGP public keys used to encrypt the output unseal keys.
        default: []
'''
EXAMPLES = '''
---
- hosts: localhost
  tasks:
    - hashivault_init:

- hosts: localhost
  tasks:
    - hashivault_init:
        secret_shares: 7
        secret_threshold: 4
'''


def main():
    argspec = hashivault_argspec()
    argspec['secret_shares'] = dict(required=False, type='int', default=5)
    argspec['secret_threshold'] = dict(required=False, type='int', default=3)
    argspec['pgp_keys'] = dict(required=False, type='list', default=[])
    module = hashivault_init(argspec)
    result = hashivault_initialize(module.params)
    if result.get('failed'):
        module.fail_json(**result)
    else:
        module.exit_json(**result)


from ansible.module_utils.basic import *
from ansible.module_utils.hashivault import *


@hashiwrapper
def hashivault_initialize(params):
    client = hashivault_client(params)
    if client.is_initialized():
        return {'changed': False}
    result =  {'changed': True}
    secret_shares = params.get('secret_shares')
    secret_threshold = params.get('secret_threshold')
    pgp_keys = params.get('pgp_keys')
    result.update(
        client.initialize(
            secret_shares=secret_shares,
            secret_threshold=secret_threshold,
            pgp_keys=pgp_keys
        )
    )
    return result


if __name__ == '__main__':
    main()
