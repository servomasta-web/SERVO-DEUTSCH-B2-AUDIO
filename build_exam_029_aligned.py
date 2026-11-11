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
tracks={"teil1_01.mp3":[["de-DE-KatjaNeural","Mitteilung der Stadtbibliothek: Ab nächster Woche können Nutzerinnen und Nutzer E-Books auch für vier Wochen ausleihen. Bisher betrug die Leihfrist zwei Wochen. Die Zahl der gleichzeitig ausleihbaren Titel bleibt auf fünf begrenzt."]],"teil1_02.mp3":[["de-DE-KatjaNeural","A: Ich dachte, Bibliotheken seien nur noch zum Ausleihen von Büchern da. B: Überhaupt nicht. Unsere Bibliothek bietet auch Arbeitsplätze, Sprachcafés und Beratung zur digitalen Suche. A: Kann man dort auch lernen? B: Ja, es gibt ruhige Räume und Gruppenplätze."]],"teil1_03.mp3":[["de-DE-KatjaNeural","Hinweis der Bibliothek: Der Workshop zur Recherche wissenschaftlicher Quellen findet am Dienstag um 16 Uhr statt. Teilnehmende sollten ihren eigenen Laptop mitbringen. Die Anmeldung ist kostenlos und erfolgt über das Bibliothekskonto."]],"teil1_04.mp3":[["de-DE-AmalaNeural","Ich lese gern auf Papier, aber auf Reisen nehme ich inzwischen einen E-Reader mit. So kann ich mehrere Bücher dabei haben. Wenn ich längere Texte bearbeiten muss, bevorzuge ich trotzdem gedruckte Seiten, weil ich mich darauf besser konzentrieren kann."]],"teil1_05.mp3":[["de-DE-KatjaNeural","Durchsage: Der Lesesaal bleibt am Freitag wegen einer technischen Prüfung geschlossen. Die Ausleihe und Rückgabe am Selbstbedienungsautomaten im Eingangsbereich funktionieren weiterhin."]],"teil2_01.mp3":[["de-DE-KatjaNeural","Moderator: Manche Menschen glauben, Bibliotheken würden durch digitale Medien überflüssig. Frau Schneider, Sie leiten eine moderne Stadtbibliothek. Wie hat sich die Einrichtung verändert?\nSchneider: Bücher bleiben wichtig, aber unser Angebot ist breiter geworden. Wir verleihen E-Books, Hörbücher und digitale Zeitschriften. Gleichzeitig stellen wir Arbeitsplätze, Gruppenräume und technische Geräte zur Verfügung.\nModerator: Welche Rolle spielt Beratung?\nSchneider: Eine große. Viele Menschen wissen nicht, wie sie zuverlässige Informationen im Internet finden oder digitale Behördendienste nutzen können. Unsere Mitarbeitenden helfen bei der Recherche und erklären, wie Quellen bewertet werden.\nModerator: Werden Bibliotheken zu sozialen Treffpunkten?\nSchneider: Ja. Sprachcafés, Lesungen und Lernangebote bringen Menschen zusammen. Wichtig ist, dass Besucher sich auch ohne Kauf oder Mitgliedschaft bei jeder Veranstaltung willkommen fühlen.\nModerator: Wie erreichen Sie Menschen, die selten kommen?\nSchneider: Wir arbeiten mit Schulen, Seniorengruppen und Vereinen zusammen. Außerdem bieten wir mobile Bibliotheksdienste in Stadtteilen an, in denen der Weg zur nächsten Filiale weit ist.\nModerator: Was bleibt trotz aller Digitalisierung unverändert?\nSchneider: Unser Auftrag, Zugang zu Wissen zu ermöglichen. Dafür brauchen wir sowohl digitale Angebote als auch gedruckte Medien und persönliche Unterstützung."]],"teil3_01.mp3":[["de-DE-KatjaNeural","Moderatorin: Sollten öffentliche Bibliotheken ihre gedruckten Bestände reduzieren, um mehr Platz für digitale Angebote zu schaffen? Herr Fischer, Sie leiten eine Zweigstelle."],["de-DE-ConradNeural","Fischer: Wir brauchen beides. Manche Nutzer lesen lieber auf Papier, andere benötigen E-Books oder Datenbanken. Wenn wir gedruckte Bestände zu schnell abbauen, verlieren wir einen Teil unseres Publikums."],["de-DE-KatjaNeural","Moderatorin: Frau Yilmaz, Sie forscht zur digitalen Bildung."],["de-DE-ConradNeural","Yilmaz: Digitale Angebote sind wichtig, besonders für Menschen, die Informationen unterwegs nutzen. Bibliotheken sollten mehr Geräte und Schulungen anbieten. Aber ich fordere nicht, dass gedruckte Bücher verschwinden."],["de-DE-ConradNeural","Fischer: Der Platz ist allerdings begrenzt. Wir müssen prüfen, welche Titel häufig genutzt werden und welche selten. Wenig genutzte Bücher können eventuell in einem gemeinsamen Magazin aufbewahrt werden."],["de-DE-ConradNeural","Yilmaz: Das ist sinnvoll, solange sie weiterhin bestellbar bleiben. Außerdem sollte die Bibliothek Räume für Gruppenarbeit und digitale Beratung schaffen."],["de-DE-KatjaNeural","Moderatorin: Beide Seiten sprechen sich für eine Mischung aus gedruckten und digitalen Angeboten aus, setzen aber unterschiedliche Prioritäten bei Raum und Bestand."]],"teil4_01.mp3":[["de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um Bibliotheken im digitalen Zeitalter. Digitale Medien verändern, wie Menschen Informationen suchen und lesen. E-Books, Datenbanken und Online-Zeitschriften ermöglichen schnellen Zugriff auf viele Inhalte. Trotzdem verlieren Bibliotheken ihre Bedeutung nicht. Sie entwickeln ihre Aufgaben weiter und verbinden verschiedene Medienformen.\nEine zentrale Aufgabe bleibt der Zugang zu verlässlichem Wissen. Bibliotheksmitarbeitende helfen bei der Recherche, erklären Suchstrategien und zeigen, wie Quellen geprüft werden können. Das ist besonders wichtig, weil im Internet Informationen unterschiedlicher Qualität nebeneinanderstehen.\nBibliotheken bieten außerdem Räume für konzentriertes Arbeiten und gemeinsames Lernen. Gruppenräume, Computer und Internetzugang unterstützen Menschen, die zu Hause keine geeignete Ausstattung haben. Sprachcafés, Lesungen und Workshops schaffen Begegnungen und fördern Bildung.\nDigitale Angebote müssen zugänglich gestaltet sein. Dazu gehören verständliche Benutzeroberflächen, Unterstützung bei der Nutzung und der Schutz persönlicher Daten. Nicht alle Menschen verfügen über dieselben Geräte oder digitalen Kenntnisse. Persönliche Beratung bleibt deshalb wichtig.\nDie Zukunft der Bibliothek liegt nicht in der Entscheidung zwischen Papier und Bildschirm. Sie besteht darin, Medien, Räume und Beratung so zu verbinden, dass möglichst viele Menschen selbstständig lernen und am gesellschaftlichen Leben teilnehmen können."]]}
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
archive=ROOT/"exam-029.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
