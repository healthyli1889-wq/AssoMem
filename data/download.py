"""
Download the four REAL base datasets into data/raw/.

    python data/download.py --all
    python data/download.py --datasets personamem locomo

Verified sources (June 2026):
  PersonaMem   HF: bowen-upenn/PersonaMem        https://huggingface.co/datasets/bowen-upenn/PersonaMem
               GH: https://github.com/bowen-upenn/PersonaMem   (MIT)
  LoCoMo       GH: https://github.com/snap-research/locomo     (data/locomo10.json)
  PerLTQA      GH: https://github.com/Elvin-Yiming-Du/PerLTQA  (data/ JSON)
  MemoryArena  HF: ZexueHe/memoryarena           https://huggingface.co/datasets/ZexueHe/memoryarena
               configs: bundled_shopping, progressive_search, group_travel_planner,
                        formal_reasoning_math, formal_reasoning_phys

Requires: `pip install datasets` and `git` on PATH. Each downloader is independent and
fails loudly with the manual URL if the automatic path is unavailable.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
MEMARENA_CONFIGS = ["bundled_shopping", "progressive_search", "group_travel_planner",
                    "formal_reasoning_math", "formal_reasoning_phys"]


def _ensure(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _git_clone(url: str, dest: str) -> None:
    if os.path.exists(dest):
        print(f"  [skip] {dest} already exists")
        return
    print(f"  git clone {url}")
    subprocess.run(["git", "clone", "--depth", "1", url, dest], check=True)


def get_personamem() -> None:
    print("[PersonaMem]")
    _ensure(RAW)
    try:
        from datasets import load_dataset
        ds = load_dataset("bowen-upenn/PersonaMem")
        out = os.path.join(RAW, "personamem")
        _ensure(out)
        for split in ds:
            ds[split].to_json(os.path.join(out, f"{split}.jsonl"))
        print(f"  saved -> {out}")
    except Exception as e:
        print(f"  [warn] HF load failed ({e}). Falling back to git clone of the repo.")
        _git_clone("https://github.com/bowen-upenn/PersonaMem", os.path.join(RAW, "PersonaMem"))


def get_locomo() -> None:
    print("[LoCoMo]")
    _ensure(RAW)
    _git_clone("https://github.com/snap-research/locomo", os.path.join(RAW, "locomo"))
    f = os.path.join(RAW, "locomo", "data", "locomo10.json")
    print(f"  data file: {f}  exists={os.path.exists(f)}")


def get_perltqa() -> None:
    print("[PerLTQA]")
    _ensure(RAW)
    _git_clone("https://github.com/Elvin-Yiming-Du/PerLTQA", os.path.join(RAW, "PerLTQA"))


def get_memoryarena() -> None:
    print("[MemoryArena]")
    _ensure(RAW)
    out = os.path.join(RAW, "memoryarena")
    _ensure(out)
    try:
        from datasets import load_dataset
        for cfg in MEMARENA_CONFIGS:
            try:
                ds = load_dataset("ZexueHe/memoryarena", cfg)
                for split in ds:
                    ds[split].to_json(os.path.join(out, f"{cfg}_{split}.jsonl"))
                print(f"  saved config {cfg}")
            except Exception as e:
                print(f"  [warn] config {cfg} failed: {e}")
    except Exception as e:
        print(f"  [warn] datasets not available ({e}); see "
              f"https://huggingface.co/datasets/ZexueHe/memoryarena")


REGISTRY = {"personamem": get_personamem, "locomo": get_locomo,
            "perltqa": get_perltqa, "memoryarena": get_memoryarena}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--datasets", nargs="*", default=[], choices=list(REGISTRY))
    args = ap.parse_args()
    targets = list(REGISTRY) if args.all or not args.datasets else args.datasets
    for t in targets:
        try:
            REGISTRY[t]()
        except subprocess.CalledProcessError as e:
            print(f"  [error] {t}: git failed ({e}). Install git or clone manually.")
        except Exception as e:
            print(f"  [error] {t}: {e}")
    print("\nDone. Raw data in:", RAW)


if __name__ == "__main__":
    main()
