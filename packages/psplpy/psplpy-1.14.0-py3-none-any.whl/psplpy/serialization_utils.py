import functools
import io
import json
import lzma
import pickle
import yaml
import re
import zlib
from pathlib import Path
from types import ModuleType
from typing import Any, Callable


class Compressor:
    LZMA = 'lzma'
    ZLIB = 'zlib'

    def __init__(self, lib: str = ZLIB):
        self.lib = lib

    def compress(self, data: bytes, lib: str = '') -> bytes:
        lib = lib or self.lib
        compressed_data = globals()[lib].compress(data)
        return compressed_data

    def decompress(self, compressed_data: bytes, lib: str = '') -> bytes:
        lib = lib or self.lib
        data = globals()[lib].decompress(compressed_data)
        return data


def _check_int_or_float(input_str: str) -> type:
    int_pattern = r'^[-+]?\d+$'
    float_pattern = r'^[-+]?\d+(\.\d+)?$'

    if re.match(int_pattern, input_str):
        return int
    elif re.match(float_pattern, input_str):
        return float
    else:
        return str


def _convert_json_dict_key_to_number(data: Any) -> Any:
    if isinstance(data, dict):
        # if data type is dict, convert it
        converted_dict = {}
        for key, value in data.items():
            if type(key) == str:
                trans_type = _check_int_or_float(key)
                key = trans_type(key)
            # process the values in dict, using recursion
            value = _convert_json_dict_key_to_number(value)
            converted_dict[key] = value
        return converted_dict
    elif isinstance(data, (list, tuple, set)):
        # if date type is list, tuple or set, process it recursively
        converted_list = []
        for item in data:
            converted_item = _convert_json_dict_key_to_number(item)
            converted_list.append(converted_item)
        return type(data)(converted_list)
    else:
        # if it's other type, don't process
        return data


def _get_empty_data_structure(data_type: type | None) -> dict | list | tuple | set | None:
    if data_type is None:
        return None
    types = (dict, list, tuple, set)
    if data_type in types:
        return data_type()
    else:
        raise TypeError(f"Unsupported data type {data_type}")


def _get_data(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(self, data: str | bytes = None, *args, **kwargs) -> Any:
        if not data:
            if not self.path:
                raise AssertionError('For loading data, please provide the data or file path.')
            try:
                data = Path(self.path).read_bytes()
            except FileNotFoundError:  # when file not found
                return _get_empty_data_structure(self.data_type)
        return func(self, data, *args, **kwargs)
    return wrapper


def _dump(self: Any, data: bytes | str) -> bytes | str:
    if self.path:
        if isinstance(data, str):
            Path(self.path).write_text(data, encoding=self.encoding)
        else:
            Path(self.path).write_bytes(data)
    return data


class Serializer:
    def __init__(self, path: str | Path = None, encoding: str = 'utf-8', data_type: type = None):
        self.path, self.encoding, self.data_type = path, encoding, data_type

    @_get_data
    def _load(self, data: str | bytes, lib: ModuleType) -> Any:
        if lib in [json, yaml] and isinstance(data, bytes):
            data = data.decode(self.encoding)
        if lib is json:
            try:
                deserialized_data = json.loads(data)
            except json.decoder.JSONDecodeError:  # when data is empty
                return _get_empty_data_structure(self.data_type)
        elif lib is yaml:
            deserialized_data = yaml.safe_load(data)
        elif lib is pickle:
            try:
                deserialized_data = pickle.loads(data)
            except EOFError:  # when data is empty
                return _get_empty_data_structure(self.data_type)
        else:
            raise AssertionError
        return deserialized_data

    def load_yaml(self, data: str = None) -> Any:
        return self._load(data, yaml)

    def load_json(self, data: str = None, trans_key_to_num: bool = False) -> Any:
        json_data = self._load(data, json)
        if trans_key_to_num:
            return _convert_json_dict_key_to_number(json_data)
        return json_data

    def load_pickle(self, data: bytes = None) -> Any:
        return self._load(data, pickle)

    def dump_yaml(self, data: Any, allow_unicode: bool = True) -> str:
        string_io = io.StringIO()
        yaml.dump(data, string_io, allow_unicode=allow_unicode)
        data = string_io.getvalue()
        return _dump(self, data)

    def dump_json(self, data: Any, indent: int = 4, ensure_ascii: bool = False, minimum: bool = True) -> str:
        kwargs = {'ensure_ascii': ensure_ascii}
        if minimum:
            kwargs['separators'] = (',', ':')
        else:
            kwargs['indent'] = indent
        data = json.dumps(data, **kwargs)
        return _dump(self, data)

    def dump_pickle(self, data: Any) -> bytes:
        data = pickle.dumps(data)
        return _dump(self, data)


class CompressSerializer:
    _UNCOMPRESSED = b'0'
    _COMPRESSED = b'1'
    _ZLIB = b'0'
    _LZMA = b'1'
    AUTO = 'auto'

    def __init__(self, path: str | Path = None, encoding: str = 'utf-8', data_type: type = None,
                 compress: bool | str = AUTO, threshold: int = 1024 * 128, compress_lib: str = Compressor.ZLIB):
        """When the data length is greater than the threshold, will execute compression"""
        self.path, self.encoding, self.data_type = path, encoding, data_type
        self.compress, self.threshold, self.compress_lib = compress, threshold, compress_lib
        self._c = Compressor(lib=self.compress_lib)
        self._s = Serializer(encoding=self.encoding, data_type=self.data_type)

    def _get_compress_lib_and_meta_data(self, compress_lib: bytes | str) -> tuple[str, bytes]:
        zlib_tuple, lzma_tuple = (Compressor.ZLIB, self._ZLIB), (Compressor.LZMA, self._LZMA)
        if compress_lib in zlib_tuple:
            return zlib_tuple
        elif compress_lib in lzma_tuple:
            return lzma_tuple
        raise AssertionError

    def _get_uncompressed_data(self, data: bytes) -> bytes:
        compressed = chr(data[0]).encode('utf-8')
        compress_lib = chr(data[1]).encode('utf-8')
        data = data[2:]

        compressed = True if compressed == self._COMPRESSED else False
        compress_lib, _ = self._get_compress_lib_and_meta_data(compress_lib)
        if compressed:
            data = self._c.decompress(data, lib=compress_lib)
        return data

    @_get_data
    def load_pickle(self, data: bytes = None) -> Any:
        return self._s.load_pickle(self._get_uncompressed_data(data))

    @_get_data
    def load_json(self, data: bytes = None, trans_key_to_num: bool = False) -> Any:
        return self._s.load_json(self._get_uncompressed_data(data).decode(encoding=self.encoding), trans_key_to_num)

    @_get_data
    def load_yaml(self, data: bytes = None) -> Any:
        return self._s.load_yaml(self._get_uncompressed_data(data).decode(encoding=self.encoding))

    def _compress_or_not(self, data: bytes, compress: bool | None) -> bool:
        if compress is None:  # if None, depends on self.compress
            if self.compress == self.AUTO and len(data) > self.threshold:
                return True
            return bool(self.compress)
        return bool(compress)

    def _get_compressed_data(self, data: bytes, compress: bool | None) -> bytes:
        compress = self._compress_or_not(data, compress)
        _, meta_data = self._get_compress_lib_and_meta_data(self.compress_lib)

        if compress:
            data = self._c.compress(data)
            meta_data = self._COMPRESSED + meta_data
        else:
            meta_data = self._UNCOMPRESSED + meta_data
        return _dump(self, meta_data + data)

    def dump_pickle(self, data: Any, compress: bool | None = None) -> bytes:
        return self._get_compressed_data(self._s.dump_pickle(data), compress)

    def dump_json(self, data: Any, compress: bool | None = None,
                  indent: int = 4, ensure_ascii: bool = False, minimum: bool = True) -> bytes:
        data = self._s.dump_json(data, indent, ensure_ascii, minimum)
        return self._get_compressed_data(data.encode(encoding=self.encoding), compress)

    def dump_yaml(self, data: Any, compress: bool | None = None, allow_unicode: bool = True) -> bytes:
        data = self._s.dump_yaml(data, allow_unicode)
        return self._get_compressed_data(data.encode(encoding=self.encoding), compress)
