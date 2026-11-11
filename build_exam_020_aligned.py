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
tracks={"teil1_01.mp3":[["de-DE-KatjaNeural","Hinweis der Hausverwaltung: Die Reparatur des Aufzugs beginnt am Montag um sieben Uhr. Während der Arbeiten kann es zu Bohrgeräuschen kommen. Die Handwerker sollen spätestens um 16 Uhr fertig sein. Der zweite Aufzug bleibt in Betrieb."]],"teil1_02.mp3":[["de-DE-KatjaNeural","A: Der neue Nachbar hört abends oft sehr laut Musik. B: Hast du schon mit ihm gesprochen? A: Noch nicht. Ich möchte zuerst freundlich erklären, dass ich früh aufstehen muss. B: Vielleicht könnt ihr eine feste Ruhezeit vereinbaren, bevor du dich an die Hausverwaltung wendest."]],"teil1_03.mp3":[["de-DE-KatjaNeural","Mitteilung des Ordnungsamts: Für private Feiern im Innenhof ist nach 22 Uhr eine Genehmigung erforderlich. Die allgemeine Nachtruhe gilt weiterhin. Anträge müssen mindestens zehn Werktage vorher gestellt werden."]],"teil1_04.mp3":[["de-DE-AmalaNeural","Ich habe mir Ohrstöpsel gekauft, weil die Straße vor meinem Fenster morgens sehr laut ist. Das hilft beim Schlafen, aber die eigentliche Lösung wäre eine bessere Verkehrsplanung. Ich habe deshalb an der städtischen Umfrage teilgenommen."]],"teil1_05.mp3":[["de-DE-KatjaNeural","Durchsage im Wohngebiet: Die Müllabfuhr kommt wegen einer Straßensperrung am Mittwoch bereits ab sechs Uhr. Bitte stellen Sie die Tonnen am Vorabend an den markierten Sammelpunkt."]],"teil2_01.mp3":[["de-DE-KatjaNeural","Moderatorin: Lärm gehört zu den häufigsten Beschwerden in Wohngebieten. Herr Baumann, Sie arbeiten in einer kommunalen Umweltberatung. Welche Lärmquellen spielen eine besonders große Rolle?\nBaumann: Verkehr, Baustellen und laute Freizeitaktivitäten. Die Belastung hängt nicht nur von der Lautstärke ab, sondern auch davon, wie lange und zu welchen Tageszeiten sie auftritt. Wiederkehrender Lärm in der Nacht kann den Schlaf stark beeinträchtigen.\nModeratorin: Was können Bewohner selbst tun?\nBaumann: Bei einem Konflikt ist ein sachliches Gespräch oft ein guter erster Schritt. Manchmal wissen Nachbarn gar nicht, wie stark Geräusche in einer anderen Wohnung zu hören sind. Wenn das nicht hilft, können Hausverwaltung oder zuständige Stellen vermitteln.\nModeratorin: Wie lässt sich Verkehrslärm verringern?\nBaumann: Durch niedrigere Geschwindigkeiten, lärmarme Straßenbeläge und eine bessere Verkehrsführung. Auch mehr öffentliche Verkehrsmittel und sichere Radwege können dazu beitragen, dass weniger Autos unterwegs sind.\nModeratorin: Sind Schallschutzfenster ausreichend?\nBaumann: Sie können Innenräume deutlich schützen, lösen aber nicht das Problem im öffentlichen Raum. Außerdem müssen Lüftung und Wohnkomfort berücksichtigt werden. Eine bauliche Maßnahme sollte Teil eines umfassenden Konzepts sein.\nModeratorin: Wie sollten Städte Prioritäten setzen?\nBaumann: Sie sollten Belastungen messen, besonders betroffene Gruppen berücksichtigen und Maßnahmen transparent erklären. Schulen, Krankenhäuser und Wohngebiete verdienen besondere Aufmerksamkeit."]],"teil3_01.mp3":[["de-DE-KatjaNeural","Moderator: Sollte die Stadt in Wohngebieten ein generelles Verbot für laute Gartenarbeiten am Samstag einführen? Frau Krüger, Sie vertreten einen Mieterverein."],["de-DE-AmalaNeural","Krüger: Viele Menschen arbeiten unter der Woche und erledigen Gartenarbeiten am Wochenende. Ein vollständiges Verbot wäre unverhältnismäßig. Wir brauchen aber klare Ruhezeiten und verständliche Informationen."],["de-DE-KatjaNeural","Moderator: Herr Scholz, Sie sind Sprecher einer Nachbarschaftsinitiative."],["de-DE-ConradNeural","Scholz: In dicht bebauten Vierteln sind Geräusche besonders störend. Wenn an jedem Samstag stundenlang Maschinen laufen, bleibt kaum Zeit zur Erholung. Ich würde bestimmte laute Arbeiten auf wenige Zeitfenster begrenzen."],["de-DE-AmalaNeural","Krüger: Zeitfenster können funktionieren, wenn sie realistisch sind. Außerdem sollten Ausnahmen für dringende Reparaturen möglich bleiben."],["de-DE-ConradNeural","Scholz: Damit kann ich leben, solange Ausnahmen nicht zur Regel werden. Die Stadt könnte zusätzlich leisere Geräte empfehlen und eine Vermittlungsstelle bei Konflikten anbieten."],["de-DE-KatjaNeural","Moderator: Beide wollen Ruhezeiten und klare Regeln, unterscheiden sich aber darin, wie streng die Einschränkungen sein sollen."]],"teil4_01.mp3":[["de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um Lärm in Wohngebieten und seine Auswirkungen auf die Lebensqualität. Geräusche gehören zum Alltag einer Stadt. Gespräche, Verkehr und Bauarbeiten lassen sich nicht vollständig vermeiden. Problematisch wird Lärm, wenn er dauerhaft, besonders laut oder zu ungünstigen Zeiten auftritt.\nLärm kann die Konzentration stören, Stress verstärken und den Schlaf beeinträchtigen. Besonders empfindlich reagieren Kinder, ältere Menschen und Personen, die gesundheitlich belastet sind. Deshalb sollten Kommunen nicht nur Durchschnittswerte betrachten, sondern auch untersuchen, wann und wo Menschen besonders stark betroffen sind.\nEine Möglichkeit ist die Verringerung des Verkehrs. Tempo-30-Zonen, lärmarme Fahrbahnbeläge und eine bessere Ampelschaltung können die Geräuschentwicklung reduzieren. Sichere Wege für Fahrräder und ein zuverlässiger öffentlicher Verkehr bieten Alternativen zum Auto.\nAuch bei Gebäuden lässt sich etwas tun. Schallschutzfenster und eine geeignete Raumaufteilung schützen Innenräume. Bei Neubauten sollten ruhige Höfe und Grünflächen eingeplant werden. Solche Maßnahmen ersetzen jedoch keine Lösungen an der Lärmquelle.\nIm direkten Zusammenleben helfen klare Ruhezeiten und gegenseitige Rücksichtnahme. Konflikte sollten zunächst sachlich angesprochen werden. Kommunale Beratungsstellen können vermitteln, wenn eine Einigung nicht gelingt. Ein wirksamer Lärmschutz verbindet technische Planung, verständliche Regeln und die Beteiligung der Anwohner."]]}
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
