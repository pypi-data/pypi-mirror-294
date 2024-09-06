from datetime import timedelta
from typing import Any, List, Optional, Union

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype
from tecton import (
    BatchFeatureView,
    BatchSource,
    BatchTriggerType,
    Entity,
    PushConfig,
    RealtimeFeatureView,
    RequestSource,
    StreamFeatureView,
    StreamSource,
    batch_feature_view,
    pandas_batch_config,
    realtime_feature_view,
    stream_feature_view,
)
from tecton.types import Field

from .._utils import set_serialization
from ..core_utils import get_df_schema
from ..knowledge import source_as_knowledge

_MAX_ROWS = 100
_DEFAULT_TIMESTAMP_FIELD = "_tecton_auto_ts"
_DEFAULT_SOURCE_TIME = "2024-01-01"

# TODO(brian): update to the official environment once that is published
_MOCK_BATCH_FEATURE_VIEW_ENVIRONMENT = "tecton-rift-custom-1_0_0rc1"


def mock_source(
    name: str,
    raw: Any,
    max_rows: Optional[int] = None,
    is_stream: bool = False,
    **source_kwargs: Any,
) -> Union[BatchSource, StreamSource]:
    df = _to_df(raw)
    _max_row = max_rows or _MAX_ROWS
    if len(df) > _max_row:
        raise ValueError(f"Dataframe has more than {_max_row} rows")

    normalized_cols = {}
    ts_fields = []
    for col in df.columns:
        cv = df[col]
        if is_datetime64_any_dtype(cv):
            cv = cv.astype(str)
            ts_fields.append(col)
        normalized_cols[col] = cv

    data = pd.DataFrame(normalized_cols).to_dict("records")

    with set_serialization():

        @pandas_batch_config()
        def api_df():
            import pandas as pd

            df = pd.DataFrame(data)
            for f in ts_fields:
                df[f] = pd.to_datetime(df[f])
            return df

    if not is_stream:
        return BatchSource(name=name, batch_config=api_df, **source_kwargs)
    else:
        return StreamSource(
            name=name,
            stream_config=PushConfig(),
            batch_config=api_df,
            schema=get_df_schema(df),
            **source_kwargs,
        )


def mock_batch_feature_view(
    name: str,
    data: Any,
    entity_keys: List[str],
    timestamp_field: Optional[str] = None,
    max_rows: Optional[int] = None,
    **fv_kwargs: Any,
) -> BatchFeatureView:
    df = _to_df(data)
    if timestamp_field is None:
        timestamp_field = _DEFAULT_TIMESTAMP_FIELD
        df = df.assign(**{timestamp_field: _DEFAULT_SOURCE_TIME})
    df = df.assign(**{timestamp_field: pd.to_datetime(df[timestamp_field])})

    source = mock_source(name + "_source", df, max_rows=max_rows)
    schema = get_df_schema(df, as_attributes=True)
    join_keys = [Field(x.name, x.dtype) for x in schema if x.name in entity_keys]
    if len(join_keys) != len(entity_keys):
        raise ValueError(f"Entity keys {entity_keys} not all found in schema {schema}")
    entity = Entity(name=name + "_entity", join_keys=join_keys)
    features = [
        x for x in schema if x.name not in entity_keys and x.name != timestamp_field
    ]

    base_args = dict(
        name=name,
        sources=[source],
        entities=[entity],
        mode="pandas",
        online=True,
        offline=True,
        features=features,
        feature_start_time=df[timestamp_field].min().to_pydatetime(),
        incremental_backfills=False,
        batch_schedule=timedelta(days=1),
        max_backfill_interval=timedelta(days=10000),
        timestamp_field=timestamp_field,
        environment=_MOCK_BATCH_FEATURE_VIEW_ENVIRONMENT,
    )
    base_args.update(fv_kwargs)

    with set_serialization():

        @batch_feature_view(**base_args)
        def dummy(_df):
            return _df

    return dummy


def mock_realtime_feature_view(
    name: str,
    data: Any,
    keys: List[str],
    **fv_kwargs: Any,
) -> RealtimeFeatureView:
    df = _to_df(data)
    request_source = RequestSource(schema=get_df_schema(df[keys]))
    features = get_df_schema(df, as_attributes=True)

    base_args = dict(
        name=name, sources=[request_source], mode="pandas", features=features
    )
    base_args.update(fv_kwargs)

    with set_serialization():

        @realtime_feature_view(**base_args)
        def dummy(request):
            import pandas as pd

            return pd.merge(request, df, on=keys, how="inner").head(1)

    return dummy


def mock_stream_feature_view(
    name: str,
    data: Any,
    entity_keys: List[str],
    timestamp_field: Optional[str] = None,
    max_rows: Optional[int] = None,
    **fv_kwargs: Any,
) -> StreamFeatureView:
    df = _to_df(data)
    if timestamp_field is None:
        timestamp_field = _DEFAULT_TIMESTAMP_FIELD
        df = df.assign(**{timestamp_field: _DEFAULT_SOURCE_TIME})
    df = df.assign(**{timestamp_field: pd.to_datetime(df[timestamp_field])})

    source = mock_source(name + "_source", df, max_rows=max_rows, is_stream=True)
    schema = get_df_schema(df, as_attributes=True)
    join_keys = [Field(x.name, x.dtype) for x in schema if x.name in entity_keys]
    if len(join_keys) != len(entity_keys):
        raise ValueError(f"Entity keys {entity_keys} not all found in schema {schema}")
    entity = Entity(name=name + "_entity", join_keys=join_keys)
    features = [
        x for x in schema if x.name not in entity_keys and x.name != timestamp_field
    ]

    base_args = dict(
        name=name,
        source=source,
        entities=[entity],
        mode="pandas",
        online=True,
        offline=True,
        features=features,
        feature_start_time=df[timestamp_field].min().to_pydatetime(),
        batch_schedule=timedelta(days=1),
        max_backfill_interval=timedelta(days=10000),
        timestamp_field=timestamp_field,
        environment=_MOCK_BATCH_FEATURE_VIEW_ENVIRONMENT,
    )
    base_args.update(fv_kwargs)

    with set_serialization():

        @stream_feature_view(**base_args)
        def dummy(_df):
            return _df

    return dummy


def mock_knowledge(
    name: str,
    data: Any,
    description: str,
    vector_db_config: Any,
    vectorize_column: str,
    timestamp_field: Optional[str] = None,
    max_rows: Optional[int] = None,
) -> Any:
    df = _to_df(data)
    if timestamp_field is None:
        timestamp_field = _DEFAULT_TIMESTAMP_FIELD
        df = df.assign(**{timestamp_field: _DEFAULT_SOURCE_TIME})
    df = df.assign(**{timestamp_field: pd.to_datetime(df[timestamp_field])})
    start = df[timestamp_field].min().to_pydatetime()
    end = df[timestamp_field].max().to_pydatetime() + timedelta(days=1)

    source = mock_source(
        name + "_source", df, max_rows=max_rows, description=description
    )
    k = source_as_knowledge(
        name=name,
        source=source,
        vector_db_config=vector_db_config,
        vectorize_column=vectorize_column,
        timestamp_field=timestamp_field,
        batch_schedule=timedelta(days=1),
        batch_trigger=BatchTriggerType.MANUAL,
        feature_start_time=start,
        environment=_MOCK_BATCH_FEATURE_VIEW_ENVIRONMENT,
    )
    bfv = k[0]
    bfv.run_transformation(start, end).to_pandas()  # force transformation to run
    return k


def _to_df(data: Any) -> pd.DataFrame:
    if isinstance(data, pd.DataFrame):
        return data
    if isinstance(data, dict):
        return pd.DataFrame([data])
    if isinstance(data, list):
        return pd.DataFrame(data)
    raise ValueError(f"Unsupported data type {type(data)}")
