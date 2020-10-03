#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bluebottle.settings.local")

    from django import VERSION
    if VERSION >= (2, 0):
        import django_compat_patcher

        django_compat_patcher.patch()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
