import contextlib
import zlib

from lib.deca import config
from lib.deca.adf_profile import *
from lib.deca.ff_adf import Adf
from lib.deca.file import ArchiveFile


class FileNotFound(Exception):
    pass


class DecompressedAdfFile():
    def __init__(self, basename: str, filename: Path, file_header: bytearray, header: bytearray,
                 data: bytearray) -> None:
        self.basename = basename
        self.filename = filename
        self.file_header = file_header
        self.header = header
        self.data = data
        self.org_size = len(header + data)

    def save(self, destination: Path, verbose=False) -> None:
        decompressed_data_bytes = self.header + self.data
        new_size = len(decompressed_data_bytes)
        if self.org_size != new_size:
            print("Org:", self.org_size, "New:", new_size)
            decompressed_size = struct.pack("I", new_size)
            self.file_header[8:12] = decompressed_size
            self.file_header[24:28] = decompressed_size
        commpressed_data_bytes = self.file_header + _compress_bytes(decompressed_data_bytes)

        adf_file = destination / self.basename
        if verbose:
            print(f"Saving modded file to {adf_file}")
        _save_file(adf_file, commpressed_data_bytes, verbose=verbose)


class ParsedAdfFile():
    def __init__(self, decompressed: DecompressedAdfFile, adf: Adf) -> None:
        self.decompressed = decompressed
        self.adf = adf


def _get_file_name(reserve: str, mod: bool) -> Path:
    save_path = config.MOD_DIR_PATH if mod else config.get_save_path()
    if save_path is None:
        raise FileNotFound("Please configure your game save path")
    filename = save_path / config.get_population_file_name(reserve)
    if not filename.exists():
        raise FileNotFound(f'{filename} does not exist')
    return filename


def _read_file(filename: Path, verbose=False):
    if verbose:
        print(f"Reading {filename}")
    return filename.read_bytes()


def _decompress_bytes(data_bytes: bytearray) -> bytearray:
    decompress = zlib.decompressobj()
    decompressed = decompress.decompress(data_bytes)
    decompressed = decompressed + decompress.flush()
    return decompressed


def _compress_bytes(data_bytes: bytearray) -> bytearray:
    compress = zlib.compressobj()
    compressed = compress.compress(data_bytes)
    compressed = compressed + compress.flush()
    return compressed


def _save_file(filename: Path, data_bytes: bytearray, verbose=False):
    Path(filename.parent).mkdir(exist_ok=True)
    filename.write_bytes(data_bytes)
    if verbose:
        print(f"Saved {filename}")


def _decompress_adf_file(filename: Path, verbose=False) -> DecompressedAdfFile:
    # read entire adf file
    data_bytes = _read_file(filename, verbose)
    data_bytes = bytearray(data_bytes)

    # split out header
    header = data_bytes[0:32]
    data_bytes = data_bytes[32:]

    # decompress data
    decompressed_data_bytes = _decompress_bytes(data_bytes)
    decompressed_data_bytes = bytearray(decompressed_data_bytes)

    # split out compression header
    decompressed_header = decompressed_data_bytes[0:5]
    decompressed_data_bytes = decompressed_data_bytes[5:]

    # save uncompressed adf data to file
    parsed_basename = filename.name
    adf_file = config.APP_DIR_PATH / f".working/{parsed_basename}_sliced"
    _save_file(adf_file, decompressed_data_bytes, verbose)

    return DecompressedAdfFile(
        parsed_basename,
        adf_file,
        header,
        decompressed_header,
        decompressed_data_bytes
    )


def _parse_adf_file(filename: Path, suffix: str = None, verbose=False) -> Adf:
    obj = Adf()
    with ArchiveFile(open(filename, 'rb')) as f:
        with contextlib.redirect_stdout(None):
            obj.deserialize(f)
    content = obj.dump_to_string()
    suffix = f"_{suffix}.txt" if suffix else ".txt"
    txt_filename = config.APP_DIR_PATH / f".working/{filename.name}{suffix}"
    _save_file(txt_filename, bytearray(content, 'utf-8'), verbose)
    return obj


def _parse_adf(filename: Path, suffix: str = None, verbose=False) -> Adf:
    if verbose:
        print(f"Parsing {filename}")
    return _parse_adf_file(filename, suffix, verbose=verbose)


def load_adf(filename: Path, verbose=False) -> ParsedAdfFile:
    data = _decompress_adf_file(filename, verbose=verbose)
    adf = _parse_adf(data.filename, verbose=verbose)
    return ParsedAdfFile(data, adf)
