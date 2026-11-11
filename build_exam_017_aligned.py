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
tracks={"teil1_01.mp3":[["de-DE-KatjaNeural","Mitteilung der Personalabteilung: Anträge auf einen festen Homeoffice-Tag müssen künftig bis zum 20. des Vormonats eingereicht werden. Die Regelung gilt zunächst für sechs Monate. Bereits genehmigte Vereinbarungen bleiben bis zu ihrem Ablauf bestehen."]],"teil1_02.mp3":[["de-DE-KatjaNeural","A: Kannst du nächste Woche die Spätschicht übernehmen? B: Am Dienstag nicht, da habe ich einen Betreuungstermin. A: Wäre Donnerstag möglich? B: Ja, wenn ich dafür am Freitag früher gehen kann. A: Das lässt sich einrichten, ich ändere den Plan."]],"teil1_03.mp3":[["de-DE-KatjaNeural","Hinweis der Familienberatung: Der Workshop 'Arbeit und Familie organisieren' findet am 12. September online statt. Die Teilnahme ist kostenlos. Eine Aufzeichnung wird aus Datenschutzgründen nicht bereitgestellt."]],"teil1_04.mp3":[["de-DE-AmalaNeural","Ich arbeite an zwei Tagen von zu Hause. Dadurch spare ich den Arbeitsweg und kann mittags mit meinem Kind essen. Trotzdem trenne ich Arbeitszeit und Familienzeit klar, damit ich nicht ständig erreichbar bin."]],"teil1_05.mp3":[["de-DE-KatjaNeural","Durchsage im Büro: Der Eltern-Kind-Raum bleibt am Mittwoch wegen einer Sicherheitsprüfung geschlossen. Beschäftigte können in dieser Zeit den Ruheraum im zweiten Stock nutzen. Die übrigen Besprechungsräume sind nicht betroffen."]],"teil2_01.mp3":[["de-DE-KatjaNeural","Moderator: Viele Eltern wünschen sich flexiblere Arbeitszeiten. Frau Berger, Sie beraten Unternehmen zur Vereinbarkeit von Beruf und Familie. Was ist dabei die wichtigste Voraussetzung?\nBerger: Flexibilität muss planbar sein. Wenn Beschäftigte jederzeit kurzfristig erreichbar sein sollen, hilft ihnen ein Homeoffice-Tag wenig. Teams brauchen klare Absprachen darüber, wann jemand arbeitet und wann eine Vertretung übernimmt.\nModerator: Ist Homeoffice für alle Eltern die beste Lösung?\nBerger: Nein. Manche Tätigkeiten lassen sich nicht von zu Hause erledigen. Außerdem haben nicht alle Familien einen ruhigen Arbeitsplatz. Flexible Schichten, Teilzeit oder verlässliche Dienstpläne können ebenso wichtig sein.\nModerator: Welche Rolle spielen Führungskräfte?\nBerger: Sie sollten Ergebnisse bewerten und nicht nur die Anwesenheit. Gleichzeitig müssen Aufgaben fair verteilt werden. Es darf nicht passieren, dass Kolleginnen ohne Kinder regelmäßig die ungünstigen Zeiten übernehmen.\nModerator: Wie können Unternehmen Eltern unterstützen?\nBerger: Durch kurzfristig nutzbare Betreuungsangebote, Notfallregelungen und Beratung. Wichtig ist auch eine offene Gesprächskultur. Beschäftigte sollten familiäre Verpflichtungen ansprechen können, ohne Nachteile befürchten zu müssen.\nModerator: Was ist langfristig entscheidend?\nBerger: Eine Kultur, in der unterschiedliche Lebenssituationen berücksichtigt werden. Einzelne Sonderlösungen helfen, aber dauerhaft braucht es faire Regeln für das ganze Team."]],"teil3_01.mp3":[["de-DE-KatjaNeural","Moderatorin: Sollten Unternehmen verpflichtet werden, flexible Arbeitszeiten für Eltern anzubieten? Herr Scholz, Sie vertreten einen Arbeitgeberverband."],["de-DE-ConradNeural","Scholz: Eine starre gesetzliche Pflicht kann für kleine Betriebe schwierig sein. In manchen Bereichen müssen bestimmte Schichten besetzt werden. Sinnvoller wären Rahmenbedingungen, die betriebliche Möglichkeiten berücksichtigen und Gespräche zwischen Beschäftigten und Leitung fördern."],["de-DE-KatjaNeural","Moderatorin: Frau Nguyen, Sie arbeiten in einer Beratungsstelle für Familien."],["de-DE-AmalaNeural","Nguyen: Ohne verbindliche Ansprüche bleiben flexible Lösungen oft vom guten Willen einzelner Vorgesetzter abhängig. Eltern brauchen verlässliche Rechte, damit sie Betreuung und Arbeit planen können."],["de-DE-ConradNeural","Scholz: Verlässlichkeit ist wichtig. Trotzdem sollte eine Lösung nicht dazu führen, dass andere Beschäftigte dauerhaft mehr Wochenend- oder Spätdienste übernehmen."],["de-DE-AmalaNeural","Nguyen: Das ist ein berechtigter Punkt. Dienstpläne müssen transparent sein und die Interessen des gesamten Teams berücksichtigen. Aber die Verantwortung für Vereinbarkeit darf nicht allein bei den Familien liegen."],["de-DE-KatjaNeural","Moderatorin: Die Diskussion zeigt, dass Flexibilität verlässlich sein und zugleich fair für das gesamte Team organisiert werden muss."]],"teil4_01.mp3":[["de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um flexible Arbeitsmodelle und die Vereinbarkeit von Beruf und Familie. Viele Beschäftigte müssen Arbeitsaufgaben mit Kinderbetreuung, Pflege oder anderen privaten Verpflichtungen koordinieren. Flexible Arbeitszeiten können dabei helfen, wenn sie verlässlich und fair organisiert werden.\nEin verbreitetes Modell ist Gleitzeit. Beschäftigte können innerhalb eines festgelegten Rahmens beginnen und enden, während bestimmte Kernzeiten die Zusammenarbeit sichern. Teilzeit ermöglicht eine Reduzierung der Wochenstunden, kann aber Auswirkungen auf Einkommen und berufliche Entwicklung haben. Homeoffice spart Wege und bietet mehr Ortsflexibilität, setzt jedoch geeignete Aufgaben und einen passenden Arbeitsplatz voraus.\nAuch Schichttausch und Jahresarbeitszeitkonten können Entlastung schaffen. Dafür müssen Dienstpläne frühzeitig bekannt sein. Kurzfristige Änderungen sollten die Ausnahme bleiben, damit Familien Betreuung organisieren können. In Bereichen mit festen Öffnungszeiten braucht es klare Vertretungsregeln.\nFührungskräfte spielen eine wichtige Rolle. Sie sollten Ergebnisse beurteilen, Aufgaben gerecht verteilen und regelmäßig mit dem Team sprechen. Flexible Arbeit darf nicht bedeuten, dass Beschäftigte ständig erreichbar sind oder Kolleginnen und Kollegen ohne familiäre Verpflichtungen dauerhaft zusätzliche Belastungen tragen.\nSchließlich profitieren Unternehmen ebenfalls von familienfreundlichen Bedingungen. Sie können Motivation und Bindung stärken und helfen, Fachkräfte zu gewinnen. Voraussetzung ist eine Kultur, die unterschiedliche Lebenssituationen respektiert und passende Lösungen gemeinsam entwickelt."]]}
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
archive=ROOT/"exam-017.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
