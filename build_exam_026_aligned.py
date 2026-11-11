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
tracks={"teil1_01.mp3":[["de-DE-KatjaNeural","Mitteilung der Austauschorganisation: Bewerbungen für den Freiwilligendienst in Portugal sind bis zum 30. März möglich. Das Orientierungsseminar findet im Mai online statt. Die Ausreise ist für Anfang August geplant."]],"teil1_02.mp3":[["de-DE-KatjaNeural","A: Ich möchte mich im Ausland sozial engagieren, aber ich weiß nicht, ob meine Sprachkenntnisse reichen. B: Im Projekt gibt es vor Ort einen Sprachkurs. Wichtig ist eher, dass du offen bist und zuverlässig mitarbeitest. A: Dann bewerbe ich mich."]],"teil1_03.mp3":[["de-DE-KatjaNeural","Hinweis des Jugendbüros: Für den Freiwilligendienst können Fahrtkosten teilweise erstattet werden. Unterkunft und Verpflegung werden vom Projekt organisiert. Persönliche Ausgaben müssen die Teilnehmenden selbst übernehmen."]],"teil1_04.mp3":[["de-DE-AmalaNeural","Ich war sechs Monate in einem Umweltprojekt in Griechenland. Wir haben Strände gereinigt und Schulgruppen über Müllvermeidung informiert. Am schwierigsten war für mich anfangs die ungewohnte Arbeitsorganisation, nicht die Sprache."]],"teil1_05.mp3":[["de-DE-KatjaNeural","Durchsage: Das Vorbereitungstreffen für die Freiwilligen findet am Samstag nicht im Rathaus, sondern im Seminarhaus am Stadtpark statt. Beginn ist um zehn Uhr; bitte bringen Sie Ihren Reisepass mit."]],"teil2_01.mp3":[["de-DE-KatjaNeural","Moderatorin: Ein Freiwilligendienst im Ausland ist für viele junge Erwachsene eine besondere Erfahrung. Frau Mertens, Sie koordinieren internationale Projekte. Was sollten Interessierte zuerst überlegen?\nMertens: Sie sollten prüfen, warum sie teilnehmen möchten und welche Aufgaben zu ihren Fähigkeiten passen. Ein Projekt sollte nicht nur als günstige Möglichkeit zum Reisen betrachtet werden. Es geht darum, mit einer Organisation zusammenzuarbeiten und Verantwortung zu übernehmen.\nModeratorin: Welche Voraussetzungen sind wichtig?\nMertens: Zuverlässigkeit, Offenheit und die Bereitschaft, sich auf andere Lebensbedingungen einzustellen. Sprachkenntnisse helfen, aber viele Programme bieten Vorbereitung oder Unterstützung vor Ort.\nModeratorin: Wie werden Freiwillige vorbereitet?\nMertens: Sie erhalten Informationen über das Einsatzland, kulturelle Besonderheiten, Sicherheitsfragen und ihre konkreten Aufgaben. Außerdem wird besprochen, an wen sie sich bei Schwierigkeiten wenden können.\nModeratorin: Welche Risiken gibt es?\nMertens: Erwartungen können unrealistisch sein. Manchmal sind Unterkünfte einfacher als gedacht oder Projekte arbeiten anders als geplant. Deshalb sollte man den Träger sorgfältig prüfen und klare Vereinbarungen zu Aufgaben, Kosten und Betreuung treffen.\nModeratorin: Was geschieht nach der Rückkehr?\nMertens: Die Erfahrung sollte ausgewertet werden. Freiwillige können überlegen, welche Fähigkeiten sie entwickelt haben und wie sie diese im Studium oder Beruf einsetzen. Ein Nachbereitungsgespräch hilft, Erlebnisse einzuordnen."]],"teil3_01.mp3":[["de-DE-KatjaNeural","Moderator: Sollten Freiwilligendienste im Ausland stärker staatlich finanziert werden? Herr Lenz, Sie leiten eine gemeinnützige Organisation."],["de-DE-ConradNeural","Lenz: Öffentliche Förderung ist wichtig, damit nicht nur junge Menschen aus wohlhabenden Familien teilnehmen können. Gleichzeitig müssen Organisationen nachweisen, dass die Projekte sinnvoll geplant sind und die lokalen Partner wirklich davon profitieren."],["de-DE-KatjaNeural","Moderator: Frau Kofi, Sie arbeiten in einer lokalen Partnerorganisation in Ghana."],["de-DE-ConradNeural","Kofi: Ich begrüße Unterstützung, aber die Projekte sollten nicht von außen bestimmt werden. Lokale Einrichtungen müssen an der Planung beteiligt sein und selbst entscheiden können, welche Hilfe sie benötigen."],["de-DE-ConradNeural","Lenz: Das sehe ich genauso. Wir versuchen, langfristige Partnerschaften aufzubauen und nicht jedes Jahr ein völlig neues Projekt zu beginnen."],["de-DE-ConradNeural","Kofi: Außerdem sollten Freiwillige keine regulären Arbeitsplätze ersetzen. Sie können unterstützen und lernen, aber Fachkräfte vor Ort müssen bezahlt und anerkannt werden."],["de-DE-KatjaNeural","Moderator: Beide Seiten befürworten Förderung, betonen aber die Verantwortung der lokalen Partner und die Qualität der Projekte."]],"teil4_01.mp3":[["de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um Freiwilligendienste im Ausland. Sie ermöglichen Menschen, sich in sozialen, ökologischen oder kulturellen Projekten zu engagieren und andere Lebensbedingungen kennenzulernen. Gleichzeitig können sie Fähigkeiten wie Teamarbeit, Selbstständigkeit und interkulturelle Kommunikation stärken.\nEin sinnvoller Dienst beginnt mit einer sorgfältigen Auswahl. Interessierte sollten prüfen, welche Aufgaben angeboten werden, wie lange der Einsatz dauert und welche Unterstützung vor Ort vorhanden ist. Ein Projekt darf nicht nur dazu dienen, möglichst günstig zu reisen. Es muss einen nachvollziehbaren Bedarf geben und mit lokalen Partnern abgestimmt sein.\nDie Vorbereitung umfasst Informationen über das Einsatzland, kulturelle Regeln, Sicherheit und die eigene Rolle. Sprachkenntnisse sind hilfreich, doch Offenheit und Lernbereitschaft sind ebenfalls wichtig. Freiwillige sollten wissen, an wen sie sich bei Problemen wenden können.\nWährend des Einsatzes ist die Zusammenarbeit mit lokalen Fachkräften entscheidend. Freiwillige können unterstützen, dürfen aber keine regulären Arbeitsplätze ersetzen. Projekte sollten die Kompetenzen vor Ort stärken und langfristig angelegt sein.\nNach der Rückkehr lohnt sich eine Auswertung. Teilnehmende können überlegen, welche Erfahrungen sie gemacht und welche Fähigkeiten sie erworben haben. Eine gute Organisation begleitet daher nicht nur die Ausreise, sondern auch die Vorbereitung, den Aufenthalt und die Rückkehr."]]}
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
archive=ROOT/"exam-026.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
