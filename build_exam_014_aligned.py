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
"teil1_01.mp3":[("de-DE-KatjaNeural","Mitteilung der Personalabteilung: Der interne Sprachstammtisch findet ab nächster Woche jeden zweiten Mittwoch statt. Beschäftigte können dort in kleinen Gruppen Deutsch, Englisch und weitere Sprachen üben. Eine Anmeldung ist nicht erforderlich.")],
"teil1_02.mp3":[("de-DE-KatjaNeural","Für das neue Projekt arbeiten Kolleginnen aus vier Ländern zusammen."),("de-DE-ConradNeural","Das kann sehr hilfreich sein, aber wir sollten wichtige Entscheidungen schriftlich festhalten."),("de-DE-KatjaNeural","Wegen der unterschiedlichen Sprachen?"),("de-DE-ConradNeural","Ja, damit alle dieselben Informationen erhalten und Missverständnisse später geklärt werden können.")],
"teil1_03.mp3":[("de-DE-KatjaNeural","Hinweis des Weiterbildungszentrums: Der Kurs Deutsch im Kundenkontakt beginnt am 6. Juni. Er richtet sich an Beschäftigte mit mindestens B1-Kenntnissen. Die Teilnahme ist kostenlos, wenn der Arbeitgeber die Anmeldung bestätigt.")],
"teil1_04.mp3":[("de-DE-AmalaNeural","In meinem Team sprechen wir im Alltag meistens Deutsch. Bei technischen Fragen helfen manchmal englische Fachbegriffe, die alle kennen. Wenn neue Kolleginnen dazukommen, erklären wir wichtige Abkürzungen zusätzlich, damit niemand ausgeschlossen wird.")],
"teil1_05.mp3":[("de-DE-KatjaNeural","Durchsage: Die Dolmetschunterstützung für das Beratungsgespräch am Donnerstag muss bis spätestens Dienstag beim Empfang bestellt werden. Für spontane Anfragen am Gesprächstag kann keine Übersetzung garantiert werden.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: In vielen Unternehmen arbeiten Menschen mit unterschiedlichen Erstsprachen zusammen. Herr Aydin, Sie beraten internationale Teams. Ist Mehrsprachigkeit grundsätzlich ein Vorteil?"),
("de-DE-AmalaNeural","Aydin: Sie kann ein großer Vorteil sein. Mitarbeitende verstehen verschiedene Märkte und können Kontakte zu Kundinnen und Kunden aufbauen. Allerdings entsteht dieser Nutzen nicht automatisch. Unternehmen müssen klären, welche Sprache in welchen Situationen verwendet wird."),
("de-DE-KatjaNeural","Moderatorin: Sollte eine Firma eine gemeinsame Arbeitssprache festlegen?"),
("de-DE-AmalaNeural","Aydin: Für Sicherheitsanweisungen, Verträge oder wichtige Projektentscheidungen ist eine gemeinsame Sprache oft sinnvoll. Das bedeutet aber nicht, dass andere Sprachen im Alltag keinen Platz haben. Informelle Gespräche oder Kontakte zu internationalen Partnern können in weiteren Sprachen stattfinden."),
("de-DE-KatjaNeural","Moderatorin: Welche Schwierigkeiten treten häufig auf?"),
("de-DE-AmalaNeural","Aydin: Fachbegriffe, unterschiedliche Kommunikationsstile und unausgesprochene Erwartungen. Manche Beschäftigte sprechen weniger, weil sie Angst vor Fehlern haben. Führungskräfte sollten deshalb deutlich machen, dass Rückfragen willkommen sind und nicht als mangelnde Kompetenz gelten."),
("de-DE-KatjaNeural","Moderatorin: Wie können Unternehmen unterstützen?"),
("de-DE-AmalaNeural","Aydin: Durch Sprachkurse, Tandemprogramme und verständliche Dokumente. Bei wichtigen Besprechungen helfen Zusammenfassungen und schriftliche Aufgabenlisten. Auch erfahrene Mitarbeitende können neue Kolleginnen sprachlich begleiten."),
("de-DE-KatjaNeural","Moderatorin: Was ist langfristig entscheidend?"),
("de-DE-AmalaNeural","Aydin: Eine offene Unternehmenskultur. Mehrsprachigkeit darf nicht nur als private Fähigkeit betrachtet werden, sondern sollte als Ressource anerkannt werden, ohne einzelne Personen ständig als Übersetzer einzusetzen.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderator: Sollten Unternehmen bei Bewerbungen ausschließlich sehr gute Deutschkenntnisse verlangen? Frau Keller, Sie leiten eine Personalabteilung."),
("de-DE-AmalaNeural","Keller: Für manche Tätigkeiten ist ein hohes Deutschniveau unverzichtbar, zum Beispiel bei rechtlichen Dokumenten oder komplexer Beratung. Bei anderen Aufgaben können Fachkenntnisse und weitere Sprachen ebenso wichtig sein. Anforderungen sollten deshalb zur konkreten Stelle passen."),
("de-DE-KatjaNeural","Moderator: Herr Mensah, Sie vertreten einen Verband internationaler Fachkräfte."),
("de-DE-ConradNeural","Mensah: Zu strenge Sprachvorgaben schließen qualifizierte Menschen aus. Oft könnten Beschäftigte die nötigen Fachbegriffe während der Einarbeitung lernen. Unternehmen sollten stärker zwischen allgemeiner Sprachsicherheit und den Anforderungen einzelner Aufgaben unterscheiden."),
("de-DE-AmalaNeural","Keller: Da stimme ich teilweise zu. Trotzdem muss ein Team sicher kommunizieren können. Wenn eine Person wichtige Anweisungen nicht versteht, kann das zu Fehlern führen."),
("de-DE-ConradNeural","Mensah: Deshalb schlage ich berufsbegleitende Sprachförderung und klare Einarbeitungspläne vor. So werden Anforderungen nicht abgesenkt, sondern gezielt entwickelt."),
("de-DE-KatjaNeural","Moderator: Beide Seiten betonen die Bedeutung verständlicher Kommunikation, setzen aber unterschiedliche Akzente bei den Zugangsvoraussetzungen.")
],
"teil4_01.mp3":[("de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um Mehrsprachigkeit am Arbeitsplatz. In internationalen Unternehmen treffen unterschiedliche sprachliche Erfahrungen aufeinander. Das kann die Zusammenarbeit bereichern, weil Mitarbeitende verschiedene Märkte, kulturelle Zusammenhänge und Kommunikationswege kennen. Gleichzeitig entstehen Herausforderungen, wenn Informationen nicht eindeutig verstanden werden. Eine wichtige Voraussetzung ist eine klare Sprachregelung. Unternehmen sollten festlegen, welche Sprache für Sicherheitsfragen, verbindliche Dokumente und zentrale Projektentscheidungen verwendet wird. Diese Regel muss transparent sein und darf nicht dazu führen, dass andere Sprachen grundsätzlich abgewertet werden. In informellen Situationen können mehrere Sprachen sinnvoll sein. Besonders wichtig ist verständliche Kommunikation. Fachbegriffe sollten erklärt, Abkürzungen eingeführt und zentrale Ergebnisse schriftlich zusammengefasst werden. Bei Besprechungen können kurze Wiederholungen sicherstellen, dass alle Beteiligten dieselben Aufgaben verstanden haben. Sprachförderung sollte eng mit der beruflichen Praxis verbunden sein. Tandemprogramme, interne Sprachkurse und gemeinsame Übungen helfen, Wortschatz aufzubauen. Führungskräfte können eine Atmosphäre schaffen, in der Nachfragen erlaubt sind und Fehler als Teil des Lernprozesses gelten. Schließlich ist Mehrsprachigkeit eine Ressource, aber keine unbegrenzte Zusatzpflicht. Beschäftigte dürfen nicht automatisch für jede Übersetzung verantwortlich gemacht werden, nur weil sie mehrere Sprachen sprechen. Professionelle Dolmetsch- oder Übersetzungsdienste bleiben bei wichtigen Inhalten notwendig. Eine inklusive Arbeitskultur verbindet daher klare Standards mit Respekt vor sprachlicher Vielfalt.")]}
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
archive=ROOT/"exam-014.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
