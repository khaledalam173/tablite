import pathlib, tempfile
import h5py

def set_working_dir(path):
    """ 
    Helper for changing the working directory.
    The working directory expects:

    - ./tablite.h5  the index file for tables, columns and pointers to pages
    - ./tablite/    the folder for individual hdf5 pages. The pages are numerated 1.h5, 2.h5, 3.h5, ..., etc
    """
    if isinstance(path,str):
        path = pathlib.Path(path)
    if not isinstance(path, pathlib.Path):
        raise TypeError
    if not path.is_dir():
        raise NotADirectoryError()
    
    global H5_FILENAME
    global H5_INDEX_FILE
    global H5_DATA_DIR
    global H5_WORKING_DIR
    H5_INDEX_FILE = path / H5_FILENAME     # E.g. tempdir/tablite.h5
    H5_DATA_DIR = path / H5_DATA_DIR_NAME  # E.g. tempdir/tablite

    if not H5_DATA_DIR.exists():
        H5_DATA_DIR.mkdir()
    
    # linux requires that files have headers, so this will guarantee it:
    if not H5_INDEX_FILE.exists():
        with h5py.File(H5_INDEX_FILE, 'w') as h5:
            h5.create_group('/table')
            h5.create_group('/column')
            h5.create_group('/page')
    

H5_DATA_DIR = ""
H5_INDEX_FILE = ""

H5_FILENAME = 'tablite.h5'
H5_DATA_DIR_NAME = 'tablite'

set_working_dir(path=pathlib.Path(tempfile.gettempdir()))

# WORKING DIRECTORY:
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
# ├───tablite         The pages folder organise all commonly
# │   ├───1.h5        blocking read/writes.
# │   ├───2.h5
# │   ├───...
# │   └───n.h5

# The /table refers to columns.
# Columns refer to pages
# pages hold data.

# TEMPORARY FILES
# So far only the file_reader requires a dir for splitting files for import.
# This is managed here:
TEMPDIR = pathlib.Path(tempfile.gettempdir()) / 'tablite-tmp'
if not TEMPDIR.exists():
    TEMPDIR.mkdir()

H5_PAGE_SIZE = 1_000_000  # sets the page size limit.
H5_ENCODING = 'UTF-8'  # sets the page encoding when using bytes
SINGLE_PROCESSING_LIMIT = 1_000_000  # when the number of fields (rows x columns) 
# exceed this value, multiprocessing is used.




