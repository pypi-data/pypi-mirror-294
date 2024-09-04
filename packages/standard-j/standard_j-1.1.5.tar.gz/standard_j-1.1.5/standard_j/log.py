from standard_j.utils import *
import typing
import datetime
import os


class LogStatusType(Enum):
    INFO: EnumItem
    SUCCESS: EnumItem
    WARNING: EnumItem
    ERROR: EnumItem


# <editor-fold desc="Private Variables">
__output_files: list[str | None] = []
__min_quit_status: LogStatusType = LogStatusType.ERROR
__time_format: str = "%m/%d/%Y %H:%M:%S:%f"
__tab_char: str = "\t"
__raw_format: str = "<status WARNING\t| mm/dd/YYYY HH:MM:SS:ffffff>\t"
__output_format: str = "<status {status}\t| {time}>\t"
__current_buffer: list[str] = []
# </editor-fold>


def get_min_quit_status():
    return __min_quit_status


def set_min_quit_status(new_status: LogStatusType):
    if type(new_status) != LogStatusType:
        raise StandardJError(f"Min quit status for the log must be of type <enum LogStatusType>; found: {new_status}")


def create_dir(path: str):
    """
    Recursively creates directories until the specified path can be created
    :param path: str Directory to create
    :return: None
    """
    parent = os.path.dirname(path)
    if parent != "" and not os.path.exists(parent):
        create_dir(parent)
    os.mkdir(path)


def create_log_file(folder: str, file: str, overwrite=False, append_output_file=True):
    """
    Method used to create a log file
    :param folder: str folder path
    :param file: str file name
    :param overwrite: Optional[bool] Only applicable if specified file already exists:
                      If True, overwrite the file. If False, raise error
    :param append_output_file: Optional[bool] If True, the file is appended to the output_files list
    :return: None
    :raises FileExistsError: If the specified file exists and overwrite is False
    """
    if not os.path.exists(folder):
        # If the folder does not yet exist, create it and any parent directories required to create it
        create_dir(folder)
    full_path = os.path.join(folder, file)
    if not overwrite:
        # If overwrite is False, attempt to create the file, if it already exists, a FileExistsError is raised
        open(full_path, "x").close()
    else:
        # If overwrite is True, delete the old file if it exists, then create the new one
        if os.path.exists(full_path):
            os.remove(full_path)
        open(full_path, "x").close()
    # If append_output_file is True, add the newly created file to the output_files list
    if append_output_file:
        __output_files.append(full_path)


def get_output_files() -> tuple[str, ...]:
    """
    A getter function for the current list of output files
    :return: tuple[str, ...] A tuple of output files that will be written to
    """
    return tuple(__output_files)


def reset_output_files() -> None:
    """
    A function that resets the current output files so that they can be reassigned
    """
    __output_files.clear()


def enable_console_output() -> None:
    """
    A function that enables console output when other files have been added to the output_files
    """
    if None not in __output_files:
        __output_files.append(None)


def disable_console_output() -> None:
    """
    A function that disables console output when other files have been added to the output_files
    NOTE: if no other output files are specified, this is ignored as the console is the default output stream
    """
    if None in __output_files:
        __output_files.remove(None)


def put(*values: object, sep: str = " ", status: LogStatusType = LogStatusType.INFO,
        files: typing.Iterable[str | None] = None) -> None:
    """
    A function used to put values to the current log files, or a specified list of files
    :param values: *object Objects to put to the log
    :param sep: Optional[str] Seperator used between each value when putting to the files
    :param status: Optional[LogStatusType] Status of the current log (See LogStatusType for details)
    :param files: Optional[str] A list of files to output to instead of the current output files. A value of None
                  Results in using the current output files
    :return: None
    :raises StandardJError: If the min_quit_status is reached
    """
    current_time = datetime.datetime.now().strftime(__time_format)
    for f in files if files is not None else __output_files if len(__output_files) > 0 else (None,):
        if isinstance(f, str):
            f = open(f, "a")
        print(__output_format.format(status=status.name, time=current_time), f"{sep.join(str(val) for val in values)}",
              sep="", file=f, flush=True)
        if f is not None:
            f.close()
    if __min_quit_status is not None and int(__min_quit_status) <= int(status):
        flush()
        raise StandardJError("<standard_j.log> min quit status reached.  See output file(s) for details")


def buffer(*values, sep: str = " ") -> None:
    """
    A function used to buffer outputs to the log.  These outputs will be put when the flush function is called, or
    when the min quit status is reached
    :param values: *object Objects to buffer for the log
    :param sep: Optional[str] Seperator used between each value when buffering for the log
    :return: None
    """
    __current_buffer.append(sep.join(str(val) for val in values))


def clear() -> None:
    """
    A function used to clear the current buffer
    :return: None
    """
    __current_buffer.clear()


def flush(end: str = "", sep: str = f"\n{''.join(' ' if c != __tab_char else c for c in __raw_format)}",
          status: LogStatusType = LogStatusType.INFO, files: typing.Iterable[str | None] = None) -> None:
    """
    A function used to flush the current buffer to the output files, or specified "files"
    :param end: Optional[str] String to be appended onto the last msg in the buffer
    :param sep: Optional[str] String to be used between each msg in the buffer
    :param status: Optional[LogStatusType] Status of the current log (See LogStatusType for details)
    :param files: Optional[list[str, None]] Files to output to instead of the current output files
    :return: None
    """
    if len(__current_buffer) == 0:
        return
    __current_buffer[-1] += end
    buf = tuple(__current_buffer)
    clear()
    put(*buf, sep=sep, status=status, files=files)
