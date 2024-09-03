"""
Functions.

This module contains helper functions to simplify the usage.
"""

from pathlib import Path
from typing import Optional, Union

import geopandas as gpd
from shapely.geometry.base import BaseGeometry

from overturemaestro.data_downloader import (
    download_data,
    download_data_for_multiple_types,
    pyarrow_filters,
)

__all__ = [
    "convert_geometry_to_parquet",
    "convert_geometry_to_parquet_for_multiple_types",
    "convert_geometry_to_geodataframe",
    "convert_geometry_to_geodataframe_for_multiple_types",
]

# TODO: add verbosity_mode, debug_memory, debug_times
# TODO: prepare examples


def convert_geometry_to_parquet(
    release: str,
    theme: str,
    type: str,
    geometry_filter: BaseGeometry,
    pyarrow_filter: Optional[pyarrow_filters] = None,
    result_file_path: Optional[Union[str, Path]] = None,
    ignore_cache: bool = False,
    working_directory: Union[str, Path] = "files",
) -> Path:
    """
    Get a GeoParquet file with Overture Maps data within given geometry.

    Automatically downloads Overture Maps dataset for a given release and theme/type
    in a concurrent manner and returns a single file as a result.

    Args:
        release (str): Release version.
        theme (str): Theme of the dataset.
        type (str): Type of the dataset.
        geometry_filter (BaseGeometry): Geometry used to filter data.
        pyarrow_filter (Optional[pyarrow_filters], optional): Filters to apply on a pyarrow dataset.
            Can be pyarrow.compute.Expression or List[Tuple] or List[List[Tuple]]. Defaults to None.
        result_file_path (Union[str, Path], optional): Where to save
            the geoparquet file. If not provided, will be generated based on hashes
            from filters. Defaults to `None`.
        ignore_cache (bool, optional): Whether to ignore precalculated geoparquet files or not.
            Defaults to False.
        working_directory (Union[str, Path], optional): Directory where to save
            the downloaded `*.parquet` files. Defaults to "files".

    Returns:
        Path: Path to the generated GeoParquet file.

    Examples:
        Get buildings in the center of London.

        >>> import overturemaestro as om
        >>> from shapely import box
        >>> london_bbox = box(-0.120077, 51.498164, -0.090809, 51.508849)
        >>> gpq_path = om.convert_geometry_to_parquet(
        ...     release="2024-08-20.0",
        ...     theme="buildings",
        ...     type="building",
        ...     geometry_filter=london_bbox,
        ... ) # doctest: +IGNORE_RESULT
        >>> gpq_path.as_posix()
        'files/2024-08-20.0/theme=buildings/type=building/7ed1...3f41_nofilter.parquet'

        Inspect the content
        >>> import geopandas as gpd
        >>> gdf = gpd.read_parquet(gpq_path)
        >>> len(gdf)
        1863
        >>> list(gdf.columns)
        ['id', 'geometry', 'bbox', 'version', 'sources', 'subtype', 'class', 'names', 'level',
        'has_parts', 'height', 'is_underground', 'num_floors', 'num_floors_underground',
        'min_height', 'min_floor', 'facade_color', 'facade_material', 'roof_material', 'roof_shape',
        'roof_direction', 'roof_orientation', 'roof_color', 'roof_height', 'theme', 'type']

        Download museums in the same area from places dataset with a filter.

        >>> gpq_path = om.convert_geometry_to_parquet(
        ...     release="2024-08-20.0",
        ...     theme="places",
        ...     type="place",
        ...     geometry_filter=london_bbox,
        ...     pyarrow_filter=[[
        ...         (("categories", "primary"), "=", "museum"),
        ...         ("confidence", ">", 0.95),
        ...     ]],
        ... ) # doctest: +IGNORE_RESULT
        >>> gdf = gpd.read_parquet(gpq_path)
        >>> len(gdf)
        5
        >>> gdf[["id", "names", "confidence"]] # doctest: +IGNORE_RESULT
                                         id                               names  confidence
        0  08f194ad1499c8b1038ff3e213d81456  {'primary': 'Florence Nightinga...    0.982253
        1  08f194ad149044c6037575af3681766f  {'primary': 'Philip Simpson Des...    0.969941
        2  08f194ad32a0d494030fdddc1b405fb1  {'primary': 'Shakespeare's Glob...    0.991993
        3  08f194ad30695784036410e184708927  {'primary': 'Clink Street Londo...    0.965185
        4  08f194ad30690a42034312e00c0254a2  {'primary': 'The Clink Prison M...    0.982253
    """
    return download_data(
        release=release,
        theme=theme,
        type=type,
        geometry_filter=geometry_filter,
        pyarrow_filter=pyarrow_filter,
        result_file_path=result_file_path,
        ignore_cache=ignore_cache,
        working_directory=working_directory,
    )


def convert_geometry_to_parquet_for_multiple_types(
    release: str,
    theme_type_pairs: list[tuple[str, str]],
    geometry_filter: BaseGeometry,
    ignore_cache: bool = False,
    working_directory: Union[str, Path] = "files",
) -> list[Path]:
    """
    Get GeoParquet files with Overture Maps data within given geometry for multiple types.

    Automatically downloads Overture Maps dataset for a given release and theme/type pairs
    in a concurrent manner and returns a list of files as a result.

    Order of paths is the same as the input theme_type_pairs list.

    Args:
        release (str): Release version.
        theme_type_pairs (list[tuple[str, str]]): Pairs of themes and types of the dataset.
        geometry_filter (BaseGeometry): Geometry used to filter data.
        pyarrow_filter (Optional[pyarrow_filters], optional): Filters to apply on a pyarrow dataset.
            Can be pyarrow.compute.Expression or List[Tuple] or List[List[Tuple]]. Defaults to None.
        result_file_path (Union[str, Path], optional): Where to save
            the geoparquet file. If not provided, will be generated based on hashes
            from filters. Defaults to `None`.
        ignore_cache (bool, optional): Whether to ignore precalculated geoparquet files or not.
            Defaults to False.
        working_directory (Union[str, Path], optional): Directory where to save
            the downloaded `*.parquet` files. Defaults to "files".

    Returns:
        list[Path]: List of paths to the generated GeoParquet files.
    """
    return download_data_for_multiple_types(
        release=release,
        theme_type_pairs=theme_type_pairs,
        geometry_filter=geometry_filter,
        ignore_cache=ignore_cache,
        working_directory=working_directory,
    )


def convert_geometry_to_geodataframe(
    release: str,
    theme: str,
    type: str,
    geometry_filter: BaseGeometry,
    pyarrow_filter: Optional[pyarrow_filters] = None,
    ignore_cache: bool = False,
    working_directory: Union[str, Path] = "files",
) -> gpd.GeoDataFrame:
    """
    Get a GeoDataFrame with Overture Maps data within given geometry.

    Automatically downloads Overture Maps dataset for a given release and theme/type
    in a concurrent manner and returns a single GeoDataFrame as a result.

    Args:
        release (str): Release version.
        theme (str): Theme of the dataset.
        type (str): Type of the dataset.
        geometry_filter (BaseGeometry): Geometry used to filter data.
        pyarrow_filter (Optional[pyarrow_filters], optional): Filters to apply on a pyarrow dataset.
            Can be pyarrow.compute.Expression or List[Tuple] or List[List[Tuple]]. Defaults to None.
        ignore_cache (bool, optional): Whether to ignore precalculated geoparquet files or not.
            Defaults to False.
        working_directory (Union[str, Path], optional): Directory where to save
            the downloaded `*.parquet` files. Defaults to "files".

    Returns:
        gpd.GeoDataFrame: GeoDataFrame with Overture Maps features.

    Examples:
        Get buildings in the center of London.

        >>> import overturemaestro as om
        >>> from shapely import box
        >>> london_bbox = box(-0.120077, 51.498164, -0.090809, 51.508849)
        >>> gdf = om.convert_geometry_to_geodataframe(
        ...     release="2024-08-20.0",
        ...     theme="buildings",
        ...     type="building",
        ...     geometry_filter=london_bbox,
        ... ) # doctest: +IGNORE_RESULT
        >>> gdf[['names', 'subtype']].sort_index()
                                                                       names       subtype
        id
        08b194ad14804fff0200fea269f9879c  {'primary': 'Park Plaza London ...          None
        08b194ad14812fff02006b5f7b4749e1                                None          None
        08b194ad14814fff02002e44dac80f43  {'primary': 'The Barn', 'common...  agricultural
        08b194ad14814fff0200c77856a66cd7                                None          None
        08b194ad14814fff0200dbc14b9a6d57                                None          None
        ...                                                              ...           ...
        08b194ad33db2fff02006a3ce00700f9  {'primary': 'citizenM hotel Lon...          None
        08b194ad33db3fff02008b05d22745ed  {'primary': 'Metal Box Factory'...          None
        08b194ad33db4fff0200cb2043a25c3c                                None    commercial
        08b194ad33db4fff0200f2ead15d53ac                                None   residential
        08b194ad33db5fff02005eaafd2ff033  {'primary': 'Cooper & Southwark...    commercial

        [1863 rows x 2 columns]

        Download museums in the same area from places dataset with a filter.

        >>> gdf = om.convert_geometry_to_geodataframe(
        ...     release="2024-08-20.0",
        ...     theme="places",
        ...     type="place",
        ...     geometry_filter=london_bbox,
        ...     pyarrow_filter=[[
        ...         (("categories", "primary"), "=", "museum"),
        ...         ("confidence", ">", 0.95),
        ...     ]],
        ... ) # doctest: +IGNORE_RESULT
        >>> gdf[["names", "confidence"]]
                                                                       names  confidence
        id
        08f194ad149044c6037575af3681766f  {'primary': 'Philip Simpson Des...    0.969941
        08f194ad1499c8b1038ff3e213d81456  {'primary': 'Florence Nightinga...    0.982253
        08f194ad30690a42034312e00c0254a2  {'primary': 'The Clink Prison M...    0.982253
        08f194ad30695784036410e184708927  {'primary': 'Clink Street Londo...    0.965185
        08f194ad32a0d494030fdddc1b405fb1  {'primary': 'Shakespeare's Glob...    0.991993
    """
    parsed_geoparquet_file = download_data(
        release=release,
        theme=theme,
        type=type,
        geometry_filter=geometry_filter,
        pyarrow_filter=pyarrow_filter,
        ignore_cache=ignore_cache,
        working_directory=working_directory,
    )
    return gpd.read_parquet(parsed_geoparquet_file).set_index("id")


def convert_geometry_to_geodataframe_for_multiple_types(
    release: str,
    theme_type_pairs: list[tuple[str, str]],
    geometry_filter: BaseGeometry,
    ignore_cache: bool = False,
    working_directory: Union[str, Path] = "files",
) -> list[gpd.GeoDataFrame]:
    """
    Get GeoDataFrames list with Overture Maps data within given geometry for multiple types.

    Automatically downloads Overture Maps dataset for a given release and theme/type pairs
    in a concurrent manner and returns a list of GeoDataFrames as a result.

    Order of GeoDataFrames is the same as the input theme_type_pairs list.

    Args:
        release (str): Release version.
        theme_type_pairs (list[tuple[str, str]]): Pairs of themes and types of the dataset.
        geometry_filter (BaseGeometry): Geometry used to filter data.
        pyarrow_filter (Optional[pyarrow_filters], optional): Filters to apply on a pyarrow dataset.
            Can be pyarrow.compute.Expression or List[Tuple] or List[List[Tuple]]. Defaults to None.
        ignore_cache (bool, optional): Whether to ignore precalculated geoparquet files or not.
            Defaults to False.
        working_directory (Union[str, Path], optional): Directory where to save
            the downloaded `*.parquet` files. Defaults to "files".

    Returns:
        list[gpd.GeoDataFrame]: List of GeoDataFrames with Overture Maps features.
    """
    parsed_geoparquet_files = download_data_for_multiple_types(
        release=release,
        theme_type_pairs=theme_type_pairs,
        geometry_filter=geometry_filter,
        ignore_cache=ignore_cache,
        working_directory=working_directory,
    )
    return [
        gpd.read_parquet(parsed_geoparquet_file).set_index("id")
        for parsed_geoparquet_file in parsed_geoparquet_files
    ]
