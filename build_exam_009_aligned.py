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
"teil1_01.mp3":[("de-DE-KatjaNeural","Mitteilung der Personalabteilung: Am Donnerstag findet die Einführung in das neue digitale Assistenzsystem nicht im großen Konferenzraum statt. Wegen einer technischen Prüfung treffen sich die angemeldeten Beschäftigten im Raum 2.14. Die Uhrzeit bleibt bei neun Uhr.")],
"teil1_02.mp3":[("de-DE-KatjaNeural","Unser Team soll künftig ein KI-Programm für Kundenanfragen nutzen. Werden dadurch Arbeitsplätze überflüssig?"),("de-DE-ConradNeural","Das Programm sortiert einfache Fragen vor. Schwierige Fälle bearbeiten weiterhin Mitarbeitende."),("de-DE-KatjaNeural","Dann müssen wir lernen, die Vorschläge sorgfältig zu prüfen.")],
"teil1_03.mp3":[("de-DE-KatjaNeural","Hinweis aus dem Weiterbildungsbüro: Beschäftigte können sich bis zum 15. Mai für den Workshop Daten verstehen anmelden. Der Kurs richtet sich auch an Personen ohne technische Vorkenntnisse. Die Teilnahme gilt als Arbeitszeit, eine Anmeldung ist jedoch erforderlich.")],
"teil1_04.mp3":[("de-DE-AmalaNeural","Ich nutze eine Software, die lange Sitzungsprotokolle zusammenfasst. Das spart Zeit, aber ich übernehme die Ergebnisse nie ungeprüft. Einmal hatte das Programm eine wichtige Einschränkung übersehen. Seitdem vergleiche ich jede Zusammenfassung mit dem Originaltext.")],
"teil1_05.mp3":[("de-DE-KatjaNeural","Durchsage im Unternehmen: Die Testphase des automatischen Übersetzungsdienstes wird um zwei Wochen verlängert. Rückmeldungen sollen weiterhin über das interne Formular erfolgen. Bitte nennen Sie dort auch Fachbegriffe, bei denen besonders häufig Fehler auftreten.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Künstliche Intelligenz hält in immer mehr Büros Einzug. Herr Seidel, Sie begleiten Betriebe bei der Einführung solcher Systeme. Wo kann KI sinnvoll unterstützen?"),
("de-DE-ConradNeural","Seidel: Vor allem bei wiederkehrenden Aufgaben: Daten sortieren, Termine koordinieren oder große Textmengen durchsuchen. Dadurch gewinnen Beschäftigte Zeit für Gespräche, Entscheidungen und kreative Tätigkeiten. Zuerst muss ein Unternehmen aber klären, welches Problem es lösen möchte."),
("de-DE-KatjaNeural","Moderatorin: Was sollte vor der Einführung geschehen?"),
("de-DE-ConradNeural","Seidel: Die Beschäftigten müssen früh beteiligt werden. Sie kennen die Arbeitsabläufe und können Schwachstellen erkennen. Außerdem braucht es klare Regeln für vertrauliche Daten. Nicht jede Information darf in ein externes System eingegeben werden."),
("de-DE-KatjaNeural","Moderatorin: Verändert KI die Anforderungen an Mitarbeitende?"),
("de-DE-ConradNeural","Seidel: Ja. Digitale Grundkenntnisse werden wichtiger, ebenso die Fähigkeit, Ergebnisse kritisch zu beurteilen. Ein System kann überzeugend formulieren und trotzdem falsche Angaben machen. Schulungen sollten deshalb auch Grenzen und Risiken behandeln."),
("de-DE-KatjaNeural","Moderatorin: Was ist mit möglichen Arbeitsplatzverlusten?"),
("de-DE-ConradNeural","Seidel: Manche Tätigkeiten verändern sich oder fallen teilweise weg. Gleichzeitig entstehen neue Aufgaben, etwa bei der Qualitätskontrolle. Unternehmen sollten Weiterbildung anbieten und Veränderungen transparent erklären."),
("de-DE-KatjaNeural","Moderatorin: Was ist besonders wichtig?"),
("de-DE-ConradNeural","Seidel: Die Verantwortung darf nicht an die Software abgegeben werden. Bei wichtigen Entscheidungen muss eine zuständige Person das Ergebnis prüfen und begründen können.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderator: Sollten Unternehmen den Einsatz künstlicher Intelligenz stärker begrenzen? Frau Brandt, Sie vertreten einen Arbeitgeberverband."),
("de-DE-AmalaNeural","Brandt: Starre Verbote wären falsch. Betriebe müssen neue Werkzeuge testen können. Voraussetzung ist, dass Beschäftigte geschult werden und klare Zuständigkeiten bestehen."),
("de-DE-KatjaNeural","Moderator: Herr Kaya, Sie sind Betriebsratsmitglied."),
("de-DE-ConradNeural","Kaya: Ich sehe die Gefahr, dass Systeme zur Leistungskontrolle eingesetzt werden. Wenn jede Bewegung am Computer ausgewertet wird, entsteht Druck. Wir brauchen Mitbestimmung und Transparenz darüber, welche Daten erhoben werden."),
("de-DE-AmalaNeural","Brandt: Transparenz unterstütze ich. Gleichzeitig sollten wir kleine Pilotprojekte ermöglichen, bevor eine Lösung im ganzen Betrieb eingeführt wird. So lassen sich Fehler früh erkennen."),
("de-DE-ConradNeural","Kaya: Pilotprojekte sind sinnvoll, wenn sie freiwillig und zeitlich begrenzt sind. Beschäftigte müssen außerdem erfahren, wie ihre Rückmeldungen berücksichtigt werden."),
("de-DE-KatjaNeural","Moderator: Einigkeit besteht also darin, dass Erprobung möglich sein soll, aber nicht ohne Schutzregeln.")
],
"teil4_01.mp3":[("de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um den verantwortungsvollen Einsatz künstlicher Intelligenz in Unternehmen. Viele Anwendungen versprechen schnellere Abläufe und eine bessere Auswertung großer Datenmengen. Doch technischer Fortschritt ist nicht automatisch ein organisatorischer Vorteil. Zuerst muss klar sein, welches Ziel erreicht werden soll und woran sich der Nutzen messen lässt. Ein wichtiger Punkt ist die Datenqualität. Werden unvollständige oder einseitige Daten verwendet, können Ergebnisse verzerrt sein. Das betrifft beispielsweise Bewerbungsverfahren, bei denen ein System bestimmte Lebensläufe systematisch schlechter bewertet. Unternehmen sollten prüfen, welche Daten einfließen und ob unterschiedliche Gruppen fair behandelt werden. Auch Datenschutz und Informationssicherheit verdienen Aufmerksamkeit. Beschäftigte müssen wissen, welche Daten verarbeitet werden, zu welchem Zweck dies geschieht und wer Zugriff erhält. Sensible Informationen sollten nur mit klarer rechtlicher Grundlage und angemessenem Schutz genutzt werden. Ein weiterer Aspekt ist die menschliche Kontrolle. KI kann Vorschläge machen, versteht aber nicht automatisch alle sozialen und betrieblichen Zusammenhänge. Bei wichtigen Entscheidungen muss eine verantwortliche Person die Ergebnisse prüfen. Das gilt besonders, wenn berufliche Chancen oder Rechte beeinflusst werden. Schließlich braucht es Weiterbildung. Nicht alle Beschäftigten müssen programmieren können. Sie sollten jedoch verstehen, wie Systeme grundsätzlich funktionieren, welche Fehler auftreten können und wann menschliches Fachwissen erforderlich ist. So unterstützt KI Menschen, statt Verantwortung unsichtbar zu machen.")]}
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
archive=ROOT/"exam-009.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
