import asyncio, subprocess, zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output")
AUDIO=ROOT/"audio"
AUDIO.mkdir(parents=True,exist_ok=True)

# Prüfung 021: Zusammenleben der Generationen
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Mitteilung des Nachbarschaftshauses: Unser Erzählcafé findet ab sofort jeden Dienstag ab sechzehn Uhr statt. Menschen jeden Alters sind herzlich eingeladen, Erinnerungen und Geschichten miteinander zu teilen. Eine Anmeldung ist nicht erforderlich.")],
"teil1_02.mp3":[("de-DE-ConradNeural","Hinweis der Stadtbibliothek: Der Medienworkshop für Jugendliche beginnt am kommenden Freitag um fünfzehn Uhr. Die Teilnahme ist kostenlos. Bitte melden Sie sich vorher in der Bibliothek oder über unsere Internetseite an, da die Plätze begrenzt sind.")],
"teil1_03.mp3":[("de-DE-AmalaNeural","Am Samstag veranstaltet die Nachbarschaftsinitiative einen gemeinsamen Gartentag. Werkzeuge und kleine Pflanzen werden bereitgestellt. Für das gemeinsame Mittagessen bitten wir alle Teilnehmenden, einen kleinen Imbiss mitzubringen. Wir treffen uns um neun Uhr am Garteneingang.")],
"teil1_04.mp3":[("de-DE-KatjaNeural","Die kommunale Beratungsstelle unterstützt Familien bei Konflikten zwischen Jung und Alt. Gespräche sind vertraulich und kostenlos. Sie erreichen unser Team montags und mittwochs zwischen vierzehn und siebzehn Uhr. Das Angebot richtet sich an alle Generationen.")],
"teil1_05.mp3":[("de-DE-ConradNeural","Für das diesjährige Generationenfest im Stadtpark suchen wir noch freiwillige Helferinnen und Helfer. Besonders gebraucht werden Personen für den Informationsstand und die Kinderaktivitäten. Interessierte können sich über das Formular auf unserer Website anmelden.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: In vielen Familien treffen unterschiedliche Lebensweisen und Erwartungen aufeinander. Frau Professorin Weber, Sozialwissenschaftlerin, warum entstehen daraus Konflikte?"),
("de-DE-AmalaNeural","Weber: Häufig geht es weniger um das Alter selbst als um unterschiedliche Erfahrungen und Vorstellungen. Ältere Familienmitglieder wünschen sich manchmal Sicherheit und Verlässlichkeit, während Jüngere mehr Freiraum und Selbstständigkeit erwarten."),
("de-DE-KatjaNeural","Moderatorin: Welche Rolle spielen digitale Medien dabei?"),
("de-DE-AmalaNeural","Weber: Sie können Generationen verbinden, etwa durch Nachrichten und Videoanrufe. Gleichzeitig entstehen Missverständnisse, wenn die eine Seite schnelle Antworten erwartet und die andere digitale Kommunikation weniger selbstverständlich nutzt. Wichtig ist, nicht vorschnell zu urteilen."),
("de-DE-KatjaNeural","Moderatorin: Wie kann man mit unterschiedlichen Meinungen umgehen?"),
("de-DE-AmalaNeural","Weber: Zunächst sollte jede Person erklären dürfen, was ihr wichtig ist. Zuhören bedeutet nicht, dass man sofort zustimmen muss. Es hilft aber, die Beweggründe der anderen Seite zu verstehen. Danach kann man nach einer Lösung suchen, die die Bedürfnisse aller berücksichtigt."),
("de-DE-KatjaNeural","Moderatorin: Sind gemeinsame Aktivitäten ebenfalls sinnvoll?"),
("de-DE-AmalaNeural","Weber: Ja, besonders wenn sie nicht unter dem Druck stehen, ein Problem lösen zu müssen. Beim Kochen, Spazierengehen oder bei einem Projekt im Garten entstehen Gespräche oft ganz natürlich. Solche Erfahrungen können Vertrauen schaffen."),
("de-DE-KatjaNeural","Moderatorin: Was sollten Großeltern beachten, wenn sie jüngere Familienmitglieder beraten?"),
("de-DE-AmalaNeural","Weber: Sie können ihre Erfahrung anbieten, sollten aber Entscheidungen nicht abnehmen. Junge Erwachsene müssen eigene Wege ausprobieren dürfen. Umgekehrt können Jüngere anerkennen, dass Lebenserfahrung wertvoll ist. Ein respektvoller Austausch funktioniert in beide Richtungen."),
("de-DE-KatjaNeural","Moderatorin: Was ist Ihr wichtigster Rat?"),
("de-DE-AmalaNeural","Weber: Nicht das Alter sollte bestimmen, wer recht hat. Entscheidend sind gegenseitiger Respekt, Geduld und die Bereitschaft, voneinander zu lernen.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Wie kann das Zusammenleben verschiedener Generationen im Stadtteil verbessert werden? Frau Neumann, Sie engagieren sich in einem Mehrgenerationenprojekt."),
("de-DE-AmalaNeural","Neumann: Meiner Ansicht nach braucht es mehr Gelegenheiten, bei denen Menschen gemeinsam etwas tun. Bei unserem Gartenprojekt arbeiten Jugendliche und ältere Nachbarn zusammen. Dabei entstehen Kontakte, die im Alltag sonst kaum zustande kämen. Erfahrung weiterzugeben ist schön, aber ältere Menschen sollten nicht alles bestimmen wollen."),
("de-DE-KatjaNeural","Moderatorin: Herr Kaya, Sie vertreten einen Jugendverein."),
("de-DE-ConradNeural","Kaya: Ich finde vor allem wichtig, Jugendlichen mehr Vertrauen entgegenzubringen. Oft wird über sie gesprochen, ohne sie an Entscheidungen zu beteiligen. Wenn junge Leute eigene Ideen umsetzen dürfen, übernehmen sie auch Verantwortung. Digitale Kommunikation kann dabei helfen, sollte persönliche Treffen aber nicht ersetzen."),
("de-DE-AmalaNeural","Neumann: Da stimme ich zu. Gemeinsame Projekte funktionieren besonders gut, wenn alle Beteiligten Aufgaben übernehmen und nicht nur eine Gruppe die Regeln festlegt. Bei Konflikten sollten wir außerdem feste Gesprächszeiten anbieten."),
("de-DE-ConradNeural","Kaya: Gesprächsregeln können sinnvoll sein, solange sie nicht zu kompliziert werden. Wichtig ist, dass niemand ausgelacht oder sofort unterbrochen wird. Und beide Seiten müssen bereit sein, sich zu verändern; Anpassung darf nicht nur von den Jüngeren verlangt werden."),
("de-DE-KatjaNeural","Moderatorin: Sie betonen also unterschiedliche Schwerpunkte, sehen aber beide Dialog und gegenseitige Beteiligung als Grundlage.")
],
"teil4_01.mp3":[("de-DE-ConradNeural","Guten Tag. In meinem Vortrag beschäftige ich mich mit der Frage, wie das Zusammenleben verschiedener Generationen gelingen kann. In Familien, Nachbarschaften und am Arbeitsplatz begegnen sich Menschen, deren Alltag und Erfahrungen teilweise sehr unterschiedlich sind. Daraus können Spannungen entstehen, aber auch wertvolle Möglichkeiten zum Lernen.\nZunächst ist wichtig zu verstehen, dass Generationen keine einheitlichen Gruppen sind. Nicht alle älteren Menschen denken gleich, und auch Jugendliche haben unterschiedliche Wünsche. Konflikte entstehen oft dann, wenn wir einzelne Erfahrungen verallgemeinern oder Erwartungen nicht offen aussprechen.\nEine Grundlage für ein gutes Miteinander ist gegenseitige Anerkennung. Ältere Menschen können Wissen und Lebenserfahrung weitergeben. Jüngere können neue Perspektiven und digitale Kenntnisse einbringen. Entscheidend ist, dass daraus kein Wettbewerb entsteht. Beide Seiten sollten Fragen stellen und die Entscheidungen der anderen ernst nehmen.\nAuch gemeinsame Begegnungsorte spielen eine wichtige Rolle. Mehrgenerationenhäuser, Vereine und Nachbarschaftsprojekte schaffen Gelegenheiten, bei denen Menschen miteinander ins Gespräch kommen. Besonders erfolgreich sind Aktivitäten, wenn alle Beteiligten mitplanen und Verantwortung übernehmen können.\nDigitale Medien bieten zusätzliche Möglichkeiten, Kontakte zu halten und Informationen auszutauschen. Dennoch ersetzen sie persönliche Begegnungen nicht vollständig. Ein gemeinsames Essen oder ein Gespräch beim Spaziergang kann Missverständnisse klären, die in kurzen Nachrichten entstehen.\nWenn Konflikte auftreten, sollte man konkrete Situationen ansprechen, statt Personen oder ganze Altersgruppen zu kritisieren. Zuhören, nachfragen und gemeinsam nach Lösungen suchen kostet Zeit, verhindert aber, dass sich Vorurteile verfestigen.\nZusammenfassend lässt sich sagen: Ein gutes Zusammenleben entsteht nicht automatisch. Es braucht Dialog, Geduld und gemeinsame Verantwortung. Wenn jede Generation bereit ist, sowohl etwas anzubieten als auch von anderen zu lernen, profitieren alle davon.")],
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
                if not part.exists() or part.stat().st_size<1000: raise RuntimeError("Audio fehlt oder ist trop petit")
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
    if len(tracks)!=8: raise RuntimeError("Il faut exactement huit pistes")
    for name,utterances in tracks.items(): await make_track(name,utterances)

asyncio.run(main())
expected=["teil1_01.mp3","teil1_02.mp3","teil1_03.mp3","teil1_04.mp3","teil1_05.mp3","teil2_01.mp3","teil3_01.mp3","teil4_01.mp3"]
archive=ROOT/"exam-021.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
