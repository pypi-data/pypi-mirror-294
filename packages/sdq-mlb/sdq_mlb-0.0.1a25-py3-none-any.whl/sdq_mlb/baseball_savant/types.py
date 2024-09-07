from typing import TypedDict


__all__: list[str] = ["HittingStats", "PitchingStats", "StatCast", "StacastRanking"]


StacastRanking = TypedDict(
    "StacastRanking",
    {
        "Season": str,
        "Age": int,
        "Pitches": int,
        "Batted Balls": int,
        "Barrels": int,
        "Barrel %": float,
        "Barrel/PA": float,
        "Exit Velocity": float,
        "Max EV": float,
        "Launch Angle": float,
        "LA Sweet-Spot %": float,
        "XBA": float,
        "XSLG": float,
        "WOBA": float,
        "XWOBA": float,
        "XWOBACON": float,
        "HardHit%": float,
        "K%": float,
        "BB%": float,
        "ERA": float,
        "xERA": float,
    },
    total=False,
)


PitchingStats = TypedDict(
    "PitchingStats",
    {
        "Season": str,
        "Tm": str,
        "LG": str,
        "BF": int,
        "W": int,
        "L": int,
        "ERA": float,
        "G": int,
        "GS": int,
        "SV": int,
        "IP": float,
        "H": int,
        "R": int,
        "ER": int,
        "HR": int,
        "BB": int,
        "SO": int,
        "WHIP": float,
    },
    total=False,
)

HittingStats = TypedDict(
    "HittingStats",
    {
        "Season": str,
        "LG": int,
        "G": int,
        "PA": int,
        "AB": int,
        "R": int,
        "H": int,
        "2B": int,
        "3B": int,
        "HR": int,
        "RBI": int,
        "BB": int,
        "SO": int,
        "SB": int,
        "CS": int,
        "HBP": int,
        "AVG": float,
        "OBP": float,
        "SLG": float,
        "OPS": float,
    },
    total=False,
)


class StatCast(TypedDict):
    hitting: dict[str, HittingStats]
    pitching: dict[str, PitchingStats]
    ranking: dict[str, StacastRanking]
