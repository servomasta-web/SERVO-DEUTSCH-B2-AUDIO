import asyncio
import subprocess
import zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output")
AUDIO=ROOT/"audio"
AUDIO.mkdir(parents=True,exist_ok=True)

# Prüfung 004: Gesunde Ernährung im Alltag.
# Die Texte sind eigens für die App-Aufgaben 004 verfasst.
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Durchsage im Supermarkt: Wegen einer technischen Störung können heute Vormittag keine frischen Backwaren an der Selbstbedienungstheke abgepackt werden. Brot und Brötchen erhalten Sie weiterhin direkt beim Personal. Die Obst- und Gemüseabteilung ist davon nicht betroffen.")],
"teil1_02.mp3":[("de-DE-KatjaNeural","Ich esse mittags oft nur schnell ein belegtes Brötchen."),("de-DE-ConradNeural","Vielleicht könntest du etwas vorbereiten und mitnehmen."),("de-DE-KatjaNeural","Dafür fehlt mir morgens die Zeit."),("de-DE-ConradNeural","Dann koche am Sonntag eine größere Portion und teile sie für mehrere Tage auf.")],
"teil1_03.mp3":[("de-DE-KatjaNeural","Hinweis der Volkshochschule: Der Vortrag Gesund essen trotz Schichtarbeit findet nicht wie angekündigt am Dienstag, sondern am Donnerstag um 18.30 Uhr statt. Der Veranstaltungsraum bleibt unverändert. Angemeldete Personen müssen sich nicht erneut registrieren.")],
"teil1_04.mp3":[("de-DE-AmalaNeural","Früher habe ich beim Einkaufen vor allem auf Sonderangebote geachtet. Seit ich die Zutatenlisten genauer lese, kaufe ich weniger Fertiggerichte. Das ist nicht unbedingt teurer, denn ich plane meine Mahlzeiten jetzt besser und werfe seltener Lebensmittel weg.")],
"teil1_05.mp3":[("de-DE-KatjaNeural","Meldung aus der Schulküche: Ab nächster Woche wird das vegetarische Gericht nicht mehr freitags, sondern mittwochs angeboten. Am Freitag steht künftig ein Fischgericht auf dem Speiseplan. Allergiehinweise können weiterhin bis spätestens Montag beim Küchenteam abgegeben werden.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderator: Viele Menschen möchten sich gesünder ernähren, scheitern aber im hektischen Alltag. Frau Keller, Sie beraten Berufstätige. Was ist der häufigste Grund?"),
("de-DE-AmalaNeural","Ernährungsberaterin: Oft fehlt nicht das Wissen, sondern eine realistische Planung. Wer erst um zwölf Uhr überlegt, was es zum Mittagessen geben soll, greift leichter zu irgendeinem schnellen Angebot. Schon ein grober Wochenplan kann helfen."),
("de-DE-KatjaNeural","Moderator: Muss man dafür jeden Sonntag stundenlang in der Küche stehen?"),
("de-DE-AmalaNeural","Beraterin: Nein. Ich empfehle, zwei oder drei Grundzutaten vorzubereiten. Gekochte Hülsenfrüchte, Gemüse oder Reis lassen sich unterschiedlich kombinieren. So entstehen mehrere Gerichte, ohne dass man jeden Tag von vorn anfangen muss."),
("de-DE-KatjaNeural","Moderator: Wie beurteilen Sie Ernährungstrends im Internet?"),
("de-DE-AmalaNeural","Beraterin: Man sollte vorsichtig sein. Manche Empfehlungen versprechen schnelle Ergebnisse, obwohl sie wissenschaftlich kaum belegt sind. Besonders problematisch sind strenge Verbote ganzer Lebensmittelgruppen. Eine ausgewogene Ernährung muss zum Gesundheitszustand und zum Alltag der jeweiligen Person passen."),
("de-DE-KatjaNeural","Moderator: Ist gesundes Essen zwangsläufig teuer?"),
("de-DE-AmalaNeural","Beraterin: Nicht unbedingt. Saisonales Gemüse, Haferflocken und Hülsenfrüchte sind häufig preiswert. Teuer wird es eher, wenn man spontan einkauft oder Lebensmittel verderben lässt."),
("de-DE-KatjaNeural","Moderator: Was raten Sie Menschen, die ihre Gewohnheiten ändern möchten?"),
("de-DE-AmalaNeural","Beraterin: Kleine Schritte sind nachhaltiger als radikale Vorsätze. Wer zunächst regelmäßig frühstückt oder täglich eine Portion Gemüse ergänzt, kann später weitere Veränderungen angehen.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderator: In unserer Gesprächsrunde geht es um gesundes Essen in Betriebskantinen. Herr Seifert, Sie leiten eine Kantine."),
("de-DE-ConradNeural","Seifert: Wir möchten mehr frische Gerichte anbieten. Allerdings müssen wir täglich eine große Zahl von Mahlzeiten zu einem festen Preis vorbereiten. Wenn wir ausschließlich regionale Bio-Produkte verwenden, können wir diesen Preis kaum halten."),
("de-DE-KatjaNeural","Moderator: Frau Yilmaz, Sie vertreten eine Initiative für ausgewogene Ernährung."),
("de-DE-AmalaNeural","Yilmaz: Niemand verlangt, dass jedes Produkt aus biologischem Anbau stammt. Wichtig wäre zunächst, Gemüsegerichte attraktiver zu gestalten und die Herkunft der Zutaten transparent zu machen. Außerdem sollte es kleinere Portionen zu einem niedrigeren Preis geben."),
("de-DE-KatjaNeural","Moderator: Herr Seifert, wäre das umsetzbar?"),
("de-DE-ConradNeural","Seifert: Kleinere Portionen könnten funktionieren. Bei der Herkunftsinformation sehe ich ebenfalls Möglichkeiten. Wir brauchen dafür allerdings verlässliche Angaben unserer Lieferanten."),
("de-DE-AmalaNeural","Yilmaz: Das ist ein guter Anfang. Zusätzlich sollten Beschäftigte regelmäßig Rückmeldung geben können. Ein Speiseplan, der an den tatsächlichen Bedürfnissen vorbeigeht, wird kaum angenommen."),
("de-DE-KatjaNeural","Moderator: Dann hängt eine Verbesserung also sowohl von der Organisation als auch von der Beteiligung der Gäste ab.")
],
"teil4_01.mp3":[
("de-DE-ConradNeural","Guten Tag. Heute geht es um die Frage, wie Schulen eine gesunde Ernährung fördern können. Dabei reicht es nicht, lediglich gesündere Speisen auf den Speiseplan zu setzen. Entscheidend ist auch, wie Kinder Lebensmittel kennenlernen und welche Gewohnheiten sie zu Hause und in der Schule entwickeln."),
("de-DE-ConradNeural","Ein erster Ansatz sind gemeinsame Mahlzeiten. Wenn Kinder in Ruhe essen und verschiedene Speisen probieren können, entdecken sie möglicherweise neue Geschmacksrichtungen. Niemand sollte jedoch gezwungen werden, etwas aufzuessen. Druck kann dazu führen, dass Kinder bestimmte Lebensmittel erst recht ablehnen."),
("de-DE-ConradNeural","Darüber hinaus kann praktischer Unterricht hilfreich sein. In einem Schulgarten lernen Schülerinnen und Schüler, wie Gemüse wächst und welche Arbeit dahintersteckt. Beim gemeinsamen Kochen erfahren sie, wie aus einfachen Zutaten eine vollständige Mahlzeit entsteht. Solche Angebote sollten altersgerecht gestaltet werden und nicht nur theoretisches Wissen vermitteln."),
("de-DE-ConradNeural","Auch die Zusammenarbeit mit Eltern ist wichtig. Schulen können Informationen anbieten, sollten aber unterschiedliche finanzielle und kulturelle Lebensbedingungen respektieren. Es wäre wenig sinnvoll, Familien pauschal zu kritisieren. Besser sind konkrete, bezahlbare Vorschläge und ein offener Austausch."),
("de-DE-ConradNeural","Zum Schluss möchte ich betonen: Eine nachhaltige Ernährungsbildung entsteht durch viele kleine Erfahrungen. Sie braucht Zeit, geeignete Rahmenbedingungen und die Bereitschaft, Kinder aktiv einzubeziehen.")
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
archive=ROOT/"exam-004.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
