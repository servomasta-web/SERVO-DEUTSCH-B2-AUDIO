#!/usr/bin/env python3
"""Reject duplicated or near-duplicated listening scripts across exam generators."""
import ast
import difflib
import json
import re
import sys
from pathlib import Path

FILES = sorted(Path(".").glob("build_exam_*_aligned.py"))
THRESHOLD = 0.92


def norm(text):
    text = text.lower()
    text = re.sub(r"[^a-zäöüß0-9<>]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def value(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name):
        if node.id == "TOPIC":
            return "<TOPIC>"
        if node.id == "CONTEXT":
            return "<CONTEXT>"
        raise ValueError(f"Unexpected name in audio text: {node.id}")
    if isinstance(node, ast.JoinedStr):
        return "".join(value(part) if not isinstance(part, ast.FormattedValue)
                       else value(part.value) for part in node.values)
    if isinstance(node, ast.FormattedValue):
        return value(node.value)
    raise ValueError(f"Unsupported audio expression: {ast.dump(node)[:180]}")


def load_tracks(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    assign = next(n for n in tree.body if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == "tracks" for t in n.targets))
    result = {}
    for key, utterances in assign.value.keys, assign.value.values:
        pass
    for key_node, utterances_node in zip(assign.value.keys, assign.value.values):
        filename = ast.literal_eval(key_node)
        texts = []
        for item in utterances_node.elts:
            # Each item is (voice, text).
            texts.append(value(item.elts[1]))
        result[filename] = norm(" ".join(texts))
    return result


def main():
    if len(FILES) < 2:
        print("Duplicate audit needs at least two exam generators.")
        return 0
    packs = {p.name: load_tracks(p) for p in FILES}
    problems = []
    names = list(packs)
    for i, left_name in enumerate(names):
        for right_name in names[i + 1:]:
            common = sorted(set(packs[left_name]) & set(packs[right_name]))
            for track in common:
                left, right = packs[left_name][track], packs[right_name][track]
                ratio = difflib.SequenceMatcher(None, left, right).ratio()
                if ratio >= THRESHOLD:
                    problems.append((left_name, right_name, track, ratio))
    # Also catch repeated complete tracks inside one exam pack.
    for pack_name, tracks in packs.items():
        entries = list(tracks.items())
        for i, (left_file, left) in enumerate(entries):
            for right_file, right in entries[i + 1:]:
                ratio = difflib.SequenceMatcher(None, left, right).ratio()
                if ratio >= THRESHOLD:
                    problems.append((pack_name, pack_name, f"{left_file} / {right_file}", ratio))
    if problems:
        print("DUPLICATE / NEAR-DUPLICATE AUDIO CONTENT DETECTED:")
        for left, right, track, ratio in problems:
            print(f"- {left} <> {right} | {track} | similarity={ratio:.1%}")
        print("Publication blocked. Rewrite the content; changing only the theme is insufficient.")
        return 1
    print(f"Duplicate audit passed: {len(packs)} packs, no same-track similarity >= {THRESHOLD:.0%}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
