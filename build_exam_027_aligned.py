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
tracks={"teil1_01.mp3":[["de-DE-KatjaNeural","Mitteilung des Modehauses: Die Reparaturannahme für Jacken und Mäntel ist am Donnerstag nur bis 16 Uhr geöffnet. Ab Freitag gelten wieder die üblichen Öffnungszeiten. Für kleine Änderungen ist keine vorherige Anmeldung nötig."]],"teil1_02.mp3":[["de-DE-KatjaNeural","A: Ich kaufe inzwischen oft Kleidung aus zweiter Hand. B: Findest du da immer etwas Passendes? A: Nicht sofort, aber ich schaue regelmäßig vorbei. B: Und wie ist das mit der Qualität? A: Ich prüfe Nähte und Reißverschlüsse genau, bevor ich etwas mitnehme."]],"teil1_03.mp3":[["de-DE-KatjaNeural","Hinweis der Verbraucherberatung: Beim Kauf von Kleidung sollte man auf Materialangaben und Pflegehinweise achten. Ein Kleidungsstück, das nur chemisch gereinigt werden kann, verursacht möglicherweise höhere Folgekosten."]],"teil1_04.mp3":[["de-DE-AmalaNeural","Ich habe an einer Kleidertauschaktion teilgenommen. Ich brachte drei gut erhaltene Hemden mit und fand eine warme Jacke. Es wurde kein Geld verlangt; die Organisatoren wollten vor allem zeigen, dass Kleidung länger genutzt werden kann."]],"teil1_05.mp3":[["de-DE-KatjaNeural","Durchsage im Einkaufszentrum: Der Vortrag über nachhaltige Textilien findet nicht wie geplant im Erdgeschoss, sondern im Seminarraum im dritten Stock statt. Beginn ist um 18 Uhr."]],"teil2_01.mp3":[["de-DE-KatjaNeural","Moderatorin: Kleidung wird oft schnell gekauft und wieder aussortiert. Frau Weber, Sie beraten Unternehmen zu nachhaltiger Mode. Was ist das wichtigste Problem der Textilbranche?\nWeber: Viele Kleidungsstücke werden nur kurze Zeit getragen. Gleichzeitig sind Herstellung und Transport ressourcenintensiv. Besonders problematisch ist, wenn niedrige Preise dazu führen, dass Qualität und Arbeitsbedingungen aus dem Blick geraten.\nModeratorin: Ist der Kauf von Bio-Baumwolle automatisch nachhaltig?\nWeber: Nicht automatisch. Man muss auch Wasserverbrauch, Färbung, Transport und die Lebensdauer des Produkts betrachten. Ein Material allein sagt noch nicht alles über die Umweltbilanz aus.\nModeratorin: Was können Verbraucher konkret tun?\nWeber: Weniger, aber bewusster kaufen. Auf gute Verarbeitung achten, Kleidung reparieren und bei Bedarf gebraucht kaufen. Auch Kleidertausch oder Leihangebote können sinnvoll sein, wenn sie tatsächlich genutzt werden.\nModeratorin: Welche Verantwortung haben Hersteller?\nWeber: Sie sollten transparente Informationen über Lieferketten bereitstellen, langlebige Produkte entwickeln und Reparaturen ermöglichen. Außerdem müssen Beschäftigte entlang der Lieferkette fair behandelt werden.\nModeratorin: Wie erkennt man glaubwürdige Nachhaltigkeitsversprechen?\nWeber: Man sollte auf überprüfbare Kriterien achten. Allgemeine Begriffe wie 'grün' oder 'bewusst' reichen nicht. Aussagekräftiger sind konkrete Angaben zu Materialien, Produktion und unabhängigen Kontrollen."]],"teil3_01.mp3":[["de-DE-KatjaNeural","Moderator: Sollten Modeunternehmen verpflichtet werden, nicht verkaufte Kleidung zu spenden statt sie zu vernichten? Herr Baum, Sie vertreten einen Handelsverband."],["de-DE-ConradNeural","Baum: Spenden können sinnvoll sein, aber nicht jedes Produkt ist dafür geeignet. Es gibt hygienische, qualitative und logistische Fragen. Eine Pflicht ohne klare Regeln könnte zusätzliche Kosten verursachen und kleinere Betriebe überfordern."],["de-DE-KatjaNeural","Moderator: Frau Fischer, Sie arbeiten für eine Umweltorganisation."],["de-DE-ConradNeural","Fischer: Die Vernichtung unverkaufter Ware ist eine Verschwendung von Ressourcen. Unternehmen sollten zuerst besser planen und Überproduktion vermeiden. Wenn Kleidung noch tragbar ist, muss eine Weitergabe Vorrang haben."],["de-DE-ConradNeural","Baum: Bessere Planung unterstütze ich. Allerdings brauchen wir auch sichere Wege, um Spenden an Einrichtungen zu verteilen, die sie wirklich benötigen."],["de-DE-ConradNeural","Fischer: Genau deshalb sollten Unternehmen mit sozialen Organisationen zusammenarbeiten und Mengen frühzeitig melden. So kann die Verteilung organisiert werden."],["de-DE-KatjaNeural","Moderator: Beide wollen Verschwendung verhindern, sehen aber unterschiedliche Herausforderungen bei einer verbindlichen Spendenpflicht."]],"teil4_01.mp3":[["de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um nachhaltige Mode. Die Textilproduktion benötigt Rohstoffe, Wasser, Energie und Transport. Wenn Kleidung nur wenige Male getragen wird, entsteht ein hoher Ressourcenverbrauch im Verhältnis zur tatsächlichen Nutzung. Nachhaltigkeit beginnt deshalb nicht erst beim Recycling, sondern bereits bei Kaufentscheidungen und Produktgestaltung.\nVerbraucher können die Lebensdauer ihrer Kleidung verlängern. Dazu gehören gute Pflege, kleine Reparaturen und die Weitergabe nicht mehr benötigter Stücke. Secondhand-Angebote und Kleidertausch ermöglichen, dass vorhandene Kleidung länger genutzt wird. Leihen kann bei besonderen Anlässen eine Alternative zum Kauf sein.\nHersteller tragen ebenfalls Verantwortung. Sie sollten langlebige Materialien auswählen, Reparaturen ermöglichen und Informationen über Herkunft und Produktionsbedingungen bereitstellen. Auch die Arbeitsbedingungen in den Lieferketten gehören zur Nachhaltigkeit. Ein niedriger Preis darf nicht auf Kosten der Beschäftigten entstehen.\nEin Problem ist die Überproduktion. Unternehmen können Nachfrage besser einschätzen, kleinere Serien herstellen und unverkaufte Ware weitergeben. Spenden müssen gut organisiert sein, damit Produkte tatsächlich gebraucht werden und nicht an anderer Stelle zu Abfall werden.\nSchließlich sollten Verbraucher Werbeversprechen kritisch prüfen. Konkrete Informationen und unabhängige Kontrollen sind verlässlicher als allgemeine Aussagen. Nachhaltige Mode bedeutet, weniger Ressourcen zu verbrauchen, Kleidung länger zu nutzen und faire Bedingungen entlang der gesamten Lieferkette zu fördern."]]}
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
archive=ROOT/"exam-027.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
