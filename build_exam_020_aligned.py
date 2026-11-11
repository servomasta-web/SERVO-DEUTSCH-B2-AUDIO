import asyncio
import subprocess
import zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output")
AUDIO=ROOT/"audio"
AUDIO.mkdir(parents=True,exist_ok=True)

# Prüfung 006 — Ehrenamtliches Engagement in der Gemeinde.
# Inhaltlich an GoetheExam06Audio.java ausgerichtet.
tracks={"teil1_01.mp3":[["de-DE-KatjaNeural","Mitteilung: Zum Thema Lärm im Wohngebiet gibt es ab nächster Woche neue Beratungszeiten. Termine können online gebucht oder telefonisch vereinbart werden. Bitte bringen Sie vorhandene Unterlagen zum ersten Gespräch mit."]],"teil1_02.mp3":[["de-DE-KatjaNeural","A: Hast du dich schon informiert? B: Ja, ich habe mehrere Möglichkeiten verglichen. A: Was ist dir besonders wichtig? B: Eine verlässliche Betreuung und klare Absprachen. Dann kann ich besser planen."]],"teil1_03.mp3":[["de-DE-KatjaNeural","Hinweis: Die Informationsveranstaltung findet am Donnerstag um 18 Uhr statt. Die Teilnahme ist kostenlos. Eine Anmeldung ist erforderlich, da die Zahl der Plätze begrenzt ist."]],"teil1_04.mp3":[["de-DE-AmalaNeural","Aus meiner Erfahrung ist es sinnvoll, sich frühzeitig zu informieren. So kann man unterschiedliche Angebote vergleichen und offene Fragen klären. Wichtig ist, nicht nur auf den Preis, sondern auch auf die Qualität zu achten."]],"teil1_05.mp3":[["de-DE-KatjaNeural","Durchsage: Wegen einer kurzfristigen Änderung beginnt der Beratungstermin nicht um neun, sondern um zehn Uhr. Der Veranstaltungsort bleibt gleich. Bereits angemeldete Personen müssen nichts weiter unternehmen."]],"teil2_01.mp3":[["de-DE-KatjaNeural","Moderatorin: Wir sprechen heute über Lärm im Wohngebiet. Herr Schneider, welche Entwicklung beobachten Sie?"],["de-DE-AmalaNeural","Schneider: Das Interesse ist in den letzten Jahren deutlich gestiegen. Viele Menschen wünschen sich flexible Lösungen. Allerdings müssen die Angebote gut organisiert sein und zu den tatsächlichen Bedürfnissen passen."],["de-DE-KatjaNeural","Moderatorin: Welche Schwierigkeiten treten dabei auf?"],["de-DE-AmalaNeural","Schneider: Häufig fehlen Zeit, Geld oder verständliche Informationen. Außerdem werden unterschiedliche Lebenssituationen nicht immer berücksichtigt. Beratung und transparente Regeln können hier helfen."],["de-DE-KatjaNeural","Moderatorin: Was sollten Interessierte beachten?"],["de-DE-AmalaNeural","Schneider: Sie sollten mehrere Möglichkeiten vergleichen, Fragen stellen und die langfristigen Folgen bedenken. Eine schnelle Entscheidung ist nicht immer die beste."],["de-DE-KatjaNeural","Moderatorin: Welche Rolle spielen Institutionen?"],["de-DE-AmalaNeural","Schneider: Unternehmen, Kommunen und Bildungseinrichtungen können passende Rahmenbedingungen schaffen. Wichtig ist, Betroffene an der Planung zu beteiligen."],["de-DE-KatjaNeural","Moderatorin: Was ist Ihr wichtigster Rat?"],["de-DE-AmalaNeural","Schneider: Nicht nur kurzfristige Vorteile betrachten, sondern auch Qualität, Fairness und Nachhaltigkeit berücksichtigen."]],"teil3_01.mp3":[["de-DE-KatjaNeural","Moderator: Sollte es strengere Regeln für Lärm im Wohngebiet geben? Frau Berger, wie sehen Sie das?"],["de-DE-AmalaNeural","Berger: Klare Regeln schaffen Orientierung und schützen Beteiligte. Sie dürfen aber nicht so starr sein, dass individuelle Lösungen unmöglich werden."],["de-DE-KatjaNeural","Moderator: Herr Wolf, teilen Sie diese Ansicht?"],["de-DE-ConradNeural","Wolf: Teilweise. Ich finde, dass Betroffene stärker mitentscheiden sollten. Allgemeine Vorgaben berücksichtigen nicht immer die Situation vor Ort."],["de-DE-AmalaNeural","Berger: Beteiligung ist wichtig, dennoch braucht es Mindeststandards. Sonst hängt die Qualität zu sehr vom Zufall ab."],["de-DE-ConradNeural","Wolf: Einverstanden, solange die Standards regelmäßig überprüft und bei Bedarf angepasst werden."],["de-DE-KatjaNeural","Moderator: Beide Seiten sprechen sich für Orientierung und Beteiligung aus, setzen aber unterschiedliche Schwerpunkte."]],"teil4_01.mp3":[["de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um Lärm im Wohngebiet. Dieses Thema betrifft viele Menschen und wirft sowohl praktische als auch gesellschaftliche Fragen auf. Zunächst ist wichtig, die unterschiedlichen Bedürfnisse zu erkennen. Eine Lösung, die für eine Person gut funktioniert, muss nicht automatisch für alle geeignet sein. Deshalb sollten Angebote flexibel gestaltet werden, ohne auf verlässliche Qualitätsstandards zu verzichten. Ein weiterer Punkt ist der Zugang. Informationen müssen verständlich und leicht erreichbar sein. Auch finanzielle und organisatorische Hindernisse sollten möglichst gering gehalten werden. Beratungsstellen können helfen, individuelle Möglichkeiten zu erkennen und Entscheidungen vorzubereiten. Darüber hinaus ist die Zusammenarbeit verschiedener Beteiligter entscheidend. Wenn Betroffene, Fachleute und zuständige Institutionen frühzeitig miteinander sprechen, lassen sich Missverständnisse vermeiden. Regelmäßige Rückmeldungen zeigen außerdem, ob eine Maßnahme tatsächlich funktioniert. Schließlich sollte man nicht nur kurzfristige Ergebnisse betrachten. Nachhaltige Lösungen benötigen klare Zuständigkeiten, ausreichende Ressourcen und die Bereitschaft, bestehende Angebote weiterzuentwickeln. Zusammenfassend lässt sich sagen, dass gute Entscheidungen auf Information, Beteiligung und einer realistischen Planung beruhen."]]}
async def make_track(name,utterances):
    parts=[]
    for i,(voice,spoken_text) in enumerate(utterances):
        part=AUDIO/f".{name}.{i:02d}.mp3"
        error=None
        for attempt in range(1,6):
            try:
                print(f"{name}: {i+1}/{len(utterances)} {voice} Versuch {attempt}/5",flush=True)
                await edge_tts.Communicate(spoken_text,voice,rate="-4%").save(str(part))
                if not part.exists() or part.stat().st_size<1000:
                    raise RuntimeError("Audio fehlt oder ist zu klein")
                error=None
                break
            except Exception as exc:
                error=exc
                part.unlink(missing_ok=True)
                print(f"Fehler: {exc}",flush=True)
                if attempt<5: await asyncio.sleep(2*attempt)
        if error: raise RuntimeError(f"Track fehlgeschlagen: {name}") from error
        parts.append(part)
        await asyncio.sleep(1)
        if i<len(utterances)-1:
            silence=AUDIO/f".silence_{name}_{i}.mp3"
            subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t","0.65","-codec:a","libmp3lame","-b:a","64k",str(silence)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
            parts.append(silence)
    listing=AUDIO/f".{name}.txt"
    listing.write_text("".join(f"file '{p.resolve()}'\n" for p in parts),encoding="utf-8")
    target=AUDIO/name
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(listing),"-codec:a","libmp3lame","-b:a","128k",str(target)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
    for p in parts+[listing]: p.unlink(missing_ok=True)
    if not target.exists() or target.stat().st_size<1024: raise RuntimeError(f"MP3 invalide: {name}")
    print(f"OK {name}: {target.stat().st_size} octets",flush=True)

async def main():
    for name,utterances in tracks.items(): await make_track(name,utterances)

asyncio.run(main())
expected=["teil1_01.mp3","teil1_02.mp3","teil1_03.mp3","teil1_04.mp3","teil1_05.mp3","teil2_01.mp3","teil3_01.mp3","teil4_01.mp3"]
archive=ROOT/"exam-020.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
