from werkzeug.utils import secure_filename as wz_secure_filename
from flask import current_app
from tempfile import NamedTemporaryFile, gettempdir
import os
import uuid


def generate_filename(filename, uuid_prefix=False, uuid_prefix_path_separator=False, keep_filename=True,
                      subfolders=False, secure_filename=True, protocol=None):
    if uuid_prefix is True:
        uuid_prefix = str(uuid.uuid4())
    if uuid_prefix and not keep_filename:
        _, ext = os.path.splitext(filename)
        filename = str(uuid_prefix) + ext
    else:
        if secure_filename:
            filename = wz_secure_filename(filename)
        if uuid_prefix:
            filename = str(uuid_prefix) + ("/" if uuid_prefix_path_separator else "-") + filename

    if subfolders:
        if uuid_prefix:
            parts = filename.split("-", 4)
            filename = os.path.join(os.path.join(*parts[:4]), filename)
        else:
            filename = os.path.join(os.path.join(*filename[:4]), filename)

    if protocol:
        filename = f"{protocol}://{filename}"

    return filename


def save_uploaded_file_temporarly(file, filename=None, tmp_dir=None):
    if not tmp_dir:
        tmp_dir = current_app.config.get('FILES_UPLOAD_TMP_DIR')
    if filename:
        tmpfilename = os.path.join(tmp_dir or gettempdir(), wz_secure_filename(filename))
    else:
        _, ext = os.path.splitext(file.filename)
        tmp = NamedTemporaryFile(delete=False, suffix=ext, dir=tmp_dir)
        tmp.close()
        tmpfilename = tmp.name
    file.save(tmpfilename)
    return tmpfilename


def file_size(file):
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size


def format_file_size(size, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(size) < 1024.0:
            return "%3.1f%s%s" % (size, unit, suffix)
        size /= 1024.0
    return "%.1f%s%s" % (size, 'Y', suffix)
