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
tracks={"teil1_01.mp3":[["de-DE-KatjaNeural","Mitteilung der Betriebsärztin: Ab nächster Woche steht im Erdgeschoss ein zusätzlicher Raum für kurze Bewegungspausen zur Verfügung. Er kann zwischen zehn und sechzehn Uhr ohne Reservierung genutzt werden. Bitte bringen Sie bei Bedarf ein Handtuch mit."]],"teil1_02.mp3":[["de-DE-KatjaNeural","A: Du machst jetzt mittags immer einen Spaziergang. B: Ja, ich sitze sonst fast den ganzen Tag vor dem Bildschirm. A: Hilft dir das wirklich? B: Ich kann danach besser denken und bin am Nachmittag weniger müde. Wenn es regnet, gehe ich wenigstens ein paar Minuten durchs Gebäude."]],"teil1_03.mp3":[["de-DE-KatjaNeural","Hinweis der Kantine: Am Donnerstag wird ein neues Angebot mit warmen vegetarischen Gerichten getestet. Rückmeldungen können über einen QR-Code auf dem Tablettständer abgegeben werden. Die Befragung dauert höchstens zwei Minuten."]],"teil1_04.mp3":[["de-DE-AmalaNeural","Früher habe ich Pausen oft ausgelassen, um früher fertig zu werden. Inzwischen stelle ich mir einen kurzen Wecker. Ich erledige dadurch nicht weniger, sondern kann mich danach wieder besser konzentrieren."]],"teil1_05.mp3":[["de-DE-KatjaNeural","Durchsage im Büro: Die jährliche Ergonomieberatung findet am Mittwoch nicht im Raum 3.12, sondern im Besprechungsraum neben der Bibliothek statt. Die gebuchten Uhrzeiten bleiben unverändert."]],"teil2_01.mp3":[["de-DE-KatjaNeural","Moderator: Viele Beschäftigte verbringen einen großen Teil des Tages im Sitzen. Frau Dr. König, Sie sind Arbeitsmedizinerin. Welche Bedeutung haben regelmäßige Pausen?\nKönig: Sie unterbrechen einseitige Belastungen und geben dem Körper Gelegenheit, sich zu bewegen. Schon wenige Minuten können helfen, besonders wenn man lange am Bildschirm arbeitet. Entscheidend ist nicht eine komplizierte Übung, sondern die Regelmäßigkeit.\nModerator: Sollte man Pausen gemeinsam im Team machen?\nKönig: Das kann motivieren, aber nicht jede Tätigkeit erlaubt dieselben Zeiten. Wichtig ist, dass Beschäftigte ihre Pausen tatsächlich nehmen können und nicht das Gefühl haben, dadurch weniger leistungsfähig zu wirken.\nModerator: Was empfehlen Sie bei Bildschirmarbeit?\nKönig: Den Blick regelmäßig in die Ferne richten, die Sitzposition wechseln und kurze Bewegungsphasen einbauen. Wer telefoniert, kann manche Gespräche im Stehen führen. Auch ein kurzer Gang zum Fenster ist besser als stundenlanges Sitzen ohne Unterbrechung.\nModerator: Wie können Unternehmen unterstützen?\nKönig: Sie sollten geeignete Räume schaffen, Pausen nicht als verlorene Arbeitszeit behandeln und Führungskräfte sensibilisieren. Außerdem helfen klare Arbeitsabläufe, damit Beschäftigte nicht ständig unter Zeitdruck stehen.\nModerator: Was ist bei der Einführung neuer Angebote wichtig?\nKönig: Man sollte die Beschäftigten fragen, was sie wirklich nutzen würden. Ein teurer Ruheraum hilft wenig, wenn er ungünstig liegt oder niemand weiß, dass er existiert."]],"teil3_01.mp3":[["de-DE-KatjaNeural","Moderatorin: Sollten Arbeitgeber eine feste Mindestzahl an Bewegungspausen pro Arbeitstag vorschreiben? Herr Seidel, Sie leiten einen Betrieb mit vielen Büroarbeitsplätzen."],["de-DE-ConradNeural","Seidel: Eine starre Zahl passt nicht zu jeder Tätigkeit. In manchen Phasen müssen Beschäftigte konzentriert arbeiten oder Kunden betreuen. Wir sollten Pausen ermöglichen, aber nicht jede Minute kontrollieren."],["de-DE-KatjaNeural","Moderatorin: Frau Brandt, Sie vertreten eine Krankenkasse."],["de-DE-ConradNeural","Brandt: Ohne klare Vorgaben werden Pausen im Alltag häufig verschoben oder ausgelassen. Eine betriebliche Regel kann zeigen, dass Gesundheit Teil der Arbeitsorganisation ist. Sie muss aber flexibel genug bleiben, um unterschiedliche Aufgaben zu berücksichtigen."],["de-DE-ConradNeural","Seidel: Ich könnte mir Erinnerungen und kurze gemeinsame Bewegungsangebote vorstellen. Die Teilnahme sollte freiwillig sein, damit niemand unter zusätzlichen Druck gerät."],["de-DE-ConradNeural","Brandt: Freiwilligkeit ist wichtig. Gleichzeitig braucht es eine klare Erwartung der Leitung, dass Beschäftigte ihre Pausen wirklich nutzen dürfen und dafür nicht kritisiert werden."],["de-DE-KatjaNeural","Moderatorin: Beide Seiten wollen Pausen stärken, setzen aber unterschiedliche Schwerpunkte bei verbindlichen Vorgaben und individueller Freiheit."]],"teil4_01.mp3":[["de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um gesunde Pausen am Arbeitsplatz. Viele Tätigkeiten erfordern langes Sitzen, konzentrierte Bildschirmarbeit oder wiederholte Bewegungen. Ohne Unterbrechung können Verspannungen, Müdigkeit und Konzentrationsprobleme entstehen. Pausen sind deshalb kein Zeichen mangelnder Arbeitsbereitschaft, sondern ein Bestandteil sinnvoller Arbeitsorganisation.\nEine kurze Bewegungspause muss nicht aufwendig sein. Aufstehen, Schultern lockern, einige Schritte gehen oder den Blick vom Bildschirm lösen kann bereits helfen. Bei längerer Bildschirmarbeit ist es sinnvoll, regelmäßig die Körperhaltung zu verändern. Wer telefoniert, kann ein Gespräch gelegentlich im Stehen führen.\nAuch die psychische Erholung ist wichtig. Ein kurzer Wechsel der Umgebung, ein Gespräch mit Kollegen oder ein paar Minuten Ruhe können helfen, Abstand zu einer schwierigen Aufgabe zu gewinnen. Pausen sollten allerdings nicht mit zusätzlichen privaten Erledigungen gefüllt werden, wenn dadurch keine Erholung entsteht.\nUnternehmen tragen Verantwortung für geeignete Bedingungen. Dazu gehören realistische Arbeitsmengen, planbare Abläufe und eine Führungskultur, die Pausen respektiert. Ein Ruheraum oder ein Bewegungsangebot kann nützlich sein, wenn es gut erreichbar ist und den Bedürfnissen der Beschäftigten entspricht.\nSchließlich sollte die Wirkung regelmäßig überprüft werden. Unternehmen können Beschäftigte befragen und beobachten, ob Angebote tatsächlich genutzt werden. Gesunde Pausen entstehen nicht allein durch eine Vorschrift, sondern durch eine Kombination aus persönlicher Gewohnheit, geeigneter Arbeitsorganisation und Unterstützung durch die Leitung."]]}
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
archive=ROOT/"exam-021.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
