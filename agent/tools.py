"""
Agent Tools — Netflix data tools with optional Headroom compression.
Each tool returns JSON (the kind of bloated output that wastes tokens).
"""

import json
import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "netflix_titles.csv"
_df = None


def _load_data() -> pd.DataFrame:
    global _df
    if _df is None:
        _df = pd.read_csv(DATA_PATH)
    return _df


def search_titles(query: str, limit: int = 10) -> dict:
    """Search Netflix titles by keyword in title, description, or cast."""
    df = _load_data()
    mask = (
        df["title"].str.contains(query, case=False, na=False)
        | df["description"].str.contains(query, case=False, na=False)
        | df["cast"].str.contains(query, case=False, na=False)
    )
    results = df[mask].head(limit)
    return {
        "status": "success",
        "query": query,
        "total_matches": int(mask.sum()),
        "returned": len(results),
        "results": results.to_dict(orient="records"),
    }


def filter_by_genre(genre: str, content_type: str = None, limit: int = 10) -> dict:
    """Filter titles by genre/category."""
    df = _load_data()
    mask = df["listed_in"].str.contains(genre, case=False, na=False)
    if content_type:
        mask &= df["type"].str.lower() == content_type.lower()
    results = df[mask].head(limit)
    return {
        "status": "success",
        "filters": {"genre": genre, "type": content_type},
        "total_matches": int(mask.sum()),
        "returned": len(results),
        "results": results.to_dict(orient="records"),
    }


def get_title_details(show_id: str) -> dict:
    """Get full details for a specific title."""
    df = _load_data()
    row = df[df["show_id"] == show_id]
    if row.empty:
        return {"status": "error", "message": f"Title {show_id} not found"}
    return {
        "status": "success",
        "data": row.iloc[0].to_dict(),
    }


def get_stats() -> dict:
    """Get overall Netflix catalog statistics."""
    df = _load_data()
    return {
        "status": "success",
        "total_titles": len(df),
        "movies": int((df["type"] == "Movie").sum()),
        "tv_shows": int((df["type"] == "TV Show").sum()),
        "countries": int(df["country"].nunique()),
        "years": {"min": int(df["release_year"].min()), "max": int(df["release_year"].max())},
        "top_directors": df["director"].value_counts().head(10).to_dict(),
        "top_genres": df["listed_in"].value_counts().head(10).to_dict(),
        "ratings": df["rating"].value_counts().to_dict(),
    }


def recommend(title_id: str, limit: int = 5) -> dict:
    """Recommend similar titles based on genre and type."""
    df = _load_data()
    row = df[df["show_id"] == title_id]
    if row.empty:
        return {"status": "error", "message": f"Title {title_id} not found"}

    source = row.iloc[0]
    same_genre = df[
        df["listed_in"].str.contains(source["listed_in"].split(",")[0].strip(), case=False, na=False)
        & (df["show_id"] != title_id)
    ]
    recommendations = same_genre.head(limit)
    return {
        "status": "success",
        "based_on": source["title"],
        "genre": source["listed_in"],
        "recommendations": recommendations[["show_id", "title", "type", "rating", "listed_in"]].to_dict(orient="records"),
    }


TOOLS = {
    "search_titles": search_titles,
    "filter_by_genre": filter_by_genre,
    "get_title_details": get_title_details,
    "get_stats": get_stats,
    "recommend": recommend,
}
