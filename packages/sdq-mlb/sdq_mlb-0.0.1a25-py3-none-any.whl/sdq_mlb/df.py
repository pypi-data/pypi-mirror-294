import math
from dataclasses import dataclass, field
import polars as pl
from .db import Client as DBClient
from .utils import get_mlb_full_df


@dataclass
class PlayerDataFrame:
    db_client: DBClient = field(default_factory=DBClient)
    df: pl.DataFrame = field(default_factory=get_mlb_full_df)

    def abhr(self) -> pl.DataFrame:
        return (
            self.df.with_columns((pl.col("ab") / pl.col("hr")).alias("ab/hr"))
            .filter(
                pl.col("ab/hr").is_not_null()
                & pl.col("ab/hr").is_not_nan()
                & (pl.col("ab/hr") != math.inf)
                & (pl.col("pa") > 3000)
            )
            .sort("ab/hr")
        )
