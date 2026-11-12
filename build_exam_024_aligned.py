import asyncio, subprocess, zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output")
AUDIO=ROOT/"audio"
AUDIO.mkdir(parents=True,exist_ok=True)

# Prüfung 024 — Wissenschaftskommunikation und Vertrauen in die Forschung.
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Hinweis der Stadtbibliothek: Am Mittwoch findet das Wissenschaftscafé diesmal im großen Lesesaal statt. Beginn ist um siebzehn Uhr. Der Eintritt ist frei; wegen der begrenzten Plätze wird jedoch um eine Anmeldung gebeten.")],
"teil1_02.mp3":[("de-DE-ConradNeural","Die Universität lädt zu einem öffentlichen Gespräch über neue Forschungsergebnisse ein. Die Veranstaltung beginnt am Dienstag um achtzehn Uhr im Hörsaal drei. Fragen können vorab über ein Onlineformular eingereicht werden.")],
"teil1_03.mp3":[("de-DE-AmalaNeural","Die Ausstellung zur Klimaforschung im Naturkundemuseum ist ab sofort auch sonntags geöffnet. Besucherinnen und Besucher können dort Experimente ausprobieren und erfahren, wie Forschende langfristige Veränderungen messen.")],
"teil1_04.mp3":[("de-DE-KatjaNeural","Das Forschungsinstitut bietet für Schulklassen eine Führung mit Experimenten an. Lehrkräfte müssen ihre Gruppe mindestens zwei Wochen vorher anmelden. Die Teilnahme ist kostenlos; die Anreise organisiert die Schule selbst.")],
"teil1_05.mp3":[("de-DE-ConradNeural","Der neue Podcast der Hochschule erklärt aktuelle Forschung in verständlicher Sprache. Eine neue Folge erscheint alle zwei Wochen. Zu jeder Sendung gibt es eine Liste mit weiterführenden Quellen und Links zu den besprochenen Studien.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Viele Menschen fragen sich, welchen wissenschaftlichen Informationen sie vertrauen können. Professorin Weber, Sie forschen zur Wissenschaftskommunikation. Was ist dafür besonders wichtig?"),
("de-DE-AmalaNeural","Weber: Vertrauen entsteht nicht dadurch, dass Forschende immer sicher klingen. Entscheidend ist, dass sie offenlegen, wie sie zu ihren Ergebnissen gekommen sind, welche Methoden sie verwendet haben und wo die Grenzen einer Untersuchung liegen."),
("de-DE-KatjaNeural","Moderatorin: Manche Menschen wundern sich, wenn neue Studien frühere Aussagen verändern. Ist das ein Zeichen für mangelnde Zuverlässigkeit?"),
("de-DE-AmalaNeural","Weber: Nein. Wissenschaft entwickelt sich weiter. Neue Daten können frühere Annahmen ergänzen oder korrigieren. Wichtig ist, dass solche Veränderungen nachvollziehbar erklärt werden. Erkenntnisse sind nicht beliebig, aber sie müssen überprüfbar bleiben."),
("de-DE-KatjaNeural","Moderatorin: Welche Verantwortung tragen Medien, wenn sie über Forschung berichten?"),
("de-DE-AmalaNeural","Weber: Journalistinnen und Journalisten sollten Quellen prüfen und Ergebnisse in den richtigen Zusammenhang stellen. Eine einzelne Studie ist selten ausreichend, um eine allgemeine Schlussfolgerung zu ziehen. Auch die Größe einer Untersuchung und mögliche Interessenkonflikte sind relevant."),
("de-DE-KatjaNeural","Moderatorin: Wie sollten Leserinnen und Leser mit besonders spektakulären Schlagzeilen umgehen?"),
("de-DE-AmalaNeural","Weber: Es lohnt sich, nicht nur die Überschrift zu lesen, sondern nach der Originalquelle zu suchen. Man sollte prüfen, ob die Meldung tatsächlich das wiedergibt, was untersucht wurde, und ob andere Studien zu ähnlichen Ergebnissen kommen."),
("de-DE-KatjaNeural","Moderatorin: Kann die Öffentlichkeit selbst zur Forschung beitragen?"),
("de-DE-AmalaNeural","Weber: Ja. Bürgerdialoge und Projekte mit freiwilligen Teilnehmenden können wichtige Fragen sichtbar machen. Die Beteiligung ersetzt jedoch keine fachliche Prüfung. Sie hilft vielmehr, gesellschaftliche Bedürfnisse zu verstehen und Forschung verständlicher zu machen."),
("de-DE-KatjaNeural","Moderatorin: Was ist Ihre wichtigste Empfehlung?"),
("de-DE-AmalaNeural","Weber: Wissenschaftseinrichtungen sollten regelmäßig, offen und in verständlicher Sprache kommunizieren. Dazu gehört auch, Unsicherheiten nicht zu verschweigen. Gerade diese Ehrlichkeit ist eine Grundlage für langfristiges Vertrauen.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderator: Wie lässt sich die Kommunikation über Forschung verbessern? Dazu diskutieren heute Frau Berger, die an einer Universität arbeitet, und Herr Neumann, Wissenschaftsredakteur einer Tageszeitung. Frau Berger, was ist Ihnen besonders wichtig?"),
("de-DE-AmalaNeural","Berger: Forschende sollten nicht nur erklären, was sie herausgefunden haben. Sie müssen auch deutlich machen, welche Fragen eine Studie nicht beantworten kann. Außerdem können Bürgerdialoge helfen, gesellschaftliche Bedürfnisse frühzeitig zu erkennen."),
("de-DE-ConradNeural","Neumann: Aus journalistischer Sicht ist die Prüfung der Quellen entscheidend. Redaktionen müssen Methoden und Belege sorgfältig prüfen. Eine vorläufige Beobachtung darf nicht als endgültige Entdeckung dargestellt werden, nur weil eine solche Überschrift mehr Aufmerksamkeit bekommt."),
("de-DE-AmalaNeural","Berger: Verständliche Sprache ist ebenfalls wichtig. Das bedeutet aber keineswegs, dass Inhalte ungenau werden dürfen. Fachbegriffe kann man erklären, ohne die Ergebnisse zu verfälschen. Und mögliche Interessenkonflikte sollten offen genannt werden."),
("de-DE-ConradNeural","Neumann: Da stimme ich zu. Auch Medien müssen offenlegen, wenn eine Studie von einem Unternehmen finanziert wurde. Gleichzeitig sollten sie nicht so tun, als seien alle wissenschaftlichen Positionen gleich gut belegt. Kritische Einordnung gehört zu unserem Beruf."),
("de-DE-KatjaNeural","Moderator: Sie setzen also beide auf Transparenz, unterscheiden sich aber in Ihren täglichen Aufgaben. Vielen Dank für das Gespräch.")
],
"teil4_01.mp3":[
("de-DE-ConradNeural","Guten Tag. In meinem Vortrag beschäftige ich mich mit der Frage, wie Wissenschaft kommuniziert werden sollte und wie dadurch Vertrauen entstehen kann. Forschung beeinflusst viele Bereiche unseres Lebens, zum Beispiel Gesundheit, Umwelt, Technik und Bildung. Deshalb ist es wichtig, dass wissenschaftliche Erkenntnisse nicht nur innerhalb von Hochschulen diskutiert werden.\nZunächst muss man verstehen, wodurch sich wissenschaftliche Aussagen von bloßen Behauptungen unterscheiden. Wissenschaftliche Erkenntnisse beruhen auf überprüfbaren Methoden, nachvollziehbaren Daten und einer kritischen Auseinandersetzung mit anderen Ergebnissen. Eine Studie liefert allerdings nicht automatisch eine endgültige Antwort. Ihre Aussagekraft hängt unter anderem von der Fragestellung, der Stichprobengröße und der Qualität der verwendeten Daten ab.\nEin weiterer Punkt ist der Umgang mit Unsicherheit. In der Forschung können sich Einschätzungen verändern, wenn neue Belege hinzukommen. Das ist kein grundsätzlicher Widerspruch, sondern ein Teil wissenschaftlicher Arbeit. Forschende sollten deshalb deutlich machen, was bereits gut belegt ist und wo noch offene Fragen bestehen.\nAuch Medien tragen eine große Verantwortung. Schlagzeilen müssen Aufmerksamkeit wecken, dürfen Ergebnisse aber nicht übertreiben. Wer über eine Studie berichtet, sollte die Originalquelle prüfen, die Methode erklären und mögliche Interessenkonflikte nennen. Besonders in sozialen Netzwerken besteht die Gefahr, dass Aussagen ohne Zusammenhang verbreitet werden.\nWie können Forschungseinrichtungen Vertrauen fördern? Sie sollten verständliche Informationen anbieten, offene Veranstaltungen organisieren und Rückfragen ernst nehmen. Bürgerinnen und Bürger können durch Dialogformate oder Beteiligungsprojekte eigene Perspektiven einbringen. Das ersetzt keine wissenschaftliche Prüfung, macht aber gesellschaftliche Erwartungen sichtbar.\nZusammenfassend lässt sich sagen: Vertrauen entsteht nicht durch vollmundige Versprechen, sondern durch Transparenz, nachvollziehbare Verfahren und die Bereitschaft, Kritik anzunehmen. Eine gute Wissenschaftskommunikation erklärt sowohl die Bedeutung von Ergebnissen als auch ihre Grenzen.")
]
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
    listing.write_text("".join(f"file '{p.resolve()}'\\n" for p in parts),encoding="utf-8")
    target=AUDIO/name
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(listing),"-codec:a","libmp3lame","-b:a","128k",str(target)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
    for p in parts+[listing]: p.unlink(missing_ok=True)
    if not target.exists() or target.stat().st_size<1024: raise RuntimeError(f"MP3 invalide: {name}")
    print(f"OK {name}: {target.stat().st_size} octets",flush=True)

async def main():
    for name,utterances in tracks.items():
        await make_track(name,utterances)

asyncio.run(main())
expected=["teil1_01.mp3","teil1_02.mp3","teil1_03.mp3","teil1_04.mp3","teil1_05.mp3","teil2_01.mp3","teil3_01.mp3","teil4_01.mp3"]
archive=ROOT/"exam-024.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
