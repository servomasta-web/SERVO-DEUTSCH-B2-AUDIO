# SERVO DEUTSCH B2 — exam 032 aligned audio generation
import asyncio
import subprocess
import zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output")
AUDIO=ROOT/"audio"
AUDIO.mkdir(parents=True,exist_ok=True)

# Audioinhalte sind auf die 30 Fragen von Prüfung 031 abgestimmt.
tracks={
"teil1_01.mp3":[["de-DE-KatjaNeural","Gute Nachrichten für alle Leserinnen und Leser: Ab kommenden Montag erweitert die Stadtbibliothek ihre Öffnungszeiten. An drei Wochentagen bleibt sie künftig bis zwanzig Uhr geöffnet. So können auch Berufstätige nach Feierabend Medien ausleihen und in Ruhe arbeiten."]],
"teil1_02.mp3":[["de-DE-ConradNeural","Hinweis für Besucherinnen und Besucher: Wer unseren Lesesaal am Abend nutzen möchte, muss am Eingang einen gültigen Bibliotheksausweis vorzeigen. Eine zusätzliche Reservierung ist nicht nötig. Die Arbeitsplätze können weiterhin nicht im Voraus gebucht werden."]],
"teil1_03.mp3":[["de-DE-AmalaNeural","Die Stadtbibliothek veranstaltet am nächsten Mittwoch einen Workshop zur digitalen Recherche. Dabei lernen Interessierte, zuverlässige Quellen im Internet zu finden und Suchmaschinen gezielt zu nutzen. Das Angebot richtet sich an Erwachsene und Jugendliche. Vorkenntnisse sind nicht erforderlich."]],
"teil1_04.mp3":[["de-DE-KatjaNeural","Ab sofort bietet die Bibliothek persönliche Beratungen zur Nutzung von E-Book-Readern an. Die erste offene Sprechstunde findet am Donnerstag um sechzehn Uhr statt. Wer bereits ein eigenes Gerät besitzt, kann es gern mitbringen. Eine Anmeldung ist nicht erforderlich."]],
"teil1_05.mp3":[["de-DE-ConradNeural","Wegen Renovierungsarbeiten wird der Lesesaal im Erdgeschoss teilweise geschlossen. Studierende und andere Besucher können jedoch weiterhin lernen: Im Nachbargebäude steht ein zusätzlicher Raum mit Arbeitsplätzen zur Verfügung. Die Beschilderung führt direkt zum Eingang."]],
"teil2_01.mp3":[["de-DE-KatjaNeural","Moderatorin: Öffentliche Bibliotheken haben sich in den vergangenen Jahren stark verändert. Frau Berger, Sie leiten eine Stadtbibliothek. Welche Aufgaben stehen heute im Mittelpunkt?\nDirektorin: Bibliotheken sind längst nicht mehr nur Orte, an denen Bücher ausgeliehen werden. Sie bieten Zugang zu gedruckten und digitalen Medien, unterstützen Menschen beim Lernen und schaffen Räume für Begegnungen. Diese Mischung ist besonders wichtig, weil die Bedürfnisse sehr unterschiedlich sind.\nModeratorin: Bedeutet das, dass gedruckte Bücher an Bedeutung verlieren?\nDirektorin: Nicht unbedingt. Viele Menschen lesen weiterhin gern auf Papier. Für manche ist das angenehmer, andere können gedruckte Bücher leichter nutzen als digitale Geräte. Deshalb sollten wir nicht die eine Form gegen die andere ausspielen.\nModeratorin: Welche Vorteile haben digitale Angebote?\nDirektorin: E-Books und digitale Zeitungen lassen sich oft auch außerhalb der Öffnungszeiten ausleihen. Das ist praktisch, besonders für Menschen, die weit entfernt wohnen oder wenig Zeit haben. Allerdings sind nicht alle Titel sofort verfügbar, und man braucht ein geeignetes Gerät sowie eine Internetverbindung.\nModeratorin: Bekommen Sie häufig Fragen zur Technik?\nDirektorin: Ja, und zwar von Menschen aller Altersgruppen. Einige möchten lernen, einen E-Book-Reader zu bedienen. Andere brauchen Unterstützung bei Online-Katalogen oder digitalen Behördendiensten. Wir bieten deshalb regelmäßige Einführungskurse an, die ohne komplizierte Anmeldung besucht werden können.\nModeratorin: Wie erreichen Sie Menschen, die bisher selten in eine Bibliothek kommen?\nDirektorin: Wir arbeiten mit Schulen, Vereinen und sozialen Einrichtungen zusammen. Außerdem organisieren wir Sprachcafés und Informationsveranstaltungen. Wichtig ist, dass niemand das Gefühl hat, bestimmte Vorkenntnisse mitbringen zu müssen.\nModeratorin: Welche Entwicklung ist für die Zukunft entscheidend?\nDirektorin: Wir müssen neue Technik sinnvoll einsetzen, ohne den persönlichen Kontakt zu verlieren. Unser Angebot soll barrierefrei sein und unterschiedliche Altersgruppen berücksichtigen. Eine moderne Bibliothek ist dann erfolgreich, wenn Menschen dort sowohl selbstständig lernen als auch miteinander ins Gespräch kommen können."]],
"teil3_01.mp3":[["de-DE-KatjaNeural","Moderatorin: Welche Bedeutung haben Bibliotheken heute noch, wenn so viele Informationen online verfügbar sind? Nora, was meinen Sie?"],["de-DE-AmalaNeural","Nora: Für mich sind Bibliotheken vor allem ein wichtiger Lernort. Nicht jede Person hat zu Hause einen ruhigen Platz oder eine stabile Internetverbindung. Gerade Schülerinnen, Studierende und Menschen, die sich beruflich weiterbilden, brauchen solche öffentlichen Räume. Ich fände außerdem längere Öffnungszeiten am Wochenende sinnvoll."],["de-DE-KatjaNeural","Moderatorin: Tim, sehen Sie das ähnlich?"],["de-DE-ConradNeural","Tim: Teilweise. Digitale Angebote sind eine große Chance, aber sie müssen für alle erreichbar sein. Wer kein modernes Gerät besitzt, darf nicht ausgeschlossen werden. Die Bibliothek sollte Leihgeräte bereitstellen und erklären, wie man sie benutzt. Und trotz aller Technik darf die persönliche Beratung nicht verschwinden."],["de-DE-KatjaNeural","Moderatorin: Selin, welche Erfahrungen haben Sie gemacht?"],["de-DE-AmalaNeural","Selin: Ich besuche regelmäßig ein Sprachcafé in unserer Bibliothek. Dort üben Menschen gemeinsam Deutsch und lernen andere aus der Nachbarschaft kennen. Das Angebot ist offen und kostenlos. Ich würde mir wünschen, dass die Bibliothek noch stärker mit lokalen Vereinen zusammenarbeitet, damit weitere Gruppen eigene Veranstaltungen anbieten können."],["de-DE-ConradNeural","Tim: Solche Begegnungen sind wertvoll. Trotzdem muss man darauf achten, dass digitale Informationen verständlich und zuverlässig bleiben."],["de-DE-KatjaNeural","Moderatorin: Offenbar geht es also nicht darum, Bücher durch Bildschirme zu ersetzen, sondern unterschiedliche Angebote miteinander zu verbinden."]],
"teil4_01.mp3":[["de-DE-ConradNeural","Guten Tag. In meinem Vortrag beschäftige ich mich mit öffentlichen Bibliotheken im digitalen Zeitalter. Obwohl Informationen heute jederzeit über das Internet abrufbar scheinen, behalten Bibliotheken eine wichtige gesellschaftliche Funktion. Ihre Aufgaben haben sich erweitert: Neben der Medienausleihe stehen Bildung, Orientierung und soziale Begegnung im Mittelpunkt.\nEine wesentliche Veränderung ist die Vielfalt der Medien. Neben gedruckten Büchern gehören E-Books, Hörbücher, Datenbanken und digitale Zeitungen zum Angebot. Dadurch können Nutzerinnen und Nutzer Informationen auf unterschiedliche Weise erreichen. Dennoch bleibt das gedruckte Buch für viele Menschen attraktiv. Eine moderne Einrichtung sollte deshalb verschiedene Formate anbieten, statt ausschließlich auf eine technische Lösung zu setzen.\nDamit Menschen digitale Inhalte sinnvoll nutzen können, benötigen sie Medienkompetenz. Dazu gehört nicht nur, Informationen zu suchen. Man muss auch beurteilen können, ob eine Quelle glaubwürdig ist, wer eine Nachricht veröffentlicht hat und zu welchem Zweck bestimmte Inhalte verbreitet werden. Gerade bei der großen Menge verfügbarer Informationen ist diese Fähigkeit entscheidend.\nBibliotheken unterstützen außerdem das lebenslange Lernen. Sie stellen Lernmaterialien bereit, bieten Kurse und ermöglichen selbstständiges Arbeiten. Für Menschen, die zu Hause keinen ruhigen Arbeitsplatz haben, sind solche Räume besonders wertvoll. Auch Sprachcafés und Veranstaltungen können dazu beitragen, dass Menschen mit unterschiedlichen Erfahrungen miteinander in Kontakt kommen.\nDie Digitalisierung bringt allerdings Herausforderungen mit sich. Nicht alle verfügen über geeignete Geräte oder ausreichende Kenntnisse. Deshalb müssen digitale Angebote verständlich gestaltet sein. Datenschutz und Barrierefreiheit dürfen bei der Einführung neuer Technologien ebenfalls nicht vernachlässigt werden. Persönliche Beratung bleibt notwendig, damit niemand wegen fehlender Erfahrung ausgeschlossen wird.\nEine weitere Stärke entsteht durch Zusammenarbeit. Wenn Bibliotheken mit Schulen, Vereinen und sozialen Einrichtungen kooperieren, können sie Angebote entwickeln, die auf konkrete Bedürfnisse vor Ort reagieren. So werden sie zu offenen Treffpunkten und stärken die Teilhabe am gesellschaftlichen Leben.\nZusammenfassend lässt sich sagen: Die Zukunft öffentlicher Bibliotheken liegt weder allein im gedruckten Buch noch ausschließlich in digitalen Medien. Entscheidend ist die Verbindung aus verlässlichen Informationen, technischer Unterstützung und gemeinschaftlichen Räumen. Vielen Dank für Ihre Aufmerksamkeit."]]
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
archive=ROOT/"exam-032.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
