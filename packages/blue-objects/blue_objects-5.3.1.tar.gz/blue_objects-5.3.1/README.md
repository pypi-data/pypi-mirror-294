# 🌀 blue-objects

🌀 `blue-objects` is an abstraction for cloud objects that are accessible in Python and Bash. For example, the Sentinel-2 [datacube](https://github.com/kamangir/blue-geo/tree/main/blue_geo/datacube) `datacube-EarthSearch-sentinel_2_l1c-S2A_10UDC_20240731_0_L1C` and 🌐 [`@geo watch`  outputs](https://github.com/kamangir/blue-geo/tree/main/blue_geo/watch) are objects.

## installation

```bash
pip install blue-objects
```

## use in Bash

```bash
@select
@catalog query copernicus sentinel_2 - . \
  --count 10 \
  --datetime 2024-07-30/2024-08-09 \
  --lat  51.83 \
  --lon -122.78

@select $(@catalog query read - . --count 1 --offset 3)
@datacube ingest scope=metadata+quick .

@publish tar .
```

from [`blue_geo/catalog/copernicus`](https://github.com/kamangir/blue-geo/tree/main/blue_geo/catalog/copernicus).

## use in Python

```python
def map_function(
    datacube_id: str,
    object_name: str,
) -> bool:
    success, target, list_of_files = load_watch(object_name)
    if not success or not list_of_files:
        return success
    filename = list_of_files[0]

    logger.info(
        "{}.map: {} @ {} -> {}".format(
            NAME,
            target,
            datacube_id,
            object_name,
        )
    )

    logger.info("🪄")

```

from [`blue_geo/watch/workflow/map.py`](https://github.com/kamangir/blue-geo/blob/main/blue_geo/watch/workflow/map.py).

---

[![PyPI version](https://img.shields.io/pypi/v/blue_objects.svg)](https://pypi.org/project/blue_objects/)