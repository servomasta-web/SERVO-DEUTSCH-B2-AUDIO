import asyncio
import subprocess
import zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output")
AUDIO=ROOT/"audio"
AUDIO.mkdir(parents=True,exist_ok=True)

# Prüfung 018 — Künstliche Intelligenz im Berufsalltag.
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Interne Mitteilung der Personalabteilung: Der Workshop zum Einsatz künstlicher Intelligenz findet am Donnerstag statt. Da der große Konferenzraum renoviert wird, treffen sich die Teilnehmenden diesmal im kleinen Besprechungsraum neben der Bibliothek. Die Uhrzeit bleibt unverändert: Beginn ist um neun Uhr.")],
"teil1_02.mp3":[("de-DE-ConradNeural","A: Hast du dich schon für die KI-Schulung angemeldet? B: Noch nicht. Ist sie denn verpflichtend? A: Nein, die Teilnahme ist freiwillig. Besonders empfohlen wird sie allerdings Beschäftigten, die regelmäßig Kundendaten bearbeiten. B: Dann sollte ich mich wohl anmelden.")],
"teil1_03.mp3":[("de-DE-KatjaNeural","Hinweis der IT-Abteilung: Die neue Textsoftware darf ab nächster Woche getestet werden. Vertrauliche Kundendaten dürfen jedoch nicht eingegeben werden, bevor die Datenschutzfreigabe der jeweiligen Abteilung vorliegt. Bitte verwendet ausschließlich die freigegebene Unternehmensversion.")],
"teil1_04.mp3":[("de-DE-AmalaNeural","Ich habe den Monatsbericht mit einem KI-Programm vorbereitet. Das hat mir viel Zeit gespart. Trotzdem musste ich alle Zahlen und Quellen noch einmal kontrollieren. Unsere Abteilungsleiterin hat ausdrücklich gesagt, dass der Bericht bis Donnerstag um neun Uhr eingereicht werden muss. Die Verantwortung liegt weiterhin bei uns.")],
"teil1_05.mp3":[("de-DE-KatjaNeural","Information des Beratungszentrums Digitalisierung: Beschäftigte, die Fragen zum Einsatz künstlicher Intelligenz haben, können einen persönlichen oder digitalen Beratungstermin vereinbaren. Die Anmeldung ist über das Intranet oder telefonisch möglich. Eine offene Sprechstunde findet jeden Freitag statt.")],
"teil2_01.mp3":[("de-DE-KatjaNeural","Moderatorin: Künstliche Intelligenz hält zunehmend Einzug in Unternehmen. Frau Professorin Seidel, welche Veränderungen beobachten Sie?\nSeidel: Viele Anwendungen unterstützen zunächst einzelne Arbeitsschritte. Sie können beispielsweise große Datenmengen sortieren, Entwürfe formulieren oder wiederkehrende Aufgaben vorbereiten. Das bedeutet aber nicht, dass ganze Berufe unmittelbar verschwinden. Häufig verändern sich vielmehr die Tätigkeiten innerhalb eines Berufs.\nModeratorin: Warum ist menschliche Kontrolle weiterhin notwendig?\nSeidel: Ein System kann überzeugend klingende, aber falsche Informationen liefern. Es kann außerdem Zusammenhänge übersehen oder problematische Muster aus den Trainingsdaten übernehmen. Deshalb müssen Ergebnisse überprüft und eingeordnet werden. Besonders in sensiblen Fällen sollte die abschließende Entscheidung bei einer verantwortlichen Person liegen.\nModeratorin: Was sollten Unternehmen bei der Einführung beachten?\nSeidel: Sie sollten Beschäftigte frühzeitig informieren und an der Auswahl der Anwendungen beteiligen. Eine Einführung von oben, ohne die Arbeitsabläufe zu erklären, führt häufig zu Unsicherheit. Sinnvoll ist ein begrenztes Pilotprojekt, aus dem man Erfahrungen sammelt, bevor man die Anwendung ausweitet.\nModeratorin: Welche Rolle spielt der Datenschutz?\nSeidel: Eine sehr große. Unternehmen müssen festlegen, welche Daten in welchen Systemen verarbeitet werden dürfen. Interne oder personenbezogene Informationen gehören nicht in beliebige kostenlose Online-Angebote. Es sollten ausschließlich geprüfte und freigegebene Anwendungen verwendet werden.\nModeratorin: Welche Kompetenzen werden künftig wichtiger?\nSeidel: Technisches Grundwissen ist hilfreich, aber nicht ausreichend. Beschäftigte müssen Ergebnisse kritisch beurteilen, gute Fragen formulieren und mit anderen kommunizieren können. Auch Fachwissen bleibt entscheidend, denn nur wer sein Arbeitsgebiet versteht, kann erkennen, ob eine Antwort sinnvoll ist. Die menschliche Rolle verschiebt sich also teilweise in Richtung Kontrolle, Einordnung und Zusammenarbeit.")],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderator: Wie lässt sich künstliche Intelligenz im Betrieb sinnvoll einsetzen? Herr Neumann, Sie leiten ein mittelständisches Unternehmen, das neue digitale Arbeitsabläufe erprobt."),
("de-DE-ConradNeural","Neumann: Wir haben mit einem kleinen Pilotprojekt begonnen. Eine Anwendung erstellt erste Entwürfe für interne Berichte. Das spart Zeit bei Routinearbeiten. Allerdings prüfen unsere Fachkräfte jedes Ergebnis, denn die Verantwortung kann nicht an eine Software abgegeben werden. Außerdem haben wir gemerkt, dass die Qualität stark davon abhängt, wie präzise wir die Aufgaben formulieren."),
("de-DE-KatjaNeural","Moderator: Frau Richter, Sie beraten Betriebsräte und Beschäftigte zu digitalen Veränderungen. Was ist Ihnen wichtig?"),
("de-DE-AmalaNeural","Richter: Zunächst brauchen wir klare Regeln zum Schutz sensibler Informationen. Die Beschäftigten müssen wissen, welche Daten sie verwenden dürfen und wer Zugriff auf die Ergebnisse hat. Außerdem sollten auch Kolleginnen und Kollegen ohne technische Vorkenntnisse beteiligt werden. Sie kennen die täglichen Arbeitsabläufe und können einschätzen, wo eine Anwendung wirklich hilfreich ist."),
("de-DE-ConradNeural","Neumann: Das stimmt. Wir haben deshalb Mitarbeitende aus verschiedenen Abteilungen in die Testphase aufgenommen. So wurden Probleme sichtbar, die unsere IT-Abteilung allein nicht erkannt hätte."),
("de-DE-AmalaNeural","Richter: Besonders vorsichtig müssen Unternehmen bei Personalentscheidungen sein. Automatische Bewertungen können Vorurteile enthalten oder wichtige persönliche Umstände übersehen. Solche Entscheidungen dürfen nicht allein einem Programm überlassen werden."),
("de-DE-KatjaNeural","Moderator: Vielen Dank. Offenbar braucht ein sinnvoller Einsatz sowohl praktische Erprobung als auch klare Schutzregeln und menschliche Verantwortung.")
],
"teil4_01.mp3":[("de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um künstliche Intelligenz im Berufsalltag und um die Frage, wie Unternehmen diese Technologie verantwortungsvoll nutzen können. KI-Anwendungen können Texte vorbereiten, Informationen ordnen oder große Datenmengen untersuchen. Dadurch lassen sich bestimmte Arbeitsschritte beschleunigen. Der tatsächliche Nutzen hängt jedoch davon ab, wie sorgfältig die Systeme eingesetzt werden.\nEin entscheidender Faktor ist die Qualität der Daten. Wenn Informationen unvollständig, veraltet oder einseitig sind, können auch die Ergebnisse problematisch sein. Deshalb reicht es nicht, eine Antwort nur deshalb zu übernehmen, weil sie sprachlich überzeugend klingt. Fachkräfte müssen prüfen, ob sie sachlich richtig und für die konkrete Situation geeignet ist.\nAuch die Formulierung der Aufgaben spielt eine Rolle. Eine klare Anfrage beschreibt das Ziel, den Zusammenhang und die gewünschte Form des Ergebnisses. Je genauer die Aufgabe gestellt wird, desto eher kann das System eine brauchbare Unterstützung liefern. Trotzdem bleibt eine Überprüfung notwendig.\nUnternehmen sollten ihre Beschäftigten deshalb nicht nur in der Bedienung einzelner Programme schulen. Wichtig sind ebenso kritisches Denken, Fachwissen und Kenntnisse über Datenschutz. Mitarbeitende müssen wissen, welche Informationen in ein System eingegeben werden dürfen und welche Anwendungen offiziell freigegeben sind.\nTransparenz schafft zusätzlich Vertrauen. Es sollte nachvollziehbar sein, wann KI verwendet wurde, welche Aufgaben sie übernommen hat und wer das Ergebnis kontrolliert. Besonders bei Personalfragen, finanziellen Entscheidungen oder anderen sensiblen Bereichen darf eine automatische Bewertung nicht unkritisch übernommen werden. Fehler und Vorurteile könnten sonst unbemerkt weitergegeben werden.\nDie Zukunft der Arbeit wird daher wahrscheinlich nicht einfach aus einem Gegensatz zwischen Mensch und Maschine bestehen. Vielmehr können technische Systeme Routineaufgaben erleichtern, während Menschen Erfahrung, Urteilsvermögen und soziale Fähigkeiten einbringen. Voraussetzung dafür sind klare Regeln, passende Weiterbildung und eine Kultur, in der Fragen und Kritik ausdrücklich erwünscht sind. Ein verantwortungsvoller KI-Einsatz verbindet also technischen Fortschritt mit menschlicher Kontrolle.")]}
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
