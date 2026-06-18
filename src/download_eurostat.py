from itertools import product
from pathlib import Path
import json

import pandas as pd
import requests


API_URL = (
    "https://ec.europa.eu/eurostat/api/"
    "dissemination/statistics/1.0/data"
)

DATASET = "edat_lfse_24"

PARAMS = {
    "lang": "en",
    "freq": "A",
    "sex": "T",
    "age": "Y20-34",
    "duration": "Y1-3",
    "unit": "PC",
    "sinceTimePeriod": "2014"
}


def download_dataset(dataset: str, params: dict) -> dict:
    response = requests.get(
        f"{API_URL}/{dataset}",
        params=params,
        timeout=60
    )

    response.raise_for_status()
    return response.json()


def ordered_codes(data: dict, dimension: str) -> list[str]:
    category = data["dimension"][dimension]["category"]
    index = category["index"]

    if isinstance(index, list):
        return index

    return [
        code
        for code, position in sorted(
            index.items(),
            key=lambda item: item[1]
        )
    ]


def jsonstat_to_dataframe(data: dict) -> pd.DataFrame:
    dimensions = data["id"]

    dimension_codes = {
        dimension: ordered_codes(data, dimension)
        for dimension in dimensions
    }

    combinations = list(
        product(*[dimension_codes[d] for d in dimensions])
    )

    values = data["value"]
    rows = []

    for position, combination in enumerate(combinations):
        if isinstance(values, list):
            value = values[position] if position < len(values) else None
        else:
            value = values.get(str(position))

        if value is None:
            continue

        row = dict(zip(dimensions, combination))
        row["value"] = value
        rows.append(row)

    return pd.DataFrame(rows)


def add_labels(df: pd.DataFrame, data: dict) -> pd.DataFrame:
    result = df.copy()

    for dimension in data["id"]:
        labels = (
            data["dimension"][dimension]["category"]
            .get("label", {})
        )

        result[f"{dimension}_label"] = (
            result[dimension].map(labels)
        )

    return result


def main() -> None:
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")

    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    data = download_dataset(DATASET, PARAMS)

    with open(
        raw_dir / f"{DATASET}.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    df = jsonstat_to_dataframe(data)
    df = add_labels(df, data)

    output_file = processed_dir / "recent_graduates_all_countries.csv"
    df.to_csv(output_file, index=False)

    print(df.info())
    print("\nFirst rows:")
    print(df.head())

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nUnique values per dimension:")

    for dimension in data["id"]:
        columns = [dimension, f"{dimension}_label"]

        print(f"\n{dimension}")
        print(df[columns].drop_duplicates().to_string(index=False))

    print(f"\nSaved: {output_file}")


if __name__ == "__main__":
    main()