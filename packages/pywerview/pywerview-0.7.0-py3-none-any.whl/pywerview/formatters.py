# This file is part of PywerView.

# PywerView is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# PywerView is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with PywerView.  If not, see <http://www.gnu.org/licenses/>.

# Yannick Méheut [yannick (at) meheut (dot) org] - Copyright © 2023

import logging
import binascii

try:
    from Cryptodome.Hash import MD4
except ImportError:
    from Crypto.Hash import MD4

from impacket.examples.ntlmrelayx.attacks.ldapattack import MSDS_MANAGEDPASSWORD_BLOB
from impacket.ldap.ldaptypes import SR_SECURITY_DESCRIPTOR

__uac_flags = {0x0000001: 'SCRIPT',
               0x0000002: 'ACCOUNTDISABLE',
               0x0000008: 'HOMEDIR_REQUIRED',
               0x0000010: 'LOCKOUT',
               0x0000020: 'PASSWD_NOTREQD',
               0x0000040: 'PASSWD_CANT_CHANGE',
               0x0000080: 'ENCRYPTED_TEXT_PWD_ALLOWED',
               0x0000100: 'TEMP_DUPLICATE_ACCOUNT',
               0x0000200: 'NORMAL_ACCOUNT',
               0x0000800: 'INTERDOMAIN_TRUST_ACCOUNT',
               0x0001000: 'WORKSTATION_TRUST_ACCOUNT',
               0x0002000: 'SERVER_TRUST_ACCOUNT',
               0x0010000: 'DONT_EXPIRE_PASSWORD',
               0x0020000: 'MNS_LOGON_ACCOUNT',
               0x0040000: 'SMARTCARD_REQUIRED',
               0x0080000: 'TRUSTED_FOR_DELEGATION',
               0x0100000: 'NOT_DELEGATED',
               0x0200000: 'USE_DES_KEY_ONLY',
               0x0400000: 'DONT_REQ_PREAUTH',
               0x0800000: 'PASSWORD_EXPIRED',
               0x1000000: 'TRUSTED_TO_AUTH_FOR_DELEGATION',
               0x4000000: 'PARTIAL_SECRETS_ACCOUNT'}

__sat_flags = {0x00000000: 'DOMAIN_OBJECT',
               0x10000000: 'GROUP_OBJECT',
               0x10000001: 'NON_SECURITY_GROUP_OBJECT',
               0x20000000: 'ALIAS_OBJECT',
               0x20000001: 'NON_SECURITY_ALIAS_OBJECT',
               # According to https://docs.microsoft.com/en-us/windows/win32/adschema/a-samaccounttype
               # USER_OBJECT and NORMAL_USER_ACCOUNT are both 0x30000000
               0x30000000: 'USER_OBJECT',
               0x30000001: 'MACHINE_ACCOUNT',
               0x30000002: 'TRUST_ACCOUNT',
               0x40000000: 'APP_BASIC_GROUP',
               0x40000001: 'APP_QUERY_GROUP',
               0x7fffffff: 'ACCOUNT_TYPE_MAX'}

__ace_flags = {0x1: 'object_inherit', 0x2: 'container_inherit',
               0x4: 'non_propagate_inherit', 0x8: 'inherit_only',
               0x10: 'inherited_ace', 0x20: 'audit_successful_accesses',
               0x40: 'audit_failed_access'}

__object_ace_flags = {0x1: 'object_ace_type_present', 0x2: 'inherited_object_ace_type_present'}

# Resources: https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/990fb975-ab31-4bc1-8b75-5da132cd4584
__access_mask = {0x1: 'create_child', 0x2: 'delete_child',
                 0x4: 'list_children', 0x08: 'self',
                 0x10: 'read_property', 0x20: 'write_property',
                 0x40: 'delete_tree', 0x80: 'list_object',
                 0x100: 'extended_right', 0x10000: 'delete',
                 0x20000: 'read_control', 0x40000: 'write_dacl',
                 0x80000: 'write_owner'}

__access_mask_generic = {0xf01ff: 'generic_all', 0x20094: 'generic_read',
                         0x20028: 'generic_write', 0x20004: 'generic_execute'}

# https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/e9a2d23c-c31e-4a6f-88a0-6646fdb51a3c
__trust_attrib = {0x1: 'TRUST_ATTRIBUTE_NON_TRANSITIVE', 
                  0x2: 'TRUST_ATTRIBUTE_UPLEVEL_ONLY',
                  0x4: 'TRUST_ATTRIBUTE_QUARANTINED_DOMAIN', 
                  0x8: 'TRUST_ATTRIBUTE_FOREST_TRANSITIVE',
                  0x10: 'TRUST_ATTRIBUTE_CROSS_ORGANIZATION', 
                  0x20: 'TRUST_ATTRIBUTE_WITHIN_FOREST',
                  0x40: 'TRUST_ATTRIBUTE_TREAT_AS_EXTERNAL',
                  0x80: 'TRUST_ATTRIBUTE_USES_RC4_ENCRYPTION',
                  # TODO: x100 seems not documented ?
                  0x100: 'TRUST_USES_AES_KEYS',
                  0X200: 'TRUST_ATTRIBUTE_CROSS_ORGANIZATION_NO_TGT_DELEGATION',
                  0x400: 'TRUST_ATTRIBUTE_PIM_TRUST',
                  0x800: 'TRUST_ATTRIBUTE_CROSS_ORGANIZATION_ENABLE_TGT_DELEGATION'}

__trust_direction = {0: 'disabled', 1: 'inbound',
                     2: 'outbound', 3: 'bidirectional'}

__trust_type = {1: 'windows_non_active_directory',
                2: 'windows_active_directory', 3: 'mit'}

def __format_flag(raw_value, flag_dict):
    try:
        int_value = int(raw_value)
    except ValueError:
        self._logger.warning('Unable to convert raw flag value to int')
        return raw_value

    parsed_flags = list()
    for flag, flag_label in flag_dict.items():
        if (int_value & flag) == flag:
            parsed_flags.append(flag_label)
    return parsed_flags

def __format_dict_lookup(raw_value, dictionary):
    try:
        return dictionary[int(raw_value)]
    except (ValueError, KeyError):
        self._logger.warning('Unable to convert raw value to int')
        return raw_value

def format_useraccountcontrol(raw_value):
    return __format_flag(raw_value, __uac_flags)

def format_samaccounttype(raw_value):
    return __sat_flags[int(raw_value)]

def format_ace_access_mask(raw_value):
    try:
        int_value = int(raw_value)
    except ValueError:
        self._logger.warning('Unable to convert raw ace acess mask value to int')
        return raw_value

    activedirectoryrights = list()
    for flag, flag_label in __access_mask_generic.items():
        if (int_value & flag) == flag:
            activedirectoryrights.append(flag_label)
            int_value ^= flag
    activedirectoryrights += __format_flag(raw_value, __access_mask)

    return activedirectoryrights


def format_managedpassword(raw_value):
    blob = MSDS_MANAGEDPASSWORD_BLOB()
    blob.fromString(raw_value)
    return binascii.hexlify(MD4.new(blob['CurrentPassword'][:-2]).digest()).decode('utf8')

def format_groupmsamembership(raw_value):
    sid = list()
    sr = SR_SECURITY_DESCRIPTOR(data=raw_value)
    for dacl in sr['Dacl']['Data']:
        sid.append(dacl['Ace']['Sid'].formatCanonical())
    return sid

def format_ace_flags(raw_value):
    return __format_flag(raw_value, __ace_flags)

def format_object_ace_flags(raw_value):
    return __format_flag(raw_value, __object_ace_flags)

def format_trustdirection(raw_value):
    return __format_dict_lookup(raw_value, __trust_direction)

def format_trusttype(raw_value):
    return __format_dict_lookup(raw_value, __trust_type)

def format_trustattributes(raw_value):
    return __format_flag(raw_value, __trust_attrib)
 
