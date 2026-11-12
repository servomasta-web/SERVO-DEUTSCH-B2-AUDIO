# SERVO DEUTSCH B2 — exam 031 aligned audio generation
import asyncio
import subprocess
import zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output")
AUDIO=ROOT/"audio"
AUDIO.mkdir(parents=True,exist_ok=True)

# Audioinhalte sind auf die 30 Fragen von Prüfung 031 abgestimmt.
tracks={
"teil1_01.mp3":[["de-DE-KatjaNeural","Hinweis des Kulturzentrums: Am Samstag findet von elf bis vierzehn Uhr ein Kleidertausch statt. Bringen Sie saubere und gut erhaltene Kleidung mit. Für jedes abgegebene Stück erhalten Sie einen Tauschpunkt. Die Teilnahme ist kostenlos, eine Anmeldung ist nicht erforderlich."]],
"teil1_02.mp3":[["de-DE-KatjaNeural","In unserem Reparaturcafé zeigen Ehrenamtliche, wie man kleine Schäden an Kleidung selbst beheben kann. Der Workshop richtet sich ausdrücklich auch an Anfängerinnen und Anfänger. Bitte bringen Sie ein Kleidungsstück mit, das einen kleinen Schaden hat. Nadeln und Faden werden gestellt."]],
"teil1_03.mp3":[["de-DE-AmalaNeural","Das Kaufhaus am Marktplatz eröffnet Mitte Juni eine neue Abteilung für gebrauchte Kleidung. Dort werden sorgfältig geprüfte Jacken, Hosen und Schuhe zu günstigen Preisen angeboten. Die Waren stammen aus privaten Spenden und aus Rücknahmen des Geschäfts."]],
"teil1_04.mp3":[["de-DE-ConradNeural","Mitteilung der Stadtverwaltung: Gut erhaltene Kleidung kann ab sofort im Bürgerbüro sowie in drei Stadtteilzentren abgegeben werden. Die Textilien werden sortiert und an soziale Einrichtungen weitergegeben. Bitte geben Sie keine stark beschädigten oder feuchten Kleidungsstücke ab."]],
"teil1_05.mp3":[["de-DE-KatjaNeural","Die Volkshochschule lädt zu einem Vortrag über die Herstellung von Textilien ein. Eine Fachjournalistin erklärt, woher Rohstoffe stammen und unter welchen Bedingungen Kleidung produziert wird. Die Veranstaltung findet am Dienstag um neunzehn Uhr statt. Eine telefonische Anmeldung ist bis Freitag möglich."]],
"teil2_01.mp3":[["de-DE-KatjaNeural","Moderatorin: Viele Menschen kaufen regelmäßig neue Kleidung. Frau Dr. Weber, Sie beschäftigen sich mit nachhaltigem Konsum. Warum ist das ein Problem?\nExpertin: Die Herstellung von Textilien benötigt Rohstoffe, Wasser und Energie. Hinzu kommen Transportwege und teilweise problematische Arbeitsbedingungen. Besonders kritisch ist das Geschäftsmodell der sogenannten Fast Fashion: Kollektionen wechseln schnell, die Preise sind niedrig und Kleidungsstücke werden oft nur kurze Zeit getragen.\nModeratorin: Ist Secondhand-Kleidung deshalb automatisch nachhaltig?\nExpertin: Sie kann einen wichtigen Beitrag leisten, weil vorhandene Produkte länger genutzt werden. Allerdings sollte man auch hier bewusst einkaufen. Wer ständig gebrauchte Kleidung bestellt, die er kaum trägt, vermeidet das Konsumproblem nicht vollständig. Bei Online-Plattformen sind Zustand, Maße und Rückgabebedingungen wichtig.\nModeratorin: Welche Alternativen gibt es noch?\nExpertin: Reparieren ist eine sehr sinnvolle Möglichkeit. Ein fehlender Knopf oder eine offene Naht bedeutet nicht, dass ein Kleidungsstück weggeworfen werden muss. Auch Kleidertauschbörsen und Leihangebote können die Nutzungsdauer verlängern.\nModeratorin: Was können Verbraucherinnen und Verbraucher konkret tun?\nExpertin: Zunächst weniger kaufen und genauer überlegen, ob man etwas wirklich braucht. Qualität, Passform und Pflege spielen ebenfalls eine Rolle. Nachhaltigkeit bedeutet nicht, ständig neue Spezialprodukte zu erwerben, sondern vorhandene Dinge länger zu verwenden.\nModeratorin: Reicht individuelles Verhalten aus?\nExpertin: Nein. Unternehmen müssen langlebige Produkte anbieten und transparente Informationen liefern. Politik und Handel können Reparatur, Rücknahme und faire Produktionsbedingungen fördern. Entscheidend ist das Zusammenspiel aller Beteiligten."]],
"teil3_01.mp3":[["de-DE-KatjaNeural","Moderatorin: Sollte nachhaltige Kleidung stärker gefördert werden, auch wenn sie dadurch teurer wird? Nora, wie sehen Sie das?"],["de-DE-AmalaNeural","Nora: Für mich beginnt Veränderung mit Bildung. Schon in Schulen sollte man erklären, welche Folgen die Textilproduktion für Umwelt und Beschäftigte hat. Außerdem müssen nachhaltige Angebote für Menschen mit kleinem Budget erreichbar bleiben. Sonst entsteht der Eindruck, verantwortungsvoller Konsum sei ein Luxus."],["de-DE-KatjaNeural","Moderatorin: Tim, stimmen Sie zu?"],["de-DE-ConradNeural","Tim: Information ist wichtig, aber sie allein reicht nicht. Ich wünsche mir klare Angaben zur Herkunft, zu den Materialien und zu den Produktionsbedingungen. Viele Verbraucher können kaum erkennen, was hinter Werbeversprechen steckt. Gleichzeitig sollten wir Secondhand nicht als einzige Lösung betrachten. Auch neue Kleidung kann langlebig und fair hergestellt sein."],["de-DE-KatjaNeural","Moderatorin: Selin, welche Erfahrungen haben Sie gemacht?"],["de-DE-AmalaNeural","Selin: In unserem Viertel organisieren wir zweimal im Jahr einen Kleidertausch. Das funktioniert überraschend gut und bringt Menschen zusammen. Zusätzlich bieten wir kleine Reparaturkurse an. Solche Kenntnisse sollten wieder stärker zum Alltag gehören, damit nicht wegen jedes kleinen Schadens etwas Neues gekauft wird."],["de-DE-ConradNeural","Tim: Solche Initiativen sind hilfreich, aber Unternehmen müssen ebenfalls Verantwortung übernehmen."],["de-DE-KatjaNeural","Moderatorin: Es wird also deutlich, dass Bildung, transparente Informationen und praktische Angebote zusammenwirken müssen."]],
"teil4_01.mp3":[["de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um Secondhand-Mode und nachhaltigen Kleidungskonsum. Kleidung erfüllt praktische und soziale Funktionen. Gleichzeitig hat ihre Herstellung erhebliche Auswirkungen auf Umwelt und Gesellschaft. Um diese Folgen zu verstehen, muss man den gesamten Lebenszyklus eines Kleidungsstücks betrachten.\nDer ökologische Fußabdruck beginnt bei der Gewinnung der Rohstoffe. Beim Baumwollanbau kann beispielsweise viel Wasser benötigt werden. Bei der Verarbeitung kommen Energie, Chemikalien und weitere Ressourcen hinzu. Danach folgen Transport, Verkauf, Nutzung und schließlich Entsorgung. Die Belastung entsteht also nicht erst beim Waschen.\nEin besonderes Problem sind sehr kurze Nutzungszeiten. Wenn Kleidung schnell aus der Mode kommt oder von geringer Qualität ist, wird sie häufig früh ersetzt. Secondhand-Angebote, Kleidertausch und Reparaturen können die Nutzungsdauer verlängern. Allerdings ist auch bei gebrauchten Produkten ein bewusster Kauf entscheidend.\nDas Recycling von Textilien ist technisch anspruchsvoll. Besonders Mischgewebe aus verschiedenen Fasern lassen sich oft nur schwer trennen. Deshalb sollten Produkte möglichst langlebig und reparierbar gestaltet werden. Unternehmen können Rücknahmeprogramme, Reparaturservices und Wiederverwendungssysteme anbieten.\nAuch die Pflege hat Einfluss. Wer Kleidung gemäß den Pflegehinweisen wäscht, sie nicht unnötig heiß trocknet und kleine Schäden früh repariert, kann ihre Lebensdauer erhöhen. Bei Textilsiegeln ist es wichtig, die zugrunde liegenden Kriterien und unabhängige Kontrollen zu prüfen, denn nicht jedes Zeichen steht für dieselben Standards.\nSchließlich kann die Politik bessere Rahmenbedingungen schaffen. Dazu gehören transparente Lieferketten, verständliche Produktinformationen und die Förderung von Reparaturangeboten. Nachhaltige Mode ist keine Aufgabe einzelner Käuferinnen und Käufer. Längere Nutzung, verantwortungsvolle Unternehmen und faire Produktionsbedingungen müssen zusammenkommen. Vielen Dank für Ihre Aufmerksamkeit."]]
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
archive=ROOT/"exam-031.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
