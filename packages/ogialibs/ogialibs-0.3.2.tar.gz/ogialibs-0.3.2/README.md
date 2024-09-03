# OGIA Python Libraries

Some commonly used python libraries.

---

## Installation

Use the url of this repository for directly installing via pip

```msdos
pip install git+https://github.com/Office-of-Groundwater-Impact-Assessment/ogialibs
```

### Installing a specific version of OgiaLibs

Please make note of the commit hash or branch name you would like to install.

Replace the *BRANCH_NAME* below. Branch or commit string should come after the "@" sign.


```msdos
pip install git+https://github.com/Office-of-Groundwater-Impact-Assessment/ogialibs@BRANCH_NAME
```

## Usage
#### cached_parquet

Creates a Parquet cache in local data directory after the first generation of an output. 
Decorated function must have a single DataFrame (or GeoDataFrame. See below for example) return value.
Below example will create a `tmp_XXXXX.parquet` file under the data folder of your project. 

```python
from ogialibs.data import cached_parquet

@cached_parquet
def get_df():
    ...
    return df
```

Custom prefixes can be set at the decorator or during the function call;
```python

@cached_parquet(tmp_prefix='foo')
def get_foo_df():
    ...
    return df

# Creates a foo_XXXXX.parquet file instead

@cached_parquet
def get_bar_df():
    ...
    return df

bar = get_bar_df(tmp_prefix='bar')

# Creates a bar_XXXXX.parquet file instead
```

When using with GeoPandas, the library must be set via the `dflib` argument 

```python
import geopandas as gpd

@cached_parquet(dflib=gpd)
def get_gdf():
    ...
    return gdf
```

# Building

Prerequisites;
- build
- twine
- Api keys from PyPi
- Local configuration file (.pypirc)


```
python -m build
```

And

```
twine upload --repository pypi dist/* --config-file .pypirc
```
