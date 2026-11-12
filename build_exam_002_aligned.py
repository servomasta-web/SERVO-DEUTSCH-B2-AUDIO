#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild exam 002 from the exact Hören text in GoetheExam02Audio.java.
Spoken words are sourced from the app question bank; voices are German neural TTS.
"""
import asyncio, json, subprocess, zipfile
from pathlib import Path
import edge_tts

EXAM = 2
ROOT = Path("output")
AUDIO = ROOT / "audio"
AUDIO.mkdir(parents=True, exist_ok=True)
TRACKS = json.loads("{\"teil1_01.mp3\":[[\"de-DE-KatjaNeural\",\"Wegen einer kurzfristigen Reparatur ist der Aufzug am Nordausgang des Hauptbahnhofs bis morgen Mittag außer Betrieb. Reisende mit Kinderwagen oder Rollstuhl werden gebeten, den barrierefreien Zugang auf der Südseite zu benutzen. Das Servicepersonal hilft bei Bedarf vor Ort.\"]],\"teil1_02.mp3\":[[\"de-DE-KatjaNeural\",\"Ich überlege, mit dem Fahrrad zur Arbeit zu fahren.\"],[\"de-DE-ConradNeural\",\"Die Strecke ist doch ziemlich lang.\"],[\"de-DE-KatjaNeural\",\"Stimmt, aber seitdem es den neuen Radweg entlang des Flusses gibt, fühle ich mich sicherer.\"],[\"de-DE-ConradNeural\",\"Dann probier es doch zunächst an zwei Tagen pro Woche aus, statt gleich ganz umzusteigen.\"]],\"teil1_03.mp3\":[[\"de-DE-KatjaNeural\",\"Ab dem ersten Juni kostet das Monatsticket für Bus und Straßenbahn weniger. Die Ermäßigung gilt allerdings nur für Personen, die das Ticket online oder am Automaten kaufen. Im Kundenzentrum bleibt der bisherige Preis bestehen, weil dort eine persönliche Beratung angeboten wird.\"]],\"teil1_04.mp3\":[[\"de-DE-KatjaNeural\",\"Ich nutze das Leihauto nur noch selten. Früher dachte ich, es sei immer günstiger als ein eigenes Fahrzeug. Inzwischen habe ich aber festgestellt, dass ich viele Wege zu Fuß erledigen kann. Für Besuche außerhalb der Stadt nehme ich meistens den Zug und miete nur dann ein Auto, wenn es wirklich notwendig ist.\"]],\"teil1_05.mp3\":[[\"de-DE-KatjaNeural\",\"Eine Meldung aus dem Verkehrsverbund: Am kommenden Samstag werden mehrere Straßen im Zentrum für den Autoverkehr gesperrt. Die Busse fahren deshalb über eine Umleitung und halten vorübergehend nicht am Rathausplatz. Die Haltestelle am Stadtpark bleibt dagegen in Betrieb.\"]],\"teil2_01.mp3\":[[\"de-DE-ConradNeural\",\"Unsere Städte wachsen, und damit nimmt auch der Verkehr zu. Frau Dr. Seidel, viele Kommunen investieren in Radwege. Reicht das aus?\"],[\"de-DE-KatjaNeural\",\"Es ist ein wichtiger Schritt, aber allein nicht ausreichend. Menschen steigen nur dann dauerhaft um, wenn Radwege durchgehend, gut beleuchtet und von starkem Autoverkehr getrennt sind. Einzelne kurze Abschnitte schaffen noch kein zuverlässiges Netz.\"],[\"de-DE-ConradNeural\",\"Was müsste zusätzlich verbessert werden?\"],[\"de-DE-KatjaNeural\",\"Der öffentliche Nahverkehr muss häufiger fahren und besser aufeinander abgestimmt sein. Besonders außerhalb der Hauptverkehrszeiten warten Fahrgäste mancherorts sehr lange. Wer nach einem langen Arbeitstag nicht sicher nach Hause kommt, entscheidet sich oft wieder für das Auto.\"],[\"de-DE-ConradNeural\",\"Ist ein niedriger Ticketpreis der wichtigste Anreiz?\"],[\"de-DE-KatjaNeural\",\"Er hilft, doch die Verlässlichkeit ist mindestens genauso wichtig. Ein günstiges Ticket überzeugt wenig, wenn Anschlüsse regelmäßig verpasst werden. Außerdem sollten sichere Fahrradstellplätze an Bahnhöfen entstehen.\"],[\"de-DE-ConradNeural\",\"Wie kann man Menschen überzeugen, die bisher ausschließlich Auto fahren?\"],[\"de-DE-KatjaNeural\",\"Nicht mit Verboten allein. Sinnvoll sind zunächst praktische Angebote und zeitlich begrenzte Tests. Wer eine gute Verbindung selbst erlebt, verändert seine Gewohnheiten eher als durch eine bloße Werbekampagne.\"]],\"teil3_01.mp3\":[[\"de-DE-KatjaNeural\",\"In unserem Stadtgespräch geht es heute um eine autofreie Innenstadt. Herr Vogt, Sie betreiben ein Geschäft im Zentrum.\"],[\"de-DE-AmalaNeural\",\"Ich habe Bedenken. Viele Kundinnen und Kunden kommen von außerhalb und können schwere Einkäufe nicht bequem mit dem Fahrrad transportieren. Wenn Parkplätze verschwinden, könnten sie künftig in Einkaufszentren am Stadtrand fahren.\"],[\"de-DE-KatjaNeural\",\"Frau Aydin, Sie engagieren sich für bessere Luft in der Stadt.\"],[\"de-DE-KatjaNeural\",\"Die Sorge der Geschäftsleute ist verständlich. Trotzdem zeigen andere Städte, dass Fußgängerzonen mehr Menschen anziehen können, wenn Busse häufig fahren und Lieferzonen gut geplant sind. Aufenthaltsqualität ist ebenfalls ein wirtschaftlicher Faktor.\"],[\"de-DE-KatjaNeural\",\"Herr Vogt, wäre eine schrittweise Einführung denkbar?\"],[\"de-DE-AmalaNeural\",\"Ja, wenn die Stadt zuerst die Erreichbarkeit verbessert und mit den Betrieben spricht. Eine Testphase mit klaren Messkriterien wäre akzeptabel.\"],[\"de-DE-KatjaNeural\",\"Damit könnte ich leben. Wichtig wäre mir, nicht nur die Umsätze zu zählen, sondern auch Lärm, Luftqualität und die Zahl der Besucher zu untersuchen.\"],[\"de-DE-KatjaNeural\",\"Wir sehen also, dass wirtschaftliche Interessen und Umweltziele gemeinsam berücksichtigt werden müssen.\"]],\"teil4_01.mp3\":[[\"de-DE-AmalaNeural\",\"Guten Tag. Ich möchte heute erläutern, weshalb eine nachhaltige Verkehrspolitik nicht nur aus dem Bau neuer Straßen oder Radwege besteht. Zunächst muss eine Stadt verstehen, welche Wege ihre Einwohner tatsächlich zurücklegen. Dafür sind Befragungen hilfreich, aber auch anonymisierte Verkehrsdaten können ein realistisches Bild liefern.\\nAuf dieser Grundlage lassen sich Maßnahmen besser planen. In dicht besiedelten Vierteln kann es sinnvoll sein, Gehwege zu verbreitern und sichere Querungen einzurichten. In Randgebieten ist dagegen häufig eine bessere Busverbindung entscheidend. Eine einheitliche Lösung für alle Stadtteile wäre deshalb wenig zweckmäßig.\\nEin oft unterschätzter Aspekt ist die Verknüpfung verschiedener Verkehrsmittel. Wer mit dem Zug ankommt, sollte problemlos ein Fahrrad ausleihen oder einen Bus erreichen können. Dafür braucht man übersichtliche Informationen und abgestimmte Fahrpläne.\\nSchließlich darf man die Bevölkerung nicht erst informieren, wenn die Entscheidung bereits gefallen ist. Frühzeitige Gespräche können Konflikte sichtbar machen und bessere Vorschläge hervorbringen. Nach der Einführung einer Maßnahme sollte die Stadt regelmäßig prüfen, ob sie ihre Ziele erreicht. Falls nicht, müssen Anpassungen möglich sein.\"]]}")
EXPECTED = [f"teil1_0{i}.mp3" for i in range(1, 6)] + ["teil2_01.mp3", "teil3_01.mp3", "teil4_01.mp3"]

async def make_track(name, utterances):
    pieces = []
    for i, (voice, spoken_text) in enumerate(utterances):
        part = AUDIO / f".{name}.{i:03d}.mp3"
        await edge_tts.Communicate(spoken_text, voice, rate="-4%").save(str(part))
        if not part.exists() or part.stat().st_size < 500:
            raise RuntimeError(f"Audio manquant ou trop petit: {name} / {i}")
        pieces.append(part)
        if i < len(utterances) - 1:
            silence = AUDIO / f".silence_{name}_{i:03d}.mp3"
            subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t","0.55","-codec:a","libmp3lame","-b:a","64k",str(silence)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            pieces.append(silence)
    listing = AUDIO / f".{name}.concat.txt"
    listing.write_text("".join(f"file '{p.resolve()}'\n" for p in pieces), encoding="utf-8")
    target = AUDIO / name
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(listing),"-codec:a","libmp3lame","-b:a","128k",str(target)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    for p in pieces + [listing]:
        p.unlink(missing_ok=True)
    if not target.exists() or target.stat().st_size < 1024:
        raise RuntimeError(f"MP3 invalide: {name}")

async def main():
    for name in EXPECTED:
        await make_track(name, TRACKS[name])
        print(f"OK {name}: {(AUDIO/name).stat().st_size} octets", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
    archive = ROOT / f"exam-{EXAM:03d}.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for name in EXPECTED:
            z.write(AUDIO/name, arcname=name)
    with zipfile.ZipFile(archive) as z:
        if sorted(z.namelist()) != sorted(EXPECTED) or any(x.file_size < 1024 for x in z.infolist()):
            raise RuntimeError("Contenu ZIP incorrect")
    print(f"Archive validée: {archive} ({archive.stat().st_size} octets)")
