#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the 30 SERVO DEUTSCH B2 Hören packs from the app's authoritative Java texts.

Run from this repository:
  python rebuild_all_30_from_app.py --app-root /path/to/SERVO-DEUTSCH-B2 --all
  python rebuild_all_30_from_app.py --app-root /path/to/SERVO-DEUTSCH-B2-7.2.0 --exam 9

Requirements: Python 3.10+, edge-tts, ffmpeg (including ffprobe).
The generated ZIP contains exactly the eight MP3 files expected by the Android app.
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

import edge_tts

VOICES = ("de-DE-KatjaNeural", "de-DE-ConradNeural", "de-DE-AmalaNeural", "de-DE-KillianNeural")
EXPECTED = [f"teil1_0{i}.mp3" for i in range(1, 6)] + ["teil2_01.mp3", "teil3_01.mp3", "teil4_01.mp3"]


def decode_java_string(raw: str) -> str:
    """Decode the Java string escapes used in the app source."""
    try:
        return json.loads('"' + raw + '"')
    except json.JSONDecodeError as exc:
        raise ValueError(f"Unsupported Java string escape: {raw[:80]!r}") from exc


def quoted_literals(source: str) -> list[str]:
    values = []
    i = 0
    while i < len(source):
        if source[i] != '"':
            i += 1
            continue
        i += 1
        start = i
        escaped = False
        while i < len(source):
            ch = source[i]
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                values.append(decode_java_string(source[start:i]))
                i += 1
                break
            i += 1
        else:
            raise ValueError("Unterminated Java string literal")
    return values


def statement_end(source: str, start: int, array: bool = False) -> int:
    quoted = False
    escaped = False
    depth = 1 if array else 0
    for i in range(start, len(source)):
        ch = source[i]
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
            continue
        if ch == '"':
            quoted = True
        elif array and ch == "{":
            depth += 1
        elif array and ch == "}":
            depth -= 1
            if depth == 0:
                return i
        elif not array and ch == ";":
            return i
    raise ValueError("Could not find the end of a Java declaration")


def extract_first_audio_array(source: str) -> tuple[str, list[str]]:
    build = source.find("static GoetheExamData.Part[] build")
    if build < 0:
        raise ValueError("build() method not found")
    match = re.search(r"String\[\]\s+(\w+)\s*=\s*\{", source[build:])
    if not match:
        raise ValueError("Part 1 short-audio array not found")
    name = match.group(1)
    start = build + match.end()
    end = statement_end(source, start, array=True)
    values = quoted_literals(source[start:end])
    if len(values) != 5:
        raise ValueError(f"Expected five Teil-1 audio texts, found {len(values)} in {name}")
    return name, values


def extract_string_variable(source: str, name: str) -> str:
    match = re.search(rf"\bString\s+{re.escape(name)}\s*=", source)
    if not match:
        raise ValueError(f"String {name} declaration not found")
    start = match.end()
    end = statement_end(source, start, array=False)
    value = "".join(quoted_literals(source[start:end])).strip()
    if len(value) < 120:
        raise ValueError(f"Extracted {name} text is unexpectedly short ({len(value)} chars)")
    return value


def voice_for_speaker(label: str, mapping: dict[str, str]) -> str:
    key = re.sub(r"\s+", " ", label.strip().lower())
    if key in mapping:
        return mapping[key]
    if key in ("a", "moderatorin") or "moderatorin" in key or "frau " in key or key.endswith("in"):
        voice = "de-DE-KatjaNeural" if key == "moderatorin" else "de-DE-AmalaNeural"
    elif key in ("b", "moderator") or "moderator" in key or "herr " in key:
        voice = "de-DE-ConradNeural"
    else:
        used = set(mapping.values())
        voice = next((v for v in ("de-DE-AmalaNeural", "de-DE-KillianNeural", "de-DE-ConradNeural") if v not in used), "de-DE-KillianNeural")
    mapping[key] = voice
    return voice


def short_utterances(text: str, index: int) -> list[tuple[str, str]]:
    """Preserve announcements; only split explicit A/B dialogue labels."""
    base = VOICES[index % len(VOICES)]
    pieces = re.split(r"(?=\s+[AB]:\s*)", text.strip())
    out = []
    for piece in pieces:
        piece = piece.strip()
        match = re.match(r"^([AB]):\s*(.*)$", piece, flags=re.S)
        if match:
            speaker = match.group(1)
            spoken = match.group(2).strip()
            voice = "de-DE-KatjaNeural" if speaker == "A" else "de-DE-ConradNeural"
        else:
            spoken = piece
            voice = base
        if spoken:
            out.append((voice, spoken))
    return out


def dialogue_utterances(text: str, moderator_default: str) -> list[tuple[str, str]]:
    mapping: dict[str, str] = {}
    out = []
    for line in (part.strip() for part in text.splitlines()):
        if not line:
            continue
        match = re.match(r"^([^:]{1,45}):\s*(.*)$", line, flags=re.S)
        if match:
            label, spoken = match.group(1).strip(), match.group(2).strip()
            voice = voice_for_speaker(label, mapping)
        else:
            spoken = line
            voice = moderator_default if not out else VOICES[len(out) % len(VOICES)]
        if spoken:
            out.append((voice, spoken))
    if not out:
        raise ValueError("Dialogue contains no speakable text")
    return out


def extract_exam_tracks(app_root: Path, exam: int) -> tuple[dict[str, list[tuple[str, str]]], str]:
    source_path = app_root / "app/src/main/java/com/servo/deutschb2" / f"GoetheExam{exam:02d}Audio.java"
    if not source_path.is_file():
        raise FileNotFoundError(f"Missing app source: {source_path}")
    source = source_path.read_text(encoding="utf-8")
    array_name, short_texts = extract_first_audio_array(source)
    interview = extract_string_variable(source, "interview")
    panel = extract_string_variable(source, "panel")
    lecture = extract_string_variable(source, "lecture")

    tracks: dict[str, list[tuple[str, str]]] = {}
    for i, text in enumerate(short_texts, start=1):
        tracks[f"teil1_0{i}.mp3"] = short_utterances(text, i - 1)
    tracks["teil2_01.mp3"] = dialogue_utterances(interview, "de-DE-KatjaNeural")
    tracks["teil3_01.mp3"] = dialogue_utterances(panel, "de-DE-ConradNeural")
    tracks["teil4_01.mp3"] = [("de-DE-AmalaNeural", lecture)]
    if set(tracks) != set(EXPECTED):
        raise ValueError(f"Exam {exam:03d}: unexpected track set")
    if any(not items or any(not voice or not text.strip() for voice, text in items) for items in tracks.values()):
        raise ValueError(f"Exam {exam:03d}: empty utterance detected")
    combined = json.dumps({k: v for k, v in tracks.items()}, ensure_ascii=False, sort_keys=True)
    return tracks, hashlib.sha256(combined.encode("utf-8")).hexdigest()


async def synthesize_track(target: Path, utterances: list[tuple[str, str]]) -> None:
    pieces: list[Path] = []
    for i, (voice, spoken_text) in enumerate(utterances):
        part = target.parent / f".{target.stem}.{i:03d}.mp3"
        last_error = None
        for attempt in range(1, 4):
            try:
                await edge_tts.Communicate(spoken_text, voice, rate="-4%").save(str(part))
                if not part.is_file() or part.stat().st_size < 500:
                    raise RuntimeError("Generated audio is missing or too small")
                last_error = None
                break
            except Exception as exc:
                last_error = exc
                part.unlink(missing_ok=True)
                if attempt < 3:
                    await asyncio.sleep(attempt * 2)
        if last_error:
            raise RuntimeError(f"TTS failed for {target.name}, utterance {i + 1}") from last_error
        pieces.append(part)
        if i < len(utterances) - 1:
            silence = target.parent / f".{target.stem}.silence.{i:03d}.mp3"
            subprocess.run(
                ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", "0.55",
                 "-codec:a", "libmp3lame", "-b:a", "64k", str(silence)],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            pieces.append(silence)

    listing = target.parent / f".{target.stem}.concat.txt"
    listing.write_text("".join(f"file '{p.resolve()}'\n" for p in pieces), encoding="utf-8")
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
             "-codec:a", "libmp3lame", "-b:a", "128k", str(target)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    finally:
        for path in pieces + [listing]:
            path.unlink(missing_ok=True)
    if not target.is_file() or target.stat().st_size < 1024:
        raise RuntimeError(f"Invalid MP3 output: {target}")


def media_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    duration = float(result.stdout.strip())
    if not (1.0 <= duration <= 900.0):
        raise ValueError(f"Unreasonable audio duration for {path.name}: {duration:.2f}s")
    return duration


async def build_exam(app_root: Path, exam: int, output_root: Path) -> dict:
    if not 1 <= exam <= 30:
        raise ValueError("Only exams 001 through 030 are supported")
    tracks, source_hash = extract_exam_tracks(app_root, exam)
    exam_dir = output_root / f"exam-{exam:03d}"
    audio_dir = exam_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "exam": exam,
        "source": f"GoetheExam{exam:02d}Audio.java",
        "source_text_sha256": source_hash,
        "voice_type": "German neural TTS (Edge TTS)",
        "track_count": 8,
        "tracks": {},
    }
    for name in EXPECTED:
        target = audio_dir / name
        await synthesize_track(target, tracks[name])
        duration = media_duration(target)
        manifest["tracks"][name] = {
            "utterances": len(tracks[name]),
            "characters": sum(len(text) for _, text in tracks[name]),
            "bytes": target.stat().st_size,
            "duration_seconds": round(duration, 2),
        }
        print(f"EXAM {exam:03d}  {name}  {duration:.1f}s  {target.stat().st_size} bytes", flush=True)

    archive = output_root / f"exam-{exam:03d}.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in EXPECTED:
            zf.write(audio_dir / name, arcname=name)
    with zipfile.ZipFile(archive) as zf:
        if sorted(zf.namelist()) != sorted(EXPECTED):
            raise RuntimeError(f"Exam {exam:03d}: ZIP must contain exactly eight expected MP3s")
        if zf.testzip() is not None:
            raise RuntimeError(f"Exam {exam:03d}: ZIP CRC check failed")
        if any(item.file_size < 1024 for item in zf.infolist()):
            raise RuntimeError(f"Exam {exam:03d}: empty or undersized MP3 in ZIP")
    manifest["archive"] = archive.name
    manifest["archive_bytes"] = archive.stat().st_size
    (output_root / f"exam-{exam:03d}.manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"VALIDATED {archive} ({archive.stat().st_size} bytes)", flush=True)
    return manifest


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Rebuild SERVO DEUTSCH B2 Hören audio from app source")
    parser.add_argument("--app-root", type=Path, default=Path(os.environ.get("SERVO_APP_ROOT", "../SERVO-DEUTSCH-B2")))
    parser.add_argument("--output", type=Path, default=Path("output"))
    parser.add_argument("--exam", type=int, action="append", help="Exam number 1-30; may be repeated")
    parser.add_argument("--all", action="store_true", help="Build all 30 exams")
    args = parser.parse_args(argv)

    app_root = args.app_root.expanduser().resolve()
    output_root = args.output.expanduser().resolve()
    if not (app_root / "app/src/main/java/com/servo/deutschb2").is_dir():
        raise SystemExit(f"App source directory not found under {app_root}. Pass --app-root.")
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        raise SystemExit("ffmpeg and ffprobe must both be installed and available on PATH.")
    exams = list(range(1, 31)) if args.all or not args.exam else sorted(set(args.exam))
    if any(not 1 <= n <= 30 for n in exams):
        raise SystemExit("Only exams 001-030 are supported.")
    output_root.mkdir(parents=True, exist_ok=True)

    async def run_all():
        results = []
        for number in exams:
            results.append(await build_exam(app_root, number, output_root))
        report = {
            "exam_count": len(results),
            "total_tracks": sum(item["track_count"] for item in results),
            "voice_type": "German neural TTS (Edge TTS)",
            "exams": [{"exam": item["exam"], "archive": item["archive"], "archive_bytes": item["archive_bytes"],
                       "source_text_sha256": item["source_text_sha256"]} for item in results],
        }
        (output_root / "audio-build-report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"BUILD COMPLETE: {len(results)} exams / {sum(x['track_count'] for x in results)} tracks", flush=True)

    asyncio.run(run_all())


if __name__ == "__main__":
    main()
