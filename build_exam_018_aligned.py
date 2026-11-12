import asyncio
import subprocess
import zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output")
AUDIO=ROOT/"audio"
AUDIO.mkdir(parents=True,exist_ok=True)

# Prüfung 018 — Nachhaltige Mobilität in der Stadt.
# Acht eigenständige, inhaltlich mit den Aufgaben abgestimmte Hörtexte.
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Verkehrshinweis der Stadt: Der Radweg an der Lindenstraße ist am Donnerstag wegen Bauarbeiten gesperrt. Radfahrerinnen und Radfahrer werden gebeten, die ausgeschilderte Umleitung über die Hafenstraße zu benutzen. Ab Freitagmorgen ist der Radweg voraussichtlich wieder frei.")],
"teil1_02.mp3":[("de-DE-ConradNeural","A: Weißt du, ob man sich für das Reparaturcafé anmelden muss? B: Nein, eine Anmeldung ist nicht nötig. Die Fachleute schauen sich das Fahrrad zunächst kostenlos an. Wenn Ersatzteile gebraucht werden, muss man diese allerdings selbst bezahlen. A: Soll ich etwas mitbringen? B: Am besten dein Fahrrad und möglichst genaue Angaben zum Modell.")],
"teil1_03.mp3":[("de-DE-KatjaNeural","Information zum neuen Carsharing-Angebot: Ab Montag stehen im Stadtgebiet zwölf Elektroautos zur Verfügung. Wer sie nutzen möchte, muss sich zunächst über die Carsharing-App registrieren und seinen Führerschein bestätigen lassen. Die Abrechnung erfolgt nach der tatsächlichen Nutzungsdauer.")],
"teil1_04.mp3":[("de-DE-AmalaNeural","Seit einigen Wochen fahre ich mit dem Bus zur Arbeit. Früher kam abends alle zehn Minuten ein Bus. Jetzt wurde der Fahrplan geändert: In den Abendstunden fährt er nur noch alle zwanzig Minuten. Die Stadt begründet das damit, dass zu dieser Zeit deutlich weniger Fahrgäste unterwegs sind. Morgens bleibt der bisherige Takt bestehen.")],
"teil1_05.mp3":[("de-DE-KatjaNeural","Durchsage am Hauptbahnhof: Wegen einer technischen Störung an der Signaltechnik fällt der Regionalzug um 18 Uhr heute aus. Ein Ersatzbus in Richtung Neustadt steht gegenüber dem Bahnhof bereit und fährt um 18 Uhr 10 ab. Bereits gekaufte Fahrkarten gelten auch im Ersatzbus.")],
"teil2_01.mp3":[("de-DE-KatjaNeural","Moderatorin: Viele Städte wollen den Verkehr umweltfreundlicher gestalten. Herr Dr. Weber, Sie beraten Kommunen bei der Verkehrsplanung. Was ist das wichtigste Ziel eines nachhaltigen Mobilitätskonzepts?\nWeber: Es geht nicht darum, das Auto einfach abzuschaffen. Vielmehr sollten Bus, Bahn, Fahrrad und Fußverkehr so miteinander verbunden werden, dass Menschen für unterschiedliche Wege eine passende Alternative haben.\nModeratorin: Reicht es, dafür neue Radwege zu bauen?\nWeber: Nein. Radwege müssen sicher und durchgehend sein. Außerdem braucht man gute Abstellmöglichkeiten, etwa an Bahnhöfen. Wenn ein Radweg plötzlich endet oder eine gefährliche Kreuzung kommt, werden viele Menschen das Fahrrad nicht regelmäßig nutzen.\nModeratorin: Wie lässt sich der öffentliche Nahverkehr attraktiver machen?\nWeber: Entscheidend sind Zuverlässigkeit, verständliche Tarife und Anschlüsse, die aufeinander abgestimmt sind. Ein günstiger Preis hilft wenig, wenn der Bus häufig ausfällt oder man lange auf den Anschluss warten muss.\nModeratorin: Welche Chancen bieten Sharing-Angebote?\nWeber: Sie können eine Ergänzung sein, besonders für Wege, die mit Bus oder Bahn nicht direkt zurückgelegt werden können. Allerdings müssen die Fahrzeuge sinnvoll verteilt und regelmäßig gewartet werden. Außerdem sollte man darauf achten, dass solche Angebote nicht nur in wohlhabenden Stadtteilen verfügbar sind.\nModeratorin: Wie können Einwohnerinnen und Einwohner beteiligt werden?\nWeber: Durch Befragungen, öffentliche Gespräche und zeitlich begrenzte Testprojekte. Wenn man eine neue Verkehrsführung zunächst ausprobiert, lassen sich Probleme erkennen, bevor viel Geld ausgegeben wird.\nModeratorin: Woran erkennt man schließlich, ob ein Konzept erfolgreich ist?\nWeber: Nicht nur an der Zahl neuer Radwege oder gekaufter Busse. Man sollte untersuchen, ob mehr Menschen umsteigen, ob wichtige Orte besser erreichbar sind und ob sich die Verkehrssicherheit verbessert.")],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Bei der Verkehrswende treffen unterschiedliche Interessen aufeinander. Herr Brandt, Sie arbeiten in einem städtischen Verkehrsplanungsbüro. Was ist aus Ihrer Sicht besonders wichtig?"),
("de-DE-ConradNeural","Brandt: Zunächst brauchen wir verlässliche Busverbindungen. Wenn Menschen nicht sicher sein können, pünktlich zur Arbeit zu kommen, bleiben sie beim Auto. Neue Radwege sind sinnvoll, aber sie lösen das Problem nicht allein. Ein Konzept sollte außerdem in einem Stadtteil getestet werden, bevor man es überall einführt. Bei der Finanzierung müssen wir nicht nur die Baukosten, sondern auch Wartung und Betrieb langfristig berücksichtigen."),
("de-DE-KatjaNeural","Moderatorin: Frau Yilmaz, Sie vertreten einen Verein, der sich für sichere und barrierefreie Wege einsetzt. Wo sehen Sie Handlungsbedarf?"),
("de-DE-AmalaNeural","Yilmaz: Die Bedürfnisse älterer Menschen werden oft übersehen. Breite Gehwege, ausreichend Sitzgelegenheiten und sichere Querungen sind für sie entscheidend. Auch Kinder müssen selbstständig und gefahrlos zur Schule kommen können. Ich wünsche mir außerdem, dass die Stadt regelmäßig veröffentlicht, welche Vorschläge aus der Bevölkerung tatsächlich umgesetzt wurden."),
("de-DE-ConradNeural","Brandt: Bei der Beteiligung stimme ich Ihnen zu. Allerdings müssen Entscheidungen auch irgendwann getroffen werden. Deshalb sollten Rückmeldungen früh gesammelt und nach nachvollziehbaren Kriterien bewertet werden."),
("de-DE-AmalaNeural","Yilmaz: Das sehe ich ähnlich. Wichtig ist, dass Beteiligung nicht nur symbolisch stattfindet. Die Menschen müssen erkennen können, welchen Einfluss ihre Hinweise auf die Planung hatten."),
("de-DE-KatjaNeural","Moderatorin: Vielen Dank. Deutlich wird, dass gute Verkehrsplanung sowohl zuverlässige Angebote als auch Sicherheit, Zugänglichkeit und transparente Beteiligung braucht.")
],
"teil4_01.mp3":[("de-DE-ConradNeural","Guten Tag. In meinem Vortrag beschäftige ich mich mit nachhaltiger Mobilität in Städten. Dabei geht es nicht allein um den Klimaschutz. Wie Menschen unterwegs sind, beeinflusst auch ihre Gesundheit, die Lebensqualität in den Stadtvierteln und den Zugang zu Arbeitsplätzen, Schulen und medizinischen Einrichtungen.\nEin wichtiger Ansatz besteht darin, verschiedene Verkehrsmittel miteinander zu verbinden. An sogenannten Mobilitätsstationen können Fahrgäste beispielsweise vom Bus auf ein Leihfahrrad oder ein Carsharing-Fahrzeug umsteigen. Solche Stationen sind besonders hilfreich, wenn sie gut erreichbar und übersichtlich gestaltet sind.\nDer Radverkehr braucht ebenfalls eine durchdachte Infrastruktur. Einzelne kurze Radwege reichen nicht aus. Wichtig sind durchgehende Verbindungen, sichere Kreuzungen, gute Beleuchtung und genügend Abstellplätze. Nur dann können auch Menschen, die bisher selten Fahrrad fahren, Vertrauen gewinnen.\nBeim öffentlichen Nahverkehr spielen Zuverlässigkeit und einfache Nutzung eine zentrale Rolle. Fahrpläne müssen verständlich sein, Anschlüsse sollten zusammenpassen und Tarife dürfen nicht unnötig kompliziert sein. Digitale Anwendungen können die Orientierung erleichtern. Sie sind jedoch keine vollständige Lösung, denn nicht alle Menschen besitzen ein geeignetes Smartphone oder verfügen über ausreichende digitale Kenntnisse. Deshalb müssen Informationen auch auf anderen Wegen zugänglich bleiben.\nSharing-Angebote können Lücken im Verkehrsnetz schließen. Damit sie einen wirklichen Beitrag leisten, müssen Fahrzeuge regelmäßig gewartet und in verschiedenen Stadtteilen verfügbar sein. Außerdem sollte geprüft werden, ob die Preise für unterschiedliche Bevölkerungsgruppen erschwinglich sind.\nSchließlich ist die Beteiligung der Bevölkerung wichtig. Befragungen und zeitlich begrenzte Versuche machen sichtbar, welche Bedürfnisse bestehen und wo Schwierigkeiten auftreten. Nach der Einführung eines Konzepts sollte die Stadt regelmäßig überprüfen, ob sich Sicherheit, Erreichbarkeit und Verkehrsmittelwahl tatsächlich verbessert haben. Nachhaltige Mobilität entsteht also durch das Zusammenspiel von Infrastruktur, zuverlässigen Angeboten, sozialer Zugänglichkeit und langfristiger Planung.")]}
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
archive=ROOT/"exam-018.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
