import json
from pathlib import PurePosixPath, PurePath
import re
import warnings
from os import PathLike
from typing import Callable, Any

import dapla as dp
import geopandas as gpd
import numpy as np
import pandas as pd
import pandas.io.formats.format as fmt
from pandas.api.types import is_dict_like
import pyarrow
import sgis as sg


# regex with the prefix _v followed by an integer (decimals) of any length
VERSION_PATTERN = r"_v(\d+)"
VERSION_PREFIX = "_v"

# regex with the prefix _p followed by four integers (year) and OPTIONALLY month and date, separated by '-'
# Note: will also match with more than 4 digits in a row, so we should catch that with an error message beforehand
PERIOD_PATTERN = r"_p(\d{4}(?:-\d{2}(?:-\d{2})?)?)"
PERIOD_PATTERN = r"_p(\d{4}(?:-\d{2}(?:-\d{2})?)?|Q[1-4])"

PERIOD_PREFIX = "_p"

PRE_TEAMNAME = "ssb-prod-"
GS_URI_PREFIX = "gs://"


class Tree:
    """Stores text to be printed/displayed in directory tree format.

    If displayed in Jupyter, paths will be copyable.
    """

    def __init__(self):
        self.repr = ()
        self.repr_html = ()

    def add(self, text: str):
        self.repr += (text,)

    def add_html(self, text: str):
        self.repr_html += (text,)

    def __repr__(self):
        return "\n".join(self.repr)

    def __str__(self):
        return "\n".join(self.repr)

    def _repr_html_(self):
        return "\n".join(self.repr_html)


def _pathseries_constructor_with_fallback(data=None, index=None, **kwargs):
    series = pd.Series(data, index, **kwargs)
    if not len(series):
        return PathSeries(
            series, name="path", index=pd.MultiIndex.from_arrays([[], []])
        )
    try:
        nparts = series.str.split("/").str.len()
        if nparts.max() == 1:
            return series
    except Exception:
        return series

    return PathSeries(series, name="path")


def _dataframe_constructor(data=None, index=None, **kwargs):
    data.name = "path"
    return pd.DataFrame(data, index=index, **kwargs)


class PathSeries(pd.Series):
    """A pandas Series for working with GCS (Google Cloud Storage) paths.

    A PathSeries should not be created directly, but by using methods of the
    Path class, chiefly the ls method. This will ensure that the values of the
    Series are Path objects, and that the index is a MultiIndex where
    the 0th level holds the timestamp of the files, and the
    1st level holds the file sizes in megabytes.

    The class share some of the properties and methods of the Path class.
    The Path method/attribute is applied to each row of the PathSeries.

    Parameters
    ----------
    data: An iterable of Path objects.

    Properties
    ----------
    version_number: Series
        The version number of the files.
    versionless: PathSeries
        The versionless paths.
    versionless_stem: PathSeries
        The versionless stems of the files.
    parent: PathSeries
        The parent directories of the files.
    files: PathSeries
        Select only the files in the Series.
    dirs: PathSeries
        Select only the directories in the Series.
    base: Path
        The common path amongst all paths in the Series.
    timestamp: pd.Index
        The timestamp of the files.
    mb: pd.Index
        The file size in megabytes.
    gb: pd.Index
        The file size in gigabytes.
    kb: pd.Index
        The file size in kilobytes.
    stem: Series
        The stem of the file paths.
    names: Series
        The names of the file paths.

    Methods
    -------
    keep_highest_numbered_versions():
        Keep only the highest-numbered versions of the files.
    keep_latest_versions(include_versionless=True):
        Keep only the latest versions of the files.
    ls_dirs(recursive=False):
        List the contents of the subdirectories.
    containing(pat, *args, **kwargs):
        Convenience method for selecting paths containing a string.
    within_minutes(minutes):
        Select files with a timestamp within the given number of minutes.
    within_hours(hours):
        Select files with a timestamp within the given number of hours.
    within_days(days):
        Select files with a timestamp within the given number of days.
    is_file():
        Check if each path in the series corresponds to a file.
    is_dir():
        Check if each path in the series corresponds to a directory.
    """

    _version_pattern = VERSION_PATTERN
    _version_prefix = VERSION_PREFIX
    _metadata = [
        "_version_pattern",
        "_max_rows",
        "_max_colwidth",
        "_defined_name",
        "name",
    ]

    def __init__(
        self,
        data: list[str] | None = None,
        index=None,
        max_rows: int | None = 10,
        max_colwidth: int = 75,
        **kwargs,
    ):
        super().__init__(data, index=index, **kwargs)

        self._max_rows = max_rows
        self._max_colwidth = max_colwidth
        pd.set_option("display.max_colwidth", max_colwidth)

    @property
    def files(self):
        """Select only the files in the Series."""
        return self.loc[self.is_file()]

    @property
    def dirs(self):
        """Select only the directories in the Series."""
        return self.loc[self.is_dir()]

    def tree(
        self,
        max_rows: int | None = 3,
        ascending: bool = True,
        indent: int = 4,
    ) -> Tree:
        return get_path_tree(
            self,
            self.base,
            max_rows=max_rows,
            ascending=ascending,
            indent=indent,
        )

    def ls_dirs(self, recursive: bool = False) -> list:
        """List the contents of the subdirectories.

        Args:
            recursive: Whether to search through directories in subfolders until there
                are no more directories.

        Returns:
            A list of PathSeries, where each holds the contents of a directory.
        """
        return [path.ls(recursive=recursive) for path in self.dirs]

    def containing(self, pat: str, *args, **kwargs):
        """Convenience method for selecting paths containing string."""
        return self.loc[lambda x: x.str.contains(pat, *args, **kwargs)]

    def within_minutes(self, minutes: int):
        """Select files with a timestamp within the given number of minutes."""
        time_then = pd.Timestamp.now() - pd.Timedelta(minutes=minutes)
        return self.files.loc[lambda x: x.timestamp > time_then]

    def within_hours(self, hours: int):
        """Select files with a timestamp within the given number of hours."""
        time_then = pd.Timestamp.now() - pd.Timedelta(hours=hours)
        return self.files.loc[lambda x: x.timestamp > time_then]

    def within_days(self, days: int):
        """Select files with a timestamp within the given number of days."""
        time_then = pd.Timestamp.now() - pd.Timedelta(days=days)
        return self.files.loc[lambda x: x.timestamp > time_then]

    def not_within_minutes(self, minutes: int):
        """Select files with a timestamp within the given number of minutes."""
        time_then = pd.Timestamp.now() - pd.Timedelta(minutes=minutes)
        return self.files.loc[lambda x: x.timestamp < time_then]

    def not_within_hours(self, hours: int):
        """Select files with a timestamp within the given number of hours."""
        time_then = pd.Timestamp.now() - pd.Timedelta(hours=hours)
        return self.files.loc[lambda x: x.timestamp < time_then]

    def not_within_days(self, days: int):
        """Select files with a timestamp within the given number of days."""
        time_then = pd.Timestamp.now() - pd.Timedelta(days=days)
        return self.files.loc[lambda x: x.timestamp < time_then]

    @property
    def stem(self) -> pd.Series:
        return self.apply(lambda x: x.stem)

    @property
    def parts(self) -> pd.DataFrame:
        parts = self.apply(lambda x: x.parts)
        indexlist = [self.index.get_level_values(i) for i in range(self.index.nlevels)]
        parts.index = pd.MultiIndex.from_arrays(indexlist + [list(range(len(self)))])
        parts.explode()
        return pd.DataFrame(np.array(parts.to_list()))

    @property
    def names(self) -> pd.Series:
        return self.apply(lambda x: x.name)

    @property
    def periods(self) -> pd.Series:
        return self.apply(lambda x: x.periods)

    @property
    def version_number(self) -> pd.Series:
        return self.apply(lambda x: x.version_number)

    @property
    def versionless(self):
        return self.apply(lambda x: x.versionless)

    @property
    def versionless_stem(self):
        return self.apply(lambda x: x.versionless_stem)

    @property
    def periodless_stem(self):
        return self.apply(lambda x: x.periodless_stem)

    @property
    def parent(self):
        return self.apply(lambda x: x.parent)

    def keep_highest_numbered_versions(self):
        """Strips all version numbers (and '_v') off the file paths in the folder and keeps only the highest.

        Does a regex search for the pattern '_v' followed by any integer.

        """
        self = self.sort_values()
        return self._drop_version_number_and_keep_last()

    def keep_latest_versions(self, include_versionless: bool = True):
        """Strips all version numbers (and '_v') off the file paths in the folder and keeps only the newest.

        Does a regex search for the pattern '_v' followed by any integer.

        """
        self = self.sort_index(level=0)
        return self._drop_version_number_and_keep_last(include_versionless)

    def is_file(self) -> pd.Series:
        return self.kb > 0

    def is_dir(self) -> pd.Series:
        return self.kb == 0

    def dir_sizes(self, part_index: int, unit: str = "gb") -> pd.Series:
        def join_parts_if_enough_parts(path):
            parts = path.parts
            try:
                path = "/".join(parts[i] for i in range(part_index + 1))
            except IndexError:
                return
            if "." in path:
                return None
            return path

        sizes = getattr(self, unit.lower())
        paths = [join_parts_if_enough_parts(path) for path in self]
        return pd.Series(list(sizes), index=paths).groupby(level=0).sum().sort_values()

    @property
    def timestamp(self) -> pd.Index:
        try:
            return self.index.get_level_values(0)
        except IndexError:
            assert not len(self)
            return self.index

    @property
    def kb(self) -> pd.Index:
        try:
            return self.mb * 1000
        except IndexError:
            assert not len(self)
            return self.index

    @property
    def mb(self) -> pd.Index:
        try:
            return self.index.get_level_values(1)
        except IndexError:
            assert not len(self)
            return self.index

    @property
    def gb(self) -> pd.Index:
        try:
            return self.mb / 1000
        except IndexError:
            assert not len(self)
            return self.index

    @property
    def tb(self) -> pd.Index:
        try:
            return self.mb / 1_000_000
        except IndexError:
            assert not len(self)
            return self.index

    @property
    def nrows(self) -> pd.Index:
        return self.apply(lambda x: x.shape[0])

    @property
    def ncols(self) -> pd.Index:
        return self.apply(lambda x: x.shape[1])

    def _drop_version_number_and_keep_last(
        self, include_versionless: bool | None = None
    ):
        # using the range index with iloc in the end
        stems = self.stem.reset_index(drop=True)

        if include_versionless is False:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                stems = stems.loc[stems.str.contains(self._version_pattern)]

        without_version_number = stems.str.replace(
            self._version_pattern, "", regex=True
        )

        only_newest = without_version_number.loc[lambda x: ~x.duplicated(keep="last")]

        return self.iloc[only_newest.index]

    @property
    def _constructor(self):
        return _pathseries_constructor_with_fallback

    @property
    def _constructor_expanddim(self):
        return _dataframe_constructor

    @property
    def base(self):
        """The common path amongst all paths in the Series."""
        if len(self) <= 1:
            return Path("")

        splitted_path: list[str] = self.iloc[0].split("/")

        common_parts = []
        for folder in splitted_path:
            if self.str.contains(folder).all():
                common_parts.append(folder)
            else:
                break

        return Path("/".join(common_parts))

    def __str__(self):
        repr_params = fmt.get_series_repr_params()
        repr_params["max_rows"] = self._max_rows

        max_len = max(len(x) for x in self) if len(self) else 0

        if self.base and max_len > self._max_colwidth:
            s = pd.Series(self).str.replace(self.base, "...")
        else:
            s = pd.Series(self)

        if len(s):
            s.index = pd.MultiIndex.from_arrays(
                [s.index.get_level_values(0), s.index.get_level_values(1).astype(int)],
                names=["timestamp", "mb (int)"],
            )

        return s.to_string(**repr_params)

    def __repr__(self):
        return self.__str__()

    def _repr_html_(self):
        df = pd.DataFrame({"path": self})

        if not len(df):
            return df._repr_html_()

        df.index = pd.MultiIndex.from_arrays(
            [
                self.index.get_level_values(0),
                self.index.get_level_values(1).astype(int),
            ],
            names=["timestamp", "mb (int)"],
        )

        if len(df) <= self._max_rows:
            return df.style.format(
                {"path": split_path_and_make_copyable_html}
            ).to_html()

        # the Styler puts the elipsis row last. I want it in the middle. Doing it manually...
        first_rows = df.head(self._max_rows // 2).style.format(
            {"path": split_path_and_make_copyable_html}
        )
        last_rows = (
            df.tail(self._max_rows // 2)
            .style.format({"path": split_path_and_make_copyable_html})
            .set_table_styles([{"selector": "thead", "props": "display: none;"}])
        )

        elipsis_values = "..."

        elipsis_row = df.iloc[[0]]
        elipsis_row.index = pd.MultiIndex.from_arrays(
            [[elipsis_values], [elipsis_values]], names=elipsis_row.index.names
        )

        elipsis_row.iloc[[0]] = [
            f"[{len(df) - self._max_rows // 2 * 2} more rows]"
        ] * len(elipsis_row.columns)
        elipsis_row = elipsis_row.style

        return first_rows.concat(elipsis_row).concat(last_rows).to_html()


def split_path_and_make_copyable_html(
    path: str, split: str | None = "/", display_prefix: str | None = ".../"
) -> str:
    """Get html text that displays the last part, but makes the full path copyable to clipboard.

    Splits the path on a delimiter and creates an html string that displays only the
    last part, but adds a hyperlink which copies the full path to clipboard when clicked.

    Parameters
    ----------
    path: File or directory path
    split: Text pattern to split the path on. Defaults to "/".
    display_prefix: The text to display instead of the parent directory. Defaults to ".../"

    Returns
    -------
    A string that holds the HTML and JavaScript code to be passed to IPython.display.display.
    """

    copy_to_clipboard_js = f"""<script>
function copyToClipboard(text) {{
    navigator.clipboard.writeText(text)
        .then(() => {{
            const alertBox = document.createElement('div');
            const selection = window.getSelection();

            alertBox.style.position = 'fixed';
            alertBox.style.top = (selection.getRangeAt(0).getBoundingClientRect().top + window.scrollY) + 'px';
            alertBox.style.left = (selection.getRangeAt(0).getBoundingClientRect().left + window.scrollX) + 'px';
            alertBox.style.backgroundColor = '#f2f2f2';
            alertBox.style.border = '1px solid #ccc';
            alertBox.style.padding = '10px';
            alertBox.innerHTML = 'Copied to clipboard';
            document.body.appendChild(alertBox);

            setTimeout(function() {{
                alertBox.style.display = 'none';
            }}, 1500);  // 1.5 seconds
        }})
        .catch(err => {{
            console.error('Could not copy text: ', err);
        }});
}}
</script>"""

    if split is not None:
        name = path.split(split)[-1]
        displayed_text = f"{display_prefix}{name}" if display_prefix else name
    else:
        displayed_text = path

    return f'{copy_to_clipboard_js}<a href="{displayed_text}" title="{path}" onclick="copyToClipboard(\'{path}\')">{displayed_text}</a>'


def as_str(obj) -> str:
    if isinstance(obj, str):
        return obj
    if hasattr(obj, "__fspath__"):
        return obj.__fspath__()
    if hasattr(obj, "_str"):
        try:
            return str(obj._str())
        except TypeError:
            return str(obj._str)
    raise TypeError(type(obj))


class Path(str):
    """Path object that works like a string, with methods for working with the GCS file system.

    The class contains:
        - Relevant properties and methods of the pathlib.Path class,
            like parent, stem and open().
        - Methods mimicking the Linux terminal, like ls, cp, mv.
        - Methods for working with versioning of files, like getting the
            latest or highest numbered version or creating a new version.
        - The pandas.DataFrame attributes 'columns', 'shape' and 'dtypes'.
        - Methods for reading and writing from and to pandas

    Parameters
    ----------
    gcs_path: string or path-like object.

    Properties
    ----------
    Pandas properties:
        dtypes: pd.Series
            Get the data types of the file.
        columns: pd.Index
            Get the columns of the file.
        shape: tuple[int, int]
            Get the shape of the file.

    Versions and periods:
        version_number: int | None
            Get the version number from the path, if any.
        periods: List[str]
            Get a list of periods in the path.
        periodless_stem: str
            Get the stem of the path before the periods.
        versionless_stem: str
            Get the stem of the path before the version number.
        versionless: Path
            Get the full path with no version number.

    Pathlib properties:
        parent: Path
            Get the parent directory of the path.
        root: Path
            Get the root of the path.
        name: str
            The final path component, if any.
        stem: str
            The name of the Path without the suffix.
        parts: tuple[str]
            Get the parts of the path as a list.
        suffix: str
            Get the suffix of the path, meaning the file extension.
        suffixes: list[str]
            Get the suffixes of the path.

    Methods
    -------
    Versions and periods:
        versions: PathSeries
            Returns a PathSeries of all current versions of the file.
        new_version(timeout: int | None = 30):  Path
            Return the Path with the highest existing version number + 1.
        highest_numbered_version: Path
            Get the highest number version of the file path.
        latest_version(include_versionless: bool = True):  Path
            Get the newest version of the file path.
        with_version(version: int)
            Replace the current version number, or adds a version number if missing.
        with_periods(*p: str)
            Replace the current period(s), or add period(s) if missing.
        add_to_version_number(number: int)
            Add a number to the version number.

    File system:
        ls(recursive: bool = False): PathSeries
            List the contents of a GCS bucket path.
        dirs(recursive: bool = False): PathSeries
            List all child directories.
        files(recursive: bool = False): PathSeries
            List all files in the directory.
        open:
            Open the file.
        exists: bool
            Check if the file exists.
        mv(new_path: str): Path
            Move the file to a new path.
        cp(new_path: str): Path
            Copy the file to a new path.
        rm_file:
            Delete the file.
        is_dir: bool
            Check if the path is a directory.
        is_file: bool
            Check if the path is a file.

    Pathlib methods:
        with_suffix(suffix: str): Path
            Change the last suffix of the path.
        with_name(name: str): Path
            Change the name of the path.
        with_stem(stem: str): Path
            Change the stem to the path.

    IO:
        read_pandas(columns: List[str] | dict[str, str] | None = None, **kwargs): pd.DataFrame
            Read the file as a pandas DataFrame.
        read_geopandas(columns: List[str] | dict[str, str] | None = None, **kwargs): gpd.GeoDataFrame
            Read the file as a GeoDataFrame.
        read(func, columns: List[str] | dict[str, str] | None = None, **kwargs): Any
            Read the file using the given function.
        write_new_version(df: pd.DataFrame, check_if_equal: bool = False, timeout: int | None = 30): None
            Write a new version of the file with incremented version number.
        write_versionless(df: pd.DataFrame): None
            Write the DataFrame to the versionless path.
    """

    _version_pattern = VERSION_PATTERN
    _version_prefix = VERSION_PREFIX
    _period_pattern = PERIOD_PATTERN
    _period_prefix = PERIOD_PREFIX

    def __new__(cls, gcs_path: str | PurePath | None = None):
        gcs_path = cls._fix_path(gcs_path or "")
        obj = super().__new__(cls, gcs_path)
        obj._path = PurePosixPath(gcs_path)
        obj._fs = None
        return obj

    @staticmethod
    def _fix_path(path: str | PurePosixPath) -> str:
        return (
            str(path)
            .replace("\\", "/")
            .replace(r"\"", "/")
            .replace("//", "/")
            .rstrip("/")
        )

    def __getattribute__(self, name):
        """stackoverflow hack to ensure we return Path when using string methods.

        It works for all but the string magigmethods, importantly __add__.
        """
        if name not in dir(str):
            # because 'name' is not a string method
            return super().__getattribute__(name)

        def method(self, *args, **kwargs):
            value = getattr(super(), name)(*args, **kwargs)
            # not every string method returns a str:
            if isinstance(value, str):
                return type(self)(value)
            elif isinstance(value, list):
                return [type(self)(i) for i in value]
            elif isinstance(value, tuple):
                return tuple(type(self)(i) for i in value)
            else:  # dict, bool, or int
                return value

        return method.__get__(self)  # bound method

    def tree(
        self,
        max_rows: int | None = 3,
        ascending: bool = True,
        indent: int = 4,
    ) -> Tree:
        files: PathSeries = self.ls(recursive=True).files.sort_values()
        return get_path_tree(
            files,
            self,
            max_rows=max_rows,
            ascending=ascending,
            indent=indent,
        )

    def glob(self, pattern: str, *args, **kwargs) -> PathSeries:
        kwargs.pop("detail", None)
        info: list[dict] | dict = self.file_system.glob(
            self / pattern, detail=True, *args, **kwargs
        )
        if isinstance(info, dict):
            info = [info]

        formated_list = [
            {key.lower(): val for key, val in inner_filedict.items()}
            for filedict in info
            for inner_filedict in filedict.values()
        ]

        return self._get_files_and_dirs(formated_list)

    def ls(self, recursive: bool = False) -> PathSeries:
        """Lists the contents of a GCS bucket path.

        Returns a PathSeries with paths as values and timestamps
        and file size as index.
        """
        if recursive:
            return self.glob("**")

        info: list[dict] = self.file_system.ls(self, detail=True)
        return self._get_files_and_dirs(info)

    # def dirs(self, recursive: bool = False) -> PathSeries:
    #     """Lists all child directories."""
    #     if not recursive:
    #         info: list[dict] = self.file_system.ls(self, detail=True)
    #         return PathSeries(
    #             self._get_directory_series(info).apply(Path).sort_index(level=0)
    #         )

    #     return self.ls(recursive=recursive).dirs

    # def files(self, recursive: bool = False) -> PathSeries:
    #     """Lists all files in the directory."""
    #     if not recursive:
    #         info: list[dict] = self.file_system.ls(self, detail=True)
    #         return PathSeries(
    #             self._get_file_series(info).apply(Path).sort_index(level=0)
    #         )

    #     return self.ls(recursive=recursive).files

    def versions(self) -> PathSeries:
        """Returns a PathSeries of all versions of the file."""
        files_in_folder = self.parent.ls().files
        return files_in_folder.loc[lambda x: x.str.contains(self.versionless_stem)]

    def new_version(self, timeout: int | None = 30):
        """Return the Path with the highest existing version number + 1.

        The method will raise an Exception if the latest version is saved
        before the timeout period is out, to avoid saving new
        versions unpurposely.

        Parameters
        ----------
        timeout:
            Minutes needed between the timestamp of the current highest
            numbered version.

        Returns
        ------
        A Path with a new version number.

        Raises
        ------
        ValueError:
            If the method is run before the timeout period is up.
        """
        try:
            highest_numbered: Path = self.highest_numbered_version()
        except FileNotFoundError:
            return self.with_version(1)

        if timeout:
            timestamp: pd.Index = highest_numbered.ls().timestamp
            assert len(timestamp) == 1

            time_should_be_at_least = pd.Timestamp.now() - pd.Timedelta(minutes=timeout)
            if timestamp[0] > time_should_be_at_least:
                raise ValueError(
                    f"Latest version of the file was updated {timestamp[0]}, which "
                    f"is less than the timeout period of {timeout} minutes. "
                    "Change the timeout argument, but be sure to not save new "
                    "versions in a loop."
                )

        return highest_numbered.add_to_version_number(1)

    def latest_version(self, include_versionless: bool = True):
        """Get the newest version of the file path.

        Lists files in the parent directory with the same versionless stem
        and selects the one with the latest timestamp (updated).

        Returns
        -------
        A Path.
        """
        versions: PathSeries = self.versions()

        if not len(versions):
            raise FileNotFoundError(self)

        latest = versions.keep_latest_versions(include_versionless=include_versionless)
        if len(latest) > 1:
            raise ValueError(
                "More than one file in the directory matches "
                f"the versionless pattern. [{', '.join(list(latest))}]"
            )
        return latest.iloc[0]

    def highest_numbered_version(self):
        """Get the highest number version of the file path.

        Lists files in the parent directory with the same versionless stem
        and selects the one with the highest version number.

        Returns
        -------
        A Path.
        """
        versions: PathSeries = self.versions()

        if not len(versions):
            raise FileNotFoundError(self)

        last = versions.keep_highest_numbered_versions()
        if len(last) > 1:
            raise ValueError(
                "More than one file in the directory matches "
                f"the versionless pattern. [{', '.join(list(last))}]"
            )
        return last.iloc[0]

    @property
    def version_number(self) -> int | None:
        try:
            last_match = re.findall(self._version_pattern, self)[-1]
            return int(last_match)
        except IndexError:
            return None

    @property
    def periods(self) -> list[str]:
        if re.findall(r"_p(\d{5})", self):
            raise ValueError(f"Invalid period format in {self}")

        try:
            return re.findall(self._period_pattern, self)
        except IndexError:
            return []

    @property
    def period_folders(self) -> list[str]:
        pat = self._period_pattern.replace(self._period_prefix, "")

        try:
            return re.findall(pat, self.parent)
        except IndexError:
            return []

    @property
    def periodless_stem(self) -> str:
        """Return the file stem before the period pattern."""
        return str(re.sub(f"{self._period_pattern}.*", "", self._path.stem))

    @property
    def versionless_stem(self) -> str:
        """Return the file stem before the version pattern."""
        return str(re.sub(self._version_pattern, "", self._path.stem))

    @property
    def versionless(self):
        return Path(f"{self.parent}/{self.versionless_stem}{self.suffix}")

    @property
    def parent(self):
        return Path(self._path.parent)

    @property
    def root(self):
        """The first part of the path."""
        return Path(self.parts[0])

    @property
    def name(self) -> str:
        return self._path.name

    @property
    def stem(self) -> str:
        return self._path.stem

    @property
    def parts(self) -> tuple[str]:
        return self._path.parts

    @property
    def suffix(self) -> str:
        return str(self._path.suffix)

    @property
    def suffixes(self):
        return self._path.suffixes

    @property
    def dtypes(self) -> pd.Series:
        with self.open() as f:
            schema = pyarrow.parquet.read_schema(f)
            index_cols = _get_index_cols(schema)
            return pd.Series(schema.types, index=schema.names).loc[
                lambda x: ~x.index.isin(index_cols)
            ]

    @property
    def columns(self) -> pd.Index:
        with self.open() as f:
            schema = pyarrow.parquet.read_schema(f)
            index_cols = _get_index_cols(schema)
            return pd.Index(schema.names).difference(index_cols)

    @property
    def shape(self) -> tuple[int, int]:
        with self.open() as f:
            meta = pyarrow.parquet.read_metadata(f)
            return meta.num_rows, meta.num_columns

    @property
    def file_system(self):
        if self._fs is None:
            self._fs = dp.FileClient.get_gcs_file_system()
        return self._fs

    @file_system.setter
    def file_system(self, val):
        self._fs = val
        return self._fs

    def open(self):
        return self.file_system.open(self)

    def exists(self) -> bool:
        return self.file_system.exists(self)

    def mv(self, new_path: str):
        self.file_system.mv(self, as_str(new_path))

    def cp(self, new_path: str):
        self.file_system.cp(self, as_str(new_path))

    def rm_file(self) -> None:
        self.file_system.rm_file(self)

    def is_dir(self) -> bool:
        return self.file_system.isdir(self)

    def is_file(self) -> bool:
        return not self.file_system.isdir(self)

    def with_suffix(self, suffix: str):
        return Path(self._path.with_suffix(suffix))

    def with_name(self, new_name: str):
        return Path(self._path.with_name(new_name))

    def with_stem(self, new_with_stem: str):
        return Path(self._path.with_stem(new_with_stem))

    def with_version(self, version: int):
        """Replace the Path's version number, if any, with a new version number.

        Examples
        --------
        >>> Path('file.parquet').with_version(1)
        'file_v1.parquet'

        >>> Path('file_v101.parquet').with_version(201)
        'file_v201.parquet'
        """

        parent = f"{self.parent}/" if self.parent != "." else ""
        return Path(
            f"{parent}{self.versionless_stem}{self._version_prefix}{version}{self.suffix}"
        )

    def with_periods(self, from_period: str, to_period: str | None = None):
        """Replace the Path's period, if any, with one or two new periods.

        Examples
        --------
        >>> Path('file_v1.parquet').with_periods("2024-01-01")
        'file_p2024-01-01_v1.parquet'

        >>> Path('file_p2022_p2023_v1.parquet').with_periods("2024-01-01")
        'file_p2024-01-01_v1.parquet'
        """
        if not isinstance(from_period, (str, int)):
            raise TypeError(
                f"'from_period' should be string or int. Got {type(from_period)}"
            )
        if to_period and not isinstance(to_period, (str, int)):
            raise TypeError(
                f"'to_period' should be string or int. Got {type(to_period)}"
            )

        periods: tuple[str] = (
            (str(from_period), str(to_period)) if to_period else (str(from_period),)
        )
        period_string: str = "".join([self._period_prefix + str(x) for x in periods])
        version = (
            f"{self._version_prefix}{self.version_number}"
            if self.version_number
            else ""
        )
        stem: str = self.periodless_stem

        parent = f"{self.parent}/" if self.parent != "." else ""

        period_folders = self.period_folders
        if len(period_folders) == 1:
            period_folder = period_folders[0]
            new_period_folders = set()
            for period in periods:
                try:
                    new_period_folders.add(period[: len(period_folder)])
                except IndexError:
                    pass
            if len(new_period_folders) == 1:
                new_period_folder = new_period_folders.pop()
                parent = parent.replace(period_folder, new_period_folder)
            elif len(new_period_folders) > 1:
                raise ValueError("Multiple new periods, only a single period folder.")

        return Path(f"{parent}{stem}{period_string}{version}{self.suffix}")

    def add_to_version_number(self, number: int):
        """Add a number to the version number."""
        new_version = self.version_number + number
        return self.with_version(new_version)

    def read_pandas(
        self,
        columns: list[str] | dict[str, str] | None = None,
        **kwargs,
    ) -> pd.DataFrame:
        """Read the file as a pandas.DataFrame.

        Parameters
        ----------
        columns:
            Iterable of columns to be read. If columns is a dict, the keys will be read,
                then the columns will be renamed to the values if the values are not None.
        **kwargs:
            Additional keyword arguments passed to the read function.
        """
        return self._read_pandas_or_geopandas(dp.read_pandas, columns, **kwargs)

    def read_geopandas(
        self,
        columns: list[str] | dict[str, str] | None = None,
        **kwargs,
    ) -> gpd.GeoDataFrame:
        """Read the file as a geopandas.GeoDataFrame.

        Parameters
        ----------
        columns:
            Iterable of columns to be read. If columns is a dict, the keys will be read,
                then the columns will be renamed to the values if the values are not None.
        **kwargs:
            Additional keyword arguments passed to the read function.
        """
        return self._read_pandas_or_geopandas(sg.read_geopandas, columns, **kwargs)

    def read_polars(self):
        pass

    def write_new_version(
        self,
        df: pd.DataFrame,
        check_if_equal: bool = False,
        timeout: int | None = 30,
        func: Callable | None = None,
        verbose: bool = False,
    ) -> None:
        """Find the newest saved version of the file, adds 1 to the version number and saves the DataFrame.

        Args:
            df: (Geo)DataFrame to write to the Path.
            check_if_equal: Whether to read the newest existing version and only write the new
                version if the newest is not equal to 'df'. Defaults to False.
            timeout: Minutes that must pass between each new version is written.
                To avoid accidental loop writes.
            func: Write function to use. Defaults to dapla.write_pandas if data is pandas
                and sgis.write_geopandas if data is geopandas.
            verbose: Whether to print info. Defaults to False.
        """
        try:
            path: Path = self.new_version(timeout)
            exists = True
        except FileNotFoundError:
            path = self.with_version(1)
            exists = False

        if exists and check_if_equal:
            if isinstance(df, gpd.GeoDataFrame):
                highest_numbered_df = path.read_geopandas()
            else:
                highest_numbered_df = path.read_pandas()
            if highest_numbered_df.equals(df):
                if verbose:
                    print(
                        "Not writing new version because new data is equal to existing data."
                    )
                return

        if func is None:
            func: Callable = (
                sg.write_geopandas
                if isinstance(df, gpd.GeoDataFrame)
                else dp.write_pandas
            )
        return func(df, path)

    def write_versionless(self, df: pd.DataFrame, func: Callable | None = None) -> None:
        """Write a DataFrame to the versionless path.

        Args:
            df: (Geo)DataFrame to write to the Path.
            func: Write function to use. Defaults to dapla.write_pandas if data is pandas
                and sgis.write_geopandas if data is geopandas.
        """
        if func is None:
            func: Callable = (
                sg.write_geopandas
                if isinstance(df, gpd.GeoDataFrame)
                else dp.write_pandas
            )

        return func(df, self.versionless)

    def _read_pandas_or_geopandas(
        self,
        func: Callable,
        columns: list[str] | dict[str, str] | None = None,
        **kwargs,
    ) -> Any:
        if self.is_dir():
            raise ValueError("Cannot read a folder as a pandas.DataFrame")
        if columns:
            df = func(self, columns=list(columns), **kwargs)
        else:
            df = func(self, **kwargs)

        if is_dict_like(columns):
            new_cols = {
                old_col: new_col
                for old_col, new_col in columns.items()
                if new_col is not None
            }

            df = df.rename(columns=new_cols, errors="raise")

        return df

    def _get_files_and_dirs(self, info: list[dict]) -> PathSeries:
        files: pd.Series = self._get_file_series(info).apply(Path)

        dirs: pd.Series = self._get_directory_series(info).apply(Path)

        if not any(len(lst) for lst in [files, dirs]):
            return PathSeries()

        out = PathSeries(pd.concat([lst for lst in [files, dirs] if len(lst)]))

        return out.sort_index(level=0)

    def _get_directory_series(self, info):
        """pandas.Series of all directories in the list returned from dapla.ls(detail=True).

        Index is a MultiIndex of all zeros (because directories have no timestamp and size).
        """
        dirs = np.array([x["name"] for x in info if x["type"] == "directory"])
        return pd.Series(
            dirs,
            index=pd.MultiIndex.from_arrays(
                [np.zeros(dirs.shape), np.zeros(dirs.shape)]
            ),
        )

    def _get_file_series(self, info: list[dict]) -> pd.Series:
        """pandas.Series of all files in the list returned from dapla.ls(detail=True).

        Index is a MultiIndex if timestamps and file size.
        """
        # 2d numpy array
        fileinfo = np.array(
            [
                (x["updated"], x["size"], x["name"])
                for x in info
                if x["type"] != "directory"
            ]
        )

        if not len(fileinfo):
            return pd.Series()

        timestamp: pd.Index = (
            pd.to_datetime(pd.Index(fileinfo[:, 0], name="updated"))
            .round("s")
            .tz_convert("Europe/Oslo")
            .tz_localize(None)
            .round("s")
        )
        mb = pd.Index(fileinfo[:, 1], name="mb (int)").astype(float) / 1_000_000

        index = pd.MultiIndex.from_arrays([timestamp, mb])

        return (
            pd.Series(fileinfo[:, 2], index=index, name="path")
            # remove dirs
            .loc[lambda x: ~x.str.endswith("/")].sort_index(level=0)
        )

    def __truediv__(self, other: str | PathLike | PurePath):
        """Append a string or Path to the path with a forward slash.

        Example
        -------
        >>> folder = 'ssb-kart-data-delt-prod/analyse_data/klargjorte-data/2023'
        >>> file_path = folder / "ABAS_kommune_flate_p2023_v1.parquet"
        >>> file_path
        'ssb-kart-data-delt-prod/analyse_data/klargjorte-data/2023/ABAS_kommune_flate_p2023_v1.parquet'
        """
        if not isinstance(other, (str, PurePath, PathLike)):
            raise TypeError(
                "unsupported operand type(s) for /: "
                f"{self.__class__.__name__} and {other.__class__.__name__}"
            )
        return Path(f"{self}/{as_str(other)}")


def get_version_number(path: Path | str, pattern: str = VERSION_PATTERN) -> int | None:
    try:
        last_match = re.findall(pattern, path)[-1]
        return int(last_match)
    except IndexError:
        return None


def get_path_tree(
    paths: PathSeries | list[Path],
    base: str | Path,
    max_rows: int | None = 3,
    ascending: bool = True,
    indent: int = 4,
) -> Tree:

    tree = Tree()

    paths = PathSeries(paths).sort_values(ascending=ascending).files

    paths_per_dir = [paths.containing(parent) for parent in paths.parent.unique()]

    tree.add_html(
        split_path_and_make_copyable_html(base, None, display_prefix="") + " /"
    )
    tree.add(base + " /")

    already_printed: set[tuple[str]] = set()

    for dir_files in paths_per_dir:
        assert isinstance(dir_files, PathSeries)

        has_version_number = dir_files.version_number.notna()
        if max_rows is not None and sum(has_version_number) >= max_rows:
            dir_files = dir_files[has_version_number]

        # tuple because hashable
        parts_so_far: tuple[str] = tuple(base.split("/"))

        j = 0

        for i, path in enumerate(dir_files):
            *folders, name = path.replace(base, "").strip("/").split("/")
            if i == 0:
                for j, folder in enumerate(folders):
                    parts_so_far += (folder,)

                    if parts_so_far in already_printed:
                        continue
                    spaces = " " * indent * (j + 1)

                    tree.add_html(
                        f"<pre>{spaces}└──{split_path_and_make_copyable_html('/'.join(parts_so_far), display_prefix='')} /<pre>",
                    )
                    tree.add(spaces + f"└──{folder} /")

                    already_printed.add(parts_so_far)

            if max_rows is not None and i > max_rows - 1:
                tree.add_html(" " * indent * (j + 2) + "└──(...)")
                tree.add(" " * indent * (j + 2) + "└──(...)")
                break

            spaces = " " * indent * (j + 2)
            tree.add_html(
                f"<pre>{spaces}└──{split_path_and_make_copyable_html('/'.join(parts_so_far + (name,)), display_prefix='')}<pre>",
            )
            tree.add(spaces + f"└──{name}")
    return tree


def _get_index_cols(schema: pyarrow.Schema) -> list[str]:
    cols = json.loads(schema.metadata[b"pandas"])["index_columns"]
    return [x for x in cols if not isinstance(x, dict)]
