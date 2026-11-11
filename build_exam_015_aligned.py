import asyncio
import subprocess
import zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output")
AUDIO=ROOT/"audio"
AUDIO.mkdir(parents=True,exist_ok=True)

# Prüfung 006 — Ehrenamtliches Engagement in der Gemeinde.
# Inhaltlich an GoetheExam06Audio.java ausgerichtet.
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Hinweis eines Onlinehändlers: Bestellungen, die bis 14 Uhr eingehen, werden normalerweise noch am selben Werktag bearbeitet. Bei individuell angefertigten Produkten kann die Lieferzeit länger sein. Die voraussichtliche Dauer wird vor dem Kauf angezeigt.")],
"teil1_02.mp3":[("de-DE-KatjaNeural","Ich kaufe Bücher inzwischen öfter in der Buchhandlung um die Ecke."),("de-DE-ConradNeural","Ist das nicht teurer?"),("de-DE-KatjaNeural","Manchmal schon, aber ich kann mich beraten lassen und das Buch sofort mitnehmen."),("de-DE-ConradNeural","Bestellst du dann gar nicht mehr online?"),("de-DE-KatjaNeural","Doch, wenn ein Titel vor Ort nicht erhältlich ist.")],
"teil1_03.mp3":[("de-DE-KatjaNeural","Mitteilung der Verbraucherzentrale: Wer Ware im Internet bestellt, sollte vor dem Bezahlen die Rücksendebedingungen prüfen. Bei manchen Sonderanfertigungen besteht kein gewöhnliches Widerrufsrecht. Die Angaben müssen im Angebot deutlich gemacht werden.")],
"teil1_04.mp3":[("de-DE-AmalaNeural","Ich vergleiche Preise nicht nur auf verschiedenen Plattformen. Ich schaue auch, ob der Händler eine erreichbare Kontaktadresse nennt und wie andere Kunden mit Reklamationen behandelt wurden. Ein sehr niedriger Preis allein überzeugt mich nicht.")],
"teil1_05.mp3":[("de-DE-KatjaNeural","Durchsage im Einkaufszentrum: Der regionale Wochenmarkt findet wegen des Stadtlaufs am Samstag ausnahmsweise auf dem Parkplatz hinter dem Kulturhaus statt. Die Öffnungszeit von acht bis zwölf Uhr bleibt unverändert.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderator: Der Onlinehandel wächst weiter, dennoch bleiben viele Menschen ihren Geschäften vor Ort treu. Frau Schuster, Sie forschen zum Einkaufsverhalten. Welche Vorteile hat der digitale Einkauf?"),
("de-DE-AmalaNeural","Schuster: Er bietet eine große Auswahl, ermöglicht Preisvergleiche und spart Wege. Besonders bei Produkten, die man bereits kennt, ist das praktisch. Allerdings können Fotos und Beschreibungen einen falschen Eindruck vermitteln. Auch Lieferwege und Verpackungen sollte man berücksichtigen."),
("de-DE-KatjaNeural","Moderator: Welche Rolle spielen lokale Geschäfte?"),
("de-DE-AmalaNeural","Schuster: Sie bieten persönliche Beratung, direkte Verfügbarkeit und oft die Möglichkeit, Waren vor dem Kauf zu prüfen. Außerdem tragen sie zu lebendigen Innenstädten bei. Ihr Nachteil sind manchmal höhere Betriebskosten und eine begrenzte Auswahl."),
("de-DE-KatjaNeural","Moderator: Können kleine Händler online konkurrenzfähig werden?"),
("de-DE-AmalaNeural","Schuster: Ja, wenn sie digitale Angebote gezielt einsetzen. Eine übersichtliche Webseite, Reservierungsmöglichkeiten oder die Abholung im Laden können den Service verbessern. Nicht jeder Betrieb muss einen riesigen Versandhandel aufbauen."),
("de-DE-KatjaNeural","Moderator: Was sollten Verbraucher beachten?"),
("de-DE-AmalaNeural","Schuster: Sie sollten überlegen, ob ein Produkt dringend benötigt wird, wie es zurückgeschickt werden kann und ob der Anbieter vertrauenswürdig ist. Bewertungen sind hilfreich, aber nicht jede Bewertung ist echt."),
("de-DE-KatjaNeural","Moderator: Wird es künftig nur noch eine Einkaufsform geben?"),
("de-DE-AmalaNeural","Schuster: Wahrscheinlich nicht. Viele Menschen werden beide Wege kombinieren. Entscheidend ist, dass Preis, Qualität, Beratung und Umweltfolgen bewusst abgewogen werden.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Sollten Innenstädte mehr autofreie Einkaufszonen bekommen? Herr Maier, Sie betreiben ein Fachgeschäft."),
("de-DE-ConradNeural","Maier: Ich unterstütze weniger Durchgangsverkehr, aber die Erreichbarkeit muss erhalten bleiben. Menschen mit eingeschränkter Mobilität und Lieferdienste brauchen praktikable Lösungen. Wenn Kunden ihre Einkäufe nicht transportieren können, weichen sie möglicherweise auf andere Orte aus."),
("de-DE-KatjaNeural","Moderatorin: Frau Roth, Sie engagieren sich in einer Initiative für nachhaltige Stadtentwicklung."),
("de-DE-AmalaNeural","Roth: Autofreie Bereiche schaffen mehr Platz für Fußgänger, Fahrräder und Außengastronomie. Das kann die Aufenthaltsqualität erhöhen. Lieferzeiten und ausgewiesene Zufahrten lassen sich trotzdem organisieren."),
("de-DE-ConradNeural","Maier: Eine gute Idee, wenn Parkmöglichkeiten am Rand und sichere Haltestellen vorhanden sind. Außerdem sollten Händler früh in die Planung einbezogen werden."),
("de-DE-AmalaNeural","Roth: Ja, die Umgestaltung muss schrittweise erfolgen. Wir können zunächst einen Abschnitt testen und anschließend Anwohner, Kunden und Geschäfte befragen."),
("de-DE-KatjaNeural","Moderatorin: Beide unterstützen eine attraktivere Innenstadt, betonen aber unterschiedliche Bedingungen für Erreichbarkeit und Umsetzung.")
],
"teil4_01.mp3":[("de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um die Zukunft des Einkaufens und die Bedeutung lokaler Geschäfte. Der Onlinehandel ermöglicht eine große Auswahl und macht Preise leicht vergleichbar. Gleichzeitig verändert er die Erwartungen der Kundschaft: Viele Menschen möchten Produkte jederzeit bestellen und schnell erhalten. Für lokale Händler entsteht dadurch ein erheblicher Wettbewerbsdruck. Geschäfte vor Ort haben jedoch Stärken, die digitale Plattformen nicht vollständig ersetzen. Kundinnen und Kunden können Waren ansehen, ausprobieren und sich persönlich beraten lassen. Bei Problemen ist ein direkter Kontakt oft einfacher. Zudem schaffen Geschäfte Arbeitsplätze und tragen dazu bei, dass Innenstädte als Orte der Begegnung lebendig bleiben. Eine Möglichkeit ist die Verbindung beider Einkaufsformen. Händler können Waren online präsentieren, Reservierungen anbieten oder bestellte Produkte zur Abholung bereitstellen. Solche Lösungen werden häufig als Mehrkanalstrategie bezeichnet. Sie müssen jedoch zum Betrieb passen und dürfen nicht mehr Aufwand verursachen, als ein kleines Unternehmen leisten kann. Auch Verbraucher tragen Verantwortung. Sie sollten nicht nur den günstigsten Preis betrachten, sondern Qualität, Haltbarkeit, Rücksendebedingungen und Transport berücksichtigen. Spontane Bestellungen führen manchmal dazu, dass Produkte ungenutzt bleiben oder aufwendig zurückgeschickt werden. Kommunen können die Entwicklung unterstützen, indem sie öffentliche Räume attraktiv gestalten, Märkte fördern und eine gute Verkehrsanbindung sichern. Die Zukunft liegt wahrscheinlich nicht in einem vollständigen Sieg des Onlinehandels oder des stationären Geschäfts, sondern in einer sinnvollen Kombination beider Angebote.")]}
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
archive=ROOT/"exam-015.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
