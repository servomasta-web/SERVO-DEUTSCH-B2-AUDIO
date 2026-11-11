import asyncio
import subprocess
import zipfile
from pathlib import Path
import edge_tts

ROOT = Path("output")
AUDIO = ROOT / "audio"
AUDIO.mkdir(parents=True, exist_ok=True)

# Examen 001 — textes repris de GoetheExamData.get(0), sans changement de contenu.
# Thème : Homeoffice und flexible Arbeitszeiten
TOPIC = "homeoffice und flexible arbeitszeiten"
CONTEXT = (
    "Ein kommunales Modellprojekt untersucht, wie Bürgerinnen und Bürger an "
    "Entscheidungen beteiligt werden können. Die Rückmeldungen fallen je nach "
    "Altersgruppe und Wohnort unterschiedlich aus."
)

tracks = {
    "teil1_01.mp3": [
        ("de-DE-KatjaNeural", "Guten Morgen zusammen. Wegen einer technischen Störung in unserem Bürogebäude findet die heutige Teamsitzung nicht im Besprechungsraum statt. Wir treffen uns wie geplant um halb zehn, allerdings per Videokonferenz. Den Zugangslink finden Sie in der Nachricht, die ich gestern Abend verschickt habe. Wer Präsentationsunterlagen zeigen möchte, sollte sie vorher öffnen.")
    ],
    "teil1_02.mp3": [
        ("de-DE-KatjaNeural", "Ich würde gern ab September an vier Tagen pro Woche arbeiten. Meine Aufgaben lassen sich gut bündeln."),
        ("de-DE-ConradNeural", "Grundsätzlich kann ich mir das vorstellen. Wir sollten aber zunächst drei Monate testen, ob die Erreichbarkeit für unsere Kundschaft gewährleistet bleibt."),
        ("de-DE-KatjaNeural", "Damit bin ich einverstanden. Ich könnte montags bis donnerstags jeweils etwas länger arbeiten.")
    ],
    "teil1_03.mp3": [
        ("de-DE-KatjaNeural", "Ab kommenden Monat können Beschäftigte die kleinen Gesprächsräume über das interne Buchungssystem reservieren. Die Reservierung ist frühestens sieben Tage im Voraus möglich und gilt jeweils für höchstens neunzig Minuten. Wer vertrauliche Kundengespräche führt, soll ausdrücklich einen geschlossenen Raum auswählen.")
    ],
    "teil1_04.mp3": [
        ("de-DE-ConradNeural", "Als ich vor einem Jahr ins Unternehmen kam, arbeitete fast das ganze Team von verschiedenen Orten aus. Am Anfang fiel es mir schwer, die richtigen Ansprechpartner zu finden. Besonders geholfen hat mir eine Kollegin, die sich jeden Freitag eine halbe Stunde Zeit für meine Fragen nahm. Inzwischen fühle ich mich gut eingebunden.")
    ],
    "teil1_05.mp3": [
        ("de-DE-KatjaNeural", "Eine kurze Information für alle: Der gemeinsame Präsenztag wird in der nächsten Woche ausnahmsweise vom Mittwoch auf Donnerstag verlegt. Bitte bringen Sie Ihren Mitarbeiterausweis mit, denn der Empfang ist an diesem Tag nur bis 17 Uhr besetzt. Die übrigen Homeoffice-Regelungen bleiben unverändert.")
    ],
    "teil2_01.mp3": [
        ("de-DE-KatjaNeural", "Willkommen bei Arbeit im Wandel. Heute geht es um die Frage, wie Beschäftigte im Homeoffice gesund und produktiv bleiben können. Frau Professorin Neumann, viele Unternehmen bieten inzwischen flexible Arbeitsorte an. Ist das automatisch ein Vorteil?"),
        ("de-DE-AmalaNeural", "Nicht unbedingt. Flexibilität kann den Alltag erleichtern, aber sie verlangt auch Selbstorganisation. Wer zu Hause arbeitet, muss beispielsweise bewusste Pausen einplanen. Sonst verschwimmen die Grenzen zwischen Beruf und Freizeit."),
        ("de-DE-KatjaNeural", "Welche Schwierigkeiten beobachten Sie besonders häufig?"),
        ("de-DE-AmalaNeural", "Viele Menschen unterschätzen die Bedeutung eines geeigneten Arbeitsplatzes. Ein Küchentisch ist für eine kurze Aufgabe in Ordnung, aber nicht unbedingt für acht Stunden Bildschirmarbeit. Außerdem fehlt manchen der spontane Austausch mit Kolleginnen und Kollegen."),
        ("de-DE-KatjaNeural", "Was können Betriebe konkret tun?"),
        ("de-DE-AmalaNeural", "Sie sollten klare Erreichbarkeitszeiten vereinbaren und Führungskräfte darin schulen, Ergebnisse statt bloßer Anwesenheit zu bewerten. Sinnvoll sind außerdem regelmäßige Gespräche, in denen nicht nur über Aufgaben, sondern auch über Belastungen gesprochen wird."),
        ("de-DE-KatjaNeural", "Bedeutet das, dass alle Beschäftigten gleich viele Tage zu Hause arbeiten sollten?"),
        ("de-DE-AmalaNeural", "Nein. Die passende Lösung hängt von der Tätigkeit, der Wohnsituation und den persönlichen Bedürfnissen ab. Wichtig ist, dass Regeln gemeinsam entwickelt und nach einer gewissen Zeit überprüft werden.")
    ],
    "teil3_01.mp3": [
        ("de-DE-KatjaNeural", "In unserem heutigen Gespräch diskutieren wir, ob Unternehmen feste gemeinsame Bürotage einführen sollten. Herr Yilmaz, Sie leiten ein Team, das überwiegend digital zusammenarbeitet."),
        ("de-DE-KillianNeural", "Ich bin für einen gemeinsamen Tag pro Woche. Bei komplizierten Projekten entstehen Missverständnisse oft schneller, wenn man sich nur über Nachrichten austauscht. Ein persönliches Treffen hilft, offene Fragen direkt zu klären."),
        ("de-DE-KatjaNeural", "Frau Roth, sehen Sie das ähnlich?"),
        ("de-DE-AmalaNeural", "Teilweise. Für neue Kolleginnen und Kollegen ist der persönliche Kontakt wichtig. Trotzdem halte ich einen verpflichtenden Tag für problematisch. Einige wohnen weit entfernt oder betreuen Angehörige. Ein zusätzlicher Fahrtweg kann den angeblichen Zeitgewinn zunichtemachen."),
        ("de-DE-KatjaNeural", "Herr Yilmaz, könnte man die Teilnahme freiwillig machen?"),
        ("de-DE-KillianNeural", "Dann kommen möglicherweise gerade diejenigen nicht, die besonders von einem Austausch profitieren würden. Ich könnte mir aber vorstellen, dass Teams den Tag selbst festlegen."),
        ("de-DE-AmalaNeural", "Das wäre ein vernünftiger Kompromiss. Außerdem sollte es Ausnahmen geben, wenn jemand an diesem Tag konzentriert an einer Aufgabe arbeiten muss."),
        ("de-DE-KatjaNeural", "Wir halten also fest: Gemeinsame Präsenz kann die Zusammenarbeit stärken, sollte jedoch flexibel organisiert werden und persönliche Lebensumstände berücksichtigen.")
    ],
    "teil4_01.mp3": [
        ("de-DE-ConradNeural", "Guten Tag. In meinem Vortrag möchte ich zeigen, wie Teams die Zusammenarbeit organisieren können, wenn ihre Mitglieder nicht am selben Ort arbeiten. Zunächst sollte man unterscheiden, welche Aufgaben direkte Abstimmung benötigen und welche unabhängig erledigt werden können. Eine kurze Rückfrage lässt sich oft schriftlich klären; bei einem Konflikt mit mehreren Beteiligten ist ein Gespräch dagegen meist effizienter."),
        ("de-DE-ConradNeural", "Ein zweiter Punkt betrifft die Kommunikation. Wenn jede Kleinigkeit sofort beantwortet werden muss, werden Beschäftigte ständig unterbrochen. Deshalb empfiehlt es sich, feste Zeitfenster für Nachrichten einzurichten und dringende Anliegen eindeutig zu kennzeichnen."),
        ("de-DE-ConradNeural", "Auch die Dokumentation darf nicht vernachlässigt werden. Entscheidungen sollten an einem gemeinsamen Ort festgehalten werden, damit neue Teammitglieder den Hintergrund nachvollziehen können. Eine lange Nachrichtensammlung ersetzt jedoch keine verständliche Zusammenfassung."),
        ("de-DE-ConradNeural", "Schließlich braucht ein verteiltes Team Vertrauen. Führungskräfte sollten nicht kontrollieren, ob jemand ständig online ist, sondern vereinbarte Ergebnisse besprechen. Gleichzeitig müssen Beschäftigte frühzeitig mitteilen, wenn Termine unrealistisch werden. So lassen sich Aufgaben neu verteilen, bevor unnötiger Druck entsteht.")
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

archive = ROOT / "exam-001.zip"
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
