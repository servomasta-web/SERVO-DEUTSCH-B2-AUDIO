# SERVO DEUTSCH B2 — exam 030 aligned audio generation
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
tracks={"teil1_01.mp3":[["de-DE-KatjaNeural","Mitteilung des Reisebüros: Für die Nachtzugverbindung nach Wien können Sitzplätze und Schlafwagenbetten ab sofort getrennt gebucht werden. Wer ein Fahrrad mitnehmen möchte, muss dafür zusätzlich einen Stellplatz reservieren. Die Zahl der Fahrradplätze ist begrenzt."]],"teil1_02.mp3":[["de-DE-KatjaNeural","A: Wir wollen im Sommer nach Italien fahren, aber nicht fliegen. B: Dann könntet ihr mit dem Zug bis München und von dort weiterreisen. A: Dauert das nicht viel länger? B: Ja, aber ihr könnt unterwegs lesen und müsst nicht zum Flughafen fahren."]],"teil1_03.mp3":[["de-DE-KatjaNeural","Hinweis des Nationalparks: Besucherinnen und Besucher werden gebeten, für Ausflüge die regionalen Busse zu nutzen. Der Parkplatz am See ist am Wochenende häufig voll. Der Shuttlebus fährt ab dem Bahnhof alle dreißig Minuten."]],"teil1_04.mp3":[["de-DE-AmalaNeural","Ich buche inzwischen Unterkünfte, die mit öffentlichen Verkehrsmitteln erreichbar sind. Dadurch brauche ich vor Ort keinen Mietwagen. Bei längeren Strecken nehme ich manchmal einen Fernbus, wenn es keine gute Bahnverbindung gibt."]],"teil1_05.mp3":[["de-DE-KatjaNeural","Durchsage am Bahnhof: Wegen Bauarbeiten fährt der Regionalzug am Sonntag nur bis zur Station West. Von dort bringt ein Ersatzbus die Reisenden zum Hauptbahnhof. Die Abfahrtszeit des Zuges bleibt unverändert."]],"teil2_01.mp3":[["de-DE-KatjaNeural","Moderator: Immer mehr Menschen möchten klimafreundlicher reisen. Frau Berger, Sie arbeiten bei einer Organisation für nachhaltigen Tourismus. Welche Entscheidung hat den größten Einfluss?\nBerger: Häufig ist es die Wahl des Verkehrsmittels. Bei kurzen und mittleren Strecken kann die Bahn eine gute Alternative zum Flugzeug sein. Allerdings kommt es auf die Verbindung, die Auslastung und die gesamte Reise an.\nModerator: Ist eine Zugreise immer die bessere Wahl?\nBerger: Nicht automatisch. Wenn eine Verbindung sehr umständlich ist oder viele zusätzliche Autofahrten nötig werden, muss man genauer vergleichen. Entscheidend ist die gesamte Strecke von der Haustür bis zum Ziel.\nModerator: Welche Rolle spielt die Unterkunft?\nBerger: Eine Unterkunft mit guter Anbindung an Bus und Bahn kann einen Mietwagen überflüssig machen. Außerdem können Reisende lokale Anbieter unterstützen und regionale Produkte nutzen.\nModerator: Was bedeutet nachhaltiger Tourismus für die besuchten Orte?\nBerger: Besucher sollten Natur und Kultur respektieren, lokale Regeln beachten und besonders empfindliche Gebiete nicht überlasten. Reisen außerhalb der Hauptsaison können helfen, Besucherströme besser zu verteilen.\nModerator: Wie lässt sich eine Reise realistisch planen?\nBerger: Man sollte nicht nur auf Werbezeichen achten, sondern konkrete Informationen prüfen: Verkehrsanbindung, Energieverbrauch, Abfallmanagement und die Zusammenarbeit mit lokalen Betrieben."]],"teil3_01.mp3":[["de-DE-KatjaNeural","Moderatorin: Sollten Flugreisen innerhalb Europas stärker besteuert werden, um klimafreundliche Alternativen zu fördern? Herr Neumann, Sie betreiben ein Reiseunternehmen."],["de-DE-ConradNeural","Neumann: Eine zusätzliche Steuer kann Menschen mit geringem Einkommen besonders treffen. Außerdem gibt es Regionen, die mit der Bahn nur schwer erreichbar sind. Wir sollten zuerst bessere Verbindungen schaffen, bevor wir Reisen verteuern."],["de-DE-KatjaNeural","Moderatorin: Frau Costa, Sie forscht zu Verkehr und Klima."],["de-DE-ConradNeural","Costa: Ohne wirtschaftliche Anreize ändert sich das Verhalten nur langsam. Die Kosten des Flugverkehrs spiegeln seine Umweltfolgen nicht vollständig wider. Einnahmen könnten in Bahnverbindungen und Nachtzüge investiert werden."],["de-DE-ConradNeural","Neumann: Investitionen sind sinnvoll, aber es braucht Übergangsregeln für abgelegene Regionen und Menschen, die aus beruflichen Gründen reisen müssen."],["de-DE-ConradNeural","Costa: Solche Ausnahmen kann man begrenzen. Wichtig ist, dass die Einnahmen zweckgebunden und transparent verwendet werden."],["de-DE-KatjaNeural","Moderatorin: Beide wollen bessere Alternativen, unterscheiden sich aber darin, ob eine Steuer vor oder nach dem Ausbau des Angebots eingeführt werden sollte."]],"teil4_01.mp3":[["de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um klimafreundliches Reisen. Tourismus ermöglicht Erholung und Begegnungen, verursacht aber auch Emissionen und belastet empfindliche Naturräume. Eine nachhaltige Reiseplanung versucht deshalb, Umweltfolgen zu reduzieren und gleichzeitig die Lebensbedingungen der Menschen am Zielort zu respektieren.\nEin wichtiger Faktor ist die Anreise. Für viele Strecken innerhalb Europas können Bahn und Fernbus Alternativen zum Flugzeug sein. Dabei sollte man die gesamte Verbindung betrachten, einschließlich der Wege zum Bahnhof und vom Ankunftsort zur Unterkunft. Eine direkte Verbindung ist nicht immer verfügbar, doch gute Planung kann unnötige Autofahrten vermeiden.\nAuch die Mobilität am Zielort zählt. Unterkünfte in der Nähe von Haltestellen, Fahrradverleih und lokale Busangebote machen einen Mietwagen häufig überflüssig. Reisende können außerdem regionale Anbieter unterstützen und Produkte aus der Umgebung nutzen.\nDie Reisezeit beeinflusst ebenfalls die Folgen. In der Hauptsaison sind manche Orte überfüllt, Wasser und Energie werden stark beansprucht und Naturgebiete können Schaden nehmen. Reisen außerhalb der Spitzenzeiten verteilen Besucher besser und können lokale Betriebe über einen längeren Zeitraum unterstützen.\nSchließlich sollten Nachhaltigkeitsversprechen überprüfbar sein. Reisende können Informationen zu Energie, Abfall, Verkehr und lokalen Arbeitsbedingungen vergleichen. Klimafreundliches Reisen bedeutet nicht, auf jede Reise zu verzichten, sondern bewusste Entscheidungen zu treffen und die Auswirkungen auf Umwelt und Gastgeber zu berücksichtigen."]]}
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
archive=ROOT/"exam-030.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
