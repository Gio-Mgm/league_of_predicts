from pydantic import BaseModel


class Match(BaseModel):
    match_ID: int
    timeline: int
    who_win: str
    blue_kills_by_timeline: int
    red_kills_by_timeline: int
    blue_gold: int
    red_gold: int
