#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild exam 003 from the exact Hören text in GoetheExam03Audio.java.
Spoken words are sourced from the app question bank; voices are German neural TTS.
"""
import asyncio, json, subprocess, zipfile
from pathlib import Path
import edge_tts

EXAM = 3
ROOT = Path("output")
AUDIO = ROOT / "audio"
AUDIO.mkdir(parents=True, exist_ok=True)
TRACKS = json.loads("{\"teil1_01.mp3\":[[\"de-DE-KatjaNeural\",\"Liebe Eltern, am Donnerstag findet der Informationsabend zur neuen Lernplattform nicht wie angekündigt in der Aula, sondern im Raum 204 statt. Beginn ist weiterhin um 18 Uhr. Bitte bringen Sie, wenn möglich, ein eigenes Smartphone oder Tablet mit. Die Schule stellt einige Leihgeräte bereit, kann aber nicht alle Teilnehmenden ausstatten.\"]],\"teil1_02.mp3\":[[\"de-DE-KatjaNeural\",\"Unsere Klasse soll künftig digitale Hausaufgaben bekommen.\"],[\"de-DE-ConradNeural\",\"Ich finde das praktisch, aber was ist mit Kindern ohne Internet zu Hause?\"],[\"de-DE-KatjaNeural\",\"Die Lehrerin hat gesagt, dass wir Aufgaben auch in der Schulbibliothek erledigen können. Außerdem dürfen wir weiterhin eine Papierversion bekommen, wenn wir sie brauchen.\"]],\"teil1_03.mp3\":[[\"de-DE-KatjaNeural\",\"Im Medienzentrum der Stadt beginnt nächste Woche ein kostenloser Kurs für Lehrkräfte. Dabei geht es nicht um die Bedienung einzelner Geräte, sondern darum, digitale Quellen kritisch zu bewerten und Datenschutz im Unterricht zu berücksichtigen. Anmeldungen sind bis Freitag über die Internetseite des Zentrums möglich.\"]],\"teil1_04.mp3\":[[\"de-DE-KatjaNeural\",\"Ich habe früher fast jede Unterrichtsstunde mit Präsentationsfolien vorbereitet. Inzwischen verwende ich digitale Medien gezielter. Bei einer Diskussion lasse ich die Geräte bewusst geschlossen, damit die Schülerinnen und Schüler einander zuhören. Für Rechercheaufgaben sind Tablets dagegen sehr hilfreich.\"]],\"teil1_05.mp3\":[[\"de-DE-KatjaNeural\",\"Hinweis für die Teilnehmenden des Schülerprojekts: Die geplante Ausstellung der selbst programmierten Lernspiele wird um eine Woche verschoben. Der Grund ist nicht ein technisches Problem, sondern die hohe Zahl an Anmeldungen anderer Klassen. Dadurch benötigen wir einen größeren Ausstellungsraum.\"]],\"teil2_01.mp3\":[[\"de-DE-ConradNeural\",\"Frau Professorin Keller, viele Schulen haben in den vergangenen Jahren Tablets angeschafft. Bedeutet das automatisch besseren Unterricht?\"],[\"de-DE-KatjaNeural\",\"Nein. Ein Gerät ist zunächst nur ein Werkzeug. Entscheidend ist, ob es ein konkretes Lernziel unterstützt. Wenn Schülerinnen und Schüler beispielsweise gemeinsam Daten auswerten, kann eine digitale Anwendung einen echten Mehrwert bieten. Eine bloße Digitalisierung des Arbeitsblatts bringt dagegen nicht unbedingt etwas.\"],[\"de-DE-ConradNeural\",\"Kritiker befürchten, dass Kinder dadurch mehr Zeit vor Bildschirmen verbringen.\"],[\"de-DE-KatjaNeural\",\"Diese Sorge sollte man ernst nehmen. Digitale Phasen müssen sinnvoll begrenzt werden. Unterricht braucht weiterhin Gespräche, Bewegung, handschriftliche Notizen und praktische Erfahrungen. Es geht nicht darum, analoge Methoden zu verdrängen, sondern beide Formen passend zu kombinieren.\"],[\"de-DE-ConradNeural\",\"Welche Rolle spielt die Ausbildung der Lehrkräfte?\"],[\"de-DE-KatjaNeural\",\"Eine sehr große. Lehrkräfte müssen nicht jede neue Anwendung sofort beherrschen. Sie sollten aber beurteilen können, ob eine Quelle zuverlässig ist, welche Daten ein Dienst sammelt und ob eine Anwendung für die jeweilige Altersgruppe geeignet ist. Dafür brauchen sie regelmäßige Fortbildungen und Zeit zum Austausch.\"],[\"de-DE-ConradNeural\",\"Und wie lässt sich verhindern, dass manche Kinder abgehängt werden?\"],[\"de-DE-KatjaNeural\",\"Schulen müssen Geräte verleihen und Lernorte mit Internetzugang anbieten. Außerdem sollten wichtige Aufgaben auch ohne private Technik erledigt werden können. Chancengleichheit darf nicht vom Einkommen der Eltern abhängen.\"]],\"teil3_01.mp3\":[[\"de-DE-ConradNeural\",\"Sollten Schulen private Smartphones während des Unterrichts verbieten? Herr Brandt, Sie leiten eine Schule.\"],[\"de-DE-AmalaNeural\",\"Ein vollständiges Verbot halte ich für schwer umsetzbar. Wir haben klare Regeln eingeführt: Während Erklärungen bleiben die Geräte in der Tasche. Für bestimmte Rechercheaufgaben dürfen Lehrkräfte sie gezielt freigeben.\"],[\"de-DE-ConradNeural\",\"Frau Nguyen, Sie vertreten einen Elternverein.\"],[\"de-DE-AmalaNeural\",\"Mir ist wichtig, dass die Regeln für alle verständlich sind. Manche Eltern möchten ihre Kinder in Pausen erreichen können. Deshalb sollte es eine erreichbare Ansprechperson im Sekretariat geben. Im Unterricht selbst sehe ich private Nachrichten allerdings kritisch.\"],[\"de-DE-ConradNeural\",\"Herr Özdemir, Sie unterrichten Medienkunde.\"],[\"de-DE-AmalaNeural\",\"Ein Verbot löst das Problem nicht dauerhaft. Jugendliche müssen lernen, Benachrichtigungen zu kontrollieren und Quellen zu prüfen. Dafür braucht es Unterricht und gemeinsame Vereinbarungen. Bei Prüfungen sind ausgeschaltete Geräte selbstverständlich notwendig.\"],[\"de-DE-KatjaNeural\",\"Mit verbindlichen Regeln und pädagogischen Ausnahmen kann ich mich einverstanden erklären.\"],[\"de-DE-AmalaNeural\",\"Entscheidend ist, dass Schulen die Eltern frühzeitig informieren und die Regeln regelmäßig überprüfen.\"]],\"teil4_01.mp3\":[[\"de-DE-AmalaNeural\",\"Guten Tag. In meinem Vortrag geht es um den sinnvollen Umgang mit digitalen Lernmaterialien. Zunächst sollte man zwischen Informationssuche und tatsächlichem Lernen unterscheiden. Eine Suchmaschine liefert in Sekunden zahlreiche Ergebnisse, aber nicht jede gefundene Seite ist fachlich zuverlässig. Lernende müssen deshalb Autorenschaft, Aktualität und Absicht einer Veröffentlichung prüfen.\\nEin zweiter Punkt betrifft die Zusammenarbeit. Gemeinsame digitale Dokumente ermöglichen es, Ideen gleichzeitig zu sammeln und zu überarbeiten. Damit diese Arbeit gelingt, braucht die Gruppe klare Aufgaben und Regeln. Sonst besteht die Gefahr, dass einzelne Personen den größten Teil übernehmen, während andere kaum beteiligt sind.\\nAuch der Datenschutz verdient Aufmerksamkeit. Kostenlose Angebote finanzieren sich teilweise durch die Auswertung persönlicher Daten. Schulen sollten daher prüfen, welche Informationen gespeichert werden und ob ein Dienst den geltenden Datenschutzanforderungen entspricht. Private Konten der Kinder dürfen nicht ohne sorgfältige Prüfung vorausgesetzt werden.\\nSchließlich ist die technische Ausstattung nicht mit pädagogischer Qualität gleichzusetzen. Ein stabiler Internetzugang und funktionierende Geräte sind wichtige Voraussetzungen, ersetzen aber keine gute Unterrichtsplanung. Lehrkräfte benötigen Zeit, um Materialien auszuwählen, Aufgaben anzupassen und Erfahrungen miteinander auszutauschen.\\nMein Fazit lautet: Digitale Medien können Unterricht bereichern, wenn sie bewusst, kritisch und altersgerecht eingesetzt werden. Ihr Wert zeigt sich nicht an der Zahl der Geräte, sondern daran, was die Lernenden damit verstehen und selbstständig leisten können.\"]]}")
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
