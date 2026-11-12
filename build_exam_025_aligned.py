import asyncio, subprocess, zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output"); AUDIO=ROOT/"audio"; AUDIO.mkdir(parents=True,exist_ok=True)
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Mitteilung der Stadt: Die dekorative Beleuchtung am Rathaus wird ab kommender Woche zwischen zweiundzwanzig Uhr und sechs Uhr ausgeschaltet. Die Eingänge bleiben aus Sicherheitsgründen beleuchtet. Die Maßnahme ist zunächst für drei Monate vorgesehen.")],
"teil1_02.mp3":[("de-DE-ConradNeural","Einladung des Planetariums: Am Freitag findet ein kostenfreier Rundgang zur Beobachtung des Sternenhimmels statt. Treffpunkt ist um einundzwanzig Uhr am Haupteingang. Bitte bringen Sie eine Taschenlampe mit rotem Licht mit, damit andere Beobachtende nicht gestört werden.")],
"teil1_03.mp3":[("de-DE-AmalaNeural","Die Stadt testet in der Lindenstraße neue Straßenlampen. Diese reduzieren ihre Helligkeit in ruhigen Stunden und werden heller, sobald Fußgängerinnen oder Radfahrer erkannt werden. Anwohner können ihre Erfahrungen bis Ende August online mitteilen.")],
"teil1_04.mp3":[("de-DE-KatjaNeural","Das Umweltzentrum veranstaltet am kommenden Donnerstag einen Vortrag über künstliches Licht und seine Folgen für Insekten. Die Veranstaltung beginnt um neunzehn Uhr. Eine Anmeldung ist per E-Mail erforderlich; die Teilnahme ist kostenlos.")],
"teil1_05.mp3":[("de-DE-ConradNeural","Die Gemeinde bittet um Vorschläge für eine umweltfreundlichere Straßenbeleuchtung. Beiträge können bis zum zwanzigsten Juni über das Beteiligungsportal eingereicht werden. Die Ergebnisse der Befragung werden im Juli im Stadtrat vorgestellt.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Künstliches Licht gehört selbstverständlich zu unserem Alltag. Wann wird Beleuchtung zum Umweltproblem?"),
("de-DE-AmalaNeural","Expertin: Von Lichtverschmutzung sprechen wir, wenn Licht unnötig stark, zur falschen Zeit oder in die falsche Richtung eingesetzt wird. Es geht nicht darum, jede Lampe abzuschaffen, sondern Beleuchtung sinnvoll zu planen."),
("de-DE-KatjaNeural","Moderatorin: Welche Auswirkungen beobachten Sie in der Natur?"),
("de-DE-AmalaNeural","Expertin: Zugvögel können durch helle Gebäude die Orientierung verlieren. Nachtaktive Insekten werden von Lampen angezogen und erschöpfen sich. Auch Pflanzen reagieren auf künstliche Helligkeit, weil sich ihre natürlichen Ruhephasen verändern können."),
("de-DE-KatjaNeural","Moderatorin: Sollte man Straßen nachts also dunkel lassen?"),
("de-DE-AmalaNeural","Expertin: Eine pauschale Abschaltung wäre nicht sinnvoll. Menschen müssen sich sicher bewegen können. Wir sollten prüfen, wo Licht gebraucht wird und welche Helligkeit ausreicht. Bewegungsmelder sind in manchen Bereichen eine gute Lösung."),
("de-DE-KatjaNeural","Moderatorin: Welche Eigenschaften sollte eine geeignete Lampe haben?"),
("de-DE-AmalaNeural","Expertin: Empfehlenswert sind warmweiße Leuchten, die ihr Licht gezielt nach unten richten. Blauhaltiges, sehr helles Licht kann stärker in natürliche Rhythmen eingreifen. Außerdem sollte die Beleuchtung in den späten Nachtstunden reduziert werden."),
("de-DE-KatjaNeural","Moderatorin: Was können Geschäfte und Unternehmen tun?"),
("de-DE-AmalaNeural","Expertin: Werbeanlagen müssen nicht die ganze Nacht leuchten. Unternehmen können Schaufensterbeleuchtung dimmen und Strahler abschalten, sobald niemand mehr vor Ort arbeitet. Das spart Energie und schützt die Umgebung."),
("de-DE-KatjaNeural","Moderatorin: Welche Aufgabe haben die Kommunen?"),
("de-DE-AmalaNeural","Expertin: Sie sollten ein Beleuchtungskonzept entwickeln, Daten auswerten und die Bevölkerung beteiligen. Pilotprojekte helfen, verschiedene Lösungen zu testen und anschließend zu prüfen, ob Sicherheit und Umweltschutz gleichermaßen gewährleistet sind.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Wie kann eine Stadt nachts sicher und zugleich umweltfreundlich beleuchtet werden? Frau Keller arbeitet in der kommunalen Umweltplanung, Herr Brandt vertritt einen Einzelhandelsverband. Frau Keller, beginnen Sie bitte."),
("de-DE-AmalaNeural","Keller: Wir sollten Sicherheit und Naturschutz gemeinsam planen. In einem Pilotgebiet haben wir bewegungsgesteuerte Lampen eingesetzt. Die Rückmeldungen waren positiv, weil Wege bei Bedarf hell genug waren und ansonsten weniger Licht abgegeben wurde."),
("de-DE-ConradNeural","Brandt: Für Geschäfte sind klare Regeln wichtig. Besonders beleuchtete Werbeschilder sollten nicht unbegrenzt leuchten. Allerdings müssen Betriebe wissen, welche Vorgaben gelten, damit sie ihre Anlagen rechtzeitig anpassen können."),
("de-DE-AmalaNeural","Keller: Eine vollständige Abschaltung ist nicht überall möglich. Wir müssen die Situation vor Ort berücksichtigen. Wichtig ist außerdem, Anwohner frühzeitig einzubeziehen, denn sie kennen dunkle Ecken und konkrete Probleme oft sehr genau."),
("de-DE-ConradNeural","Brandt: Auch ich halte Beteiligung für sinnvoll. Trotzdem darf man die Bedürfnisse der Kundschaft und Beschäftigten nicht übersehen. In bestimmten Straßen wäre eine vollständige Abschaltung nicht praktikabel. Einheitliche Regeln für Werbeanlagen könnten dagegen helfen."),
("de-DE-AmalaNeural","Keller: Deshalb schlage ich Pilotprojekte vor. So können wir unterschiedliche Systeme testen, Messungen durchführen und Erfahrungen sammeln. Erst danach sollte eine Stadt entscheiden, welche Lösung dauerhaft geeignet ist."),
("de-DE-KatjaNeural","Moderatorin: Vielen Dank. Sie sind sich einig, dass örtliche Bedingungen und die Beteiligung der Bevölkerung wichtig sind, setzen aber unterschiedliche Schwerpunkte.")
],
"teil4_01.mp3":[
("de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um Lichtverschmutzung und die Frage, wie Städte ihre Straßen und öffentlichen Plätze verantwortungsvoll beleuchten können. Künstliches Licht ermöglicht Mobilität und Orientierung nach Sonnenuntergang. Gleichzeitig kann unnötige Beleuchtung Umwelt und Gesundheit beeinträchtigen. Ziel moderner Planung ist deshalb nicht, möglichst viel Licht bereitzustellen, sondern Licht dort und dann einzusetzen, wo es gebraucht wird."),
("de-DE-ConradNeural","Zunächst zu den Auswirkungen auf Tiere und Pflanzen. Viele Insekten orientieren sich an natürlichen Lichtquellen. Künstliche Lampen können sie anziehen und von Nahrungssuche oder Fortpflanzung abhalten. Zugvögel können durch beleuchtete Gebäude irritiert werden. Auch Pflanzen reagieren auf veränderte Lichtverhältnisse: Ihre Wachstums- und Ruhephasen können sich verschieben."),
("de-DE-ConradNeural","Ein wichtiger Faktor ist die Lichtfarbe. Besonders starkes, blauhaltiges Licht kann biologische Rhythmen beeinflussen. Für viele öffentliche Bereiche sind warmweiße Leuchten besser geeignet. Ebenso entscheidend ist die Ausrichtung: Lampen sollten ihr Licht gezielt nach unten abgeben, statt Fassaden oder den Himmel anzustrahlen."),
("de-DE-ConradNeural","Neben der Technik spielt die Steuerung eine große Rolle. Bewegungsmelder und zeitabhängige Systeme können die Helligkeit an die tatsächliche Nutzung anpassen. In Wohnstraßen muss nicht jede Lampe während der gesamten Nacht mit voller Leistung leuchten. Sicherheitsanforderungen und barrierefreie Wege müssen dennoch berücksichtigt werden."),
("de-DE-ConradNeural","Kommunen sollten außerdem die Bürgerinnen und Bürger beteiligen. Bewohner können auf problematische Stellen hinweisen und erklären, wo sie sich unsicher fühlen. Solche Rückmeldungen ersetzen keine technischen Messungen, ergänzen sie aber um Alltagserfahrungen. Pilotprojekte helfen, Lösungen unter realen Bedingungen zu vergleichen."),
("de-DE-ConradNeural","Schließlich ist eine regelmäßige Auswertung notwendig. Städte sollten Energieverbrauch, Beleuchtungsstärke und mögliche Auswirkungen auf die Umgebung überprüfen. Nur so lässt sich feststellen, ob eine Maßnahme wirkt oder unbeabsichtigte Nachteile verursacht."),
("de-DE-ConradNeural","Zusammenfassend lässt sich sagen: Umweltfreundliche Beleuchtung bedeutet weder völlige Dunkelheit noch maximale Helligkeit. Entscheidend sind eine passende Lichtfarbe, eine gezielte Ausrichtung und eine bedarfsgerechte Steuerung. Wenn Kommunen Fachwissen und Erfahrungen der Bevölkerung verbinden, können sie Sicherheit und Naturschutz besser vereinbaren. Vielen Dank für Ihre Aufmerksamkeit.")
]
}
async def make(voice,text,path):
    await edge_tts.Communicate(text,voice).save(str(path))
async def main():
    for filename,segments in tracks.items():
        parts=[]
        for i,(voice,text) in enumerate(segments):
            part=AUDIO/f"{filename[:-4]}_{i:02d}.mp3"
            await make(voice,text,part); parts.append(part)
        if len(parts)==1:
            parts[0].replace(AUDIO/filename)
        else:
            manifest=ROOT/f"{filename[:-4]}_concat.txt"
            manifest.write_text("".join(f"file '{p.resolve()}'\n" for p in parts),encoding="utf-8")
            subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(manifest),"-c","copy",str(AUDIO/filename)],check=True)
            for p in parts: p.unlink()
            manifest.unlink()
    out=ROOT/"exam-025.zip"
    with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(AUDIO.glob("*.mp3")): z.write(p,p.name)
    expected={f"teil1_0{i}.mp3" for i in range(1,6)}|{"teil2_01.mp3","teil3_01.mp3","teil4_01.mp3"}
    with zipfile.ZipFile(out) as z:
        actual={n for n in z.namelist() if n.endswith(".mp3")}
        assert actual==expected,(actual,expected)
        assert all(z.getinfo(n).file_size>10000 for n in expected)
    print(f"Created {out} ({out.stat().st_size} bytes), {len(expected)} tracks")
if __name__=="__main__": asyncio.run(main())
