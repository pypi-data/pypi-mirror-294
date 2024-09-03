from hashlib import sha1
from os.path import exists as path_exists
from pathlib import Path
from traceback import print_exc
import pandas

TMP_LOCATION = "data"


def check_data_path(p=TMP_LOCATION):
    if not path_exists(p):
        Path(p).mkdir(parents=True, exist_ok=True)


def cached_parquet(*args, **kwargs):
    """Stores the resulting DataFrame of the function in local
    cache (TMP_LOCATION) as parquet format. Returns from stored parquet when
    available.
    
    Decorated method should have a DataFrame return type
    For GeoDataFrame types, set pqlib to geopandas(gps)
    """

    def decorator(func):
        def wrapper(*f_args, **f_kwargs):
            # Check if already accessed & return
            prefix = kwargs.get('tmp_prefix', 'tmp')
            prefix = f_kwargs.pop('tmp_prefix', prefix)

            pqlib = kwargs.get('dflib', pandas)

            args_str = func.__name__ + ''.join(map(str, f_args)) + str(f_kwargs)
            file_hash = sha1(args_str.encode("UTF-8")).hexdigest()[:16]
            tmp_loc = f"{TMP_LOCATION}/{prefix}_{file_hash}.parquet"
            if path_exists(tmp_loc):
                print("Using stored file: ", tmp_loc)
                return pqlib.read_parquet(tmp_loc)

            # Store locally for faster re-access
            df = func(*f_args, **f_kwargs)
            print("Storing", tmp_loc)
            try:
                df.to_parquet(tmp_loc, compression="gzip")
            except Exception:
                print_exc()
                print("Failed to store output as parquet!")
            return df

        return wrapper

    if len(args) == 1 and callable(args[0]):
        return decorator(args[0])

    return decorator


check_data_path()
