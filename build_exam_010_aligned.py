import asyncio
import subprocess
import zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output")
AUDIO=Path("audio/exam-010")
AUDIO.mkdir(parents=True,exist_ok=True)

# Prüfung 010 — Digitale Medien und Konzentration im Alltag.
tracks={
    "teil1_01.mp3": [("de-DE-KatjaNeural", "Mitteilung der Stadtbibliothek: Wegen einer technischen Umstellung bleibt der Lesesaal am kommenden Dienstag bis vierzehn Uhr geschlossen. Die Ausleihe am Automaten ist weiterhin möglich. Ab Mittwoch gelten wieder die üblichen Öffnungszeiten.")],
    "teil1_02.mp3": [("de-DE-KatjaNeural", "Du hast dein Handy abends jetzt öfter ausgeschaltet. Fällt dir das leicht?"), ("de-DE-ConradNeural", "Nicht immer. Aber ich schlafe inzwischen schneller ein. Früher habe ich noch lange Nachrichten gelesen und Videos angeschaut."), ("de-DE-KatjaNeural", "Und wie bleibst du erreichbar?"), ("de-DE-ConradNeural", "Meine Familie kann mich im Notfall über das Festnetz erreichen.")],
    "teil1_03.mp3": [("de-DE-KatjaNeural", "Hinweis des Weiterbildungszentrums: Der Kurs Digitale Bildbearbeitung beginnt nicht wie geplant am fünften Mai, sondern eine Woche später am zwölften Mai. Der Unterricht findet weiterhin donnerstags von siebzehn bis neunzehn Uhr statt. Bereits angemeldete Personen müssen nichts weiter unternehmen.")],
    "teil1_04.mp3": [("de-DE-AmalaNeural", "Seit ich im Homeoffice arbeite, mache ich mittags einen kurzen Spaziergang. Das hilft mir, den Kopf frei zu bekommen. Früher habe ich oft ohne Pause weitergearbeitet und war am Abend völlig erschöpft. Jetzt kann ich mich nach der Pause besser konzentrieren.")],
    "teil1_05.mp3": [("de-DE-KatjaNeural", "Durchsage im Stadtmuseum: Die Ausstellung über Fotografie im digitalen Zeitalter wird wegen zusätzlicher Nachfrage bis zum dreißigsten September verlängert. Der Eintritt ist jeden ersten Sonntag im Monat kostenlos. Führungen müssen weiterhin online reserviert werden.")],
    "teil2_01.mp3": [("de-DE-KatjaNeural", "Moderatorin: Viele Menschen haben das Gefühl, ständig erreichbar sein zu müssen. Herr Berger, Sie untersuchen die Auswirkungen digitaler Medien auf den Alltag. Ist diese Sorge berechtigt?"), ("de-DE-ConradNeural", "Berger: In vielen Fällen ja. Nachrichten und Benachrichtigungen unterbrechen Tätigkeiten, selbst wenn man das Telefon nur kurz überprüft. Dadurch dauert es oft länger, bis man sich wieder auf eine anspruchsvolle Aufgabe konzentrieren kann."), ("de-DE-KatjaNeural", "Moderatorin: Sollte man das Smartphone deshalb möglichst selten benutzen?"), ("de-DE-ConradNeural", "Berger: Nicht unbedingt. Digitale Geräte erleichtern Kommunikation, Organisation und Informationssuche. Entscheidend ist, ob wir sie bewusst einsetzen oder automatisch auf jeden Hinweis reagieren."), ("de-DE-KatjaNeural", "Moderatorin: Welche Regeln können helfen?"), ("de-DE-ConradNeural", "Berger: Man kann Benachrichtigungen auf das Notwendige beschränken und bestimmte Zeiten für E-Mails festlegen. Beim Lernen oder bei Gesprächen hilft es, das Gerät außer Sichtweite zu legen. Solche Regeln sollten jedoch flexibel bleiben."), ("de-DE-KatjaNeural", "Moderatorin: Was ist mit Kindern und Jugendlichen?"), ("de-DE-ConradNeural", "Berger: Verbote allein bringen wenig. Junge Menschen brauchen Orientierung und sollten lernen, Inhalte kritisch zu bewerten und ihre Bildschirmzeit selbst zu steuern. Erwachsene müssen dabei ein glaubwürdiges Vorbild sein."), ("de-DE-KatjaNeural", "Moderatorin: Kann Technik auch die Konzentration fördern?"), ("de-DE-ConradNeural", "Berger: Ja. Lernprogramme, digitale Kalender und barrierefreie Anwendungen können den Alltag erleichtern. Es kommt auf den Zweck und die Nutzungsweise an.")],
    "teil3_01.mp3": [("de-DE-KatjaNeural", "Moderator: Sollten Schulen private Smartphones während des gesamten Schultages verbieten? Frau Keller, Sie sind Lehrerin."), ("de-DE-AmalaNeural", "Keller: Ein vollständiges Verbot halte ich für zu streng. Smartphones können im Unterricht sinnvoll eingesetzt werden, etwa für Recherche oder Lernanwendungen. Allerdings braucht jede Klasse klare Regeln."), ("de-DE-KatjaNeural", "Moderator: Herr Roth, Sie vertreten eine Elterninitiative."), ("de-DE-ConradNeural", "Roth: Viele Eltern berichten, dass ihre Kinder in den Pausen kaum miteinander sprechen, weil sie auf Bildschirme schauen. Deshalb sollte das private Handy während der Pausen ausgeschaltet bleiben. Für Unterrichtszwecke kann es Ausnahmen geben."), ("de-DE-AmalaNeural", "Keller: Pausen sind tatsächlich wichtig für persönliche Kontakte. Trotzdem sollten Schulen auch Medienkompetenz vermitteln, statt digitale Geräte grundsätzlich als Störung zu betrachten."), ("de-DE-ConradNeural", "Roth: Medienkompetenz ist notwendig, aber sie entsteht nicht dadurch, dass Jugendliche jederzeit online sind. Ein handyfreier Zeitraum kann helfen, sich auf andere Aktivitäten zu konzentrieren."), ("de-DE-KatjaNeural", "Moderator: Beide Gesprächspartner befürworten klare Regeln, sind sich aber uneinig, wie weit Einschränkungen gehen sollten.")],
    "teil4_01.mp3": [("de-DE-AmalaNeural", "Guten Tag. In meinem Vortrag beschäftige ich mich mit digitaler Mediennutzung und Konzentration. Digitale Geräte sind aus Beruf, Bildung und Freizeit kaum wegzudenken. Sie ermöglichen schnellen Informationsaustausch und erleichtern viele organisatorische Aufgaben. Gleichzeitig kann die ständige Verfügbarkeit von Nachrichten unsere Aufmerksamkeit belasten. Besonders problematisch sind häufige Unterbrechungen. Wenn während einer Aufgabe mehrere Benachrichtigungen erscheinen, wechseln wir immer wieder zwischen verschiedenen Tätigkeiten. Dieser Wechsel kostet Zeit und kann die Fehlerquote erhöhen. Eine bewusste Nutzung bedeutet deshalb nicht, auf digitale Medien zu verzichten. Vielmehr sollte man entscheiden, wann und wofür man sie einsetzt. Hilfreich sind feste Zeiten für E-Mails, ausgeschaltete Hinweise und Pausen ohne Bildschirm. Auch die Gestaltung des Arbeitsplatzes spielt eine Rolle. Ein aufgeräumter Schreibtisch und ein Gerät außer Sichtweite können Ablenkungen reduzieren. Im Bildungsbereich sollten Schülerinnen und Schüler lernen, Informationen zu prüfen, Quellen zu vergleichen und persönliche Daten zu schützen. Dabei sind Erwachsene gefordert, nicht nur Regeln aufzustellen, sondern selbst einen verantwortungsvollen Umgang vorzuleben. Andererseits bieten digitale Medien große Chancen: Lernplattformen ermöglichen individuelles Üben, Übersetzungsprogramme unterstützen den Spracherwerb und digitale Kalender helfen bei der Planung. Entscheidend ist, dass die Technik einem konkreten Ziel dient und nicht jede freie Minute füllt. Abschließend lässt sich festhalten: Konzentration entsteht nicht durch einen vollständigen Verzicht auf digitale Geräte, sondern durch bewusste Entscheidungen, klare Gewohnheiten und ausreichende Erholungszeiten.")],
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
