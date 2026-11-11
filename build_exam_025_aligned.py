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
tracks={"teil1_01.mp3":[["de-DE-KatjaNeural","Hinweis des Wertstoffhofs: Kleine Elektrogeräte können ab sofort auch ohne vorherige Terminbuchung abgegeben werden. Für Kühlschränke und Waschmaschinen ist weiterhin eine Anmeldung erforderlich, damit der Transport vorbereitet werden kann."]],"teil1_02.mp3":[["de-DE-KatjaNeural","A: Ich habe mein altes Fahrrad reparieren lassen. B: Lohnt sich das noch? A: Ja, nur die Bremsen und die Kette mussten ersetzt werden. B: Gut, sonst werden viele Dinge viel zu schnell weggeworfen. A: Außerdem war die Reparatur günstiger als ein neues Fahrrad."]],"teil1_03.mp3":[["de-DE-KatjaNeural","Mitteilung der Gemeinde: Am Samstag findet ein Tauschmarkt für Kleidung und Haushaltsgegenstände statt. Besucher können bis zu zehn gut erhaltene Artikel mitbringen. Geld wird nicht getauscht; jedes Teil erhält eine Tauschmarke."]],"teil1_04.mp3":[["de-DE-AmalaNeural","Ich trenne Papier und Glas sorgfältig, aber bei Verpackungen bin ich manchmal unsicher. Die Abfallberatung hat mir erklärt, dass stark verschmutzte Pizzakartons nicht ins Altpapier gehören."]],"teil1_05.mp3":[["de-DE-KatjaNeural","Durchsage: Die Abholung von Sperrmüll muss mindestens fünf Werktage vorher angemeldet werden. Gegenstände dürfen erst am Vorabend des bestätigten Termins an die Straße gestellt werden."]],"teil2_01.mp3":[["de-DE-KatjaNeural","Moderator: Viele Produkte werden nach kurzer Zeit weggeworfen. Frau Lehmann, Sie beraten Kommunen zur Kreislaufwirtschaft. Was bedeutet dieser Begriff?\nLehmann: Produkte und Materialien sollen möglichst lange genutzt werden. Statt Rohstoffe einmal zu verwenden und danach zu entsorgen, versucht man, Dinge zu reparieren, wiederzuverwenden und am Ende möglichst hochwertig zu recyceln.\nModerator: Ist Recycling immer die beste Lösung?\nLehmann: Nein. Es braucht Energie und kann Materialqualität verlieren. Wenn ein Gerät repariert oder weitergegeben werden kann, ist das häufig sinnvoller. Die Reihenfolge lautet deshalb: vermeiden, länger nutzen, reparieren, wiederverwenden und erst danach recyceln.\nModerator: Was können Hersteller beitragen?\nLehmann: Sie sollten Produkte langlebig und reparierbar gestalten. Ersatzteile müssen verfügbar sein, und Geräte sollten sich ohne großen Aufwand öffnen lassen. Außerdem können Unternehmen Rücknahmesysteme anbieten.\nModerator: Welche Rolle spielen Verbraucher?\nLehmann: Sie können beim Kauf auf Qualität und Reparierbarkeit achten, Gegenstände teilen und gebrauchte Produkte kaufen. Wichtig ist aber auch eine gute Infrastruktur: Reparaturwerkstätten, Sammelstellen und verständliche Informationen.\nModerator: Wie kann eine Kommune beginnen?\nLehmann: Mit konkreten Projekten, zum Beispiel einem Reparaturcafé, einem Leihsystem oder einem Tauschmarkt. Danach sollte sie prüfen, welche Angebote genutzt werden und wo noch Hindernisse bestehen."]],"teil3_01.mp3":[["de-DE-KatjaNeural","Moderatorin: Sollten Hersteller verpflichtet werden, Ersatzteile für jedes Gerät mindestens zehn Jahre lang anzubieten? Herr Vogt, Sie vertreten einen Verband kleiner Unternehmen."],["de-DE-ConradNeural","Vogt: Eine feste Frist für alle Produkte kann unverhältnismäßig sein. Bei manchen Geräten ändern sich technische Standards schnell. Kleine Betriebe brauchen außerdem Planungssicherheit, damit Lagerkosten nicht zu hoch werden."],["de-DE-KatjaNeural","Moderatorin: Frau Santos, Sie arbeiten für eine Verbraucherorganisation."],["de-DE-ConradNeural","Santos: Ohne verbindliche Regeln sind Ersatzteile oft schon nach wenigen Jahren nicht mehr erhältlich. Das macht Reparaturen unmöglich und zwingt Menschen zum Neukauf. Wir brauchen klare Mindestfristen und Informationen über Reparaturmöglichkeiten."],["de-DE-ConradNeural","Vogt: Ich unterstütze mehr Transparenz. Vielleicht könnte die Frist je nach Produktgruppe unterschiedlich sein. Wichtig ist, dass Regeln technisch realistisch bleiben."],["de-DE-ConradNeural","Santos: Eine abgestufte Regelung ist denkbar, solange Verbraucher wissen, wie lange Teile verfügbar sind und welche Reparaturkosten zu erwarten sind."],["de-DE-KatjaNeural","Moderatorin: Beide wollen Reparierbarkeit verbessern, unterscheiden sich aber bei einer einheitlichen Mindestfrist."]],"teil4_01.mp3":[["de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um Recycling und Kreislaufwirtschaft. Viele Produkte enthalten wertvolle Rohstoffe, deren Gewinnung Energie und natürliche Ressourcen benötigt. Wenn Gegenstände nach kurzer Nutzung weggeworfen werden, gehen Materialien verloren und es entsteht zusätzlicher Abfall.\nEine Kreislaufwirtschaft versucht, diesen Verlust zu vermeiden. Am Anfang steht die Frage, ob ein Produkt überhaupt neu gekauft werden muss. Leihen, Teilen und Gebrauchtkauf können den Bedarf an neuen Waren verringern. Wenn ein Gegenstand vorhanden ist, sollte er möglichst lange genutzt und bei Bedarf repariert werden.\nWiederverwendung bedeutet, dass ein Produkt oder Bauteil erneut eingesetzt wird. Das kann bei Möbeln, Kleidung und technischen Geräten funktionieren. Recycling ist wichtig, wenn eine weitere Nutzung nicht mehr möglich ist. Dabei werden Materialien getrennt und verarbeitet. Die Qualität kann jedoch sinken, und nicht alle Stoffe lassen sich gleich gut zurückgewinnen.\nHersteller beeinflussen die Kreislauffähigkeit schon bei der Entwicklung. Langlebige Materialien, austauschbare Teile und verständliche Reparaturanleitungen erleichtern eine längere Nutzung. Kommunen können Sammelstellen, Reparaturangebote und Tauschbörsen fördern.\nAuch Verbraucher tragen Verantwortung, indem sie Abfälle korrekt trennen und Produkte bewusst auswählen. Die größte Wirkung entsteht, wenn Design, Handel, kommunale Infrastruktur und Kaufverhalten zusammenpassen. Recycling allein löst das Abfallproblem nicht; entscheidend ist, Abfälle möglichst gar nicht erst entstehen zu lassen."]]}
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
archive=ROOT/"exam-025.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
