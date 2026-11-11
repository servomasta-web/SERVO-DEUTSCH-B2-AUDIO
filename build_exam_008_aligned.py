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
"teil1_01.mp3":[("de-DE-KatjaNeural","Mitteilung der Wohnungsverwaltung: Am Dienstag werden im Haus B die Wasserzähler abgelesen. Die Mitarbeitenden beginnen im Erdgeschoss um acht Uhr. Wer nicht zu Hause ist, kann bis Freitag einen Ersatztermin vereinbaren. Die Kosten sind bereits in den Nebenkosten enthalten.")],
"teil1_02.mp3":[("de-DE-KatjaNeural","Du wohnst jetzt auf dem Land. Vermisst du die Stadt?"),("de-DE-ConradNeural","Manchmal, besonders die kurzen Wege zu kulturellen Angeboten. Dafür habe ich mehr Platz und kann im Garten arbeiten."),("de-DE-KatjaNeural","Und wie kommst du zur Arbeit?"),("de-DE-ConradNeural","Ich fahre meistens mit dem Zug; das dauert etwas länger, ist aber zuverlässig.")],
"teil1_03.mp3":[("de-DE-KatjaNeural","Hinweis des Bürgerbüros: Für die Beratung zum Wohngeld ist ab sofort eine vorherige Terminvereinbarung nötig. Unterlagen können weiterhin online eingereicht werden. Wer keinen Internetzugang hat, erhält Unterstützung am Empfang im Erdgeschoss.")],
"teil1_04.mp3":[("de-DE-AmalaNeural","Ich habe mich bewusst für eine kleinere Wohnung in der Nähe meines Arbeitsplatzes entschieden. Die Miete pro Quadratmeter ist höher als am Stadtrand, aber ich spare Fahrtkosten und gewinne jeden Tag Zeit. Einen Balkon hätte ich trotzdem gern.")],
"teil1_05.mp3":[("de-DE-KatjaNeural","Durchsage im Wohnquartier: Die Arbeiten am neuen Spielplatz verzögern sich wegen starker Regenfälle. Die Eröffnung findet nicht wie angekündigt am kommenden Samstag, sondern voraussichtlich zwei Wochen später statt. Über den endgültigen Termin informiert die Stadt auf ihrer Internetseite.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Viele Menschen überlegen, ob sie lieber in einer Großstadt oder in einer kleineren Gemeinde wohnen möchten. Frau Hartmann, Sie beraten Kommunen zur Wohnraumentwicklung. Welche Faktoren sind bei dieser Entscheidung besonders wichtig?"),
("de-DE-AmalaNeural","Hartmann: Man sollte nicht nur die Mietpreise vergleichen. Entscheidend sind auch Arbeitswege, Einkaufsmöglichkeiten, medizinische Versorgung und soziale Kontakte. Eine günstige Wohnung kann teuer werden, wenn man täglich lange Strecken zurücklegen muss."),
("de-DE-KatjaNeural","Moderatorin: Welche Vorteile bietet das Leben auf dem Land?"),
("de-DE-AmalaNeural","Hartmann: Häufig gibt es mehr Wohnfläche, Zugang zur Natur und eine ruhigere Umgebung. Familien finden manchmal leichter ein Haus mit Garten. Allerdings ist man stärker auf ein Auto angewiesen, wenn Busse nur selten fahren."),
("de-DE-KatjaNeural","Moderatorin: Und was spricht für die Stadt?"),
("de-DE-AmalaNeural","Hartmann: Dort liegen Arbeitsplätze, Hochschulen und kulturelle Einrichtungen oft näher beieinander. Viele Wege lassen sich mit öffentlichen Verkehrsmitteln oder dem Fahrrad erledigen. Dafür sind Wohnungen häufig kleiner und die Mieten höher."),
("de-DE-KatjaNeural","Moderatorin: Kann man die Unterschiede verringern?"),
("de-DE-AmalaNeural","Hartmann: Ja. Ländliche Regionen brauchen zuverlässige Verkehrsverbindungen und digitale Infrastruktur. Städte wiederum sollten bezahlbaren Wohnraum schaffen und Grünflächen erhalten. Außerdem können kleinere Orte durch gemeinschaftliche Arbeitsräume und medizinische Angebote attraktiver werden."),
("de-DE-KatjaNeural","Moderatorin: Was raten Sie Menschen, die umziehen möchten?"),
("de-DE-AmalaNeural","Hartmann: Sie sollten ihren Alltag realistisch planen. Ein Probewohnen oder mehrere Besuche zu verschiedenen Tageszeiten können zeigen, ob ein Ort wirklich zu den eigenen Bedürfnissen passt.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderator: Sollten mehr Menschen aus Großstädten in kleinere Gemeinden ziehen, um die Wohnungsnot zu lindern? Herr Reuter, Sie vertreten einen Mieterverein."),
("de-DE-ConradNeural","Reuter: Ein Umzug kann für einzelne Haushalte sinnvoll sein, aber er darf nicht als einfache Lösung dargestellt werden. Viele Menschen sind an ihren Arbeitsplatz, Schulen oder die Pflege von Angehörigen gebunden. Außerdem fehlen in manchen Gemeinden passende Mietwohnungen."),
("de-DE-KatjaNeural","Moderator: Frau Yilmaz, Sie sind Bürgermeisterin einer ländlichen Gemeinde."),
("de-DE-AmalaNeural","Yilmaz: Wir möchten neue Einwohner gewinnen. Leer stehende Gebäude könnten renoviert und für Familien oder ältere Menschen genutzt werden. Dafür brauchen wir aber Investitionen in Busverbindungen, Kinderbetreuung und ärztliche Versorgung."),
("de-DE-ConradNeural","Reuter: Genau diese Infrastruktur ist entscheidend. Wenn Menschen nach dem Umzug für jede Kleinigkeit ein Auto brauchen, entstehen neue Kosten und Abhängigkeiten."),
("de-DE-AmalaNeural","Yilmaz: Das stimmt. Wir planen deshalb einen Rufbus und einen gemeinsamen Dorfladen. Trotzdem müssen wir realistisch bleiben: Solche Angebote kosten Geld und brauchen genügend Nutzer."),
("de-DE-KatjaNeural","Moderator: Die Diskussion zeigt, dass Umzüge nur dann zur Entlastung beitragen, wenn Wohnraum und Infrastruktur gemeinsam entwickelt werden.")
],
"teil4_01.mp3":[("de-DE-ConradNeural","Guten Tag. In meinem Vortrag beschäftige ich mich mit der Frage, wie Städte und ländliche Regionen lebenswert bleiben können. Die Entscheidung für einen Wohnort hängt heute von vielen Faktoren ab. Neben der Wohnung selbst spielen Arbeit, Mobilität, Bildung, Gesundheit und Freizeit eine wichtige Rolle. Deshalb lässt sich die Lebensqualität nicht allein am Mietpreis messen. In Großstädten sind Arbeitsplätze, Hochschulen und kulturelle Angebote häufig gut erreichbar. Gleichzeitig führen hohe Nachfrage und begrenzte Flächen zu steigenden Wohnkosten. Kommunen können gegensteuern, indem sie neue Wohnungen bauen, leer stehende Gebäude nutzen und unterschiedliche Wohnformen fördern. Dazu gehören kleinere Wohnungen für Einzelpersonen, barrierefreie Angebote und gemeinschaftliche Wohnprojekte. Ländliche Gebiete bieten oft mehr Platz und Nähe zur Natur. Damit Menschen dort dauerhaft leben können, müssen jedoch wichtige Einrichtungen erreichbar bleiben. Dazu zählen Arztpraxen, Schulen, Einkaufsmöglichkeiten und zuverlässige Verkehrsverbindungen. Flexible Busangebote können dort helfen, wo eine regelmäßige Linie wirtschaftlich nicht möglich ist. Auch digitale Infrastruktur gewinnt an Bedeutung, weil sie Homeoffice und den Zugang zu Dienstleistungen erleichtert. Entscheidend ist, dass Wohnungsbau und Infrastruktur zusammen geplant werden. Neue Wohnungen allein lösen keine Probleme, wenn Arbeitsplätze, Betreuung und Mobilität fehlen. Umgekehrt können gute Verkehrsangebote dazu beitragen, dass Menschen auch außerhalb großer Städte passende Wohnorte finden. Eine nachhaltige Wohnraumpolitik berücksichtigt deshalb die unterschiedlichen Bedürfnisse der Bevölkerung und stärkt sowohl städtische Quartiere als auch ländliche Gemeinden.")]}
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
archive=ROOT/"exam-008.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
