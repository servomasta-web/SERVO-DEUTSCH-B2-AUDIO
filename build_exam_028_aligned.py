import asyncio, subprocess, zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output"); AUDIO=ROOT/"audio"; AUDIO.mkdir(parents=True,exist_ok=True)
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Das Grünflächenamt bietet am Samstag eine Führung zu klimaangepassten Stadtbäumen an. Treffpunkt ist um elf Uhr am Brunnen im Stadtpark. Die Teilnahme ist kostenlos. Eine Anmeldung ist möglich, aber nicht zwingend erforderlich.")],
"teil1_02.mp3":[("de-DE-ConradNeural","Bei der nächsten Pflanzaktion werden junge Bäume entlang des neuen Radwegs eingesetzt. Freiwillige sind auch ohne Erfahrung willkommen. Bitte bringen Sie, wenn möglich, eigene Arbeitshandschuhe mit. Werkzeuge und Pflanzen stellt die Stadt bereit.")],
"teil1_03.mp3":[("de-DE-AmalaNeural","Hausgemeinschaften können beim Umweltbüro eine Regentonne beantragen, sofern eine geeignete Dachfläche und ein sicherer Aufstellort vorhanden sind. Das Angebot richtet sich an Eigentümer und gemeinsam organisierte Hausgemeinschaften.")],
"teil1_04.mp3":[("de-DE-KatjaNeural","Wer eine beschädigte Baumscheibe oder einen kranken Straßenbaum entdeckt, kann dies über das Online-Formular des Grünflächenamtes melden. Wichtig sind die genaue Lage und möglichst ein Foto.")],
"teil1_05.mp3":[("de-DE-ConradNeural","Die Stadt sucht Schulen, die sich an einem Projekt für mehr Schatten auf Schulhöfen beteiligen möchten. Interessierte Einrichtungen können sich bis zum dreißigsten September beim Klimaschutzbüro melden.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Stadtbäume gelten als wichtige Hilfe gegen sommerliche Hitze. Trotzdem leiden viele von ihnen unter dem Klimawandel. Woran liegt das?"),
("de-DE-AmalaNeural","Ein wesentlicher Grund sind versiegelte Flächen. Asphalt und Beton speichern Wärme, während Regenwasser oft schnell abfließt. Dadurch trocknen Böden aus. Bäume brauchen jedoch Wasser und Platz für ihre Wurzeln."),
("de-DE-KatjaNeural","Sollte man deshalb einfach möglichst viele Bäume pflanzen?"),
("de-DE-AmalaNeural","Mehr Bäume sind wichtig, aber die Auswahl muss zum Standort passen. Wir brauchen Arten, die mit höheren Temperaturen und längeren Trockenperioden zurechtkommen. Vielfalt ist ebenfalls entscheidend: Ein gemischter Bestand ist weniger gefährdet, wenn eine Krankheit auftritt."),
("de-DE-KatjaNeural","Wie lässt sich die Bewässerung verbessern?"),
("de-DE-AmalaNeural","Regenwasser sollte stärker genutzt und gespeichert werden. Außerdem muss man gezielt gießen. Eine Bodenabdeckung kann helfen, Feuchtigkeit länger zu halten. Bei Bauprojekten muss die Wasserplanung von Anfang an berücksichtigt werden."),
("de-DE-KatjaNeural","Welche Aufgaben können Bürgerinnen und Bürger übernehmen?"),
("de-DE-AmalaNeural","Viele Städte ermöglichen Baumpatenschaften. Anwohner können junge Bäume nach Absprache gießen und Schäden melden. Das ist eine wertvolle Ergänzung. Fachliche Kontrollen und notwendige Pflegearbeiten bleiben aber Aufgabe ausgebildeter Beschäftigter."),
("de-DE-KatjaNeural","Was muss sich in der Stadtplanung ändern?"),
("de-DE-AmalaNeural","Bäume dürfen nicht erst am Ende eines Bauprojekts eingeplant werden. Sie brauchen Wurzelraum, geeignete Böden und Schutz vor Baustellenverkehr. Straßenbau, Leitungsplanung und Grünflächenpflege müssen früh zusammenarbeiten.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Wie können Städte ihre Bäume besser vor Hitze schützen? Darüber sprechen Frau Neumann von einer Bürgerinitiative und Herr Krüger, ein Stadtplaner."),
("de-DE-AmalaNeural","Neumann: In unserem Viertel haben wir ein Gießprojekt gestartet. Freiwillige übernehmen Patenschaften für junge Bäume und tragen ihre Einsätze in einen Kalender ein. Das funktioniert gut. Wir möchten außerdem Schulen stärker in Pflanzaktionen einbeziehen."),
("de-DE-ConradNeural","Krüger: Bürgerengagement ist hilfreich, aber bei Neubauten müssen wir vor allem den Wurzelraum sichern. Unter Straßen liegen zahlreiche Leitungen. Deshalb müssen Versorgungsbetriebe und Grünflächenamt früh miteinander sprechen."),
("de-DE-AmalaNeural","Neumann: Wir wünschen uns mehr Informationen. Wenn Anwohner wissen, welche Bäume besonders viel Wasser benötigen oder bereits geschädigt sind, können sie gezielter helfen. Eine verständliche Übersicht wäre nützlich."),
("de-DE-ConradNeural","Krüger: Eine solche Übersicht ist sinnvoll. Wir erfassen zunehmend den Zustand der Bäume. Allerdings kann freiwillige Hilfe fachliche Pflege nicht ersetzen. Bei Krankheiten oder Standsicherheitsproblemen sind Fachleute gefragt."),
("de-DE-KatjaNeural","Vielen Dank. Gute Baumpflege braucht Beteiligung, vorausschauende Planung und fachliche Verantwortung.")
],
"teil4_01.mp3":[
("de-DE-ConradNeural","Guten Tag. Heute spreche ich über die Bedeutung von Stadtbäumen in Zeiten des Klimawandels. Hitzewellen werden in vielen Städten häufiger. Besonders betroffen sind dicht bebaute Viertel mit wenig Grün. Bäume spenden Schatten und kühlen ihre Umgebung durch Verdunstung."),
("de-DE-ConradNeural","Diese Wirkung entsteht jedoch nicht automatisch. Ein Baum braucht einen geeigneten Standort. Besonders wichtig ist ausreichend durchwurzelbarer Boden. Die Wurzeln müssen Wasser aufnehmen und sich entwickeln können. Kleine Baumscheiben zwischen Betonflächen reichen dafür oft nicht aus."),
("de-DE-ConradNeural","Bei der Auswahl neuer Arten sollten Kommunen auch langfristige Klimaprognosen beachten. Manche traditionelle Baumarten reagieren empfindlich auf Trockenheit oder Schädlinge. Eine größere Vielfalt kann das Risiko verringern, dass ein großer Teil des Bestandes gleichzeitig geschädigt wird."),
("de-DE-ConradNeural","Auch die Pflege muss sich verändern. In trockenen Perioden brauchen junge Bäume eine abgestimmte Bewässerung. Regenwasser sollte möglichst vor Ort gespeichert werden. Eine geeignete Bodenabdeckung kann die Verdunstung reduzieren. Wasser muss sparsam eingesetzt werden."),
("de-DE-ConradNeural","Stadtbäume konkurrieren im Untergrund manchmal mit Strom-, Wasser- und Datenleitungen. Deshalb müssen Grünflächenamt, Straßenbau und Versorgungsunternehmen eng zusammenarbeiten. Werden Bäume erst nach der technischen Planung berücksichtigt, fehlt ihnen häufig der notwendige Platz."),
("de-DE-ConradNeural","Die Bevölkerung kann ebenfalls beitragen. Baumpatenschaften, Pflanzaktionen und Meldungen über Schäden stärken die Verbindung zwischen Bewohnern und öffentlichem Grün. Schulen können solche Projekte mit Unterricht verbinden. Die fachliche Kontrolle bleibt dennoch unverzichtbar."),
("de-DE-ConradNeural","Zusammenfassend lässt sich sagen: Stadtbäume sind eine wirksame, aber keine allein ausreichende Antwort auf zunehmende Hitze. Sie benötigen passende Standorte, vielfältige Arten, Wasser und langfristige Pflege. Wenn Verwaltung, Fachleute und Bevölkerung gemeinsam handeln, können Städte widerstandsfähiger und lebenswerter werden. Vielen Dank für Ihre Aufmerksamkeit.")
]}
async def synthesize(voice,text,path):
    await edge_tts.Communicate(text,voice).save(str(path))
async def main():
    for filename,segments in tracks.items():
        pieces=[]
        for i,(voice,text) in enumerate(segments):
            p=AUDIO/f"{filename[:-4]}_{i:02d}.mp3"
            await synthesize(voice,text,p); pieces.append(p)
        target=AUDIO/filename
        if len(pieces)==1: pieces[0].replace(target)
        else:
            manifest=ROOT/f"{filename[:-4]}_concat.txt"
            manifest.write_text("".join("file '"+str(p.resolve())+"'\n" for p in pieces),encoding="utf-8")
            subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(manifest),"-c","copy",str(target)],check=True)
            for p in pieces:p.unlink()
            manifest.unlink()
    archive=ROOT/"exam-028.zip"
    with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(AUDIO.glob("*.mp3")): z.write(p,p.name)
    expected={f"teil1_0{i}.mp3" for i in range(1,6)}|{"teil2_01.mp3","teil3_01.mp3","teil4_01.mp3"}
    with zipfile.ZipFile(archive) as z:
        actual={n for n in z.namelist() if n.endswith(".mp3")}
        assert actual==expected,(actual,expected)
        assert all(z.getinfo(n).file_size>10000 for n in expected)
    print(f"Created {archive} ({archive.stat().st_size} bytes), 8 validated tracks")
if __name__=="__main__": asyncio.run(main())
