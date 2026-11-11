import asyncio
import subprocess
import zipfile
from pathlib import Path
import edge_tts

ROOT = Path("output")
AUDIO = ROOT / "audio"
AUDIO.mkdir(parents=True, exist_ok=True)

# Examen 002 — textes repris de GoetheExamData.get(1), sans changement de contenu.
# Thème : Nachhaltige Mobilität in Großstädten
TOPIC = "nachhaltige mobilität in großstädten"
CONTEXT = (
    "Ein unabhängiges Forschungszentrum vergleicht mehrere praktische Lösungen. "
    "Dabei werden Kosten, Alltagstauglichkeit und mögliche Nebenwirkungen getrennt bewertet. "
    "Im fiktiven Fallbeispiel zu „Nachhaltige Mobilität in Großstädten“ wurden 277 Personen aus "
    "4 Regionen einbezogen. Die Ergebnisse dienen als Grundlage für die folgenden Texte und Aufgaben."
)

tracks = {
    "teil1_01.mp3": [
        ("de-DE-KatjaNeural", f"Guten Tag. Der Informationsabend zum Thema {TOPIC} findet nicht wie angekündigt am Donnerstag, sondern am Freitag um 18 Uhr statt. Bitte melden Sie sich bis Mittwoch im Sekretariat an.")
    ],
    "teil1_02.mp3": [
        ("de-DE-KatjaNeural", f"Hast du schon von der neuen Regelung zu {TOPIC} gehört?"),
        ("de-DE-ConradNeural", "Ja, ich finde sie grundsätzlich sinnvoll. Allerdings sollten die Verantwortlichen zuerst eine Testphase durchführen."),
        ("de-DE-KatjaNeural", "Genau, danach können wir die Erfahrungen auswerten."),
        ("de-DE-ConradNeural", "Wichtig wäre mir außerdem, dass die Betroffenen rechtzeitig informiert werden.")
    ],
    "teil1_03.mp3": [
        ("de-DE-KatjaNeural", f"Die Stadtbibliothek erweitert ihr Angebot im Rahmen eines Projekts zu {TOPIC}. Ab nächster Woche können Besucherinnen und Besucher Medien auch online reservieren. Die Abholung bleibt während der normalen Öffnungszeiten möglich. Bei Fragen hilft das Personal am Informationsschalter.")
    ],
    "teil1_04.mp3": [
        ("de-DE-ConradNeural", f"Im Praktikum zu {TOPIC} war ich überrascht, wie viel Verantwortung ich übernehmen durfte. Natürlich musste ich auch einfache Aufgaben erledigen, aber besonders hilfreich waren die Gespräche mit meiner Betreuerin. Sie hat mir gezeigt, wie man Schwierigkeiten systematisch löst.")
    ],
    "teil1_05.mp3": [
        ("de-DE-KatjaNeural", f"Ein Hinweis für alle Fahrgäste: Wegen einer Baustelle im Zusammenhang mit {TOPIC} fährt die Linie 6 am Samstag nur bis zum Rathaus. Zum Bahnhof gelangen Sie mit dem Ersatzbus 16. Planen Sie bitte etwas mehr Zeit ein.")
    ],
    "teil2_01.mp3": [
        ("de-DE-KatjaNeural", f"Moderator: Heute sprechen wir über {TOPIC}. {CONTEXT} Frau Dr. Weber, Sie forschen zu diesem Thema. Warum ist es derzeit so aktuell?"),
        ("de-DE-AmalaNeural", "Expertin: Viele Veränderungen bieten Chancen, bringen aber auch neue Anforderungen mit sich. Entscheidend ist, dass die Menschen rechtzeitig informiert und an den Entscheidungen beteiligt werden."),
        ("de-DE-KatjaNeural", "Moderator: Welche Schwierigkeiten beobachten Sie?"),
        ("de-DE-AmalaNeural", "Expertin: Häufig fehlen Zeit und klare Zuständigkeiten. Außerdem werden die langfristigen Kosten manchmal unterschätzt."),
        ("de-DE-KatjaNeural", "Moderator: Was empfehlen Sie?"),
        ("de-DE-AmalaNeural", "Expertin: Zunächst sollte man verlässliche Informationen sammeln. Danach empfiehlt sich ein begrenzter Versuch, dessen Ergebnisse unabhängig ausgewertet werden. Erst dann sollte man über eine größere Einführung entscheiden."),
        ("de-DE-KatjaNeural", "Moderator: Welche Rolle spielt die Öffentlichkeit?"),
        ("de-DE-AmalaNeural", "Expertin: Eine sehr große. Akzeptanz entsteht durch Transparenz und die Möglichkeit, Fragen zu stellen. Eine Lösung ist nur dann dauerhaft erfolgreich, wenn sie praktisch umsetzbar ist und von den Betroffenen verstanden wird.")
    ],
    "teil3_01.mp3": [
        ("de-DE-KatjaNeural", f"Moderator: Willkommen zu unserer Diskussion über {TOPIC}. Ich moderiere das Gespräch und fasse am Ende die wichtigsten Punkte zusammen. Herr Braun, was ist Ihnen besonders wichtig?"),
        ("de-DE-KillianNeural", "Herr Braun: Entscheidend ist für mich eine verlässliche Finanzierung. Ohne realistische Kostenplanung und ausreichende Mittel scheitert selbst ein überzeugendes Vorhaben. Auch mögliche Folgekosten müssen von Anfang an berücksichtigt werden."),
        ("de-DE-AmalaNeural", "Frau Keller: Ich halte es für genauso wichtig, die betroffenen Menschen frühzeitig einzubeziehen. Sie kennen die Schwierigkeiten aus dem Alltag und können sagen, welche Lösungen tatsächlich funktionieren."),
        ("de-DE-KatjaNeural", "Moderator: Herr Braun, würden Sie also zuerst die Kosten prüfen?"),
        ("de-DE-KillianNeural", "Herr Braun: Ja. Ich würde einen Finanzplan erstellen und einen Puffer für unerwartete Ausgaben vorsehen."),
        ("de-DE-AmalaNeural", "Frau Keller: Und ich würde zuerst Gespräche mit den Betroffenen führen. Ihre Erfahrungen sollten bereits in die Planung einfließen."),
        ("de-DE-KatjaNeural", "Moderator: Zusammenfassend brauchen wir beides: eine solide Finanzierung und eine Planung, die sich an den Erfahrungen der Menschen orientiert.")
    ],
    "teil4_01.mp3": [
        ("de-DE-ConradNeural", f"Guten Tag. In meinem Vortrag geht es heute um {TOPIC}. {CONTEXT} Zunächst möchte ich betonen, dass gute Ergebnisse eine klare Zielsetzung voraussetzen. Wer mehrere Aufgaben gleichzeitig beginnt, verliert häufig den Überblick. Deshalb ist es sinnvoll, größere Vorhaben in überschaubare Schritte aufzuteilen."),
        ("de-DE-ConradNeural", "Ein weiterer wichtiger Punkt ist die Planung. Man sollte Prioritäten setzen und für anspruchsvolle Aufgaben ausreichend Zeit reservieren. Kurze Pausen helfen dabei, die Konzentration zu erhalten."),
        ("de-DE-ConradNeural", "Auch Informationen müssen sorgfältig geprüft werden. Nicht jede Nachricht ist zuverlässig oder für die eigene Entscheidung relevant. Es empfiehlt sich daher, verschiedene Quellen zu vergleichen."),
        ("de-DE-ConradNeural", "Zum Schluss: Veränderungen gelingen selten sofort. Wer die Ergebnisse regelmäßig überprüft, Rückmeldungen ernst nimmt und seine Vorgehensweise anpasst, kann langfristig bessere Lösungen erreichen. Dabei ist es wichtig, auch unerwartete Folgen zu dokumentieren und nicht nur positive Ergebnisse zu veröffentlichen. Nur so entsteht ein realistisches Bild der Situation.")
    ]
}

async def make_track(name, utterances):
    parts = []
    for i, (voice, spoken_text) in enumerate(utterances):
        part = AUDIO / f".{name}.{i:02d}.mp3"
        last_error = None
        for attempt in range(1, 6):
            try:
                print(f"{name}: réplique {i + 1}/{len(utterances)}, {voice}, essai {attempt}/5", flush=True)
                await edge_tts.Communicate(spoken_text, voice, rate="-4%").save(str(part))
                if not part.exists() or part.stat().st_size < 1000:
                    raise RuntimeError("Fichier audio absent ou trop petit")
                last_error = None
                break
            except Exception as exc:
                last_error = exc
                part.unlink(missing_ok=True)
                print(f"Erreur {name}, réplique {i + 1}, {voice}: {exc}", flush=True)
                if attempt < 5:
                    await asyncio.sleep(2 * attempt)
        if last_error is not None:
            raise RuntimeError(f"Échec définitif pour {name}, réplique {i + 1}") from last_error
        parts.append(part)
        await asyncio.sleep(1)
        if i < len(utterances) - 1:
            silence = AUDIO / f".silence_{name}_{i}.mp3"
            subprocess.run([
                "ffmpeg", "-y", "-f", "lavfi", "-i",
                "anullsrc=r=24000:cl=mono", "-t", "0.65",
                "-codec:a", "libmp3lame", "-b:a", "64k", str(silence)
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            parts.append(silence)

    listing = AUDIO / f".{name}.txt"
    listing.write_text("".join(f"file '{p.resolve()}'\n" for p in parts), encoding="utf-8")
    target = AUDIO / name
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
        "-codec:a", "libmp3lame", "-b:a", "128k", str(target)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    for part in parts + [listing]:
        part.unlink(missing_ok=True)
    if not target.exists() or target.stat().st_size < 1024:
        raise RuntimeError(f"Piste finale invalide : {name}")
    print(f"OK {name}: {target.stat().st_size} octets", flush=True)

async def main():
    for name, utterances in tracks.items():
        await make_track(name, utterances)

asyncio.run(main())

archive = ROOT / "exam-002.zip"
expected = [
    "teil1_01.mp3", "teil1_02.mp3", "teil1_03.mp3", "teil1_04.mp3",
    "teil1_05.mp3", "teil2_01.mp3", "teil3_01.mp3", "teil4_01.mp3"
]
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
    for name in expected:
        z.write(AUDIO / name, arcname=name)
with zipfile.ZipFile(archive) as z:
    actual = sorted(z.namelist())
    if sorted(expected) != actual:
        raise RuntimeError(f"Contenu ZIP inattendu : {actual}")
    for info in z.infolist():
        if info.file_size < 1024:
            raise RuntimeError(f"Piste ZIP invalide : {info.filename}")
print(f"Archive validée : {archive} ({archive.stat().st_size} octets)", flush=True)
