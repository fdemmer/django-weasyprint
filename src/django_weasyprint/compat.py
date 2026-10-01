"""
Backports of Django functionality missing in the oldest supported Django versions.

Copied verbatim from Django 6.1.1 (BSD-3-Clause, Copyright Django Software Foundation).
Excluded from the quote and pyupgrade pre-commit hooks to keep them unmodified.
"""
import re
from urllib.parse import quote


try:
    from django.utils.http import content_disposition_header
except ImportError:  # Django < 4.2
    def content_disposition_header(as_attachment, filename):
        """
        Construct a Content-Disposition HTTP header value from the given filename
        as specified by RFC 6266.
        """
        if filename:
            disposition = "attachment" if as_attachment else "inline"
            try:
                filename.encode("ascii")
                is_ascii = True
            except UnicodeEncodeError:
                is_ascii = False
            # Quoted strings can contain horizontal tabs, space characters, and
            # characters from 0x21 to 0x7e, except 0x22 (`"`) and 0x5C (`\`) which
            # can still be expressed but must be escaped with their own `\`.
            # https://datatracker.ietf.org/doc/html/rfc9110#name-quoted-strings
            quotable_characters = r"^[\t \x21-\x7e]*$"
            if is_ascii and re.match(quotable_characters, filename):
                file_expr = 'filename="{}"'.format(
                    filename.replace("\\", "\\\\").replace('"', r"\"")
                )
            else:
                file_expr = "filename*=utf-8''{}".format(quote(filename))  # noqa: UP032
            return f"{disposition}; {file_expr}"
        elif as_attachment:
            return "attachment"
        else:
            return None
