#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import logging
from typing import Optional

import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://pokeapi.co/api/v2/"


def build_pokemon_url(pokemon_name: str) -> str:
    return f"{BASE_URL}pokemon/{pokemon_name}"


def get_pokemon_info(
    pokemon_name: str,
    *,
    timeout: float = 10.0,
    session: Optional[requests.Session] = None,
) -> Optional[dict]:
    url = build_pokemon_url(pokemon_name)
    sess = session or requests.Session()
    try:
        resp = sess.get(url, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        return data
    except requests.exceptions.RequestException as exc:
        logger.error("Failed to retrieve data for %s: %s", pokemon_name, exc)
        return None


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fetch basic Pokémon information from PokeAPI.",
    )
    parser.add_argument(
        "name", nargs="?", default="gyarados", help="Pokémon name (default: gyarados)"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="HTTP timeout in seconds (default: 10.0)",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s]: %(message)s",
    )

    info = get_pokemon_info(args.name, timeout=args.timeout)
    if not info:
        logger.error("No information returned for %s", args.name)
        return 1

    print(f"{info['name']} - Height: {info['height']}, Weight: {info['weight']}")
    return 0


pokemon_name = "gyarados"
if __name__ == "__main__":
    raise SystemExit(main())
