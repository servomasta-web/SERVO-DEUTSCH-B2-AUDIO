import asyncio
import subprocess
import zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output")
AUDIO=ROOT/"audio"
AUDIO.mkdir(parents=True,exist_ok=True)

# Goethe B2 Hören — Prüfung 016: Kultur für alle.
# Acht aligned tracks with German dialogue voices and one- or two-play exam playback.
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Mitteilung des Kulturhauses: Für die Lesung am Freitag sind noch Plätze frei. Karten können bis Donnerstagabend online reserviert werden. An der Abendkasse ist nur eine begrenzte Anzahl verfügbar.")],
"teil1_02.mp3":[("de-DE-KatjaNeural","Ich würde gern öfter ins Theater gehen, aber die Karten sind teuer."),("de-DE-ConradNeural","Das Stadttheater bietet am ersten Sonntag im Monat ermäßigte Plätze an."),("de-DE-KatjaNeural","Gilt das auch für Studierende?"),("de-DE-ConradNeural","Ja, wenn du deinen Studierendenausweis an der Kasse vorzeigst.")],
"teil1_03.mp3":[("de-DE-KatjaNeural","Hinweis des Museums: Die Führung in einfacher Sprache beginnt am Samstag um 14 Uhr. Sie ist für Besucherinnen und Besucher mit unterschiedlichen Deutschkenntnissen geeignet. Eine Anmeldung wird empfohlen, ist aber nicht verpflichtend.")],
"teil1_04.mp3":[("de-DE-AmalaNeural","Ich helfe bei einem kleinen Musikfestival. Wir haben beschlossen, einen Teil der Eintrittskarten kostenlos an soziale Einrichtungen abzugeben. So können auch Menschen teilnehmen, die sich den regulären Preis nicht leisten können.")],
"teil1_05.mp3":[("de-DE-KatjaNeural","Durchsage der Stadt: Das Open-Air-Kino wird wegen der angekündigten Gewitter nicht im Park, sondern im Saal des Jugendzentrums gezeigt. Beginn und Eintrittspreis bleiben unverändert.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Kulturveranstaltungen sollen möglichst viele Menschen erreichen. Herr Neumann, Sie organisieren Programme für ein städtisches Kulturzentrum. Was bedeutet kulturelle Teilhabe?"),
("de-DE-AmalaNeural","Neumann: Nicht nur, dass eine Veranstaltung theoretisch offen ist. Menschen müssen sie auch erreichen und sich willkommen fühlen können. Dazu gehören bezahlbare Eintrittspreise, verständliche Informationen und Räume, die auch mit Rollstuhl zugänglich sind."),
("de-DE-KatjaNeural","Moderatorin: Wie kann man Menschen ansprechen, die selten Kulturveranstaltungen besuchen?"),
("de-DE-AmalaNeural","Neumann: Man sollte mit Schulen, Vereinen und sozialen Einrichtungen zusammenarbeiten. Mobile Angebote in Stadtteilen können erste Kontakte schaffen. Außerdem ist es wichtig, verschiedene Interessen zu berücksichtigen und nicht nur klassische Konzerte oder Ausstellungen anzubieten."),
("de-DE-KatjaNeural","Moderatorin: Welche Rolle spielt die Sprache?"),
("de-DE-AmalaNeural","Neumann: Eine große. Mehrsprachige Hinweise, Veranstaltungen in einfacher Sprache oder Übersetzungen können Barrieren abbauen. Das bedeutet nicht, dass jede Veranstaltung in vielen Sprachen stattfinden muss. Entscheidend ist, Informationen verständlich und zielgruppengerecht bereitzustellen."),
("de-DE-KatjaNeural","Moderatorin: Wie lässt sich die Qualität beurteilen?"),
("de-DE-AmalaNeural","Neumann: Nicht nur anhand der Besucherzahl. Wir fragen auch, wer gekommen ist, wer sich nicht angesprochen fühlte und welche Hindernisse bestanden. Rückmeldungen sollten in die nächste Planung einfließen."),
("de-DE-KatjaNeural","Moderatorin: Was ist langfristig wichtig?"),
("de-DE-AmalaNeural","Neumann: Kontinuität. Ein einzelner kostenloser Abend verändert wenig, wenn danach wieder alle Angebote unerschwinglich oder schwer erreichbar sind. Teilhabe muss bei der gesamten Programmplanung mitgedacht werden.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderator: Sollten öffentliche Kulturveranstaltungen grundsätzlich kostenlos sein? Frau Fuchs, Sie leiten ein kleines Theater."),
("de-DE-AmalaNeural","Fuchs: Ein kostenloser Eintritt klingt attraktiv, aber Produktionen kosten Geld. Wenn keine Einnahmen erzielt werden, hängt das Theater vollständig von Zuschüssen ab. Ich halte gestaffelte Preise und einzelne kostenfreie Veranstaltungen für realistischer."),
("de-DE-KatjaNeural","Moderator: Herr Ali, Sie engagieren sich in einer Initiative für kulturelle Bildung."),
("de-DE-ConradNeural","Ali: Eintrittspreise sind für manche Familien eine echte Hürde. Öffentliche Kultur sollte nicht davon abhängen, wie viel Geld jemand hat. Deshalb brauchen wir verlässliche Fördermittel und kostenlose Plätze für Menschen mit geringem Einkommen."),
("de-DE-AmalaNeural","Fuchs: Solche Plätze finde ich wichtig. Gleichzeitig müssen wir sicherstellen, dass Künstlerinnen und Künstler fair bezahlt werden. Eine Veranstaltung kann nicht dauerhaft nur durch freiwillige Arbeit entstehen."),
("de-DE-ConradNeural","Ali: Natürlich. Kostenfreiheit darf nicht bedeuten, dass Kulturschaffende auf ihr Honorar verzichten. Kommunen und Förderer sollten die Kosten übernehmen, wenn sie Teilhabe ermöglichen wollen."),
("de-DE-KatjaNeural","Moderator: Beide wollen finanzielle Hürden senken und eine faire Bezahlung sichern, unterscheiden sich aber bei der allgemeinen Preisgestaltung.")
],
"teil4_01.mp3":[("de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es darum, wie Kulturveranstaltungen für unterschiedliche Bevölkerungsgruppen zugänglich werden. Kultur schafft Begegnungen, eröffnet neue Perspektiven und ermöglicht Menschen, ihre Erfahrungen auszutauschen. Damit diese Wirkung entsteht, müssen Angebote mehr Menschen erreichen als nur ein bereits interessiertes Stammpublikum. Eine wichtige Hürde sind die Kosten. Ermäßigte Karten, Familienangebote und Kontingente für soziale Einrichtungen können helfen. Kostenfreiheit ist jedoch nicht die einzige Lösung. Veranstalter müssen auch sicherstellen, dass Künstlerinnen, Techniker und andere Beschäftigte angemessen bezahlt werden. Öffentliche Förderung kann dabei eine wichtige Rolle spielen. Auch der Ort entscheidet über die Teilnahme. Wenn Veranstaltungen nur in der Innenstadt stattfinden, sind sie für Menschen in äußeren Stadtteilen oder ländlichen Regionen schwer erreichbar. Mobile Bühnen, Kooperationen mit Schulen und Angebote in Nachbarschaftszentren können neue Gruppen ansprechen. Barrierefreiheit umfasst mehr als einen stufenlosen Eingang. Dazu gehören verständliche Informationen, geeignete Sitzplätze, Angebote in einfacher Sprache und bei Bedarf Gebärdensprach- oder Übersetzungsunterstützung. Veranstalter sollten frühzeitig prüfen, welche Bedürfnisse ihr Publikum hat. Schließlich braucht es Rückmeldung und langfristige Planung. Besucherzahlen allein zeigen nicht, ob ein Angebot wirklich offen ist. Gespräche mit Menschen, die bisher nicht teilnehmen, können Hindernisse sichtbar machen. Kulturelle Teilhabe gelingt dann, wenn Preis, Ort, Sprache und Zugänglichkeit gemeinsam berücksichtigt werden.")]}
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
archive=ROOT/"exam-016.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
