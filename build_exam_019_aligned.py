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
tracks={"teil1_01.mp3":[["de-DE-KatjaNeural","Mitteilung des Bildungszentrums: Der Kurs 'Digitale Grundkenntnisse' beginnt am 3. Oktober. Die ersten beiden Termine finden in Präsenz statt, danach arbeiten die Teilnehmenden mit Lernmaterialien online. Ein eigener Laptop kann ausgeliehen werden."]],"teil1_02.mp3":[["de-DE-KatjaNeural","A: Ich überlege, noch einmal eine Fremdsprache zu lernen. B: Wie möchtest du das organisieren? A: Ich habe wenig Zeit. B: Vielleicht passt ein Kurs am Samstag oder eine Lernpartnerschaft, bei der ihr euch gegenseitig unterstützt."]],"teil1_03.mp3":[["de-DE-KatjaNeural","Hinweis der Bibliothek: Ab sofort können Erwachsene kostenlos an einer Lernberatung teilnehmen. Dabei werden persönliche Ziele besprochen und passende Kurse vorgeschlagen. Die Beratung ersetzt keine berufliche Anerkennungsprüfung."]],"teil1_04.mp3":[["de-DE-AmalaNeural","Ich habe nach vielen Jahren wieder einen Mathematikkurs besucht. Am Anfang war ich unsicher, aber die Lehrerin hat die Aufgaben mit Beispielen aus dem Alltag erklärt. Jetzt kann ich die Inhalte auch bei meiner Arbeit besser anwenden."]],"teil1_05.mp3":[["de-DE-KatjaNeural","Durchsage: Die Informationsveranstaltung zum Nachholen eines Schulabschlusses wird vom Dienstag auf Donnerstag verlegt. Sie beginnt weiterhin um 16 Uhr im Raum 104. Bereits angemeldete Personen müssen sich nicht erneut registrieren."]],"teil2_01.mp3":[["de-DE-KatjaNeural","Moderatorin: Berufliche und persönliche Anforderungen verändern sich ständig. Herr Peters, Sie leiten ein Zentrum für Erwachsenenbildung. Warum ist lebenslanges Lernen wichtig?\nPeters: Wissen veraltet in manchen Bereichen schneller als früher. Gleichzeitig lernen Menschen nicht nur für den Beruf. Sie möchten digitale Dienste nutzen, Sprachen sprechen oder persönliche Interessen vertiefen. Weiterbildung kann also verschiedene Ziele haben.\nModeratorin: Haben Erwachsene andere Lernbedürfnisse als Jugendliche?\nPeters: Häufig bringen sie mehr Berufserfahrung und konkrete Fragen mit. Sie möchten verstehen, wofür ein Inhalt nützlich ist. Gute Kurse knüpfen deshalb an Alltag und Arbeit an und berücksichtigen unterschiedliche Lerngeschwindigkeiten.\nModeratorin: Welche Hindernisse gibt es?\nPeters: Zeit, Kosten und fehlendes Selbstvertrauen. Manche Menschen glauben, sie seien zu alt oder hätten zu lange nicht gelernt. Flexible Zeiten, Beratung und kleine Lernschritte können helfen. Auch Arbeitgeber können Lernzeit ermöglichen.\nModeratorin: Welche Rolle spielen digitale Kurse?\nPeters: Sie bieten Flexibilität, verlangen aber Selbstorganisation. Nicht alle haben einen geeigneten Internetzugang oder ausreichende digitale Kenntnisse. Eine Kombination aus Präsenz und Online-Lernen ist deshalb oft sinnvoll.\nModeratorin: Wie erkennt man den Erfolg?\nPeters: Nicht nur an einem Zertifikat. Entscheidend ist, ob Menschen neue Kenntnisse anwenden können und sich zutrauen, weitere Lernschritte zu machen."]],"teil3_01.mp3":[["de-DE-KatjaNeural","Moderator: Sollte jeder Arbeitnehmer jedes Jahr an einer Weiterbildung teilnehmen müssen? Frau Franke, Sie leiten eine Personalabteilung."],["de-DE-AmalaNeural","Franke: Eine jährliche Pflicht für alle wäre zu starr. In manchen Berufen ändern sich Anforderungen schnell, in anderen ist der Bedarf geringer. Besser wäre ein regelmäßiges Gespräch, in dem Beschäftigte und Führungskräfte passende Lernziele vereinbaren."],["de-DE-KatjaNeural","Moderator: Herr Weber, Sie vertreten eine Gewerkschaft."],["de-DE-ConradNeural","Weber: Ohne verbindliche Zeit und Finanzierung bleiben Weiterbildungspläne oft unverbindlich. Beschäftigte dürfen nicht ihre Freizeit opfern müssen, um notwendige berufliche Kenntnisse zu erwerben."],["de-DE-AmalaNeural","Franke: Dass Lernzeit zur Arbeitszeit gehören sollte, sehe ich ähnlich. Trotzdem muss das Angebot zur Tätigkeit passen. Ein Kurs ohne konkreten Nutzen hilft niemandem."],["de-DE-ConradNeural","Weber: Deshalb sollten Beschäftigte an der Auswahl beteiligt werden. Sie wissen häufig selbst, wo ihnen Kenntnisse fehlen. Außerdem brauchen Menschen mit geringeren Grundkenntnissen zusätzliche Unterstützung."],["de-DE-KatjaNeural","Moderator: Beide Seiten wollen Weiterbildung ermöglichen, unterscheiden sich aber darin, wie verbindlich die Teilnahme geregelt werden soll."]],"teil4_01.mp3":[["de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um lebenslanges Lernen. Lernen endet nicht mit dem Schulabschluss oder einer Berufsausbildung. Technische Entwicklungen, gesellschaftliche Veränderungen und persönliche Interessen führen dazu, dass Menschen in verschiedenen Lebensphasen neue Kenntnisse erwerben.\nWeiterbildung kann beruflich motiviert sein. Beschäftigte lernen neue Software, aktualisieren Fachwissen oder bereiten sich auf andere Aufgaben vor. Daneben gibt es allgemeine Bildung, etwa Sprachkurse, politische Bildung oder digitale Grundkenntnisse. Auch informelles Lernen im Alltag ist wichtig: Menschen eignen sich Fähigkeiten durch Projekte, Hobbys und gegenseitigen Austausch an.\nErwachsene lernen häufig besonders erfolgreich, wenn Inhalte an ihre Erfahrungen anknüpfen. Kurse sollten deshalb praktische Beispiele nutzen und unterschiedliche Vorkenntnisse berücksichtigen. Kleine Lernabschnitte können helfen, wenn Beruf und Familie wenig freie Zeit lassen.\nEine zentrale Voraussetzung ist der Zugang. Kosten, fehlende Beratung oder mangelnde digitale Ausstattung dürfen nicht dazu führen, dass bestimmte Gruppen ausgeschlossen werden. Arbeitgeber, Bildungseinrichtungen und Kommunen können mit finanzieller Unterstützung, flexiblen Zeiten und erreichbaren Lernorten helfen.\nSchließlich sollte Lernen nicht nur an Prüfungen gemessen werden. Entscheidend ist, ob Menschen Wissen anwenden, Probleme selbstständiger lösen und neue Herausforderungen annehmen können. Lebenslanges Lernen stärkt damit sowohl berufliche Möglichkeiten als auch persönliche Selbstständigkeit."]]}
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
archive=ROOT/"exam-019.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
