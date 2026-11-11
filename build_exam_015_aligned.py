import asyncio
import subprocess
import zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output")
AUDIO=ROOT/"audio"
AUDIO.mkdir(parents=True,exist_ok=True)

# Goethe B2 Hören — Prüfung 015: Onlinehandel und lokale Geschäfte.
# Eight aligned tracks, with varied German neural voices.
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Information des Stadtmarketings: Der neue Wochenmarkt mit regionalen Produkten findet ab dem kommenden Samstag nicht mehr auf dem Rathausplatz, sondern auf dem Parkplatz am Bahnhof statt. Die Öffnungszeiten bleiben von acht bis dreizehn Uhr.")],
"teil1_02.mp3":[("de-DE-ConradNeural","Ich bestelle inzwischen vieles im Internet, weil ich dadurch Zeit spare. Ich kaufe lieber im Geschäft, besonders wenn ich Kleidung brauche. Aber online kann man doch Preise vergleichen. Das stimmt. Im Laden kann ich die Sachen allerdings direkt anprobieren und bekomme sofort Beratung.")],
"teil1_03.mp3":[("de-DE-AmalaNeural","Hinweis für Kundinnen und Kunden: Bestellungen, die bis Mittwoch um zwölf Uhr eingehen, können noch vor dem Feiertag abgeholt werden. Für Lieferungen nach Hause gilt eine längere Bearbeitungszeit.")],
"teil1_04.mp3":[("de-DE-KillianNeural","Seit unser Viertel einen kleinen Unverpackt-Laden hat, kaufe ich dort regelmäßig Nudeln und Waschmittel. Man muss eigene Behälter mitbringen. Das ist etwas umständlicher, aber ich produziere dadurch weniger Verpackungsmüll.")],
"teil1_05.mp3":[("de-DE-SeraphinaNeural","Durchsage im Einkaufszentrum: Wegen einer technischen Störung ist die Paketannahme heute nur bis sechzehn Uhr geöffnet. Retouren können morgen wieder zu den üblichen Zeiten abgegeben werden.")],
"teil2_01.mp3":[("de-DE-BerndNeural","Moderatorin: Der Onlinehandel wächst seit Jahren. Herr Weber, Sie beraten kleine Einzelhandelsgeschäfte. Welche Chancen bietet der digitale Verkauf? Weber: Kleine Geschäfte können mit einem eigenen Onlineshop auch Menschen erreichen, die nicht in der Nähe wohnen. Außerdem lassen sich Öffnungszeiten und Produktinformationen unabhängig vom Standort anbieten. Allerdings braucht man Zeit und Kenntnisse, um Bestellungen, Bezahlung und Versand zuverlässig zu organisieren. Moderatorin: Bedeutet das, dass jedes Geschäft online verkaufen muss? Weber: Nicht unbedingt. Manche Betriebe leben vor allem von persönlicher Beratung oder davon, dass Kundinnen Produkte direkt ausprobieren können. Für sie kann eine einfache Internetseite mit aktuellen Informationen schon hilfreich sein. Entscheidend ist, dass die digitale Lösung zum Angebot und zu den eigenen Möglichkeiten passt. Moderatorin: Was erwarten Kundinnen und Kunden heute? Weber: Viele möchten flexibel wählen: online informieren, im Laden abholen oder sich die Ware nach Hause schicken lassen. Solche kombinierten Angebote verbinden die Vorteile beider Einkaufsformen. Kleine Händler können dafür mit anderen Geschäften oder lokalen Lieferdiensten zusammenarbeiten. Moderatorin: Welche Probleme darf man nicht unterschätzen? Weber: Preisdruck, Rücksendungen und Verpackungsmüll. Auch große Plattformen verlangen teilweise Gebühren. Händler sollten deshalb genau kalkulieren und nicht versuchen, jeden Preis zu unterbieten. Moderatorin: Was ist für die Zukunft wichtig? Weber: Eine erkennbare lokale Identität und guter Service. Technik ist ein Werkzeug, aber Vertrauen und persönliche Beziehungen bleiben für viele Kundinnen ein Grund, vor Ort einzukaufen.")],
"teil3_01.mp3":[("de-DE-ElkeNeural","Moderator: Sollten Innenstädte an einem Tag pro Woche autofrei sein, um den lokalen Handel zu stärken? Frau Roth, Sie vertreten einen Handelsverband. Roth: Eine autofreie Innenstadt kann die Aufenthaltsqualität verbessern. Menschen bleiben vielleicht länger, besuchen Cafés und entdecken kleinere Geschäfte. Allerdings müssen Lieferungen und der Zugang für Menschen mit eingeschränkter Mobilität weiterhin möglich sein. Moderator: Herr Diallo, Sie betreiben ein Geschäft am Stadtrand. Diallo: Ich sehe das kritisch. Viele Kundinnen kommen mit dem Auto, weil sie größere Einkäufe transportieren müssen. Wenn Parkplätze wegfallen, könnten sie in Einkaufszentren außerhalb der Stadt ausweichen. Ein guter öffentlicher Nahverkehr wäre daher eine Voraussetzung. Roth: Das ist ein wichtiger Punkt. Man könnte zunächst einzelne Straßen testen und die Ergebnisse auswerten. Gleichzeitig sollten Busse häufiger fahren und sichere Fahrradständer eingerichtet werden. Diallo: Ein zeitlich begrenzter Versuch wäre akzeptabel, wenn Anwohner, Händler und Lieferbetriebe vorher beteiligt werden. Eine Entscheidung ohne ihre Erfahrungen würde ich ablehnen. Moderator: Beide Gesprächspartner wünschen sich eine bessere Innenstadt, unterscheiden sich aber bei den Voraussetzungen und beim Tempo der Veränderungen.")],
"teil4_01.mp3":[("de-DE-ChristophNeural","Guten Tag. In meinem Vortrag geht es um Onlinehandel und lokale Geschäfte. Beide Einkaufsformen haben Vorteile, erfüllen aber nicht immer dieselben Bedürfnisse. Der Einkauf im Internet ist bequem und ermöglicht einen schnellen Preisvergleich. Viele Produkte können unabhängig von Öffnungszeiten bestellt werden. Andererseits lassen sich Waren vor dem Kauf nicht immer prüfen, und Rücksendungen verursachen zusätzlichen Aufwand sowie Transportwege. Lokale Geschäfte bieten persönliche Beratung, unmittelbare Verfügbarkeit und die Möglichkeit, Produkte anzufassen oder anzuprobieren. Außerdem tragen sie zur Vielfalt eines Stadtviertels bei und schaffen Arbeitsplätze vor Ort. Häufig sind ihre Preise jedoch höher, weil kleinere Betriebe nicht dieselben Einkaufsmengen wie große Plattformen erreichen. Eine sinnvolle Lösung besteht darin, beide Formen miteinander zu verbinden. Kundinnen können sich online informieren und die Ware anschließend im Geschäft abholen. Händler können digitale Kataloge anbieten, ohne sofort einen umfangreichen Onlineshop aufbauen zu müssen. Solche Angebote sparen teilweise Versandkosten und stärken den Kontakt zur Kundschaft. Auch Verbraucherinnen und Verbraucher tragen Verantwortung. Sie können überlegen, welche Produkte sie dringend benötigen, unnötige Rücksendungen vermeiden und bei bestimmten Einkäufen bewusst lokale Anbieter wählen. Städte wiederum können Märkte, attraktive Fußwege und gute Verkehrsanbindungen fördern. Meiner Ansicht nach sollte nicht eine Einkaufsform die andere vollständig ersetzen. Wichtig sind faire Wettbewerbsbedingungen, transparente Informationen und ein guter Service. Wenn digitale Möglichkeiten mit persönlicher Beratung und regionaler Verantwortung verbunden werden, profitieren sowohl Kundinnen als auch die lokale Wirtschaft.")]
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
    listing=AUDIO/f".{name}.txt"
    listing.write_text("".join(f"file '{p.resolve()}'\\n" for p in parts),encoding="utf-8")
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
