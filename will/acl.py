# -*- coding: utf-8 -*-
import logging
from will import settings


def get_acl_members(acl):
    acl_members = []
    acl = acl.lower()

    if getattr(settings, "ACL", None):
        try:
            # Case-insensitive checks
            for k in settings.ACL.keys():
                if k.lower() == acl:
                    acl_members = settings.ACL[k]
                    break
        except AttributeError:
            pass

    return acl_members


def is_acl_allowed(user_id, acl):
    if not getattr(settings, "ACL", None):
        logging.warning(
            "%s was just allowed to perform actions in %s because no ACL settings exist. This can be a security risk." % (
                user_id,
                acl,
            )
        )
        return True
    for a in acl:
        acl_members = get_acl_members(a)
        if user_id in acl_members:
            return True

    return False


def verify_acl(message, acl):
    try:
        if settings.DISABLE_ACL:
            return True

        allowed = is_acl_allowed(message.sender.id, acl)
        if allowed:
            return True
        if hasattr(message, "data") and hasattr(message.data, "backend_supports_acl"):
            if not message.data.backend_supports_acl:
                logging.warning(
                    "%s was just allowed to perform actions in %s because the backend does not support ACL.  This can be a security risk." % (
                        message.sender.handle,
                        acl,
                    ) + "To fix this, set ACL groups in your config.py, or set DISABLE_ACL = True"
                )
                return True
    except:
        pass

    return False
