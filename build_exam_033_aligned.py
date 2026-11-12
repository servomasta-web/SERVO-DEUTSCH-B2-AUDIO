# SERVO DEUTSCH B2 — exam 033 aligned audio generation
import asyncio
import subprocess
import zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output")
AUDIO=ROOT/"audio"
AUDIO.mkdir(parents=True,exist_ok=True)

# Audioinhalte sind auf die 30 Fragen von Prüfung 031 abgestimmt.
tracks={
"teil1_01.mp3":[["de-DE-KatjaNeural","Die Stadt lädt Schülerinnen und Schüler im Frühjahr zu einer Informationsmesse zur Berufsorientierung ein. Am Samstag von zehn bis fünfzehn Uhr stellen Betriebe und Berufsschulen ihre Angebote vor. Jugendliche können mit Auszubildenden sprechen und Fragen zum Arbeitsalltag stellen. Der Eintritt ist frei."]],
"teil1_02.mp3":[["de-DE-ConradNeural","Das Kreiskrankenhaus bietet im Juli ein einwöchiges Schülerpraktikum an. Interessierte Jugendliche ab sechzehn Jahren können verschiedene Bereiche kennenlernen. Für die Bewerbung genügt ein kurzes Motivationsschreiben. Bewerbungsschluss ist der fünfzehnte Juni."]],
"teil1_03.mp3":[["de-DE-AmalaNeural","Die Handwerkskammer veranstaltet am kommenden Freitag einen Workshop zum Thema Bewerbung. Fachleute erklären, wie man einen Lebenslauf gestaltet und sich auf ein Vorstellungsgespräch vorbereitet. Die Teilnahme ist kostenlos. Eine Anmeldung über die Internetseite ist erforderlich."]],
"teil1_04.mp3":[["de-DE-KatjaNeural","Das Jugendzentrum vermittelt junge Menschen an soziale Einrichtungen, in denen sie ein freiwilliges Orientierungsprojekt absolvieren können. Dabei helfen sie zum Beispiel bei Freizeitangeboten für Kinder oder bei Veranstaltungen für ältere Menschen. Das Projekt dauert zwischen zwei und vier Wochen."]],
"teil1_05.mp3":[["de-DE-ConradNeural","Die Berufsberatung der Arbeitsagentur erweitert ihr Angebot. Jugendliche können ab sofort auch online einen Beratungstermin vereinbaren. Wer lieber persönlich sprechen möchte, kann weiterhin telefonisch einen Termin buchen. Die Beratung ist kostenlos und unabhängig von Schulnoten."]],
"teil2_01.mp3":[["de-DE-KatjaNeural","Moderatorin: Viele Jugendliche wissen nach der Schule noch nicht genau, welchen Beruf sie wählen sollen. Frau Schneider, Sie beraten junge Menschen. Wie können Praktika helfen?\nBeraterin: Sie ermöglichen einen realistischen Einblick in den Arbeitsalltag. Man erlebt, welche Aufgaben tatsächlich anfallen und wie ein Team zusammenarbeitet. Das ist oft aussagekräftiger als eine Beschreibung in einer Broschüre.\nModeratorin: Reicht ein kurzer Besuch in einem Betrieb aus?\nBeraterin: Für einen ersten Eindruck vielleicht. Ein Praktikum sollte aber möglichst mehrere Tage dauern. Vor Beginn ist es sinnvoll zu klären, welche Aufgaben und Lernziele vorgesehen sind. Nur Kaffee zu kochen oder Unterlagen zu kopieren, bringt kaum berufliche Orientierung.\nModeratorin: Welche Rolle spielen Gespräche mit Auszubildenden?\nBeraterin: Eine sehr große. Auszubildende können aus eigener Erfahrung berichten, wie der Einstieg abläuft, welche Anforderungen es gibt und was ihnen an ihrem Beruf gefällt. Jugendliche trauen sich manchmal eher, ihnen Fragen zu stellen als einer Führungskraft.\nModeratorin: Was können Schulen beitragen?\nBeraterin: Sie sollten Praktika gut vorbereiten und danach gemeinsam mit den Jugendlichen auswerten. Dabei geht es nicht nur darum, ob ein Beruf gefallen hat. Man sollte auch überlegen, welche Fähigkeiten man einsetzen konnte und welche Arbeitsbedingungen wichtig sind.\nModeratorin: Was raten Sie Jugendlichen, die noch völlig unsicher sind?\nBeraterin: Sie sollten mehrere Berufsfelder kennenlernen und nicht sofort eine endgültige Entscheidung treffen. Auch freiwillige Projekte oder Gespräche mit Berufstätigen können helfen. Entscheidend ist, eigene Interessen mit den tatsächlichen Anforderungen eines Berufs zu vergleichen.\nModeratorin: Und was ist mit der Verantwortung der Betriebe?\nBeraterin: Sie müssen Praktikanten sinnvoll betreuen. Dazu gehören eine feste Ansprechperson, verständliche Aufgaben und regelmäßige Rückmeldungen. Ein Praktikum ist eine Lerngelegenheit und keine Möglichkeit, dauerhaft fehlende Arbeitskräfte zu ersetzen."]],
"teil3_01.mp3":[["de-DE-KatjaNeural","Moderatorin: Wie gut bereiten Praktika junge Menschen auf die Berufswahl vor? Nora, wie sehen Sie das?"],["de-DE-AmalaNeural","Nora: Ich finde, ein Praktikum sollte nicht nur zwei oder drei Tage dauern. Erst nach einer gewissen Zeit versteht man, wie ein Betrieb funktioniert und welche Aufgaben zu einem Beruf gehören. Außerdem brauchen Jugendliche Unterstützung dabei, sich auf Bewerbungsgespräche vorzubereiten. Das wird in der Schule meiner Meinung nach noch zu selten geübt."],["de-DE-KatjaNeural","Moderatorin: Tim, was ist Ihnen besonders wichtig?"],["de-DE-ConradNeural","Tim: Entscheidend ist die Qualität des Praktikums. Es darf nicht passieren, dass Jugendliche nur als billige Arbeitskräfte eingesetzt werden und den ganzen Tag einfache Hilfsarbeiten erledigen. Betriebe sollten klare Lernaufgaben festlegen und eine Person benennen, die Fragen beantwortet. Nur dann können beide Seiten davon profitieren."],["de-DE-KatjaNeural","Moderatorin: Selin, haben Sie selbst Erfahrungen gesammelt?"],["de-DE-AmalaNeural","Selin: Ja, ich habe an einem freiwilligen Projekt in einem Seniorenheim teilgenommen. Zunächst dachte ich, soziale Arbeit sei nichts für mich. Durch die Begegnungen habe ich aber gemerkt, wie gern ich mit Menschen arbeite. Deshalb halte ich Gespräche mit Beschäftigten aus verschiedenen Berufen für sehr hilfreich. Man entdeckt manchmal Interessen, die man vorher gar nicht kannte."],["de-DE-ConradNeural","Tim: Das stimmt. Trotzdem müssen die Aufgaben im Praktikum gut organisiert sein, sonst bleibt der Lerneffekt gering."],["de-DE-KatjaNeural","Moderatorin: Es kommt also sowohl auf praktische Erfahrungen als auch auf eine gute Betreuung an."]],
"teil4_01.mp3":[["de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um Praktika und Berufsorientierung für junge Menschen. Die Wahl eines Berufs gehört zu den wichtigen Entscheidungen im Leben. Gleichzeitig fällt es vielen Jugendlichen schwer, sich eine konkrete Tätigkeit vorzustellen, solange sie nur aus dem Unterricht oder aus Medien davon hören. Berufsorientierung soll deshalb helfen, Interessen, Fähigkeiten und berufliche Möglichkeiten miteinander zu verbinden.\nEin zentrales Instrument sind Praktika. Sie ermöglichen Einblicke in den Arbeitsalltag und machen sichtbar, welche Aufgaben, Arbeitszeiten und Anforderungen mit einem Beruf verbunden sind. Ein einzelnes kurzes Praktikum reicht jedoch häufig nicht aus, um alle Seiten eines Berufsfeldes kennenzulernen. Es ist daher sinnvoll, unterschiedliche Erfahrungen zu sammeln und Eindrücke miteinander zu vergleichen.\nNeben fachlichen Kenntnissen spielen überfachliche Kompetenzen eine wichtige Rolle. Kommunikation, Teamarbeit, Zuverlässigkeit und die Fähigkeit, Probleme zu lösen, werden in vielen Berufen gebraucht. Praktika bieten die Gelegenheit, solche Fähigkeiten auszuprobieren und weiterzuentwickeln. Sie zeigen Jugendlichen außerdem, wo sie noch Unterstützung benötigen.\nDamit ein Praktikum erfolgreich ist, müssen Schulen und Betriebe zusammenarbeiten. Schulen können bei der Vorbereitung helfen, Kontakte vermitteln und die Erfahrungen anschließend auswerten. Betriebe sollten sinnvolle Aufgaben anbieten, eine feste Ansprechperson benennen und regelmäßig Rückmeldung geben. Ohne Betreuung besteht die Gefahr, dass Praktikanten hauptsächlich einfache Hilfsarbeiten übernehmen und wenig lernen.\nBei der Auswahl eines Praktikumsplatzes sollten Jugendliche nicht nur auf den Namen eines Unternehmens achten. Wichtig sind die eigenen Interessen, die Lernmöglichkeiten und die Qualität der Betreuung. Auch kleinere Einrichtungen können wertvolle Erfahrungen bieten. Gespräche mit Auszubildenden und Beschäftigten ergänzen den praktischen Einblick und machen unterschiedliche Berufswege sichtbar.\nNach dem Praktikum ist eine Reflexion besonders wichtig. Jugendliche sollten überlegen, welche Tätigkeiten ihnen gefallen haben, welche Schwierigkeiten aufgetreten sind und welche Fähigkeiten sie einsetzen konnten. Auf dieser Grundlage lassen sich weitere Schritte planen, etwa ein zweites Praktikum, ein Beratungsgespräch oder eine Bewerbung um einen Ausbildungsplatz.\nZusammenfassend lässt sich sagen: Eine gute Berufsorientierung besteht nicht aus einer einzigen Entscheidung. Sie entwickelt sich durch praktische Erfahrungen, verlässliche Beratung und die eigene Reflexion. So können junge Menschen einen realistischen Weg finden, der zu ihren Interessen und Fähigkeiten passt. Vielen Dank für Ihre Aufmerksamkeit."]]
}

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
archive=ROOT/"exam-033.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
