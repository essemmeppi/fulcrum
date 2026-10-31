"""Validate a hand- or agent-written survey file against its schema and print its tier.

Usage:
  python -m survey.validate country fi
  python -m survey.validate authority fi kela
  python -m survey.validate service fi-kela-general-housing-allowance
"""

import json
import sys
from pathlib import Path

from pydantic import ValidationError

from .schema import LAYERS, AuthorityProfile, CountryProfile, ServiceSourceSet, scores_dict, tier_for

SURVEY = Path(__file__).resolve().parent


def main(argv: list[str]) -> None:
    kind, *rest = argv
    if kind == "country":
        path, model = SURVEY / "countries" / f"{rest[0]}.json", CountryProfile
    elif kind == "authority":
        path, model = SURVEY / "authorities" / rest[0] / f"{rest[1]}.json", AuthorityProfile
    else:
        path, model = SURVEY / "services" / f"{rest[0]}.json", ServiceSourceSet
    try:
        obj = model.model_validate_json(path.read_text())
    except (ValidationError, json.JSONDecodeError) as e:
        print(f"INVALID {path}:\n{e}")
        sys.exit(1)
    s = scores_dict(obj.layer_scores)
    missing = [l for l in LAYERS if l not in {x.layer for x in obj.layer_scores}]
    if missing:
        print(f"INVALID {path}: layer_scores missing {missing}")
        sys.exit(1)
    # normalise: rewrite the file through the model so field order and defaults are canonical
    path.write_text(obj.model_dump_json(indent=2))
    extra = ""
    if kind == "country":
        extra = f", {len(obj.authorities)} authorities, {len(obj.evidence)} evidence entries"
    elif kind == "authority":
        extra = f", {len(obj.services)} services, {len(obj.internal_documents)} internal documents"
    else:
        extra = f", {len(obj.sources)} sources"
    print(f"OK {path.name}: tier {tier_for(s)} scores {s}{extra}")


if __name__ == "__main__":
    main(sys.argv[1:])
