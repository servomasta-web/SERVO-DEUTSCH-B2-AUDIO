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
tracks={"teil1_01.mp3":[["de-DE-KatjaNeural","Mitteilung der Personalabteilung: Neue internationale Mitarbeitende können sich ab sofort für eine Einführungsveranstaltung anmelden. Sie findet am 8. November von neun bis zwölf Uhr statt. Die Teilnahme gilt als Arbeitszeit und wird nicht vom Urlaub abgezogen."]],"teil1_02.mp3":[["de-DE-KatjaNeural","A: Unsere neue Kollegin ist erst seit zwei Wochen hier. B: Hat sie schon eine Ansprechperson? A: Ja, ein erfahrener Mitarbeiter begleitet sie in den ersten Monaten. B: Das ist gut. Dann kann sie Fragen zu Abläufen stellen, ohne jedes Mal die Teamleitung suchen zu müssen."]],"teil1_03.mp3":[["de-DE-KatjaNeural","Hinweis der Ausländerberatung: Für die Anerkennung eines ausländischen Berufsabschlusses müssen beglaubigte Übersetzungen der Zeugnisse eingereicht werden. Einfache Kopien können zur ersten Beratung mitgebracht werden, ersetzen aber nicht die vollständigen Unterlagen."]],"teil1_04.mp3":[["de-DE-AmalaNeural","Ich habe meinen Abschluss aus dem Ausland anerkennen lassen. Der Prozess dauerte länger als erwartet, weil ein Dokument fehlte. Die Beratungsstelle hat mir erklärt, welche Stelle es ausstellen muss. Danach konnte ich den Antrag vervollständigen."]],"teil1_05.mp3":[["de-DE-KatjaNeural","Durchsage im Unternehmen: Der Workshop zu interkultureller Zusammenarbeit wird wegen einer Erkrankung der Referentin vom Donnerstag auf den folgenden Montag verschoben. Der Raum und die Uhrzeit bleiben gleich."]],"teil2_01.mp3":[["de-DE-KatjaNeural","Moderatorin: Viele Unternehmen suchen Fachkräfte aus dem Ausland. Frau Yilmaz, Sie leiten ein Beratungsprojekt für internationale Beschäftigte. Welche Hürden treten nach der Ankunft häufig auf?\nYilmaz: Neben der Wohnungssuche und den Behördenwegen ist oft die Orientierung im Betrieb schwierig. Abkürzungen, unausgesprochene Regeln und unterschiedliche Kommunikationsstile können Missverständnisse verursachen. Eine gute Einführung hilft, solche Unsicherheiten zu reduzieren.\nModeratorin: Was gehört zu einer guten Einführung?\nYilmaz: Eine feste Ansprechperson, ein verständlicher Einarbeitungsplan und Informationen zu wichtigen Abläufen. Neue Mitarbeitende sollten wissen, an wen sie sich bei fachlichen oder organisatorischen Fragen wenden können.\nModeratorin: Welche Rolle spielt die Anerkennung ausländischer Abschlüsse?\nYilmaz: Sie kann für bestimmte Berufe entscheidend sein. Das Verfahren ist manchmal lang und verlangt beglaubigte Dokumente. Beratungsstellen helfen dabei, die zuständige Stelle zu finden und fehlende Unterlagen zu identifizieren.\nModeratorin: Reicht ein Sprachkurs aus, um Integration zu sichern?\nYilmaz: Nein. Sprachkenntnisse sind wichtig, aber auch Teams müssen sich öffnen. Kolleginnen und Kollegen sollten langsam und verständlich sprechen, Fachbegriffe erklären und Rückfragen zulassen. Gleichzeitig brauchen internationale Beschäftigte Gelegenheit, ihre Kenntnisse im Arbeitsalltag anzuwenden.\nModeratorin: Was ist langfristig entscheidend?\nYilmaz: Entwicklungsmöglichkeiten und faire Bedingungen. Internationale Fachkräfte sollten nicht dauerhaft auf einfache Aufgaben beschränkt bleiben, sondern entsprechend ihrer Qualifikation Verantwortung übernehmen können."]],"teil3_01.mp3":[["de-DE-KatjaNeural","Moderator: Sollten Unternehmen verpflichtend interkulturelle Schulungen für alle Beschäftigten anbieten? Herr Kranz, Sie sind Geschäftsführer eines mittelständischen Betriebs."],["de-DE-ConradNeural","Kranz: Schulungen können helfen, aber eine Pflichtveranstaltung allein verändert noch keine Zusammenarbeit. Wir brauchen konkrete Regeln im Alltag und Führungskräfte, die bei Konflikten vermitteln. Außerdem sollten Inhalte zur tatsächlichen Situation des Betriebs passen."],["de-DE-KatjaNeural","Moderator: Frau Diallo, Sie vertreten ein Netzwerk internationaler Fachkräfte."],["de-DE-ConradNeural","Diallo: Ohne Sensibilisierung entstehen leicht Vorurteile. Viele internationale Beschäftigte berichten, dass ihre Qualifikation unterschätzt wird oder sie bei wichtigen Gesprächen nicht einbezogen werden. Schulungen können solche Muster sichtbar machen."],["de-DE-ConradNeural","Kranz: Das ist richtig. Ich würde kurze Trainings mit gemeinsamen Projekten verbinden. So können Mitarbeitende unterschiedliche Arbeitsweisen direkt kennenlernen."],["de-DE-ConradNeural","Diallo: Entscheidend ist, dass die Leitung Verantwortung übernimmt und Maßnahmen überprüft. Eine einmalige Veranstaltung ohne Folgen reicht nicht."],["de-DE-KatjaNeural","Moderator: Beide sehen Schulungen als möglichen Baustein, betonen aber, dass sie mit Veränderungen im Arbeitsalltag verbunden sein müssen."]],"teil4_01.mp3":[["de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um die Integration internationaler Fachkräfte in Unternehmen. Viele Betriebe benötigen qualifizierte Mitarbeitende aus dem Ausland. Damit diese langfristig bleiben und ihre Fähigkeiten einbringen können, reicht es nicht, einen Arbeitsvertrag abzuschließen. Integration beginnt mit einer guten Vorbereitung und setzt sich im Alltag fort.\nVor der Ankunft sind klare Informationen hilfreich. Dazu gehören Hinweise zu Wohnungssuche, Behörden, Versicherungen und den ersten Arbeitstagen. Im Betrieb sollte eine feste Ansprechperson zur Verfügung stehen. Ein Einarbeitungsplan erklärt Aufgaben, Zuständigkeiten und wichtige Regeln.\nEin weiterer Punkt ist die Anerkennung beruflicher Qualifikationen. Je nach Beruf müssen Zeugnisse geprüft und Übersetzungen beglaubigt werden. Beratungsstellen können erklären, welche Unterlagen fehlen und welche Behörde zuständig ist. Unternehmen sollten Beschäftigte während dieses Verfahrens unterstützen, statt ihre Fähigkeiten vorschnell zu unterschätzen.\nAuch die Kommunikation im Team spielt eine zentrale Rolle. Fachbegriffe, Abkürzungen und informelle Regeln sind für neue Kolleginnen und Kollegen nicht immer selbstverständlich. Verständliche Sprache, offene Rückfragen und gemeinsame Projekte erleichtern die Zusammenarbeit. Interkulturelle Kompetenz bedeutet dabei nicht, jede Person einer bestimmten Gruppe zuzuordnen, sondern individuelle Erfahrungen ernst zu nehmen.\nLangfristig sind faire Entwicklungsmöglichkeiten entscheidend. Internationale Fachkräfte sollten Zugang zu Weiterbildung und verantwortungsvollen Aufgaben erhalten. Wenn Unternehmen ihre Kompetenzen anerkennen und ein respektvolles Arbeitsumfeld schaffen, profitieren sowohl die Beschäftigten als auch der Betrieb."]]}
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
archive=ROOT/"exam-023.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
