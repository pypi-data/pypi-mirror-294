from .utils import file_size
from werkzeug.exceptions import BadRequest


class FileNotAllowedExtError(BadRequest):
    pass


class FileTooBigError(BadRequest):
    pass


def validate_file(file, allowed_exts=None, max_size=None, raise_exc=True):
    if allowed_exts:
        if not file.filename.split(".", 1)[1].lower() in allowed_exts:
            if not raise_exc:
                return False
            raise FileNotAllowedExtError()
        
    if max_size is not None:
        if file_size(file) > max_size:
            if not raise_exc:
                return False
            raise FileTooBigError()
        
    return True