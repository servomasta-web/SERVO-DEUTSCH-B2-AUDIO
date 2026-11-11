import asyncio
import subprocess
import zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output")
AUDIO=ROOT/"audio"
AUDIO.mkdir(parents=True,exist_ok=True)

# Prüfung 011 — Öffentliche Verkehrsmittel und Klimaschutz.
# Acht eigenständige Hörtexte, passend zu exam-011.json.
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Information des Verkehrsverbunds: Wegen einer Baustelle fährt die Straßenbahnlinie 4 ab Montag nicht bis zum Rathaus. Fahrgäste steigen bitte an der Haltestelle Markt aus und nutzen dort den Ersatzbus. Die übrigen Linien verkehren nach Plan.")],
"teil1_02.mp3":[("de-DE-KatjaNeural","Ich überlege, ob ich für den Arbeitsweg ein Monatsticket kaufen soll."),("de-DE-ConradNeural","Wie oft fährst du ins Büro?"),("de-DE-KatjaNeural","Vier Tage pro Woche."),("de-DE-ConradNeural","Dann lohnt sich vielleicht ein Abo. Prüfe aber, ob dein Arbeitgeber einen Zuschuss anbietet.")],
"teil1_03.mp3":[("de-DE-KatjaNeural","Hinweis am Bahnhof: Fahrräder können außerhalb der Hauptverkehrszeiten kostenlos in Regionalzügen mitgenommen werden. Zwischen sieben und neun Uhr ist dafür eine zusätzliche Fahrradkarte erforderlich. Klappfahrräder gelten als normales Handgepäck.")],
"teil1_04.mp3":[("de-DE-AmalaNeural","Seit die neue Busverbindung eingerichtet wurde, lasse ich das Auto häufiger stehen. Besonders praktisch ist, dass der Bus auch am frühen Abend fährt. Allerdings muss ich morgens manchmal zehn Minuten länger warten als früher.")],
"teil1_05.mp3":[("de-DE-KatjaNeural","Durchsage: Wegen eines technischen Defekts ist der Fahrkartenautomat am Gleis 2 außer Betrieb. Fahrgäste können Tickets am Automaten in der Eingangshalle oder über die offizielle App erwerben. Bitte kaufen Sie Ihr Ticket vor Fahrtantritt.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderator: Viele Städte möchten mehr Menschen zum Umstieg auf Bus und Bahn bewegen. Frau König, Sie planen Verkehrsangebote für eine mittelgroße Stadt. Was ist dafür am wichtigsten?"),
("de-DE-AmalaNeural","König: Zunächst muss der öffentliche Verkehr zuverlässig sein. Wenn Anschlüsse häufig verpasst werden oder Busse unregelmäßig kommen, verlieren Fahrgäste das Vertrauen. Ein dichter Fahrplan allein hilft wenig, wenn die Verbindungen nicht zusammenpassen."),
("de-DE-KatjaNeural","Moderator: Welche Gruppen müssen besonders berücksichtigt werden?"),
("de-DE-AmalaNeural","König: Menschen mit eingeschränkter Mobilität, ältere Fahrgäste und Eltern mit Kinderwagen. Haltestellen müssen erreichbar sein, und Informationen sollten verständlich angezeigt und angesagt werden. Barrierefreiheit gehört zur Grundplanung."),
("de-DE-KatjaNeural","Moderator: Wie lässt sich der Autoverkehr reduzieren?"),
("de-DE-AmalaNeural","König: Neben besseren Bus- und Bahnverbindungen braucht es sichere Radwege und gute Fußwege. Park-and-Ride-Anlagen können sinnvoll sein, wenn sie an leistungsfähige Linien angeschlossen sind. Ein pauschales Autoverbot löst nicht jedes Problem, besonders außerhalb des Zentrums."),
("de-DE-KatjaNeural","Moderator: Welche Bedeutung haben die Kosten?"),
("de-DE-AmalaNeural","König: Preiswerte Tickets helfen, aber sie müssen langfristig finanzierbar sein. Manche Städte bieten Ermäßigungen für bestimmte Gruppen an. Arbeitgeber können Jobtickets unterstützen. Wichtig ist, dass Tarife einfach und nachvollziehbar bleiben."),
("de-DE-KatjaNeural","Moderator: Woran erkennt man, ob eine Maßnahme erfolgreich ist?"),
("de-DE-AmalaNeural","König: Man sollte nicht nur Fahrgastzahlen betrachten. Auch Pünktlichkeit, Zufriedenheit, Zugänglichkeit und die Entwicklung des Autoverkehrs sind wichtige Kennzahlen.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderator: Wir sprechen über die Einführung einer City-Maut, mit der der Autoverkehr im Zentrum reduziert werden soll. Herr Vogt, Sie betreiben ein Geschäft in der Innenstadt."),
("de-DE-ConradNeural","Vogt: Ich habe Bedenken. Wenn Kundinnen und Kunden für die Anfahrt zusätzlich zahlen müssen, könnten sie in Einkaufszentren am Stadtrand ausweichen. Kleine Geschäfte wären besonders betroffen."),
("de-DE-KatjaNeural","Moderator: Frau Stein, Sie sind Verkehrsplanerin."),
("de-DE-AmalaNeural","Stein: Eine Gebühr kann den Verkehr verringern, wenn es gleichzeitig gute Alternativen gibt. Die Einnahmen sollten sichtbar in Busse, Radwege und sichere Gehwege investiert werden. Ohne solche Angebote wäre die Maßnahme sozial ungerecht."),
("de-DE-ConradNeural","Vogt: Für Lieferverkehr und Menschen mit Behinderungen braucht es Ausnahmen. Außerdem sollten Betriebe frühzeitig informiert werden."),
("de-DE-AmalaNeural","Stein: Bei notwendigen Lieferungen stimme ich zu. Ausnahmen müssen klar geregelt sein. Wir könnten zunächst eine befristete Testphase durchführen und die Auswirkungen untersuchen."),
("de-DE-KatjaNeural","Moderator: Eine City-Maut muss also zusammen mit Alternativen, Ausnahmen und einer Überprüfung beurteilt werden.")
],
"teil4_01.mp3":[("de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um den Beitrag öffentlicher Verkehrsmittel zum Klimaschutz. Der Verkehrssektor verursacht einen erheblichen Teil der energiebedingten Treibhausgasemissionen. Besonders problematisch ist der hohe Anteil des motorisierten Individualverkehrs, wenn viele Menschen allein im Auto unterwegs sind. Busse und Bahnen können pro beförderter Person weniger Energie benötigen, sofern sie ausreichend genutzt und sinnvoll betrieben werden. Der Umstieg gelingt jedoch nicht allein durch Appelle. Entscheidend ist ein Angebot, das im Alltag funktioniert: kurze Wartezeiten, verlässliche Anschlüsse, verständliche Informationen und Haltestellen in erreichbarer Nähe. Auf dem Land sind Wege oft länger und die Nachfrage schwankt stärker. Flexible Kleinbusse oder Rufangebote können dort eine Ergänzung zum festen Linienverkehr sein. Auch die Anbindung verschiedener Verkehrsmittel ist wichtig. Wer mit dem Fahrrad zum Bahnhof fahren oder einen sicheren Fußweg nutzen kann, erreicht den öffentlichen Verkehr leichter. Fahrradstellplätze, barrierefreie Zugänge und übersichtliche Umsteigepunkte machen die Reisekette attraktiver. Die Finanzierung bleibt eine Herausforderung. Fahrkartenpreise sollen bezahlbar sein, zugleich müssen Personal, Fahrzeuge und Infrastruktur zuverlässig bezahlt werden. Öffentliche Investitionen und langfristige Planung sind deshalb notwendig. Einnahmen aus Parkgebühren oder einer City-Maut können beitragen, sofern sie transparent eingesetzt werden. Schließlich muss die Wirkung überprüft werden. Mehr Fahrgäste bedeuten nicht automatisch weniger Autoverkehr, wenn zusätzliche Fahrten entstehen oder Busse kaum ausgelastet sind. Städte sollten Emissionen, Auslastung, Pünktlichkeit und Zugänglichkeit beobachten. Klimafreundliche Mobilität entsteht durch ein zusammenhängendes System, das unterschiedliche Lebenssituationen berücksichtigt.")]}
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
archive=ROOT/"exam-011.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
