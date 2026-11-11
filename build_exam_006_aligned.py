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
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Mitteilung des Nachbarschaftszentrums: Der für Samstag geplante Reparaturtag beginnt eine Stunde später als angekündigt, also um elf Uhr. Werkzeuge können vor Ort ausgeliehen werden. Wer ein eigenes Gerät mitbringt, sollte es vorher mit seinem Namen kennzeichnen.")],
"teil1_02.mp3":[("de-DE-KatjaNeural","Ich würde mich gern in der Hausaufgabenhilfe engagieren."),("de-DE-ConradNeural","Das ist schön. Hast du schon mit dem Verein gesprochen?"),("de-DE-KatjaNeural","Noch nicht. Ich kann allerdings nur an zwei Nachmittagen im Monat."),("de-DE-ConradNeural","Dann sag das gleich bei der Anmeldung. Vielleicht lässt sich ein passender Einsatzplan finden.")],
"teil1_03.mp3":[("de-DE-KatjaNeural","Information der Stadtbibliothek: Für das Vorleseprojekt mit Kindern werden noch Freiwillige gesucht. Vorkenntnisse sind nicht erforderlich. Vor dem ersten Einsatz findet ein kostenloser Workshop statt. Interessierte können sich bis zum 20. des Monats per E-Mail melden.")],
"teil1_04.mp3":[("de-DE-AmalaNeural","Ich habe zunächst bei der Kleiderkammer geholfen, weil ich etwas Praktisches tun wollte. Inzwischen organisiere ich auch die Ausgabezeiten. Besonders wichtig finde ich, dass wir die Besucherinnen und Besucher nicht nach ihrer Lebenssituation beurteilen, sondern ihnen respektvoll begegnen.")],
"teil1_05.mp3":[("de-DE-KatjaNeural","Durchsage beim Stadtteilfest: Der Stand der freiwilligen Feuerwehr befindet sich wegen der Bauarbeiten nicht wie im Programm angegeben am Haupteingang, sondern auf dem Platz hinter der Turnhalle. Die Vorführung für Kinder beginnt trotzdem pünktlich um 15 Uhr.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderator: Viele Vereine suchen dringend freiwillige Helferinnen und Helfer. Frau Neumann, Sie koordinieren seit Jahren ein Freiwilligenzentrum. Was motiviert Menschen, sich zu engagieren?"),
("de-DE-AmalaNeural","Neumann: Die Gründe sind unterschiedlich. Einige möchten anderen helfen, andere suchen soziale Kontakte oder wollen ihre Fähigkeiten sinnvoll einsetzen. Manche entdecken durch ein Ehrenamt sogar ein neues berufliches Interesse. Wichtig ist, dass die Aufgabe zu den eigenen Möglichkeiten passt."),
("de-DE-KatjaNeural","Moderator: Wie finden Interessierte eine passende Tätigkeit?"),
("de-DE-AmalaNeural","Neumann: Zunächst sollten sie überlegen, wie viel Zeit sie regelmäßig aufbringen können und welche Aufgaben ihnen liegen. Danach kann eine Beratungsstelle passende Organisationen vorstellen. Ein unverbindliches Kennenlerngespräch hilft beiden Seiten, Erwartungen zu klären."),
("de-DE-KatjaNeural","Moderator: Gibt es typische Schwierigkeiten?"),
("de-DE-AmalaNeural","Neumann: Ja. Manchmal wird unterschätzt, wie viel Abstimmung notwendig ist. Ehrenamtliche brauchen klare Ansprechpersonen und eine Einführung. Ohne diese Unterstützung entstehen Missverständnisse, und engagierte Menschen verlieren schnell die Motivation."),
("de-DE-KatjaNeural","Moderator: Sollte ehrenamtliche Arbeit bezahlt werden?"),
("de-DE-AmalaNeural","Neumann: Eine vollständige Bezahlung würde den freiwilligen Charakter verändern. Trotzdem sollten Auslagen wie Fahrtkosten erstattet werden. Bei bestimmten Aufgaben kann auch eine begrenzte Aufwandsentschädigung sinnvoll sein."),
("de-DE-KatjaNeural","Moderator: Was können Organisationen tun, damit Freiwillige langfristig bleiben?"),
("de-DE-AmalaNeural","Neumann: Sie sollten Rückmeldungen ernst nehmen, Fortbildungen ermöglichen und Aufgaben bei Bedarf anpassen. Außerdem muss man akzeptieren, wenn jemand eine Pause braucht. Engagement darf nicht zu einer dauerhaften Überforderung führen.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: In unserer Runde sprechen wir darüber, wie eine Gemeinde mehr Menschen für freiwillige Projekte gewinnen kann. Herr Lange, Sie leiten einen Sportverein."),
("de-DE-ConradNeural","Lange: Wir erreichen viele Familien, aber nur wenige übernehmen regelmäßig Aufgaben. Ich denke, wir müssen Tätigkeiten besser aufteilen. Nicht jeder kann jedes Wochenende helfen, doch kleine Aufgaben lassen sich oft flexibel verteilen."),
("de-DE-KatjaNeural","Moderatorin: Frau Okafor, Sie arbeiten in einer Initiative für Integration."),
("de-DE-AmalaNeural","Okafor: Für mich ist vor allem wichtig, dass Informationen verständlich und mehrsprachig angeboten werden. Manche Menschen würden gern mitmachen, erfahren aber gar nicht, welche Möglichkeiten es gibt. Persönliche Begegnungen sind ebenfalls hilfreich."),
("de-DE-KatjaNeural","Moderatorin: Herr Lange, wäre eine digitale Plattform eine Lösung?"),
("de-DE-ConradNeural","Lange: Sie kann Termine und Aufgaben sichtbar machen. Allerdings darf sie den direkten Kontakt nicht ersetzen. Gerade neue Freiwillige möchten wissen, an wen sie sich bei Fragen wenden können."),
("de-DE-AmalaNeural","Okafor: Da stimme ich zu. Zusätzlich sollten Projekte gemeinsam mit den Menschen vor Ort entwickelt werden. Wenn die Gemeinde nur fertige Angebote präsentiert, fühlen sich manche Gruppen nicht angesprochen."),
("de-DE-KatjaNeural","Moderatorin: Wir halten fest: Gute Information, flexible Aufgaben und echte Beteiligung gehören zusammen.")
],
"teil4_01.mp3":[("de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um die Bedeutung des freiwilligen Engagements für Städte und Gemeinden. Viele soziale, kulturelle und sportliche Angebote wären ohne Menschen, die einen Teil ihrer Freizeit zur Verfügung stellen, kaum möglich. Freiwillige ergänzen damit öffentliche Einrichtungen und stärken das Zusammenleben vor Ort. Ein Ehrenamt kann sehr unterschiedlich aussehen. Manche Menschen begleiten ältere Personen zu Terminen, andere unterstützen Kinder beim Lernen oder helfen bei Veranstaltungen. Auch digitale Tätigkeiten, etwa die Gestaltung einer Vereinsseite, können einen wichtigen Beitrag leisten. Entscheidend ist nicht die Größe der Aufgabe, sondern dass sie zuverlässig und sinnvoll ausgeführt wird. Damit Engagement gelingt, müssen Organisationen gute Bedingungen schaffen. Dazu gehören klare Aufgabenbeschreibungen, eine erreichbare Kontaktperson und eine angemessene Vorbereitung. Niemand sollte ohne Erklärung Verantwortung übernehmen müssen. Bei Tätigkeiten mit besonderen Anforderungen sind außerdem Schulungen und gegebenenfalls Nachweise erforderlich. Eine weitere Herausforderung ist die Vereinbarkeit mit Beruf, Familie und anderen Verpflichtungen. Deshalb sollten Einsatzzeiten möglichst flexibel sein. Projektbezogene Mitarbeit oder zeitlich begrenzte Aktionen ermöglichen auch Menschen eine Beteiligung, die keine regelmäßige wöchentliche Aufgabe übernehmen können. Schließlich darf freiwillige Arbeit nicht dazu führen, dass notwendige öffentliche Leistungen dauerhaft durch unbezahlte Tätigkeiten ersetzt werden. Ehrenamt braucht Anerkennung und Unterstützung, aber auch klare Grenzen. Wenn Gemeinden diese Punkte beachten, kann Engagement das Gemeinschaftsleben langfristig bereichern.")]
}
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
archive=ROOT/"exam-006.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
