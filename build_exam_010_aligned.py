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
"teil1_01.mp3":[("de-DE-KatjaNeural","Hinweis im Supermarkt: Mehrwegboxen für Käse und Wurst können ab sofort an der Information zurückgegeben werden. Bitte bringen Sie die gereinigten Behälter mit. Die Rückgabe ist auch ohne Kassenbon möglich.")],
"teil1_02.mp3":[("de-DE-KatjaNeural","Ich möchte weniger Verpackungsmüll produzieren."),("de-DE-ConradNeural","Dann könntest du auf dem Wochenmarkt einkaufen."),("de-DE-KatjaNeural","Das mache ich schon, aber für manche Produkte brauche ich eine praktische Lösung."),("de-DE-ConradNeural","Vielleicht kannst du Gläser wiederverwenden und größere Packungen mit anderen Haushalten teilen.")],
"teil1_03.mp3":[("de-DE-KatjaNeural","Mitteilung der Gemeinde: Am Samstag wird im Bürgerhaus eine kostenlose Beratung zur Abfalltrennung angeboten. Eine Anmeldung ist nicht nötig. Wer möchte, kann Fotos von Abfällen mitbringen, bei deren Entsorgung Unsicherheit besteht.")],
"teil1_04.mp3":[("de-DE-AmalaNeural","Ich habe früher viele Einwegflaschen gekauft. Seit ich einen Wasserfilter benutze, fülle ich Leitungswasser in eine Flasche aus Edelstahl. Das bedeutet weniger Verpackung, und ich muss seltener Getränke nach Hause tragen.")],
"teil1_05.mp3":[("de-DE-KatjaNeural","Durchsage im Wohnhaus: Ab nächster Woche gibt es einen zusätzlichen Behälter für Bioabfälle. Kunststoffverpackungen gehören weiterhin in die gelbe Tonne und dürfen nicht in den neuen Behälter geworfen werden.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderator: Viele Haushalte möchten weniger Plastik verwenden. Frau Winter, Sie beraten Verbraucherinnen und Verbraucher. Wo sollte man anfangen?"),
("de-DE-AmalaNeural","Winter: Am besten dort, wo regelmäßig große Mengen Einwegverpackungen entstehen: bei Getränken, Reinigungsmitteln und Lebensmitteln. Es muss aber nicht alles auf einmal verändert werden. Wer sich zwei oder drei konkrete Gewohnheiten vornimmt, bleibt eher dabei."),
("de-DE-KatjaNeural","Moderator: Sind unverpackte Läden für alle eine Lösung?"),
("de-DE-AmalaNeural","Winter: Sie sind eine Möglichkeit, aber nicht überall erreichbar und manchmal teurer. Man kann auch im normalen Supermarkt Produkte mit wenig Verpackung wählen oder Nachfüllangebote nutzen. Wichtig ist, dass die Lösung zum Alltag und zum Budget passt."),
("de-DE-KatjaNeural","Moderator: Was halten Sie von biologisch abbaubaren Kunststoffen?"),
("de-DE-AmalaNeural","Winter: Der Begriff kann missverstanden werden. Viele dieser Materialien zerfallen nur unter bestimmten Bedingungen in industriellen Anlagen. Im heimischen Kompost verschwinden sie nicht unbedingt schnell. Deshalb gehören sie nicht automatisch in die Biotonne."),
("de-DE-KatjaNeural","Moderator: Welche Rolle spielt Wiederverwendung?"),
("de-DE-AmalaNeural","Winter: Eine große. Ein stabiler Behälter kann Einwegverpackungen ersetzen. Allerdings sollte man ihn lange verwenden und nicht ständig neue Mehrwegprodukte kaufen."),
("de-DE-KatjaNeural","Moderator: Was können Kommunen beitragen?"),
("de-DE-AmalaNeural","Winter: Sie können Trinkbrunnen, Reparatur- und Tauschmöglichkeiten fördern und verständliche Informationen zur Entsorgung anbieten. Hersteller sollten zugleich stärker dafür verantwortlich sein, unnötige Verpackungen zu vermeiden.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Sollten Geschäfte Einwegverpackungen vollständig abschaffen? Herr Peters, Sie führen einen kleinen Lebensmittelmarkt."),
("de-DE-ConradNeural","Peters: Ein sofortiges Verbot wäre für kleine Läden schwer umzusetzen. Manche Waren benötigen aus hygienischen oder logistischen Gründen eine Verpackung. Wir sollten zuerst Mehrwegsysteme ausbauen und Lieferanten einbeziehen."),
("de-DE-KatjaNeural","Moderatorin: Frau Demir, Sie engagieren sich in einer Umweltinitiative."),
("de-DE-AmalaNeural","Demir: Freiwillige Lösungen reichen nicht. Solange Einwegverpackungen billiger sind, entscheiden sich viele Unternehmen dafür. Es braucht verbindliche Ziele und eine klare Kennzeichnung, damit Kundinnen und Kunden Alternativen erkennen."),
("de-DE-ConradNeural","Peters: Eine Kennzeichnung finde ich sinnvoll. Regeln müssen aber für kleine Betriebe realistisch sein. Wenn Rücknahmesysteme kompliziert sind, werden sie kaum genutzt."),
("de-DE-AmalaNeural","Demir: Deshalb sollten Kommunen gemeinsame Rückgabestellen schaffen. Dann muss nicht jedes Geschäft ein eigenes System entwickeln."),
("de-DE-KatjaNeural","Moderatorin: Beide Seiten sehen Mehrweg als wichtigen Schritt, unterscheiden sich aber beim Tempo und bei der Verbindlichkeit der Regeln.")
],
"teil4_01.mp3":[("de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es darum, wie Haushalte Plastik vermeiden können. Kunststoff ist leicht, vielseitig und in vielen Bereichen nützlich. Problematisch wird er vor allem dann, wenn Produkte nur kurz verwendet werden und anschließend als Abfall in die Umwelt gelangen. Ein erster Ansatz ist die Vermeidung. Leitungswasser in einer wiederbefüllbaren Flasche, Einkaufstaschen aus dauerhaftem Material und unverpackte oder nachfüllbare Produkte können Einwegartikel ersetzen. Vorhandene Gegenstände sollte man möglichst lange nutzen. Ein neu gekaufter Stoffbeutel ist nicht automatisch umweltfreundlicher, wenn er selten verwendet wird. Der zweite Ansatz ist die Wiederverwendung. Gläser, Dosen und robuste Behälter lassen sich mehrfach einsetzen. Bei Mehrwegsystemen ist entscheidend, dass Rückgabe und Reinigung gut organisiert sind. Lange Transportwege oder sehr geringe Umlaufzahlen können den ökologischen Vorteil verringern. Recycling bleibt wichtig, steht aber hinter Vermeidung und Wiederverwendung. Nicht jeder Kunststoff lässt sich gleich gut recyceln. Unterschiedliche Materialarten, Verschmutzungen und Verbundverpackungen erschweren die Sortierung. Deshalb müssen Abfälle richtig getrennt werden, und Hersteller sollten Produkte so gestalten, dass Materialien leichter wiederverwertet werden können. Schließlich braucht es gemeinsame Verantwortung. Verbraucher können bewusster einkaufen, Geschäfte Nachfüll- und Rücknahmesysteme anbieten und Kommunen eine verständliche Abfallinfrastruktur bereitstellen. Die größte Wirkung entsteht, wenn diese Maßnahmen zusammenwirken.")]}
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
archive=ROOT/"exam-010.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
