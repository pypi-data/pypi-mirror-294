from unittest import TestCase

from pathlib import Path
from os import path, listdir, unlink

from ogialibs.data import cached_parquet


def _tmp_loc():
    from ogialibs.data import TMP_LOCATION
    return TMP_LOCATION


def clear_folder(tmp_path=_tmp_loc()):
    for filename in listdir(tmp_path):
        file_path = path.join(tmp_path, filename)
        unlink(file_path)


class TestIngestions(TestCase):
    def setUp(self) -> None:
        self.tmp_location = _tmp_loc()
        self.data = {
            'Name': ['John', 'Anna', 'Peter', 'Linda'],
            'Age': [28, 24, 35, 32],
            'City': ['New York', 'Paris', 'Berlin', 'London']
        }
        return super().setUp()

    def tearDown(self):
        clear_folder()

    def test_generates_parquet_file(self):
        # Import and test data path created
        clear_folder()
        self.assertTrue(path.exists(self.tmp_location))

        # Without the parentheses
        @cached_parquet
        def get_df():
            from pandas import DataFrame
            return DataFrame(self.data)

        # Check file created
        foo = get_df()
        foo_dict = {
            'Name': {0: 'John', 1: 'Anna', 2: 'Peter', 3: 'Linda'},
            'Age': {0: 28, 1: 24, 2: 35, 3: 32},
            'City': {0: 'New York', 1: 'Paris', 2: 'Berlin', 3: 'London'}
        }
        self.assertEqual(foo.to_dict(), foo_dict)

        # A tmp file is created
        files = listdir(_tmp_loc())
        self.assertEqual(1, len(files))

    def test_uses_parquet_file(self):
        clear_folder()
        # Parquet file is used instead of re-generated data
        from pandas import DataFrame
        import pickle

        pickle_loc = f"{self.tmp_location}/test.pickle"

        with open(pickle_loc, 'wb') as handle:
            pickle.dump(self.data, handle)

        @cached_parquet()
        def get_df(extra_col_value=None):
            with open(pickle_loc, 'rb') as handle:
                data = pickle.load(handle)
            df = DataFrame(data)
            if extra_col_value:
                df['extra'] = extra_col_value
            return df

        test_val = 5
        foo = get_df(extra_col_value=test_val)
        self.assertEqual(list(foo.extra), [test_val for _ in self.data['Age']])

        # Generates new file for different value
        new_val = 9
        bar = get_df(extra_col_value=new_val)
        self.assertEqual([new_val for _ in self.data['Age']], list(bar.extra))
        files = listdir(_tmp_loc())
        expected_files = [
            'Pickle file',
            'First parquet file',
            'Second parquet file'
        ]
        self.assertEqual(len(expected_files), len(files))

        # Still returns when source file is unavailable
        file_to_rem = Path(pickle_loc)
        file_to_rem.unlink()

        bar = get_df(extra_col_value=test_val)
        self.assertEqual(list(foo.extra), list(bar.extra))

    def test_prefix_set_at_decorator(self):
        clear_folder()
        test_prefix = 'foo'

        @cached_parquet(tmp_prefix=test_prefix)
        def get_df():
            from pandas import DataFrame
            return DataFrame(self.data)

        _df = get_df()

        files = listdir(_tmp_loc())
        self.assertEqual(1, len(files))
        self.assertEqual(f"{test_prefix}_", files[0][0:4])

    def test_prefix_set_at_runtime(self):
        clear_folder()
        test_prefix = 'bar'

        @cached_parquet
        def get_df():
            from pandas import DataFrame
            return DataFrame(self.data)

        _df = get_df(tmp_prefix=test_prefix)

        files = listdir(_tmp_loc())
        self.assertEqual(1, len(files))
        self.assertEqual(f"{test_prefix}_", files[0][0:4])

    def test_geopandas(self):
        import geopandas as gpd

        @cached_parquet(dflib=gpd)
        def get_gdf(city_name):
            from pandas import DataFrame
            from shapely.geometry import Point
            df = DataFrame(
                {
                    'City': ['London', 'Paris', city_name],
                    'Country': ['England', 'France', 'Germany'],
                    'Latitude': [51.5074, 48.8566, 52.5200],
                    'Longitude': [-0.1278, 2.3522, 13.4050]
                }
            )
            df['Coordinates'] = list(zip(df.Longitude, df.Latitude))
            df['Coordinates'] = df['Coordinates'].apply(Point)
            return gpd.GeoDataFrame(df, geometry='Coordinates')

        clear_folder()
        gdf = get_gdf('Berlin')
        self.assertIsInstance(gdf, gpd.GeoDataFrame)

        tmp_path = _tmp_loc()
        files = listdir(tmp_path)
        self.assertEqual(1, len(files))
        gen_gdf = gpd.read_parquet(path.join(tmp_path, files[0]))
        self.assertIsInstance(gen_gdf, gpd.GeoDataFrame)

        # Returns second time
        del gdf
        gdf = get_gdf('Berlin')
        self.assertIsInstance(gdf, gpd.GeoDataFrame)
