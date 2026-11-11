import asyncio
import subprocess
import zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output")
AUDIO=ROOT/"audio"
AUDIO.mkdir(parents=True,exist_ok=True)

# Prüfung 007 — Tourismus und Umweltschutz.
# Inhaltlich an GoetheExam07Audio.java ausgerichtet.
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Ansage im Naturpark: Der Rundweg am Wasserfall bleibt am kommenden Dienstag wegen Pflegearbeiten geschlossen. Besucherinnen und Besucher können stattdessen den markierten Höhenweg nutzen. Bitte bleiben Sie auf den Wegen, da sich seltene Pflanzen am Hang befinden.")],
"teil1_02.mp3":[("de-DE-KatjaNeural","Wir wollten doch am Wochenende in die Altstadt fahren."),("de-DE-ConradNeural","Ja, aber ich habe gelesen, dass dort ein autofreier Tag stattfindet."),("de-DE-KatjaNeural","Dann nehmen wir den Regionalzug und leihen uns vor Ort Fahrräder."),("de-DE-ConradNeural","Gute Idee, so müssen wir auch keinen Parkplatz suchen.")],
"teil1_03.mp3":[("de-DE-KatjaNeural","Mitteilung eines Gästehauses: Ab Juli wird das Frühstück überwiegend mit Produkten aus der Umgebung angeboten. Gäste, die auf eine bestimmte Ernährungsweise achten müssen, werden gebeten, dies bereits bei der Buchung anzugeben. Ein Aufpreis für das regionale Angebot wird nicht erhoben.")],
"teil1_04.mp3":[("de-DE-AmalaNeural","Ich arbeite als Stadtführerin und merke, dass viele Besucher inzwischen nach umweltfreundlichen Angeboten fragen. Besonders beliebt sind Spaziergänge in kleinen Gruppen. Dabei kann ich auch Orte zeigen, die in den üblichen Reiseführern kaum erwähnt werden.")],
"teil1_05.mp3":[("de-DE-KatjaNeural","Durchsage am Strand: Bitte benutzen Sie für Glasflaschen und Verpackungen die getrennten Sammelbehälter neben dem Haupteingang. Die Abfallstation direkt am Strand ist heute außer Betrieb. Das Verbot, in den Dünen zu grillen, gilt weiterhin.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderator: Viele Urlaubsregionen leiden unter starkem Besucherandrang. Herr Berger, Sie beraten Gemeinden im Bereich nachhaltiger Tourismus. Was bedeutet nachhaltiger Tourismus konkret?"),
("de-DE-AmalaNeural","Berger: Es geht darum, wirtschaftliche Interessen, die Lebensqualität der Bevölkerung und den Schutz der Natur miteinander zu verbinden. Reisen lässt sich nicht völlig ohne Auswirkungen organisieren. Man kann aber versuchen, Belastungen zu verringern und einen größeren Teil der Einnahmen in der Region zu halten."),
("de-DE-KatjaNeural","Moderator: Welche Maßnahmen sind besonders wirksam?"),
("de-DE-AmalaNeural","Berger: Ein gutes Verkehrskonzept ist entscheidend. Wenn Gäste mit Bus und Bahn anreisen können und vor Ort verlässliche Verbindungen haben, wird das Auto weniger notwendig. Ebenso wichtig sind Besucherlenkung und Informationen: empfindliche Gebiete sollten nicht unbegrenzt zugänglich sein."),
("de-DE-KatjaNeural","Moderator: Manche Unternehmen befürchten, solche Regeln würden Gäste abschrecken."),
("de-DE-AmalaNeural","Berger: Kurzfristig kann eine Begrenzung einzelner Angebote Einnahmen kosten. Langfristig schützt sie jedoch die Grundlage des Tourismus. Wenn Wege erodieren oder Wasser knapp wird, verliert ein Ort gerade das, weswegen Menschen ihn besuchen."),
("de-DE-KatjaNeural","Moderator: Welche Rolle spielen die Einwohner?"),
("de-DE-AmalaNeural","Berger: Eine zentrale. Entscheidungen dürfen nicht nur von Reiseveranstaltern getroffen werden. Die Bevölkerung kennt die Belastungen im Alltag und sollte an der Planung beteiligt werden. Außerdem müssen Arbeitsplätze fair bezahlt und saisonale Beschäftigte besser abgesichert werden."),
("de-DE-KatjaNeural","Moderator: Können Reisende selbst etwas beitragen?"),
("de-DE-AmalaNeural","Berger: Natürlich. Sie können länger an einem Ort bleiben, lokale Betriebe unterstützen, Wasser und Energie sparsam nutzen und Regeln respektieren. Es geht nicht darum, auf Urlaub zu verzichten, sondern bewusster zu reisen.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderator: In unserer Gesprächsrunde geht es um die Frage, ob beliebte Naturziele die Zahl ihrer Besucher stärker begrenzen sollten. Frau Roth, Sie betreiben einen kleinen Campingplatz."),
("de-DE-AmalaNeural","Roth: Ich verstehe den Schutzgedanken, aber pauschale Obergrenzen halte ich für problematisch. Viele Familienbetriebe leben von der Sommersaison. Besser wäre es, Besucher auf weniger bekannte Orte und unterschiedliche Tageszeiten zu verteilen."),
("de-DE-KatjaNeural","Moderator: Herr Yilmaz, Sie arbeiten bei einem Naturschutzverband."),
("de-DE-ConradNeural","Yilmaz: Eine zeitliche Verteilung reicht nicht immer aus. In manchen Gebieten brüten seltene Vogelarten. Dort müssen bestimmte Wege zeitweise gesperrt werden, auch wenn das für einzelne Betriebe unbequem ist. Die Natur kann sich nicht an unseren Veranstaltungskalender anpassen."),
("de-DE-KatjaNeural","Moderator: Frau Roth, könnten digitale Reservierungen helfen?"),
("de-DE-AmalaNeural","Roth: Ja, wenn sie einfach zu bedienen sind. So könnten Gäste vorab sehen, wann ein Gebiet stark besucht ist. Allerdings dürfen Menschen ohne Smartphone nicht ausgeschlossen werden."),
("de-DE-ConradNeural","Yilmaz: Das ist ein wichtiger Punkt. Zusätzlich brauchen wir verständliche Informationen vor Ort und Kontrollen. Regeln funktionieren nur, wenn sie bekannt sind und tatsächlich eingehalten werden."),
("de-DE-KatjaNeural","Moderator: Offenbar braucht es also sowohl eine faire Planung für Betriebe als auch verbindliche Schutzmaßnahmen.")
],
"teil4_01.mp3":[("de-DE-ConradNeural","Guten Tag. Heute beschäftige ich mich mit den Auswirkungen des Tourismus auf Küstenregionen und damit, wie Gemeinden darauf reagieren können. Der Tourismus schafft Arbeitsplätze und ermöglicht Investitionen in Infrastruktur. Gleichzeitig steigt in der Hauptsaison der Verbrauch von Wasser und Energie. Auch Verkehr, Abfälle und der Bau neuer Unterkünfte können empfindliche Ökosysteme belasten. Besonders deutlich wird das an Küsten. Dünen schützen das Hinterland vor Sturmfluten und bieten spezialisierten Pflanzen und Tieren Lebensraum. Werden sie betreten oder für Parkplätze und Gebäude eingeebnet, geht diese natürliche Schutzfunktion verloren. Deshalb sind markierte Wege, Schutzbereiche und eine konsequente Bauplanung wichtig. Ein zweiter Bereich ist die Wasserversorgung. Hotels, Schwimmbäder und Gärten benötigen in trockenen Monaten große Mengen Wasser. Gerade dann kann es zu Konflikten mit der Landwirtschaft und den Haushalten kommen. Gemeinden können wassersparende Technik fördern, Leckagen schneller beheben und neue Anlagen an klare Verbrauchsregeln binden. Auch die wirtschaftliche Organisation spielt eine Rolle. Wenn Unterkünfte, Restaurants und Ausflugsanbieter in regionaler Hand bleiben, profitieren eher die Menschen vor Ort. Saisonale Arbeitsplätze sollten verlässliche Bedingungen bieten. Eine Region, die ihre natürlichen und sozialen Grundlagen verliert, gefährdet auf Dauer auch ihre wirtschaftliche Zukunft. Nachhaltiger Tourismus bedeutet daher nicht, Besucher grundsätzlich fernzuhalten. Er verlangt eine Planung, die ökologische Grenzen ernst nimmt, die Bevölkerung beteiligt und Gästen nachvollziehbare Möglichkeiten für verantwortungsvolles Verhalten bietet.")]
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
archive=ROOT/"exam-007.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)

# Re-run generation after workflow registration.
