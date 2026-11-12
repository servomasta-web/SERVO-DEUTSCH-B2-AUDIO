import asyncio, subprocess, zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output"); AUDIO=ROOT/"audio"; AUDIO.mkdir(parents=True,exist_ok=True)
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Das Stadtteilzentrum lädt zum Nachbarschaftsfrühstück ein. Es findet jeden ersten Sonntag im Monat um zehn Uhr statt. Alle Bewohnerinnen und Bewohner sind willkommen. Eine Anmeldung ist nicht erforderlich.")],
"teil1_02.mp3":[("de-DE-ConradNeural","Sie sind neu in unserem Viertel und möchten Menschen kennenlernen? Schreiben Sie uns eine kurze Nachricht und werfen Sie sie in den Briefkasten des Stadtteilzentrums. Wir melden uns und informieren Sie über die nächsten Treffen.")],
"teil1_03.mp3":[("de-DE-AmalaNeural","Die Nachbarschaftsinitiative organisiert Unterstützung für ältere Menschen. Wer Hilfe beim Einkaufen benötigt, kann seinen Bedarf bis Dienstag in eine wöchentliche Liste eintragen. Freiwillige melden sich anschließend direkt bei den betreffenden Personen.")],
"teil1_04.mp3":[("de-DE-KatjaNeural","Im Nachbarschaftshaus gibt es jetzt einen öffentlichen Tauschschrank. Während der Öffnungszeiten können gut erhaltene Bücher, Geschirr und kleine Haushaltsgegenstände abgegeben oder kostenlos mitgenommen werden. Bitte legen Sie keine beschädigten Gegenstände hinein.")],
"teil1_05.mp3":[("de-DE-ConradNeural","Der Nachbarschaftsgarten sucht weitere freiwillige Helferinnen und Helfer. Die Gartengruppe trifft sich jeden Mittwoch um siebzehn Uhr. Auch Menschen ohne Gartenerfahrung können mitmachen. Werkzeuge werden vor Ort zur Verfügung gestellt.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: In vielen Städten wohnen Menschen jahrelang Tür an Tür, ohne sich zu kennen. Warum sind Nachbarschaftskontakte so schwach?"),
("de-DE-AmalaNeural","Sozialforscherin: Viele Menschen haben wenig Zeit, und häufige Wohnungswechsel erschweren langfristige Beziehungen. Schon kurze Gespräche im Treppenhaus können jedoch Vertrauen schaffen. Wer sich kennt, fragt eher nach, ob jemand beim Einkaufen oder beim Blumengießen Hilfe braucht. Solche kleinen Gesten können Isolation verringern, ersetzen aber keine professionellen sozialen Dienste."),
("de-DE-KatjaNeural","Moderatorin: Wie erreicht man Menschen mit unterschiedlichen Lebensgeschichten?"),
("de-DE-AmalaNeural","Sozialforscherin: Angebote sollten offen und niedrigschwellig sein. Ein gemeinsames Frühstück, ein Tauschschrank oder ein Gartenprojekt sind gute Anlässe. Niemand sollte das Gefühl bekommen, erst bestimmte Voraussetzungen erfüllen zu müssen."),
("de-DE-KatjaNeural","Moderatorin: Welche Herausforderungen gibt es für Freiwillige?"),
("de-DE-AmalaNeural","Sozialforscherin: Oft tragen wenige Engagierte zu viele Aufgaben. Das führt langfristig zu Überlastung. Deshalb müssen Verantwortlichkeiten klar verteilt werden. Man sollte klein anfangen und Aufgaben anbieten, die zeitlich überschaubar sind."),
("de-DE-KatjaNeural","Moderatorin: Können digitale Gruppen helfen?"),
("de-DE-AmalaNeural","Sozialforscherin: Ja, sie sind praktisch für kurzfristige Absprachen. Allerdings ersetzen Nachrichten keine persönlichen Begegnungen. Gruppenregeln sind wichtig, damit private Daten geschützt werden und Diskussionen respektvoll bleiben."),
("de-DE-KatjaNeural","Moderatorin: Ihr wichtigster Rat für eine neue Initiative?"),
("de-DE-AmalaNeural","Sozialforscherin: Beginnen Sie mit einem konkreten Angebot, das im Viertel gebraucht wird. Eine kleine, verlässliche Initiative ist oft wirksamer als ein großes Konzept, das niemand umsetzt.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Wie gelingt gute Nachbarschaft? Dazu sprechen Frau Berger, die eine Initiative leitet, und Herr Yilmaz, der ein digitales Nachbarschaftsnetz betreut."),
("de-DE-AmalaNeural","Berger: Für mich stehen persönliche Begegnungen im Mittelpunkt. Beim gemeinsamen Kochen oder bei einem Straßenfest entstehen Gespräche ganz natürlich. Wir möchten besonders neu zugezogene Menschen erreichen. Allerdings haben wir manchmal Schwierigkeiten, genügend Freiwillige zu finden."),
("de-DE-ConradNeural","Yilmaz: Digitale Angebote sind eine hilfreiche Ergänzung. Über unsere Gruppe können Bewohner schnell fragen, ob jemand ein Paket annehmen oder ein Werkzeug ausleihen kann. Aufgaben müssen aber klar beschrieben und zeitlich begrenzt werden, damit Absprachen verlässlich bleiben."),
("de-DE-AmalaNeural","Berger: Ein persönliches Willkommen und eine Einladung zu einer konkreten Aktivität sind oft wirksamer als ein allgemeiner Aushang. Neue Bewohner sollen nicht nur Informationen erhalten, sondern wirklich mitgestalten können."),
("de-DE-ConradNeural","Yilmaz: Gleichzeitig dürfen wir nicht erwarten, dass Ehrenamtliche jede Aufgabe übernehmen. Bei Pflege, medizinischen Fragen oder schwierigen sozialen Problemen braucht es professionelle Unterstützung. Unsere Gruppe kann Kontakte vermitteln, aber keine Fachkräfte ersetzen."),
("de-DE-KatjaNeural","Moderatorin: Vielen Dank. Persönliche Begegnungen und digitale Hilfen können also zusammenwirken, wenn Aufgaben und Grenzen klar sind.")
],
"teil4_01.mp3":[
("de-DE-ConradNeural","Guten Tag. Heute geht es um die Frage, wie Nachbarschaften zu Orten werden können, an denen Menschen sich zugehörig fühlen und sich gegenseitig unterstützen. In vielen Wohngebieten kennen sich die Bewohner kaum. Stabile Kontakte im Wohnumfeld können Isolation verringern und das Sicherheitsgefühl stärken."),
("de-DE-ConradNeural","Nachbarschaft bedeutet nicht, dass alle Menschen enge Freundschaften schließen müssen. Schon ein freundlicher Gruß, ein kurzes Gespräch oder eine kleine Hilfeleistung kann Vertrauen entstehen lassen. Solche Kontakte bilden eine Grundlage, auf der bei Bedarf Unterstützung möglich wird."),
("de-DE-ConradNeural","Damit Menschen teilnehmen, müssen Angebote leicht zugänglich sein. Ein gemeinsames Frühstück, ein Tauschregal oder ein Gartenprojekt bieten einen konkreten Anlass, ohne eine langfristige Verpflichtung vorauszusetzen. Menschen unterschiedlichen Alters und unterschiedlicher Herkunft sollten willkommen sein. Ihre Erfahrungen und Fähigkeiten können sich ergänzen."),
("de-DE-ConradNeural","Wo viele Menschen zusammenkommen, können Konflikte entstehen. Unterschiedliche Vorstellungen über Lärm, Sauberkeit oder die Nutzung gemeinsamer Flächen sind nicht ungewöhnlich. Entscheidend ist, Probleme frühzeitig und respektvoll anzusprechen. Klare Gesprächsregeln und transparente Entscheidungen helfen, Missverständnisse zu vermeiden."),
("de-DE-ConradNeural","Eine weitere Herausforderung ist die Verteilung ehrenamtlicher Aufgaben. Wenn immer dieselben Personen organisieren und aufräumen, droht Überlastung. Aufgaben sollten deshalb überschaubar sein und regelmäßig wechseln. Die Grenzen freiwilliger Hilfe müssen deutlich bleiben: Professionelle Pflege und Beratung können Nachbarschaftsprojekte nicht ersetzen."),
("de-DE-ConradNeural","Kommunen können gute Rahmenbedingungen schaffen. Sie können Räume bereitstellen, Initiativen beraten und Kontakte zwischen Vereinen, sozialen Einrichtungen und Bewohnern vermitteln. Erfolgreiche Projekte brauchen jedoch Spielraum, damit Menschen vor Ort eigene Ideen entwickeln können."),
("de-DE-ConradNeural","Zusammenfassend lässt sich sagen: Eine lebendige Nachbarschaft entsteht weder von allein noch durch digitale Kommunikation allein. Sie braucht persönliche Begegnungen, verlässliche Absprachen, eine faire Aufgabenverteilung und unterstützende Strukturen. Wenn Bewohner und Kommunen gemeinsam Verantwortung übernehmen, kann aus einem Wohnort ein echtes soziales Umfeld werden. Vielen Dank für Ihre Aufmerksamkeit.")
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
        if len(pieces)==1:
            pieces[0].replace(target)
        else:
            manifest=ROOT/f"{filename[:-4]}_concat.txt"
            manifest.write_text("".join("file '"+str(p.resolve())+"'\n" for p in pieces),encoding="utf-8")
            subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(manifest),"-c","copy",str(target)],check=True)
            for p in pieces:p.unlink()
            manifest.unlink()
    archive=ROOT/"exam-027.zip"
    with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(AUDIO.glob("*.mp3")): z.write(p,p.name)
    expected={f"teil1_0{i}.mp3" for i in range(1,6)}|{"teil2_01.mp3","teil3_01.mp3","teil4_01.mp3"}
    with zipfile.ZipFile(archive) as z:
        actual={n for n in z.namelist() if n.endswith(".mp3")}
        assert actual==expected,(actual,expected)
        assert all(z.getinfo(n).file_size>10000 for n in expected)
    print(f"Created {archive} ({archive.stat().st_size} bytes), 8 validated tracks")
if __name__=="__main__": asyncio.run(main())
