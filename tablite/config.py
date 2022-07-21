import pathlib, os, tempfile

# The data is from hereon stored as:

# Each table must be loaded with a path. ROOT is the default
# folder. If a table is created with another path, e.g.:
# working_dir, then tablite.hdf5 and /pages must be present.
# Each table must have hdf5-key.

# Table.reload_tables(path) reads all tables on a path using
# tablite.hdf5 as index.

# H5_DIR - default folder for tablite tables.
# ├───tablite.hdf5    The tablite.hdf5 file organise the metadata.
# │   ├───/table      As it mainly sees short metadata read/writes
# │   │   ├───1       blocking is tolerated.
# │   │   ├───2
# │   │   ├───...
# │   │   └───n
# │   └───/column
# │       ├───11
# │       ├───12
# │       ├───...
# │       └───n
# ├───pages           The pages folder organise all commonly
# │   ├───1.h5        blocking read/writes.
# │   ├───2.h5
# │   ├───...
# │   └───n.h5

# The /table refers to columns.
# Columns refer to pages
# pages hold data.

H5_FILENAME = 'tablite.h5'
H5_PAGES_NAME = 'pages'
H5_DIR = pathlib.Path(tempfile.gettempdir()) / "tablite"
H5_STORAGE = H5_DIR / H5_FILENAME
if not H5_DIR.exists():
    H5_DIR.mkdir()
# to overwrite first import the config class:
# >>> from tablite.config import Config
# >>> Config.H5_STORAGE = /a/new/directory
# Every new table will used this path.

H5_PAGES = H5_DIR / 'pages'
if not H5_PAGES.exists():
    H5_PAGES.mkdir()

H5_PAGE_SIZE = 1_000_000  # sets the page size limit.
H5_ENCODING = 'UTF-8'  # sets the page encoding when using bytes
SINGLE_PROCESSING_LIMIT = 1_000_000  # when the number of fields (rows x columns) 
# exceed this value, multiprocessing is used.


# EXPORT - An exported tablite table is a simple lz4 compressed folder. Why LZ4?
# This is why: https://gist.github.com/root-11/021b63697e7389e93ecd92abe3cdd806#file-compression_benchmark-py
#
# somename.lz4
# ├───tablite.hdf5
# │   ├───/table
# │   │   ├───1
# │   │   ├───2
# │   │   ├───...
# │   │   └───n
# │   └───/column
# │       ├───11
# │       ├───12
# │       ├───...
# │       └───n
# ├───pages
# │   ├───1.h5
# │   ├───2.h5
# │   ├───...
# │   └───n.h5


# IMPORT - As Table.path points to the root, which is a dir - it's readwriteable.
# nothing else needs to be done.

# TEMPORARY FILES
# So far only the file_reader requires a dir for splitting files for import.
# This is managed here:
TEMPDIR = pathlib.Path(tempfile.gettempdir()) / 'tablite-tmp'
if not TEMPDIR.exists():
    TEMPDIR.mkdir()



