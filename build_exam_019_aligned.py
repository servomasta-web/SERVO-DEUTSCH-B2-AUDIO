import asyncio
import subprocess
import zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output")
AUDIO=ROOT/"audio"
AUDIO.mkdir(parents=True,exist_ok=True)

# Prüfung 019 — Haustiere in Mietwohnungen.
# Inhaltlich an GoetheExam06Audio.java ausgerichtet.
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Mitteilung der Hausverwaltung: Im Wohnhaus am Park wird die Hausordnung zum Thema Haustiere präzisiert. Ein generelles Verbot gilt nicht. Wer ein neues Haustier aufnehmen möchte, soll es jedoch vorher schriftlich bei der Verwaltung anmelden. Die bestehenden Regelungen im Mietvertrag bleiben weiterhin gültig.")],
"teil1_02.mp3":[("de-DE-ConradNeural","A: Weißt du, ob ich für meinen Hamster eine Genehmigung brauche? B: Nach der Information der Hausverwaltung sind Kleintiere wie Hamster oder Zierfische normalerweise davon ausgenommen. A: Gut zu wissen. Und wie ist es bei Hunden? B: Die muss man vorher anmelden.")],
"teil1_03.mp3":[("de-DE-KatjaNeural","Hinweis für alle Bewohnerinnen und Bewohner: Hunde müssen in den gemeinschaftlich genutzten Bereichen des Hauses an einer kurzen Leine geführt werden. Bitte achten Sie außerdem darauf, dass andere Bewohnerinnen und Bewohner nicht behindert oder erschreckt werden.")],
"teil1_04.mp3":[("de-DE-AmalaNeural","Am kommenden Samstag bietet die Hausverwaltung eine kostenlose Beratung für Mieterinnen und Mieter mit Haustieren an. Die Veranstaltung beginnt um elf Uhr im Gemeinschaftsraum im Erdgeschoss. Eine Anmeldung ist bis Mittwochmittag erforderlich.")],
"teil1_05.mp3":[("de-DE-KatjaNeural","Die Nachbarschaftsinitiative Tier und Mensch unterstützt Bewohner bei Fragen zur verantwortungsvollen Tierhaltung. Sie vermittelt nicht nur Hunde, sondern informiert auch über Katzen, Kleintiere und ältere Tiere. Kontakt ist über das Stadtportal oder telefonisch möglich.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Haustiere gehören für viele Menschen zum Alltag. Gleichzeitig entstehen in Mietwohnungen manchmal Konflikte. Herr Doktor Weber, Sie beraten Wohnungsunternehmen und Mieter. Wie hat sich die Situation entwickelt?"),
("de-DE-ConradNeural","Weber: Das Thema wird häufiger angesprochen, weil viele Menschen auch in einer Mietwohnung mit einem Tier leben möchten. Dabei geht es nicht nur um Hunde und Katzen. Manche halten Kleintiere oder Vögel. Eine pauschale Regelung für alle Tierarten ist deshalb wenig sinnvoll. Die Bedürfnisse und möglichen Auswirkungen unterscheiden sich deutlich."),
("de-DE-KatjaNeural","Moderatorin: Was sollten Mieter beachten, bevor sie ein Tier anschaffen?"),
("de-DE-ConradNeural","Weber: Zunächst sollte man den Mietvertrag prüfen und sich bei Unsicherheiten an die Vermietung wenden. Außerdem muss man ehrlich einschätzen, ob die Wohnung und der eigene Alltag zum Tier passen. Ein großer Hund braucht beispielsweise ausreichend Bewegung. Wer lange arbeitet und kaum Zeit hat, sollte die Entscheidung besonders sorgfältig treffen."),
("de-DE-KatjaNeural","Moderatorin: Welche Rolle spielt die Hausgemeinschaft?"),
("de-DE-ConradNeural","Weber: Eine wichtige. Hausbewohner können gemeinsame Regeln vereinbaren, etwa zur Leinenpflicht, zur Sauberkeit oder zur Nutzung des Gartens. Dabei geht es nicht darum, Tierhalter zu benachteiligen, sondern Konflikte zu vermeiden. Rücksichtnahme muss allerdings von allen Seiten kommen."),
("de-DE-KatjaNeural","Moderatorin: Was ist bei Beschwerden über Lärm sinnvoll?"),
("de-DE-ConradNeural","Weber: Zuerst sollte man die konkrete Situation klären. Vielleicht bellt ein Hund, weil er zu lange allein bleibt. Dann können Training, Beschäftigung oder eine andere Tagesroutine helfen. Eine Kündigung oder die Abgabe des Tieres sollte nicht die erste Reaktion sein. Wichtig ist ein sachliches Gespräch."),
("de-DE-KatjaNeural","Moderatorin: Und wie lautet Ihre grundsätzliche Einschätzung?"),
("de-DE-ConradNeural","Weber: Haustiere in Mietwohnungen können gut funktionieren. Voraussetzung ist, dass die Rechte der anderen Bewohner, die Pflichten der Tierhalter und vor allem das Wohl des Tieres berücksichtigt werden. Klare Absprachen schaffen dafür eine gute Grundlage.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Sollten Haustiere in Mietwohnungen stärker eingeschränkt werden? Herr Berger, Sie vertreten einen Mieterverein. Wie sehen Sie das?"),
("de-DE-ConradNeural","Berger: Ein generelles Verbot halte ich für unangemessen. Viele Tiere verursachen überhaupt keine Probleme. Entscheidend sind die konkreten Umstände. Eine klare Hausordnung hilft, Missverständnisse zu vermeiden. Außerdem sollten Vermieter die jeweilige Tierart und die Wohnsituation prüfen, statt alle Fälle gleich zu behandeln."),
("de-DE-KatjaNeural","Moderatorin: Frau Yilmaz, Sie engagieren sich in einer Nachbarschaftsinitiative. Was ist Ihnen wichtig?"),
("de-DE-AmalaNeural","Yilmaz: Ich finde, dass man auch die Menschen berücksichtigen muss, die Angst vor Hunden haben oder allergisch reagieren. Rücksichtnahme darf keine Einbahnstraße sein. Tierhalter müssen Verantwortung übernehmen, aber Nachbarn sollten ebenfalls offen miteinander sprechen. Oft lassen sich einfache Lösungen finden."),
("de-DE-KatjaNeural","Moderatorin: Herr Berger, welche Pflichten sollten besonders klar geregelt sein?"),
("de-DE-ConradNeural","Berger: Zum Beispiel die Leinenpflicht in bestimmten Bereichen und die Reinigung gemeinsamer Flächen. Solche Regeln sind nachvollziehbar und schützen alle Bewohner. Gleichzeitig sollte man nicht jede Kleinigkeit zum Anlass nehmen, Tierhaltung grundsätzlich infrage zu stellen."),
("de-DE-KatjaNeural","Moderatorin: Frau Yilmaz, was kann Konflikte verhindern?"),
("de-DE-AmalaNeural","Yilmaz: Beratungsangebote und frühzeitige Gespräche. Wenn ein Tier regelmäßig Lärm macht, sollte man zunächst herausfinden, warum. Vielleicht fehlt Bewegung oder es braucht Training. Auch die Bedürfnisse des Tieres müssen ernst genommen werden. Eine Wohnung ist nur dann geeignet, wenn das Tier dort gut leben kann."),
("de-DE-KatjaNeural","Moderatorin: Vielen Dank. Es geht also sowohl um klare Regeln als auch um gegenseitiges Verständnis.")
],
"teil4_01.mp3":[
("de-DE-AmalaNeural","Vortrag: Haustiere in Mietwohnungen – Verantwortung und Zusammenleben. Haustiere können das Leben bereichern. Sie geben vielen Menschen Gesellschaft und fördern soziale Kontakte. Dennoch ist die Haltung in einem Mehrfamilienhaus mit besonderen Anforderungen verbunden. Damit das Zusammenleben gelingt, müssen mehrere Aspekte beachtet werden."),
("de-DE-AmalaNeural","Erstens sollte die Entscheidung für ein Tier gut vorbereitet sein. Interessierte müssen sich über Lebensdauer, Pflege, Kosten und Bewegungsbedarf informieren. Ein Tier darf nicht allein danach ausgewählt werden, ob es in der Wohnung niedlich aussieht. Entscheidend ist, ob seine Bedürfnisse langfristig erfüllt werden können."),
("de-DE-AmalaNeural","Zweitens spielt die Wohnsituation eine Rolle. Die Größe der Wohnung ist nicht das einzige Kriterium. Wichtig sind auch die Umgebung, sichere Rückzugsmöglichkeiten und der Zugang zu Bewegung. Bei Hunden muss beispielsweise geklärt sein, ob ausreichend Zeit für Spaziergänge vorhanden ist."),
("de-DE-AmalaNeural","Drittens sollten Mieter den Mietvertrag und mögliche Vereinbarungen beachten. Schriftliche Absprachen können nachvollziehbar machen, was vereinbart wurde. Sie ersetzen jedoch nicht die geltenden gesetzlichen Regeln. Bei Unsicherheit ist es sinnvoll, fachkundige Beratung einzuholen, bevor ein Tier angeschafft wird."),
("de-DE-AmalaNeural","Ein weiterer Punkt betrifft die Nachbarschaft. Lärm, Verschmutzung oder freilaufende Tiere können zu Spannungen führen. Tierhalter sollten deshalb auf Sauberkeit achten, Tiere in gemeinschaftlichen Bereichen angemessen sichern und auf Ruhezeiten Rücksicht nehmen. Training, Beschäftigung und eine feste Tagesroutine helfen, störendes Verhalten zu reduzieren."),
("de-DE-AmalaNeural","Wenn dennoch ein Konflikt entsteht, ist ein frühzeitiges Gespräch meist hilfreicher als gegenseitige Vorwürfe. Die Beteiligten sollten konkrete Situationen beschreiben und gemeinsam nach Lösungen suchen. Hausverwaltungen können vermitteln oder Beratungsangebote empfehlen. Pauschale Forderungen führen dagegen selten zu einer dauerhaften Verbesserung."),
("de-DE-AmalaNeural","Nicht zuletzt muss das Tierwohl im Mittelpunkt stehen. Ein Tier, das dauerhaft zu wenig Bewegung, Aufmerksamkeit oder Platz erhält, leidet. Die Verantwortung endet nicht mit der Zustimmung des Vermieters. Sie begleitet die Halter während des gesamten Lebens des Tieres."),
("de-DE-AmalaNeural","Zusammenfassend lässt sich sagen: Haustiere und Mietwohnungen schließen einander nicht aus. Ein friedliches Zusammenleben ist möglich, wenn die Haltung gut vorbereitet wird, klare Absprachen gelten und alle Beteiligten Verantwortung sowie gegenseitige Rücksichtnahme zeigen.")
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
