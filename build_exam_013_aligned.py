import asyncio
import subprocess
import zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output")
AUDIO=ROOT/"audio"
AUDIO.mkdir(parents=True,exist_ok=True)

# Prüfung 013 — Sportangebote für Jugendliche.
# Acht Hörtracks mit vier Prüfungsteilen und abwechslungsreichen Stimmen.
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Mitteilung des Sportvereins: Das Schwimmtraining für Jugendliche beginnt am kommenden Montag nicht um 17 Uhr, sondern um 17.30 Uhr. Die Trainingsdauer bleibt unverändert. Teilnehmende sollen ihre Schwimmkarten am Eingang vorzeigen.")],
"teil1_02.mp3":[("de-DE-KatjaNeural","Ich möchte nach der Schule mehr Sport machen, aber der Fußballverein passt zeitlich nicht."),("de-DE-ConradNeural","Im Jugendzentrum gibt es dienstags einen offenen Klettertreff."),("de-DE-KatjaNeural","Muss man dafür schon Erfahrung haben?"),("de-DE-ConradNeural","Nein, die ersten Termine werden von einer Trainerin begleitet.")],
"teil1_03.mp3":[("de-DE-KatjaNeural","Hinweis der Stadt: Für Jugendliche zwischen 14 und 18 Jahren werden in den Sommerferien kostenlose Probetrainings in mehreren Sporthallen angeboten. Die Anmeldung ist online möglich. Sportkleidung muss selbst mitgebracht werden.")],
"teil1_04.mp3":[("de-DE-AmalaNeural","Seit ich zweimal pro Woche mit dem Rad zur Schule fahre, fühle ich mich fitter. Ich nehme dafür einen etwas längeren Weg durch den Park, weil dort weniger Autos unterwegs sind. Bei starkem Regen fahre ich allerdings mit dem Bus.")],
"teil1_05.mp3":[("de-DE-KatjaNeural","Durchsage im Stadion: Wegen einer Reparatur bleibt die Leichtathletikbahn bis einschließlich Donnerstag gesperrt. Die Laufgruppe trainiert in dieser Woche auf dem Sportplatz am Fluss. Der Treffpunkt bleibt um 18 Uhr.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderator: Viele Jugendliche bewegen sich im Alltag zu wenig. Frau Seifert, Sie koordinieren Sportprogramme für junge Menschen. Wie kann man sie besser erreichen?"),
("de-DE-AmalaNeural","Seifert: Angebote müssen zeitlich und finanziell zugänglich sein. Wenn Training erst spät am Abend stattfindet oder hohe Beiträge kostet, können viele Jugendliche nicht teilnehmen. Offene Sporttreffs ohne langfristige Mitgliedschaft sind ein guter Einstieg."),
("de-DE-KatjaNeural","Moderator: Sollte man stärker auf Wettbewerb setzen?"),
("de-DE-AmalaNeural","Seifert: Für manche ist ein Wettkampf motivierend. Andere möchten sich bewegen, ohne ständig bewertet zu werden. Deshalb brauchen wir beides: leistungsorientierte Vereine und Freizeitangebote, bei denen Freude und Gemeinschaft im Mittelpunkt stehen."),
("de-DE-KatjaNeural","Moderator: Welche Rolle spielen Schulen?"),
("de-DE-AmalaNeural","Seifert: Schulen können verschiedene Sportarten vorstellen und mit Vereinen zusammenarbeiten. Wichtig ist, dass nicht nur besonders talentierte Jugendliche gefördert werden. Auch Anfängerinnen und Anfänger sollen positive Erfahrungen machen."),
("de-DE-KatjaNeural","Moderator: Wie lassen sich Jugendliche langfristig motivieren?"),
("de-DE-AmalaNeural","Seifert: Sie sollten mitentscheiden dürfen. Wenn sie Trainingszeiten, Musik oder Aktivitäten mitgestalten, fühlen sie sich ernst genommen. Außerdem helfen erreichbare Sportstätten und eine sichere Umgebung."),
("de-DE-KatjaNeural","Moderator: Was ist mit digitalen Angeboten?"),
("de-DE-AmalaNeural","Seifert: Fitness-Apps können ergänzen, aber sie ersetzen keine persönliche Anleitung. Gerade bei neuen Übungen ist es wichtig, Bewegungen korrekt zu lernen und Überlastung zu vermeiden.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Sollten Schulen täglich eine verpflichtende Sportstunde anbieten? Herr Brandt, Sie leiten eine weiterführende Schule."),
("de-DE-ConradNeural","Brandt: Bewegung ist wichtig, aber eine zusätzliche Pflichtstunde lässt sich nicht überall einfach in den Stundenplan einbauen. Es fehlen teilweise Hallen und qualifizierte Lehrkräfte. Wir sollten zunächst bestehende Pausen und Unterrichtsformen bewegungsfreundlicher gestalten."),
("de-DE-KatjaNeural","Moderatorin: Frau Okafor, Sie vertreten einen Jugend-Sportverband."),
("de-DE-AmalaNeural","Okafor: Eine feste tägliche Bewegungszeit wäre ein klares Signal. Sie müsste nicht immer aus klassischem Sportunterricht bestehen. Auch Tanz, Spiele oder kurze Bewegungseinheiten könnten dazugehören."),
("de-DE-ConradNeural","Brandt: Solche flexiblen Formen finde ich interessant. Trotzdem darf Bewegung nicht zu einer weiteren benoteten Leistung werden. Jugendliche mit gesundheitlichen Einschränkungen brauchen passende Alternativen."),
("de-DE-AmalaNeural","Okafor: Einverstanden, die Teilnahme sollte vielfältig gestaltet werden. Außerdem könnten Vereine einzelne Angebote begleiten, wenn Schulen geeignete Räume und Zeiten bereitstellen."),
("de-DE-KatjaNeural","Moderatorin: Beide sehen den Nutzen regelmäßiger Bewegung, unterscheiden sich aber bei der Frage, ob eine zusätzliche tägliche Pflichtstunde nötig ist.")
],
"teil4_01.mp3":[("de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um Sportangebote für Jugendliche und ihre Bedeutung für Gesundheit und Zusammenleben. Regelmäßige Bewegung stärkt Herz und Kreislauf, unterstützt die Konzentration und kann Stress abbauen. Sport bietet außerdem Gelegenheiten, Freundschaften zu schließen und Regeln des fairen Miteinanders zu lernen. Trotz dieser Vorteile nehmen nicht alle Jugendlichen gleichermaßen teil. Manche Angebote sind zu teuer, liegen weit entfernt oder passen zeitlich nicht zum Schul- und Familienalltag. Andere fühlen sich in leistungsorientierten Gruppen unsicher, wenn sie noch wenig Erfahrung haben. Ein vielfältiges Angebot sollte deshalb unterschiedliche Fähigkeiten und Interessen berücksichtigen. Vereine können feste Trainingsgruppen und fachliche Betreuung anbieten. Offene Treffs in Parks oder Jugendzentren ermöglichen einen unkomplizierten Einstieg. Schulen können Sportarten vorstellen und Räume außerhalb des Unterrichts zugänglich machen. Kommunen sollten darauf achten, dass Sportstätten gut erreichbar und sicher sind. Auch die Beteiligung der Jugendlichen ist entscheidend. Wenn sie bei der Auswahl von Aktivitäten und Zeiten mitreden, steigt die Wahrscheinlichkeit, dass sie regelmäßig kommen. Trainerinnen und Trainer sollten Rückmeldungen ernst nehmen und eine Atmosphäre schaffen, in der Fehler zum Lernen gehören. Digitale Trainingsangebote können ergänzend motivieren, benötigen aber eine kritische Nutzung. Bei körperlich anspruchsvollen Übungen bleibt fachliche Anleitung wichtig. Erfolgreiche Jugendsportpolitik verbindet daher Gesundheit, Zugänglichkeit, Mitbestimmung und Gemeinschaft.")]}
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
archive=ROOT/"exam-013.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
