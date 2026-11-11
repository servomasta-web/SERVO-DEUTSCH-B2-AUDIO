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
tracks={"teil1_01.mp3":[["de-DE-KatjaNeural","Mitteilung der Schulleitung: Ab dem nächsten Monat können Schülerinnen und Schüler das Mittagessen bis 9 Uhr am selben Tag online abbestellen. Bisher war eine Abmeldung nur am Vortag möglich. Die Änderung soll Lebensmittelabfälle verringern."]],"teil1_02.mp3":[["de-DE-KatjaNeural","A: Mein Sohn isst in der Schule kaum Gemüse. B: Gibt es dort eine Auswahl? A: Ja, aber er nimmt meistens Nudeln. B: Vielleicht könnt ihr gemeinsam den Speiseplan ansehen und ein neues Gericht auswählen, das er probieren möchte."]],"teil1_03.mp3":[["de-DE-KatjaNeural","Hinweis der Mensa: Am Mittwoch wird ein vegetarisches Gericht mit Linsen angeboten. Allergene sind auf dem Speiseplan gekennzeichnet. Bei Fragen zu einzelnen Zutaten können sich Eltern direkt an das Küchenteam wenden."]],"teil1_04.mp3":[["de-DE-AmalaNeural","Ich finde es gut, dass die Schule jetzt Leitungswasser kostenlos bereitstellt. Früher haben viele Kinder süße Getränke gekauft. Seitdem die Trinkstation aufgestellt wurde, benutzen sie häufiger ihre eigenen Flaschen."]],"teil1_05.mp3":[["de-DE-KatjaNeural","Durchsage: Die Befragung zum Schulessen wird um eine Woche verlängert. Fragebögen können bis zum 18. Juni online ausgefüllt werden. Die Ergebnisse werden im nächsten Elternbrief zusammengefasst."]],"teil2_01.mp3":[["de-DE-KatjaNeural","Moderator: Das Mittagessen in Schulen beeinflusst Gesundheit und Konzentration. Frau Dr. Seifert, Sie beraten Schulträger zur Verpflegung. Was zeichnet ein gutes Schulessen aus?\nSeifert: Es sollte ausgewogen, abwechslungsreich und für die Kinder bezahlbar sein. Dazu gehören Gemüse, Obst, Vollkornprodukte und geeignete Eiweißquellen. Wichtig ist auch, dass die Portionen zum Alter passen.\nModerator: Wie kann man Kinder an neue Speisen gewöhnen?\nSeifert: Durch wiederholtes Probieren ohne Druck. Kinder brauchen manchmal mehrere Begegnungen mit einem Lebensmittel, bevor sie es akzeptieren. Es hilft, wenn sie bei der Auswahl beteiligt werden oder sehen, wie Gerichte zubereitet werden.\nModerator: Welche Rolle spielen Allergien und Unverträglichkeiten?\nSeifert: Sie müssen zuverlässig berücksichtigt werden. Schulen brauchen aktuelle Angaben und klare Abläufe, damit kein Kind versehentlich ein ungeeignetes Gericht erhält. Gleichzeitig sollten Alternativen angeboten werden, damit betroffene Kinder nicht ausgeschlossen sind.\nModerator: Wie wichtig ist die Atmosphäre in der Mensa?\nSeifert: Sehr wichtig. Wenn Kinder in Ruhe essen können und ausreichend Zeit haben, nehmen sie Mahlzeiten bewusster wahr. Lärm und Zeitdruck führen oft dazu, dass Essen hastig heruntergeschlungen wird.\nModerator: Was können Eltern beitragen?\nSeifert: Sie können Rückmeldungen geben und mit ihren Kindern über ausgewogene Ernährung sprechen. Schule und Familie sollten dabei zusammenarbeiten, statt sich gegenseitig Vorwürfe zu machen."]],"teil3_01.mp3":[["de-DE-KatjaNeural","Moderatorin: Sollten Schulen ausschließlich vegetarisches Mittagessen anbieten? Herr Roth, Sie sind Elternvertreter."],["de-DE-AmalaNeural","Roth: Ich halte eine verpflichtende Einschränkung für schwierig. Familien haben unterschiedliche Essgewohnheiten, und Kinder sollten lernen, verschiedene Lebensmittel ausgewogen zu kombinieren. Wichtig ist, dass die Qualität stimmt und vegetarische Gerichte attraktiv zubereitet werden."],["de-DE-KatjaNeural","Moderatorin: Frau Müller, Sie leiten eine Initiative für nachhaltige Schulverpflegung."],["de-DE-ConradNeural","Müller: Ein stärker vegetarisches Angebot kann Umweltbelastungen reduzieren. Es muss nicht bedeuten, dass es gar keine Wahl mehr gibt. Schulen könnten mehrere fleischfreie Tage einführen und regionale Zutaten verwenden."],["de-DE-AmalaNeural","Roth: Solche Tage finde ich in Ordnung, wenn Eltern informiert werden und die Gerichte ausreichend Nährstoffe enthalten."],["de-DE-ConradNeural","Müller: Genau. Außerdem sollten Kinder an der Menüplanung beteiligt werden. Wenn sie Gerichte mitentwickeln, probieren sie Neues eher aus."],["de-DE-KatjaNeural","Moderatorin: Beide Seiten unterstützen eine hochwertige Ernährung, unterscheiden sich aber bei der Frage, wie verbindlich vegetarische Angebote sein sollen."]],"teil4_01.mp3":[["de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um Schulessen und Gesundheit. Kinder benötigen Energie und Nährstoffe, um sich zu entwickeln, zu lernen und sich zu bewegen. Eine ausgewogene Mahlzeit kann dazu beitragen, dass sie am Nachmittag konzentriert bleiben. Dabei kommt es nicht auf einzelne perfekte Lebensmittel an, sondern auf eine abwechslungsreiche Ernährung über längere Zeit.\nEin gutes Schulessen sollte Gemüse, Obst, Vollkornprodukte und geeignete Eiweißquellen enthalten. Wasser sollte leicht verfügbar sein. Süße Getränke sind keine notwendige Ergänzung. Portionen müssen dem Alter und dem individuellen Bedarf entsprechen.\nAuch die Qualität der Zutaten spielt eine Rolle. Regionale und saisonale Produkte können Transportwege verkürzen und die Verbindung zur Landwirtschaft sichtbar machen. Das bedeutet nicht, dass jedes Produkt aus der unmittelbaren Umgebung stammen muss. Entscheidend sind Qualität, Verfügbarkeit und eine sinnvolle Planung.\nSchulen müssen Allergien und Unverträglichkeiten ernst nehmen. Dafür braucht es aktuelle Informationen, klare Kennzeichnungen und sichere Abläufe in der Küche. Betroffene Kinder sollen passende Alternativen erhalten und gemeinsam mit ihren Mitschülern essen können.\nSchließlich ist die Essenssituation wichtig. Ausreichend Zeit, eine angenehme Atmosphäre und Beteiligung der Kinder fördern die Akzeptanz. Schulen können Speisepläne erklären, Rückmeldungen sammeln und gemeinsam mit Eltern nach Verbesserungen suchen. Gesundes Schulessen verbindet Ernährung, Bildung und soziale Teilhabe."]]}
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
archive=ROOT/"exam-028.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
