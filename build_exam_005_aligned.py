import asyncio
import subprocess
import zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output")
AUDIO=ROOT/"audio"
AUDIO.mkdir(parents=True,exist_ok=True)

# Prüfung 005 — Weiterbildung während des Berufslebens.
# Inhaltlich an GoetheExam05Audio.java ausgerichtet.
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Mitteilung der Personalabteilung: Die interne Schulung zum Thema Tabellenkalkulation beginnt am kommenden Mittwoch nicht um neun, sondern erst um zehn Uhr. Der Raum im zweiten Stock bleibt derselbe. Wer ein eigenes Notebook besitzt, kann es mitbringen; Geräte stehen jedoch auch vor Ort zur Verfügung.")],
"teil1_02.mp3":[("de-DE-KatjaNeural","Ich würde gern einen Sprachkurs machen, aber mein Arbeitstag endet oft spät."),("de-DE-ConradNeural","Hast du schon nach einem Kurs am Samstag gesucht?"),("de-DE-KatjaNeural","Ja, allerdings findet der nur jede zweite Woche statt."),("de-DE-ConradNeural","Vielleicht kannst du die fehlenden Einheiten online nachholen.")],
"teil1_03.mp3":[("de-DE-KatjaNeural","Hinweis des Bildungszentrums: Für den Kurs Projektmanagement sind noch drei Plätze frei. Die Anmeldung ist bis Freitag möglich. Beschäftigte kleiner Unternehmen können eine Ermäßigung beantragen, müssen dafür aber eine Bestätigung ihres Arbeitgebers vorlegen.")],
"teil1_04.mp3":[("de-DE-AmalaNeural","Ich habe früher gedacht, eine Weiterbildung müsse immer mehrere Monate dauern. Mein letzter Kurs bestand aber aus vier kurzen Online-Modulen, die ich abends bearbeiten konnte. Gerade weil ich das Gelernte direkt im Betrieb ausprobiert habe, war der Nutzen für mich besonders groß.")],
"teil1_05.mp3":[("de-DE-KatjaNeural","Durchsage im Betrieb: Die Beratung zu Fördermöglichkeiten findet heute nicht wie geplant im Konferenzraum statt. Sie wurde in das kleinere Besprechungszimmer neben dem Empfang verlegt. Der Beginn um 14 Uhr bleibt unverändert. Eine Anmeldung ist nicht erforderlich.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Viele Beschäftigte müssen sich beruflich weiterentwickeln, obwohl ihre Arbeitszeit bereits sehr voll ist. Herr Dr. Weber, wie können Unternehmen darauf reagieren?"),
("de-DE-ConradNeural","Weiterbildungsexperte: Zunächst sollten sie nicht einfach möglichst viele Kurse anbieten. Sinnvoller ist es, gemeinsam mit den Beschäftigten festzustellen, welche Fähigkeiten in den kommenden Jahren tatsächlich gebraucht werden. Daraus kann ein passender Lernplan entstehen."),
("de-DE-KatjaNeural","Moderatorin: Sollte Weiterbildung während der Arbeitszeit stattfinden?"),
("de-DE-ConradNeural","Experte: Wenn es organisatorisch möglich ist, halte ich das für vorteilhaft. Lernen nach Feierabend kann zwar funktionieren, führt aber auf Dauer zu zusätzlicher Belastung. Manche Betriebe ermöglichen deshalb feste Lernstunden oder flexible Arbeitszeiten."),
("de-DE-KatjaNeural","Moderatorin: Welche Rolle spielen digitale Angebote?"),
("de-DE-ConradNeural","Experte: Sie bieten große Freiheit, weil man Inhalte zeitlich unabhängig bearbeiten kann. Allerdings braucht man dafür Selbstdisziplin. Außerdem fehlt bei rein digitalen Kursen manchmal der direkte Austausch, der gerade bei komplexen Themen hilfreich ist. Eine Kombination aus Online-Phasen und persönlichen Treffen ist oft überzeugend."),
("de-DE-KatjaNeural","Moderatorin: Wie lässt sich feststellen, ob eine Weiterbildung erfolgreich war?"),
("de-DE-ConradNeural","Experte: Nicht allein durch eine Abschlussprüfung. Entscheidend ist, ob die Teilnehmenden das Gelernte später bei ihrer Arbeit anwenden können. Vorgesetzte sollten dafür geeignete Aufgaben und Rückmeldungen anbieten."),
("de-DE-KatjaNeural","Moderatorin: Und was ist mit älteren Beschäftigten, die sich unsicher fühlen?"),
("de-DE-ConradNeural","Experte: Man sollte sie nicht unterschätzen. Erfahrung ist eine wichtige Grundlage. Wenn Lernangebote verständlich aufgebaut sind und genügend Zeit lassen, profitieren Menschen in jedem Alter davon.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderator: Heute diskutieren wir, ob Unternehmen ihre Beschäftigten stärker zur Weiterbildung verpflichten sollten. Frau Roth, Sie sind Geschäftsführerin eines mittelständischen Betriebs."),
("de-DE-AmalaNeural","Roth: Ich halte eine allgemeine Pflicht für problematisch. Nicht jede Person braucht zur gleichen Zeit dieselben Kenntnisse. Wir sollten gemeinsam Ziele vereinbaren und passende Angebote machen, statt pauschale Vorgaben zu erlassen."),
("de-DE-KatjaNeural","Moderator: Herr Demir, Sie vertreten einen Betriebsrat."),
("de-DE-ConradNeural","Demir: Freiwilligkeit klingt gut, aber in der Praxis fehlt vielen Beschäftigten die Zeit. Wenn Weiterbildung nur zusätzlich zur normalen Arbeit stattfindet, nehmen vor allem diejenigen teil, die ohnehin viel Eigeninitiative zeigen. Deshalb müssen Lernzeiten verbindlich eingeplant werden."),
("de-DE-KatjaNeural","Moderator: Frau Roth, können Sie sich darauf einlassen?"),
("de-DE-AmalaNeural","Roth: Ja, auf feste Zeitfenster kann man sich einigen. Die Inhalte sollten aber gemeinsam ausgewählt werden. Wir müssen auch berücksichtigen, dass kleine Teams nicht jederzeit auf einzelne Fachkräfte verzichten können."),
("de-DE-ConradNeural","Demir: Das verstehe ich. Gerade deshalb sollte die Planung früh beginnen. Außerdem brauchen Beschäftigte eine klare Information darüber, welche Kosten der Betrieb übernimmt."),
("de-DE-KatjaNeural","Moderator: Beide Seiten sprechen sich also für strukturierte Planung aus, setzen aber unterschiedliche Schwerpunkte.")
],
"teil4_01.mp3":[("de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um berufliche Weiterbildung in Zeiten schneller Veränderungen. Viele Tätigkeiten verändern sich durch neue Technologien, andere Arbeitsabläufe und veränderte Erwartungen der Kundschaft. Deshalb reicht es heute oft nicht mehr aus, einmal erworbene Kenntnisse bis zum Ende des Berufslebens unverändert zu nutzen. Weiterbildung kann unterschiedliche Formen annehmen. Neben längeren Lehrgängen gibt es kurze Fachseminare, digitale Lernmodule und den Austausch mit erfahrenen Kolleginnen und Kollegen. Welche Form geeignet ist, hängt vom Lernziel und von der verfügbaren Zeit ab. Ein kurzer Kurs kann eine konkrete Software erklären, während eine umfassende Umschulung deutlich mehr Begleitung benötigt. Wichtig ist außerdem, dass Lernen nicht nur als private Aufgabe betrachtet wird. Arbeitgeber können Lernzeit ermöglichen, Kosten übernehmen und Aufgaben anbieten, bei denen neue Kenntnisse praktisch erprobt werden. Beschäftigte wiederum sollten ihre Lernziele aktiv mitgestalten und frühzeitig auf Unterstützungsbedarf hinweisen. Ein weiterer Punkt ist die Anerkennung bereits vorhandener Fähigkeiten. Wer viele Jahre Berufserfahrung gesammelt hat, verfügt häufig über Kompetenzen, die nicht in einem Zeugnis stehen. Gespräche, praktische Aufgaben und eine strukturierte Einschätzung können helfen, diese Kenntnisse sichtbar zu machen. Abschließend lässt sich sagen: Erfolgreiche Weiterbildung verbindet persönliche Motivation mit guten betrieblichen Rahmenbedingungen. Sie ist kein einmaliges Ereignis, sondern ein fortlaufender Prozess, der regelmäßig überprüft und angepasst werden sollte.")]
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
archive=ROOT/"exam-005.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
