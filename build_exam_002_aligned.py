import asyncio
import subprocess
import zipfile
from pathlib import Path
import edge_tts

ROOT = Path("output")
AUDIO = ROOT / "audio"
AUDIO.mkdir(parents=True, exist_ok=True)

async def make_track(name, utterances):
    parts = []
    for i, (voice, spoken_text) in enumerate(utterances):
        part = AUDIO / f".{name}.{i:02d}.mp3"
        last_error = None
        for attempt in range(1, 6):
            try:
                print(f"{name}: réplique {i + 1}/{len(utterances)}, {voice}, essai {attempt}/5", flush=True)
                await edge_tts.Communicate(spoken_text, voice, rate="-4%").save(str(part))
                if not part.exists() or part.stat().st_size < 1000:
                    raise RuntimeError("Fichier audio absent ou trop petit")
                last_error = None
                break
            except Exception as exc:
                last_error = exc
                part.unlink(missing_ok=True)
                print(f"Erreur {name}, réplique {i + 1}, {voice}: {exc}", flush=True)
                if attempt < 5:
                    await asyncio.sleep(2 * attempt)
        if last_error is not None:
            raise RuntimeError(f"Échec définitif pour {name}, réplique {i + 1}") from last_error
        parts.append(part)
        await asyncio.sleep(1)
        if i < len(utterances) - 1:
            silence = AUDIO / f".silence_{name}_{i}.mp3"
            subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                            "-t", "0.65", "-codec:a", "libmp3lame", "-b:a", "64k", str(silence)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            parts.append(silence)
    listing = AUDIO / f".{name}.txt"
    listing.write_text("".join(f"file '{p.resolve()}'\n" for p in parts), encoding="utf-8")
    target = AUDIO / name
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
                    "-codec:a", "libmp3lame", "-b:a", "128k", str(target)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    for part in parts + [listing]:
        part.unlink(missing_ok=True)
    if not target.exists() or target.stat().st_size < 1024:
        raise RuntimeError(f"Piste finale invalide : {name}")
    print(f"OK {name}: {target.stat().st_size} octets", flush=True)

# Prüfung 002 — Nachhaltige Mobilität in Großstädten.
# Audioinhalte stimmen mit GoetheExam02Audio.java in der App überein.
tracks = {
"teil1_01.mp3": [("de-DE-KatjaNeural", "Achtung an alle Fahrgäste: Wegen einer kurzfristigen Reparatur ist der Aufzug am Nordausgang des Hauptbahnhofs bis morgen Mittag außer Betrieb. Reisende mit Kinderwagen oder Rollstuhl werden gebeten, den barrierefreien Zugang auf der Südseite zu benutzen. Das Servicepersonal hilft bei Bedarf vor Ort.")],
"teil1_02.mp3": [("de-DE-KatjaNeural", "Ich überlege, mit dem Fahrrad zur Arbeit zu fahren."), ("de-DE-ConradNeural", "Die Strecke ist doch ziemlich lang."), ("de-DE-KatjaNeural", "Stimmt, aber seitdem es den neuen Radweg entlang des Flusses gibt, fühle ich mich sicherer."), ("de-DE-ConradNeural", "Dann probier es doch zunächst an zwei Tagen pro Woche aus, statt gleich ganz umzusteigen.")],
"teil1_03.mp3": [("de-DE-KatjaNeural", "Die Stadtverwaltung informiert: Ab dem ersten Juni kostet das Monatsticket für Bus und Straßenbahn weniger. Die Ermäßigung gilt allerdings nur für Personen, die das Ticket online oder am Automaten kaufen. Im Kundenzentrum bleibt der bisherige Preis bestehen, weil dort eine persönliche Beratung angeboten wird.")],
"teil1_04.mp3": [("de-DE-AmalaNeural", "Ich nutze das Leihauto nur noch selten. Früher dachte ich, es sei immer günstiger als ein eigenes Fahrzeug. Inzwischen habe ich aber festgestellt, dass ich viele Wege zu Fuß erledigen kann. Für Besuche außerhalb der Stadt nehme ich meistens den Zug und miete nur dann ein Auto, wenn es wirklich notwendig ist.")],
"teil1_05.mp3": [("de-DE-KatjaNeural", "Eine Meldung aus dem Verkehrsverbund: Am kommenden Samstag werden mehrere Straßen im Zentrum für den Autoverkehr gesperrt. Die Busse fahren deshalb über eine Umleitung und halten vorübergehend nicht am Rathausplatz. Die Haltestelle am Stadtpark bleibt dagegen in Betrieb.")],
"teil2_01.mp3": [
("de-DE-KatjaNeural", "Moderator: Unsere Städte wachsen, und damit nimmt auch der Verkehr zu. Frau Dr. Seidel, viele Kommunen investieren in Radwege. Reicht das aus?"),
("de-DE-AmalaNeural", "Expertin: Es ist ein wichtiger Schritt, aber allein nicht ausreichend. Menschen steigen nur dann dauerhaft um, wenn Radwege durchgehend, gut beleuchtet und von starkem Autoverkehr getrennt sind. Einzelne kurze Abschnitte schaffen noch kein zuverlässiges Netz."),
("de-DE-KatjaNeural", "Moderator: Was müsste zusätzlich verbessert werden?"),
("de-DE-AmalaNeural", "Expertin: Der öffentliche Nahverkehr muss häufiger fahren und besser aufeinander abgestimmt sein. Besonders außerhalb der Hauptverkehrszeiten warten Fahrgäste mancherorts sehr lange. Wer nach einem langen Arbeitstag nicht sicher nach Hause kommt, entscheidet sich oft wieder für das Auto."),
("de-DE-KatjaNeural", "Moderator: Ist ein niedriger Ticketpreis der wichtigste Anreiz?"),
("de-DE-AmalaNeural", "Expertin: Er hilft, doch die Verlässlichkeit ist mindestens genauso wichtig. Ein günstiges Ticket überzeugt wenig, wenn Anschlüsse regelmäßig verpasst werden. Außerdem sollten sichere Fahrradstellplätze an Bahnhöfen entstehen."),
("de-DE-KatjaNeural", "Moderator: Wie kann man Menschen überzeugen, die bisher ausschließlich Auto fahren?"),
("de-DE-AmalaNeural", "Expertin: Nicht mit Verboten allein. Sinnvoll sind zunächst praktische Angebote und zeitlich begrenzte Tests. Wer eine gute Verbindung selbst erlebt, verändert seine Gewohnheiten eher als durch eine bloße Werbekampagne.")
],
"teil3_01.mp3": [
("de-DE-KatjaNeural", "Moderatorin: In unserem Stadtgespräch geht es heute um eine autofreie Innenstadt. Herr Vogt, Sie betreiben ein Geschäft im Zentrum."),
("de-DE-ConradNeural", "Vogt: Ich habe Bedenken. Viele Kundinnen und Kunden kommen von außerhalb und können schwere Einkäufe nicht bequem mit dem Fahrrad transportieren. Wenn Parkplätze verschwinden, könnten sie künftig in Einkaufszentren am Stadtrand fahren."),
("de-DE-KatjaNeural", "Moderatorin: Frau Aydin, Sie engagieren sich für bessere Luft in der Stadt."),
("de-DE-AmalaNeural", "Aydin: Die Sorge der Geschäftsleute ist verständlich. Trotzdem zeigen andere Städte, dass Fußgängerzonen mehr Menschen anziehen können, wenn Busse häufig fahren und Lieferzonen gut geplant sind. Aufenthaltsqualität ist ebenfalls ein wirtschaftlicher Faktor."),
("de-DE-KatjaNeural", "Moderatorin: Herr Vogt, wäre eine schrittweise Einführung denkbar?"),
("de-DE-ConradNeural", "Vogt: Ja, wenn die Stadt zuerst die Erreichbarkeit verbessert und mit den Betrieben spricht. Eine Testphase mit klaren Messkriterien wäre akzeptabel."),
("de-DE-AmalaNeural", "Aydin: Damit könnte ich leben. Wichtig wäre mir, nicht nur die Umsätze zu zählen, sondern auch Lärm, Luftqualität und die Zahl der Besucher zu untersuchen."),
("de-DE-KatjaNeural", "Moderatorin: Wir sehen also, dass wirtschaftliche Interessen und Umweltziele gemeinsam berücksichtigt werden müssen.")
],
"teil4_01.mp3": [("de-DE-ConradNeural", "Guten Tag. Ich möchte heute erläutern, weshalb eine nachhaltige Verkehrspolitik nicht nur aus dem Bau neuer Straßen oder Radwege besteht. Zunächst muss eine Stadt verstehen, welche Wege ihre Einwohner tatsächlich zurücklegen. Dafür sind Befragungen hilfreich, aber auch anonymisierte Verkehrsdaten können ein realistisches Bild liefern. Auf dieser Grundlage lassen sich Maßnahmen besser planen. In dicht besiedelten Vierteln kann es sinnvoll sein, Gehwege zu verbreitern und sichere Querungen einzurichten. In Randgebieten ist dagegen häufig eine bessere Busverbindung entscheidend. Eine einheitliche Lösung für alle Stadtteile wäre deshalb wenig zweckmäßig. Ein oft unterschätzter Aspekt ist die Verknüpfung verschiedener Verkehrsmittel. Wer mit dem Zug ankommt, sollte problemlos ein Fahrrad ausleihen oder einen Bus erreichen können. Dafür braucht man übersichtliche Informationen und abgestimmte Fahrpläne. Schließlich darf man die Bevölkerung nicht erst informieren, wenn die Entscheidung bereits gefallen ist. Frühzeitige Gespräche können Konflikte sichtbar machen und bessere Vorschläge hervorbringen. Nach der Einführung einer Maßnahme sollte die Stadt regelmäßig prüfen, ob sie ihre Ziele erreicht. Falls nicht, müssen Anpassungen möglich sein.")]
}

async def main():
    expected = ["teil1_01.mp3","teil1_02.mp3","teil1_03.mp3","teil1_04.mp3",
                "teil1_05.mp3","teil2_01.mp3","teil3_01.mp3","teil4_01.mp3"]
    if set(tracks) != set(expected):
        raise RuntimeError(f"Liste de pistes incorrecte: {sorted(tracks)}")
    for name in expected:
        await make_track(name, tracks[name])

asyncio.run(main())

archive = ROOT / "exam-002.zip"
expected = ["teil1_01.mp3","teil1_02.mp3","teil1_03.mp3","teil1_04.mp3",
            "teil1_05.mp3","teil2_01.mp3","teil3_01.mp3","teil4_01.mp3"]
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
    for name in expected:
        z.write(AUDIO / name, arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist()) != sorted(expected):
        raise RuntimeError(f"Contenu ZIP inattendu : {z.namelist()}")
    for info in z.infolist():
        if info.file_size < 1024:
            raise RuntimeError(f"Piste ZIP invalide : {info.filename}")
print(f"Archive validée : {archive} ({archive.stat().st_size} octets)", flush=True)
