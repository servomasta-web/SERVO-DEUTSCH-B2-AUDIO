import asyncio, subprocess, zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output")
AUDIO=ROOT/"audio"
AUDIO.mkdir(parents=True,exist_ok=True)

# Prüfung 020: Tourismus in historischen Städten
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Information der Stadtbibliothek: Während der Renovierung im Erdgeschoss bleibt die Bibliothek geöffnet. Der Lesesaal und die Kinderabteilung können weiterhin genutzt werden. Die Cafeteria und der Veranstaltungssaal sind dagegen bis Ende des Monats geschlossen.")],
"teil1_02.mp3":[("de-DE-ConradNeural","A: Findet die Führung durch das historische Rathaus nicht am Mittwoch statt? B: Nein, sie wurde auf Donnerstag verlegt. A: Muss man sich vorher anmelden? B: Ja, das geht am Informationsschalter oder über die Internetseite der Stadt.")],
"teil1_03.mp3":[("de-DE-KatjaNeural","Hinweis für Reiseveranstalter: Reisebusse dürfen nicht mehr auf dem Marktplatz halten. Bitte nutzen Sie ab sofort den ausgewiesenen Busparkplatz außerhalb der Altstadt. Von dort erreichen Ihre Gäste das Zentrum in wenigen Minuten zu Fuß.")],
"teil1_04.mp3":[("de-DE-AmalaNeural","Das Stadtmuseum erinnert daran, dass am ersten Sonntag jedes Monats der Eintritt für alle Besucher kostenlos ist. Familien mit Kindern können außerdem an einer besonderen Führung teilnehmen. Diese beginnt um vierzehn Uhr im Eingangsbereich.")],
"teil1_05.mp3":[("de-DE-KatjaNeural","Unsere Altstadtführung endet heute nicht wie üblich am Rathaus, sondern im historischen Handwerkerviertel. Dort haben Sie Gelegenheit, traditionelle Werkstätten zu besuchen und mit einigen Handwerkerinnen und Handwerkern ins Gespräch zu kommen.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Historische Städte ziehen jedes Jahr zahlreiche Besucher an. Gleichzeitig wird über volle Straßen und steigende Belastungen diskutiert. Frau Dr. Neumann, Sie sind Stadtplanerin. Wie beurteilen Sie die Entwicklung?"),
("de-DE-AmalaNeural","Neumann: Das Interesse an historischen Orten ist in den vergangenen Jahren deutlich gewachsen. Besonders an Wochenenden und während der Hauptsaison kommen viele Gäste. Das bringt Einnahmen und Arbeitsplätze, stellt die Städte aber auch vor Herausforderungen. Öffentliche Plätze, Verkehrsmittel und die Infrastruktur werden stark beansprucht."),
("de-DE-KatjaNeural","Moderatorin: Welche Probleme entstehen dadurch konkret?"),
("de-DE-AmalaNeural","Neumann: In engen Altstadtstraßen können Reisebusse und private Autos den Verkehr behindern. Hinzu kommen Lärm und Abfälle. Wenn sich zu viele Menschen gleichzeitig an wenigen Sehenswürdigkeiten aufhalten, leidet außerdem das Besuchserlebnis. Deshalb haben wir Busse bereits an einen Parkplatz am Stadtrand geleitet."),
("de-DE-KatjaNeural","Moderatorin: Können die örtlichen Geschäfte dennoch profitieren?"),
("de-DE-AmalaNeural","Neumann: Ja, selbstverständlich. Vor allem kleine Betriebe können Gäste gewinnen, wenn sie regionale Produkte, Handwerk und lokale Dienstleistungen anbieten. Wichtig ist allerdings, dass nicht nur Souvenirläden entstehen. Eine vielfältige Altstadt braucht auch Geschäfte und Angebote für die Einwohner."),
("de-DE-KatjaNeural","Moderatorin: Wie lässt sich der Besucherstrom besser verteilen?"),
("de-DE-AmalaNeural","Neumann: Wir sollten weniger bekannte Viertel und Sehenswürdigkeiten stärker vorstellen. Auch thematische Rundgänge und digitale Hinweise auf ruhigere Zeiten können helfen. So entdecken Gäste mehr von der Stadt, während einzelne Plätze entlastet werden."),
("de-DE-KatjaNeural","Moderatorin: Was ist Ihr wichtigstes Ziel für die Zukunft?"),
("de-DE-AmalaNeural","Neumann: Tourismus darf nicht nur nach Besucherzahlen bewertet werden. Wir brauchen ein Gleichgewicht: Die Wirtschaft soll profitieren, aber die Lebensqualität der Einwohner und der Schutz des kulturellen Erbes müssen erhalten bleiben.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderator: Wie kann unsere historische Altstadt mit den steigenden Besucherzahlen umgehen? Frau Neumann, Sie arbeiten in der Stadtplanung. Was schlagen Sie vor?"),
("de-DE-AmalaNeural","Neumann: Die Stadt muss klare Regeln aufstellen, damit öffentliche Plätze nicht überfüllt werden. Ich halte zusätzliche Busparkplätze außerhalb des Zentrums für sinnvoll. Außerdem sollten wir Besucher auf weniger bekannte Sehenswürdigkeiten aufmerksam machen."),
("de-DE-KatjaNeural","Moderator: Herr Roth, Sie betreiben ein Geschäft in der Altstadt. Wie erleben Sie den Tourismus?"),
("de-DE-ConradNeural","Roth: Für viele kleine Betriebe ist er eine wichtige Einnahmequelle. Wir profitieren, wenn Gäste länger bleiben und lokale Angebote nutzen. Trotzdem darf man nicht vergessen, dass die Altstadt zuerst ein Wohnort für die Menschen vor Ort ist. Zu viel Verkehr und Lärm machen den Alltag schwierig."),
("de-DE-KatjaNeural","Moderator: Welche Lösung wäre aus Ihrer Sicht fair?"),
("de-DE-AmalaNeural","Neumann: Wir sollten die Besucherströme besser lenken und den öffentlichen Nahverkehr stärken. Die Regeln müssen gemeinsam mit den Bewohnern und den Geschäftsleuten entwickelt werden."),
("de-DE-ConradNeural","Roth: Ich stimme zu, solange kleine Unternehmen beteiligt werden. Ein gutes Gleichgewicht zwischen wirtschaftlichen Chancen und dem Alltag der Bewohner ist entscheidend. Wenn die Altstadt lebendig bleibt, kommen auch die Gäste gern wieder."),
("de-DE-KatjaNeural","Moderator: Vielen Dank für diese Einschätzungen.")
],
"teil4_01.mp3":[
("de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um den Tourismus in historischen Städten und die Frage, wie sich Besucherinteressen mit dem Schutz des städtischen Lebens verbinden lassen. Historische Orte sind wegen ihrer Architektur, ihrer Geschichte und ihrer kulturellen Angebote attraktiv."),
("de-DE-AmalaNeural","Mit wachsender Beliebtheit entstehen jedoch Belastungen. Viele Autos und Reisebusse verursachen Lärm, schlechte Luft und gefährliche Situationen für Fußgänger. Auch öffentliche Plätze und Verkehrsmittel können überfüllt sein. Deshalb sind Verkehrsplanung und gut erreichbare Parkmöglichkeiten außerhalb des Zentrums wichtig."),
("de-DE-ConradNeural","Eine nachhaltige Strategie beginnt mit der Beteiligung der Einwohner. Sie kennen die Probleme im Alltag und können beurteilen, welche Veränderungen sinnvoll sind. Stadtverwaltungen sollten deshalb regelmäßig mit Bewohnern, Geschäftsleuten und Kulturinstitutionen sprechen."),
("de-DE-AmalaNeural","Digitale Informationen können ebenfalls helfen. Besucher lassen sich über weniger frequentierte Wege, alternative Sehenswürdigkeiten und ruhigere Besuchszeiten informieren. Dadurch verteilt sich der Besucherstrom besser, und auch weniger bekannte Stadtteile erhalten Aufmerksamkeit."),
("de-DE-ConradNeural","Besondere Sorgfalt ist beim Umgang mit historischen Gebäuden erforderlich. Denkmalschutz und eine sinnvolle Nutzung müssen miteinander vereinbart werden. Renovierungen sollen die historische Substanz bewahren und gleichzeitig ermöglichen, dass Gebäude weiterhin genutzt werden können."),
("de-DE-AmalaNeural","Auch die lokale Wirtschaft kann einen Beitrag leisten. Wer regionale Produkte kauft, örtliche Restaurants besucht oder traditionelles Handwerk kennenlernt, unterstützt die Menschen vor Ort. Entscheidend ist, dass die Altstadt nicht nur aus Angeboten für Touristen besteht, sondern ihren alltäglichen Charakter behält."),
("de-DE-ConradNeural","Nachhaltiger Tourismus bedeutet daher, die Bedürfnisse der Gäste, der Einwohner und des kulturellen Erbes gemeinsam zu berücksichtigen. Keine dieser Perspektiven darf dauerhaft auf Kosten der anderen bevorzugt werden."),
("de-DE-AmalaNeural","Zusammenfassend lässt sich sagen: Historische Städte brauchen Besucher und die wirtschaftlichen Chancen des Tourismus. Langfristig erfolgreich ist er aber nur dann, wenn Lebensqualität, Denkmalschutz und eine gute Planung im Mittelpunkt stehen. Vielen Dank für Ihre Aufmerksamkeit.")
]
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
                if not part.exists() or part.stat().st_size<1000: raise RuntimeError("Audio fehlt oder zu klein")
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
    listing.write_text("".join(f"file '{p.resolve()}'\\n" for p in parts),encoding="utf-8")
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
