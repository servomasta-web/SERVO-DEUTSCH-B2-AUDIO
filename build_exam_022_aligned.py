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
tracks={"teil1_01.mp3":[["de-DE-KatjaNeural","Mitteilung des Bürgerbüros: Ab sofort können Meldebescheinigungen online beantragt werden. Für den Zugang benötigen Bürgerinnen und Bürger ein digitales Nutzerkonto. Wer Unterstützung braucht, kann weiterhin einen Termin vor Ort vereinbaren."]],"teil1_02.mp3":[["de-DE-KatjaNeural","A: Hast du deinen Antrag auf Bewohnerparken schon online gestellt? B: Ja, aber ich musste zuerst ein Foto vom Fahrzeugschein hochladen. A: War das kompliziert? B: Nicht besonders. Nur die Bestätigung kam nicht sofort, sondern erst am nächsten Werktag."]],"teil1_03.mp3":[["de-DE-KatjaNeural","Hinweis der Stadtverwaltung: Wegen einer Systemumstellung ist das Portal für die Kfz-Zulassung am Samstag von acht bis zwölf Uhr nicht erreichbar. Bereits gespeicherte Entwürfe bleiben erhalten. Neue Anträge können danach wieder eingereicht werden."]],"teil1_04.mp3":[["de-DE-AmalaNeural","Ich erledige Behördengänge gern online, wenn die Webseite verständlich aufgebaut ist. Bei einem komplizierten Formular rufe ich lieber an, bevor ich falsche Angaben mache. Eine echte Ansprechperson sollte es meiner Meinung nach weiterhin geben."]],"teil1_05.mp3":[["de-DE-KatjaNeural","Durchsage: Für die digitale Beantragung eines neuen Personalausweises müssen Antragstellende weiterhin persönlich erscheinen, um ihre Identität und biometrischen Daten prüfen zu lassen. Die Terminbuchung kann online erfolgen."]],"teil2_01.mp3":[["de-DE-KatjaNeural","Moderator: Immer mehr Verwaltungsleistungen werden digital angeboten. Frau Reimann, Sie leiten ein Projekt zur Modernisierung kommunaler Dienste. Was ist der größte Vorteil?\nReimann: Viele Anliegen können unabhängig von Öffnungszeiten erledigt werden. Menschen müssen nicht für jede Bescheinigung ins Bürgerbüro fahren. Das spart Zeit und kann auch die Verwaltung entlasten.\nModerator: Welche Voraussetzungen müssen erfüllt sein?\nReimann: Die Portale müssen verständlich und barrierearm sein. Nutzer sollten erkennen, welche Unterlagen nötig sind und wie lange die Bearbeitung dauert. Außerdem braucht es sichere Verfahren zur Identifizierung und zum Schutz persönlicher Daten.\nModerator: Können alle Menschen solche Dienste nutzen?\nReimann: Nein. Manche haben keinen zuverlässigen Internetzugang oder Schwierigkeiten mit digitalen Formularen. Deshalb darf persönliche Unterstützung nicht verschwinden. Bibliotheken, Bürgerbüros und Beratungsstellen können Hilfe anbieten.\nModerator: Wie lässt sich Vertrauen schaffen?\nReimann: Durch transparente Informationen, nachvollziehbare Bearbeitungsstände und erreichbare Kontaktstellen. Wenn ein Antrag abgelehnt wird, muss verständlich erklärt werden, warum und welche Möglichkeiten es gibt.\nModerator: Werden Beschäftigte in der Verwaltung dadurch überflüssig?\nReimann: Ihre Aufgaben verändern sich. Routineanträge können automatisiert werden, während Beratung und die Bearbeitung komplexer Fälle wichtiger bleiben. Digitalisierung sollte den Kontakt verbessern, nicht einfach abschaffen."]],"teil3_01.mp3":[["de-DE-KatjaNeural","Moderatorin: Sollten alle Verwaltungsleistungen ausschließlich online angeboten werden? Herr Peters, Sie sind Bürgermeister einer Kleinstadt."],["de-DE-ConradNeural","Peters: Das wäre für viele Menschen ein Problem. Wir haben Bürgerinnen und Bürger, die digitale Formulare nicht sicher bedienen können. Außerdem lassen sich komplizierte Lebenssituationen nicht immer in standardisierte Felder eintragen."],["de-DE-KatjaNeural","Moderatorin: Frau Seifert, Sie arbeiten für eine Digitalisierungsinitiative."],["de-DE-ConradNeural","Seifert: Ich fordere nicht, dass jede persönliche Beratung verschwindet. Aber einfache Vorgänge sollten online möglich sein. Dadurch werden Schalter entlastet und Mitarbeitende können sich stärker um schwierige Anliegen kümmern."],["de-DE-ConradNeural","Peters: Dafür brauchen wir verlässliche Systeme und eine Anlaufstelle, wenn etwas nicht funktioniert. Ein Portal, das regelmäßig ausfällt, schafft kein Vertrauen."],["de-DE-ConradNeural","Seifert: Da stimme ich zu. Wir sollten außerdem Menschen vor Ort unterstützen, etwa durch digitale Lotsen in Bibliotheken oder Bürgerbüros."],["de-DE-KatjaNeural","Moderatorin: Beide unterstützen digitale Angebote, lehnen aber einen vollständigen Ersatz persönlicher Hilfe ab."]],"teil4_01.mp3":[["de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um digitale Behördendienste und ihre Auswirkungen auf Bürger und Verwaltung. Online-Portale können viele Abläufe vereinfachen. Eine Bescheinigung lässt sich beantragen, ein Termin buchen oder ein Formular übermitteln, ohne persönlich zum Amt zu gehen. Das ist besonders hilfreich für Menschen mit langen Arbeitszeiten oder weiter Anfahrt.\nDamit digitale Dienste funktionieren, müssen sie verständlich aufgebaut sein. Nutzer brauchen klare Hinweise zu erforderlichen Dokumenten, Gebühren und Bearbeitungszeiten. Formulare sollten auf unterschiedlichen Geräten nutzbar sein und auch Menschen mit Einschränkungen berücksichtigen. Eine sichere Identifizierung schützt persönliche Daten und verhindert Missbrauch.\nNicht alle Anliegen lassen sich vollständig automatisieren. Bei komplexen Fällen, Widersprüchen oder persönlichen Notlagen ist Beratung notwendig. Außerdem haben manche Menschen wenig Erfahrung mit digitalen Anwendungen. Kommunen sollten deshalb Unterstützung vor Ort anbieten und alternative Kontaktwege erhalten.\nAuch die Verwaltung verändert sich. Routineaufgaben können schneller bearbeitet werden, während Beschäftigte mehr Zeit für Beratung und schwierige Entscheidungen gewinnen. Dafür benötigen sie Weiterbildung und klare Zuständigkeiten.\nSchließlich ist Vertrauen entscheidend. Bürger müssen nachvollziehen können, was mit ihrem Antrag geschieht und wie sie bei Problemen Hilfe erhalten. Digitale Verwaltung ist dann erfolgreich, wenn sie Verfahren vereinfacht, Daten schützt und den Zugang zu öffentlichen Leistungen für möglichst alle Menschen verbessert."]]}
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
archive=ROOT/"exam-022.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
