import asyncio
import subprocess
import zipfile
from pathlib import Path
import edge_tts
ROOT=Path("output")
AUDIO=ROOT/"audio"
AUDIO.mkdir(parents=True,exist_ok=True)
# Goethe B2 Hören — Prüfung 017: Lebenslanges Lernen und Weiterbildung.
tracks={
  "teil1_01.mp3": [
    [
      "de-DE-KatjaNeural",
      "Hinweis des Bildungszentrums: Der Informationsabend zum Thema berufliche Weiterbildung findet am Mittwoch um 18 Uhr online statt. Eine Anmeldung ist bis Montag um 12 Uhr möglich. Interessierte erhalten den Zugangslink anschließend per E-Mail."
    ]
  ],
  "teil1_02.mp3": [
    [
      "de-DE-KatjaNeural",
      "A: Ich weiß nicht, ob ich gleich einen umfangreichen Kurs buchen soll. B: Vielleicht probierst du zuerst einen kurzen Onlinekurs aus. Dann merkst du, ob das Thema wirklich zu dir passt. A: Das ist vernünftig. So kann ich den Aufwand besser einschätzen."
    ],
    [
      "de-DE-ConradNeural",
      "B: Genau. Unsere Beratung ist übrigens kostenlos und steht auch Menschen ohne abgeschlossene Berufsausbildung offen."
    ]
  ],
  "teil1_03.mp3": [
    [
      "de-DE-AmalaNeural",
      "Die kommunale Beratungsstelle informiert: Unsere Beratung zu beruflichen Entwicklungsmöglichkeiten ist kostenlos. Sie richtet sich ausdrücklich auch an Menschen, die bisher keine abgeschlossene Berufsausbildung haben. Termine können telefonisch vereinbart werden."
    ]
  ],
  "teil1_04.mp3": [
    [
      "de-DE-KatjaNeural",
      "A: Weißt du, warum der Kursbeginn verschoben wurde? B: Ja, der Unterrichtsraum wird renoviert. A: Gibt es schon einen neuen Termin? B: Der Kurs beginnt jetzt zwei Wochen später."
    ]
  ],
  "teil1_05.mp3": [
    [
      "de-DE-ConradNeural",
      "Hinweis der Stadtbibliothek: Für Lerngruppen stehen ab sofort zwei zusätzliche Arbeitsräume zur Verfügung. Interessierte können online einen Termin reservieren. Die Teilnahme ist erst verbindlich, wenn die Bibliothek die Buchung per E-Mail bestätigt hat."
    ]
  ],
  "teil2_01.mp3": [
    [
      "de-DE-KatjaNeural",
      "Moderatorin: Berufliche Weiterbildung ist für viele Erwachsene ein wichtiges Thema. Frau Dr. Weber, Sie beraten Menschen bei ihrer beruflichen Entwicklung. Warum interessieren sich heute so viele für Weiterbildung?"
    ],
    [
      "de-DE-AmalaNeural",
      "Weber: Die Anforderungen verändern sich schnell. Neue Programme, digitale Arbeitsabläufe und andere Organisationsformen führen dazu, dass Kenntnisse regelmäßig aktualisiert werden müssen. Manche möchten sich auch beruflich neu orientieren oder nach einer Familienphase wieder einsteigen."
    ],
    [
      "de-DE-KatjaNeural",
      "Moderatorin: Welche Lernformen sind besonders geeignet?"
    ],
    [
      "de-DE-AmalaNeural",
      "Weber: Das hängt von der Situation ab. Kurze Lernmodule lassen sich oft gut in den Alltag integrieren. Präsenzkurse bieten dagegen mehr direkten Austausch und praktische Übungen. Eine Kombination kann sehr sinnvoll sein."
    ],
    [
      "de-DE-KatjaNeural",
      "Moderatorin: Welche Schwierigkeiten gibt es beim Online-Lernen?"
    ],
    [
      "de-DE-AmalaNeural",
      "Weber: Man braucht Selbstdisziplin und eine gute Lernorganisation. Wer zu Hause viele Verpflichtungen hat, findet nicht immer Ruhe. Deshalb sollten Lernende realistische Ziele setzen und feste Zeiten einplanen."
    ],
    [
      "de-DE-KatjaNeural",
      "Moderatorin: Was können Arbeitgeber tun?"
    ],
    [
      "de-DE-AmalaNeural",
      "Weber: Sie können Lernzeiten ermöglichen, Entwicklungsgespräche führen und einen Teil der Kosten übernehmen. Wichtig ist, dass Weiterbildung nicht nur als private Angelegenheit betrachtet wird, wenn der Betrieb ebenfalls davon profitiert."
    ],
    [
      "de-DE-KatjaNeural",
      "Moderatorin: Und wenn jemand nur ein begrenztes Budget hat?"
    ],
    [
      "de-DE-AmalaNeural",
      "Weber: Dann lohnt es sich, nach öffentlichen Förderprogrammen und unabhängigen Beratungsstellen zu suchen. Man sollte außerdem prüfen, ob ein Kurs transparente Lernziele hat und ob der Abschluss anerkannt wird."
    ],
    [
      "de-DE-KatjaNeural",
      "Moderatorin: Was ist Ihr wichtigster Rat?"
    ],
    [
      "de-DE-AmalaNeural",
      "Weber: Vor der Anmeldung sollte man klären, welche Fähigkeiten man wirklich braucht. Ein teurer Kurs ist nicht automatisch gut. Entscheidend ist, ob die Inhalte zu den eigenen Zielen passen."
    ]
  ],
  "teil3_01.mp3": [
    [
      "de-DE-KatjaNeural",
      "Moderatorin: Sollte berufliche Weiterbildung stärker von Unternehmen finanziert werden? Frau Keller, Sie leiten die Personalentwicklung eines mittelständischen Betriebs."
    ],
    [
      "de-DE-AmalaNeural",
      "Keller: Ja, zumindest dann, wenn die erworbenen Kenntnisse dem Unternehmen zugutekommen. Wir ermöglichen Lernzeiten während der Arbeitszeit und fördern interne Lernpartnerschaften. Auch kleinere Betriebe können sich mit anderen Unternehmen zusammenschließen."
    ],
    [
      "de-DE-KatjaNeural",
      "Moderatorin: Herr Özdemir, Sie sind Betriebsrat und beschäftigen sich mit Weiterbildung."
    ],
    [
      "de-DE-ConradNeural",
      "Özdemir: Unterstützung ist wichtig, aber nicht jeder Kursabschluss verbessert automatisch die Berufschancen. Beschäftigte müssen wissen, welche Kompetenzen tatsächlich vermittelt werden. Außerdem ist es für Menschen mit Familie oft schwierig, zusätzlich regelmäßig zu lernen."
    ],
    [
      "de-DE-AmalaNeural",
      "Keller: Das stimmt. Deshalb bieten wir flexible Lernzeiten und Gespräche an, in denen individuelle Ziele festgelegt werden. Nicht alle müssen denselben Weg gehen."
    ],
    [
      "de-DE-ConradNeural",
      "Özdemir: Ich würde mir wünschen, dass diese Angebote verbindlicher werden. Es darf nicht vom direkten Vorgesetzten abhängen, ob jemand eine Weiterbildung machen kann. Auch die Qualität der Kurse muss regelmäßig überprüft werden."
    ],
    [
      "de-DE-KatjaNeural",
      "Moderatorin: Beide Seiten halten Unterstützung für notwendig. Offen bleibt, wie verbindlich die Finanzierung und die Lernzeit geregelt werden sollen."
    ]
  ],
  "teil4_01.mp3": [
    [
      "de-DE-ConradNeural",
      "Guten Tag. In meinem Vortrag geht es um lebenslanges Lernen und berufliche Weiterbildung. Früher blieb das Wissen aus der Ausbildung häufig über viele Jahre ausreichend. Heute verändern sich Technologien, Arbeitsabläufe und Anforderungen deutlich schneller. Deshalb müssen viele Beschäftigte ihre Kenntnisse regelmäßig erweitern. Weiterbildung kann unterschiedliche Formen annehmen. Neben längeren Lehrgängen gibt es kurze Seminare, digitale Lernmodule, berufsbegleitende Studiengänge und praktische Schulungen im Betrieb. Jede Form hat Vorteile und Grenzen. Online-Angebote ermöglichen zeit- und ortsunabhängiges Lernen. Sie verlangen jedoch Eigenmotivation und eine gute Planung. Präsenzveranstaltungen bieten direkten Austausch, sind aber nicht für alle zeitlich erreichbar. Vor der Auswahl eines Angebots sollte man zunächst die eigenen Ziele klären. Welche Aufgaben möchte man künftig übernehmen? Welche Kenntnisse fehlen noch? Auch die Qualität des Kurses ist wichtig. Transparente Lernziele, qualifizierte Lehrkräfte und anerkannte Zertifikate können bei der Entscheidung helfen. Ein Zertifikat garantiert zwar keine Beförderung, macht erworbene Kompetenzen aber nachvollziehbar. Unternehmen können Weiterbildung durch Lernbudgets, Mentoring und planbare Lernzeiten unterstützen. Gerade kleine Betriebe können mit anderen Unternehmen oder Bildungseinrichtungen kooperieren. Gleichzeitig tragen Lernende selbst Verantwortung: Sie sollten realistische Ziele setzen und regelmäßig Zeit zum Üben einplanen. Eine Herausforderung bleibt der Zeitmangel. Wer Beruf, Familie und Lernen vereinbaren muss, benötigt flexible Angebote und verständliche Beratung. Lebenslanges Lernen gelingt daher am besten, wenn Eigeninitiative und institutionelle Unterstützung zusammenkommen."
    ]
  ]
}
async def make_track(name,utterances):
    parts=[]
    for i,(voice,spoken_text) in enumerate(utterances):
        part=AUDIO/f".{name}.{i:02d}.mp3"
        for attempt in range(1,6):
            try:
                await edge_tts.Communicate(spoken_text,voice,rate="-4%").save(str(part))
                if not part.exists() or part.stat().st_size<1000: raise RuntimeError("Audio missing or too small")
                break
            except Exception:
                part.unlink(missing_ok=True)
                if attempt==5: raise
                await asyncio.sleep(2*attempt)
        parts.append(part)
        if i<len(utterances)-1:
            silence=AUDIO/f".silence_{name}_{i}.mp3"
            subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t","0.65","-codec:a","libmp3lame","-b:a","64k",str(silence)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
            parts.append(silence)
    listing=AUDIO/f".{name}.txt"
    listing.write_text("".join(f"file '{p.resolve()}'\n" for p in parts),encoding="utf-8")
    target=AUDIO/name
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(listing),"-codec:a","libmp3lame","-b:a","128k",str(target)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
    for p in parts+[listing]: p.unlink(missing_ok=True)
    if not target.exists() or target.stat().st_size<1024: raise RuntimeError(f"Invalid MP3: {name}")
    print(f"OK {name}: {target.stat().st_size} bytes",flush=True)
async def main():
    for name,utterances in tracks.items(): await make_track(name,utterances)
asyncio.run(main())
expected=["teil1_01.mp3","teil1_02.mp3","teil1_03.mp3","teil1_04.mp3","teil1_05.mp3","teil2_01.mp3","teil3_01.mp3","teil4_01.mp3"]
archive=ROOT/"exam-017.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Wrong ZIP contents")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Empty or too-small track")
print(f"Validated archive: {archive} ({archive.stat().st_size} bytes)",flush=True)
