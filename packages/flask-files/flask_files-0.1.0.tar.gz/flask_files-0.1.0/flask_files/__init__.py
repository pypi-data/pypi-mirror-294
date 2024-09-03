from dataclasses import dataclass
from typing import Optional, Any
from flask import url_for, send_from_directory, current_app
from werkzeug.utils import cached_property
import fsspec
import os
import mimetypes
import urllib.parse

from .utils import generate_filename, file_size, save_uploaded_file_temporarly, format_file_size
from .form import validate_file, FileTooBigError, FileNotAllowedExtError


@dataclass
class FilesState:
    upload_dir: str
    uuid_prefix: bool
    keep_filename: bool
    subfolders: bool
    uuid_prefix_path_separator: bool
    instance: "Files"
    default_filesystem: str
    upload_url: Optional[str] = None


class Files:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app, default_filesystem=None, upload_dir="uploads", upload_url="/uploads", uuid_prefix=True, keep_filename=True,
                 subfolders=False, uuid_prefix_path_separator=False):
        
        self.app = app
        self.state = state = FilesState(
            upload_dir=app.config.get("FILES_UPLOAD_DIR", upload_dir),
            upload_url=app.config.get("FILES_UPLOAD_URL", upload_url),
            default_filesystem=app.config.get("FILES_DEFAULT_FILESYSTEM", default_filesystem),
            uuid_prefix=app.config.get("FILES_UUID_PREFIXES", uuid_prefix),
            keep_filename=app.config.get("FILES_KEEP_FILENAME", keep_filename),
            subfolders=app.config.get("FILES_SUBFOLDERS", subfolders),
            uuid_prefix_path_separator=app.config.get("FILES_UUID_PREFIX_PATH_SEPARATOR", uuid_prefix_path_separator),
            instance=self
        )

        app.extensions["files"] = state
        app.jinja_env.globals["url_for_upload"] = url_for_upload

        if state.upload_dir:
            if not os.path.isabs(state.upload_dir):
                state.upload_dir = os.path.join(app.root_path, state.upload_dir)
            #os.makedirs(state.upload_dir, exist_ok=True)
            self.local_fs = fsspec.filesystem("dir", path=state.upload_dir, fs=fsspec.filesystem("local", auto_mkdir=True))

            if state.upload_url:
                def send_uploaded_file(filename):
                    return send_from_directory(state.upload_dir, filename)
                app.add_url_rule(f"{state.upload_url}/<path:filename>",
                                endpoint="static_upload",
                                view_func=send_uploaded_file)
            
    def filesystem(self, protocol=None):
        if not protocol:
            protocol = self.state.default_filesystem
        if not protocol:
            return self.local_fs
        return fsspec.filesystem(protocol)


def save_file(file, name=None, protocol=None, uuid_prefix=None):
    config = current_app.extensions["files"]
    filesystem = config.instance.filesystem(protocol)
    if uuid_prefix is None:
        uuid_prefix = config.uuid_prefix
        
    path = generate_filename(file.filename, uuid_prefix=uuid_prefix, keep_filename=config.keep_filename,
                                    uuid_prefix_path_separator=config.uuid_prefix_path_separator,
                                    subfolders=config.subfolders)
    
    with filesystem.open(path, "wb") as f:
        file.save(f)

    return File(path, protocol or config.default_filesystem, name or file.filename, file.mimetype, file_size(file))


def url_for_upload(file):
    state = current_app.extensions["files"]
    if isinstance(file, str):
        file = File.from_uri(file)
    if file.protocol:
        fs = state.instance.filesystem(file.protocol)
        if hasattr(fs, "url"):
            return fs.url(file.path)
    if state.upload_url:
        return url_for("static_upload", filename=file.path)
    return file.uri


class File:
    @classmethod
    def split_uri(cls, uri):
        state = current_app.extensions["files"]
        if "://" in uri:
            protocol, path = uri.split("://", 1)
        else:
            protocol = state.default_filesystem
            path = uri
        return protocol, path
    
    @classmethod
    def from_uri(cls, uri):
        protocol, path = cls.split_uri(uri)
        filename = None
        if "#" in path:
            path, filename = path.rsplit("#", 1)
        params = {}
        if "?" in path:
            path, qs = path.split("?", 1)
            params = urllib.parse.parse_qs(qs)
        return cls(path, protocol, filename, params.get("mimetype"), params.get("size"))
    
    @classmethod
    def from_json(cls, data):
        protocol, path = cls.split_uri(data["uri"])
        return cls(path, protocol, data.get("filename"), data.get("mimetype"), data.get("size"))

    def __init__(self, path, protocol=None, filename=None, mimetype=None, size=None):
        state = current_app.extensions["files"]
        if not filename:
            filename = os.path.basename(path)
            if not state.uuid_prefix_path_separator and state.uuid_prefix and state.keep_filename:
                filename = filename[36:]
        self.protocol = protocol
        self.path = path
        self.filename = filename
        self._mimetype = mimetype
        self._size = size

    @cached_property
    def filesystem(self):
        return current_app.extensions["files"].instance.filesystem(self.protocol)
    
    @cached_property
    def mimetype(self):
        if self._mimetype is None:
            return mimetypes.guess_type(self.filename)[0]
        return self._mimetype

    @cached_property
    def size(self):
        if self._size is None:
            return self.filesystem.du(self.path)
        return self._size
    
    @property
    def uuid(self):
        state = current_app.extensions["files"]
        if not state.uuid_prefix:
            return
        if state.uuid_prefix_path_separator:
            return os.path.basename(os.path.dirname(self.path))
        return os.path.basename(self.path)[:36]
    
    @property
    def uri(self):
        return f"{self.protocol}://{self.path}" if self.protocol else self.path
    
    def open(self, mode="rb"):
        return self.filesystem.open(self.path, mode)
    
    def save(self, fp):
        with self.open() as f:
            fp.write(f.read())
    
    def to_json(self, read_size=False):
        o = {
            "filename": self.filename,
            "uri": self.uri,
            "mimetype": self.mimetype
        }
        if self._size is not None:
            o["size"] = self._size
        elif read_size:
            o["size"] = self.size
        return o
    
    def full_uri(self, read_size=False):
        params = self.to_json(read_size)
        uri = params.pop("uri")
        qs = urllib.parse.urlencode({k: v for k, v in params.items() if v})
        if qs:
            uri += f"?{qs}"
        return f"{uri}#{params['filename']}"
    
    def __str__(self):
        return self.uri