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
tracks={"teil1_01.mp3":[["de-DE-KatjaNeural","Mitteilung des Career Centers: Die Bewerbungsunterlagen für das Sommerpraktikum müssen bis zum 10. April eingereicht werden. Das Auswahlgespräch findet erst nach Ende der Prüfungsphase statt. Fehlende Arbeitszeugnisse können nachgereicht werden."]],"teil1_02.mp3":[["de-DE-KatjaNeural","A: Ich habe ein Praktikum in einer kleinen Firma gefunden. B: Ist das bezahlt? A: Ja, aber wichtiger ist mir, dass ich ein eigenes Projekt übernehmen darf. B: Dann frag am besten nach, wer dich betreut und wie regelmäßig ihr Feedback besprecht."]],"teil1_03.mp3":[["de-DE-KatjaNeural","Hinweis der Hochschule: Studierende können sich ab Montag für die Praxisbörse anmelden. Dort stellen Unternehmen und gemeinnützige Organisationen ihre Praktikumsplätze vor. Die Teilnahme ist kostenlos, eine Anmeldung ist wegen der begrenzten Plätze erforderlich."]],"teil1_04.mp3":[["de-DE-AmalaNeural","Während meines Praktikums habe ich gemerkt, dass die Aufgaben ganz anders waren als in der Stellenbeschreibung. Ich habe das Gespräch mit meiner Betreuerin gesucht. Danach wurden meine Tätigkeiten neu abgestimmt und ich durfte auch bei Kundenterminen mitarbeiten."]],"teil1_05.mp3":[["de-DE-KatjaNeural","Durchsage im Prüfungsamt: Die Bescheinigungen über Pflichtpraktika werden ab sofort nicht mehr am Schalter ausgestellt. Studierende können sie über das Hochschulportal beantragen und als PDF herunterladen."]],"teil2_01.mp3":[["de-DE-KatjaNeural","Moderator: Ein Praktikum gehört für viele Studierende zum Studium. Frau Dr. Vogler, Sie untersuchen den Übergang von der Hochschule in den Beruf. Was macht ein gutes Praktikum aus?\nVogler: Es sollte Lernziele haben und nicht nur aus einfachen Hilfsarbeiten bestehen. Studierende brauchen eine Ansprechperson, die Aufgaben erklärt und regelmäßig Rückmeldung gibt. Außerdem sollte klar sein, wie das Praktikum mit dem Studienfach zusammenhängt.\nModerator: Ist ein Praktikum während des Semesters sinnvoll?\nVogler: Das hängt von der Dauer und dem Studienplan ab. Ein kurzes Teilzeitpraktikum kann möglich sein. Ein längerer Einsatz passt oft besser in die vorlesungsfreie Zeit. Wichtig ist, dass Prüfungen und Lehrveranstaltungen nicht dauerhaft vernachlässigt werden.\nModerator: Was sollten Studierende vor der Zusage klären?\nVogler: Aufgaben, Arbeitszeiten, Vergütung und Betreuung. Sie sollten auch fragen, ob es eine schriftliche Vereinbarung gibt und wie mit vertraulichen Informationen umgegangen wird.\nModerator: Was ist mit unbezahlten Praktika?\nVogler: Sie können den Zugang erschweren, besonders für Menschen, die ihren Lebensunterhalt selbst finanzieren müssen. Deshalb sollten Hochschulen und Unternehmen faire Bedingungen fördern. Eine Vergütung ist nicht der einzige Qualitätsfaktor, aber sie ist ein wichtiger Aspekt.\nModerator: Wie lässt sich der Lernerfolg sichern?\nVogler: Durch ein kurzes Zielgespräch am Anfang, regelmäßige Zwischenbesprechungen und eine Auswertung am Ende. Studierende sollten ihre Erfahrungen dokumentieren und überlegen, welche Fähigkeiten sie entwickelt haben."]],"teil3_01.mp3":[["de-DE-KatjaNeural","Moderatorin: Sollten Pflichtpraktika im Studium immer bezahlt werden? Herr Lauer, Sie vertreten einen Verband mittelständischer Unternehmen."],["de-DE-ConradNeural","Lauer: Eine Vergütung ist wünschenswert, aber kleine Betriebe können nicht in jedem Fall dieselben Beträge zahlen wie große Konzerne. Wir sollten auch berücksichtigen, dass Unternehmen Zeit in Anleitung und Betreuung investieren."],["de-DE-KatjaNeural","Moderatorin: Frau Özdemir, Sie beraten Studierende."],["de-DE-AmalaNeural","Özdemir: Ohne Bezahlung können viele Studierende gar nicht teilnehmen. Sie müssen Miete und Lebenshaltungskosten finanzieren. Ein Pflichtpraktikum darf nicht davon abhängen, ob die Familie den Zeitraum finanziell überbrücken kann."],["de-DE-ConradNeural","Lauer: Vielleicht könnte es eine Mindestvergütung geben, die nach Dauer und Umfang gestaffelt ist. Zusätzlich könnten öffentliche Förderprogramme kleine Betriebe unterstützen."],["de-DE-AmalaNeural","Özdemir: Eine Staffelung wäre möglich, solange sie transparent ist und Studierende nicht zu unbezahlter Vollzeitarbeit verpflichtet werden. Auch die Qualität der Betreuung muss kontrolliert werden."],["de-DE-KatjaNeural","Moderatorin: Beide Seiten erkennen finanzielle Grenzen an, suchen aber nach Regeln, die faire Teilnahme und gute Betreuung sichern."]],"teil4_01.mp3":[["de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um Praktika während des Studiums. Sie können eine Brücke zwischen theoretischem Wissen und beruflicher Praxis bilden. Studierende lernen Arbeitsabläufe kennen, bauen Kontakte auf und erhalten einen realistischen Eindruck von einem Berufsfeld. Ein Praktikum ist jedoch nicht automatisch lehrreich, nur weil es in einem Unternehmen stattfindet.\nVor Beginn sollten Ziele und Aufgaben geklärt werden. Eine schriftliche Vereinbarung kann Arbeitszeit, Dauer, Vergütung, Urlaub und Ansprechpersonen festhalten. Besonders wichtig ist eine fachliche Betreuung. Studierende brauchen Aufgaben, die zu ihrem Lernstand passen, und Rückmeldungen, mit denen sie ihre Arbeit verbessern können.\nDie zeitliche Planung verdient Aufmerksamkeit. Während des Semesters muss ein Praktikum mit Lehrveranstaltungen und Prüfungen vereinbar sein. Längere Praktika finden deshalb häufig in der vorlesungsfreien Zeit statt. Hochschulen können beraten und bei der Suche nach geeigneten Plätzen helfen.\nAuch die finanzielle Seite beeinflusst den Zugang. Wenn ein Praktikum verpflichtend ist, aber nicht bezahlt wird, können Studierende mit wenig finanziellen Ressourcen benachteiligt sein. Faire Vergütung und Fördermöglichkeiten tragen zu gleichen Chancen bei.\nAm Ende sollte eine Auswertung stattfinden. Studierende können dokumentieren, welche Aufgaben sie übernommen und welche Fähigkeiten sie entwickelt haben. Unternehmen erhalten dadurch ebenfalls Rückmeldung. Ein gutes Praktikum ist eine Lernphase mit klaren Zielen, angemessener Betreuung und nachvollziehbaren Bedingungen."]]}
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
archive=ROOT/"exam-018.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
