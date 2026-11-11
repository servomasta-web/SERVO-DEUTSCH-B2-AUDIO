import asyncio
import subprocess
import zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output")
AUDIO=ROOT/"audio"
AUDIO.mkdir(parents=True,exist_ok=True)

# Prüfung 009 — Gesundheit und Prävention im Alltag.
# Acht neu formulierte Hörtexte mit drei deutschen Neuralstimmen.
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Mitteilung der Krankenkasse: Der kostenlose Gesundheitscheck für Versicherte ab 35 Jahren findet in diesem Monat nicht am Freitag, sondern am Mittwoch statt. Die Untersuchungen beginnen wie geplant um acht Uhr. Bitte bringen Sie Ihre Versichertenkarte und eine aktuelle Medikamentenliste mit.")],
"teil1_02.mp3":[("de-DE-KatjaNeural","Du gehst jetzt dreimal pro Woche schwimmen. Hilft dir das wirklich?"),("de-DE-ConradNeural","Auf jeden Fall. Früher hatte ich nach der Arbeit oft Rückenschmerzen. Seit ich regelmäßig trainiere, fühle ich mich beweglicher. Außerdem schlafe ich besser."),("de-DE-KatjaNeural","Und ist das nicht ziemlich teuer?"),("de-DE-ConradNeural","Ich habe eine günstige Mitgliedschaft im Verein gefunden.")],
"teil1_03.mp3":[("de-DE-KatjaNeural","Hinweis der Hausarztpraxis: Wegen einer Fortbildung bleibt die Praxis am kommenden Montag geschlossen. Bereits vereinbarte Termine werden telefonisch verschoben. In dringenden Fällen wenden Sie sich bitte an den ärztlichen Bereitschaftsdienst. Die regulären Sprechzeiten gelten ab Dienstag wieder.")],
"teil1_04.mp3":[("de-DE-AmalaNeural","Ich versuche, im Alltag weniger Zucker zu essen. Ganz darauf verzichten möchte ich aber nicht. Ich lese inzwischen die Zutatenlisten und bereite häufiger selbst etwas zu. Das kostet zwar Zeit, doch ich weiß dann genauer, was in meinem Essen steckt.")],
"teil1_05.mp3":[("de-DE-KatjaNeural","Durchsage im Gesundheitszentrum: Der Vortrag zum Thema Stressbewältigung beginnt heute nicht wie angekündigt um achtzehn Uhr, sondern erst um achtzehn Uhr dreißig. Der Veranstaltungsraum bleibt unverändert. Eine Anmeldung ist weiterhin nicht erforderlich.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Viele Menschen möchten gesünder leben, finden aber im Alltag nur schwer Zeit dafür. Frau Doktor Neumann, Sie arbeiten im Bereich Gesundheitsprävention. Was ist aus Ihrer Sicht der wichtigste erste Schritt?"),
("de-DE-AmalaNeural","Neumann: Man sollte nicht versuchen, das ganze Leben von heute auf morgen umzustellen. Kleine, realistische Veränderungen sind oft nachhaltiger. Wer bisher kaum Bewegung hat, kann zum Beispiel einen Teil des Arbeitswegs zu Fuß zurücklegen oder regelmäßig die Treppe nehmen."),
("de-DE-KatjaNeural","Moderatorin: Reicht Bewegung allein aus?"),
("de-DE-AmalaNeural","Neumann: Nein. Ausreichender Schlaf, ausgewogene Ernährung und Erholungsphasen gehören ebenfalls dazu. Entscheidend ist das Zusammenspiel. Eine strenge Diät bringt wenig, wenn jemand dauerhaft unter Schlafmangel leidet und sich kaum bewegt."),
("de-DE-KatjaNeural","Moderatorin: Welche Rolle spielt Stress?"),
("de-DE-AmalaNeural","Neumann: Eine große. Dauerhafter Stress kann körperliche Beschwerden verstärken und die Konzentration beeinträchtigen. Hilfreich sind feste Pausen, realistische Tagesziele und Aktivitäten, bei denen man abschalten kann. Nicht jede Entspannungstechnik passt allerdings zu jedem Menschen."),
("de-DE-KatjaNeural","Moderatorin: Wie kann man Menschen motivieren, dranzubleiben?"),
("de-DE-AmalaNeural","Neumann: Ziele sollten messbar, aber erreichbar sein. Statt sich vorzunehmen, sofort jeden Tag Sport zu treiben, könnte man mit zwei festen Terminen pro Woche beginnen. Auch gemeinsame Aktivitäten mit Freunden erhöhen häufig die Verbindlichkeit."),
("de-DE-KatjaNeural","Moderatorin: Und was sollten Arbeitgeber beitragen?"),
("de-DE-AmalaNeural","Neumann: Sie können gesunde Arbeitsbedingungen schaffen, etwa ergonomische Arbeitsplätze, bewegte Pausen und eine gute Pausenkultur. Gesundheitsförderung darf aber nicht zur Kontrolle werden. Die Teilnahme muss freiwillig bleiben.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderator: Sollten Unternehmen verpflichtet werden, mehr Angebote zur Gesundheitsförderung bereitzustellen? Herr Vogt, Sie vertreten einen Arbeitgeberverband."),
("de-DE-ConradNeural","Vogt: Verpflichtende Programme halte ich für wenig sinnvoll. Betriebe unterscheiden sich stark. Ein Büro braucht andere Maßnahmen als ein Handwerksbetrieb. Arbeitgeber sollten selbst entscheiden können, welche Angebote zu ihrer Belegschaft passen."),
("de-DE-KatjaNeural","Moderator: Frau Seifert, Sie sind Betriebsrätin. Wie sehen Sie das?"),
("de-DE-AmalaNeural","Seifert: Ohne klare Verantwortung passiert oft zu wenig. Viele Beschäftigte arbeiten unter hohem Zeitdruck und können Pausen kaum einhalten. Mindeststandards für ergonomische Arbeitsplätze und ausreichende Erholungszeiten halte ich deshalb für notwendig."),
("de-DE-ConradNeural","Vogt: Bei Sicherheit und Ergonomie bin ich einverstanden. Zusätzliche Sportkurse sollten jedoch freiwillig sein. Sonst entsteht der Eindruck, Beschäftigte seien selbst schuld, wenn sie krank werden."),
("de-DE-AmalaNeural","Seifert: Das sehe ich ähnlich. Gesundheitsangebote dürfen nicht den Druck erhöhen. Wichtig wären auch anonyme Beratung und eine Beteiligung der Beschäftigten an der Planung."),
("de-DE-KatjaNeural","Moderator: Beide Seiten befürworten also bessere Arbeitsbedingungen, unterscheiden sich aber darin, wie verbindlich zusätzliche Angebote geregelt werden sollen.")
],
"teil4_01.mp3":[("de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um Gesundheitsprävention und darum, wie sie im Alltag gelingen kann. Gesundheit wird häufig erst dann zum Thema, wenn Beschwerden auftreten. Dabei können viele Erkrankungen durch langfristige Gewohnheiten beeinflusst werden. Prävention bedeutet jedoch nicht, dass jeder Mensch einem perfekten Lebensstil folgen muss. Vielmehr geht es darum, Risiken zu verringern und die eigenen Möglichkeiten realistisch einzuschätzen. Ein wichtiger Bereich ist die Bewegung. Wer lange am Schreibtisch sitzt, sollte regelmäßig aufstehen und kurze Wege aktiv zurücklegen. Sport kann das Herz-Kreislauf-System stärken, muss aber nicht immer in einem Fitnessstudio stattfinden. Auch Radfahren, Tanzen oder Gartenarbeit bringen den Körper in Bewegung. Ebenso bedeutsam ist die Ernährung. Eine abwechslungsreiche Auswahl an Gemüse, Obst, Vollkornprodukten und geeigneten Eiweißquellen kann zu einer ausgewogenen Versorgung beitragen. Verbote und kurzfristige Diäten sind dagegen selten eine dauerhafte Lösung. Darüber hinaus darf die psychische Gesundheit nicht übersehen werden. Dauerhafte Belastungen, fehlende Erholung und soziale Isolation können das Wohlbefinden beeinträchtigen. Gespräche, ausreichend Schlaf und klare Grenzen zwischen Arbeit und Freizeit können entlasten. Schulen, Betriebe und Kommunen tragen ebenfalls Verantwortung. Sie können gesunde Mahlzeiten ermöglichen, sichere Radwege schaffen und Arbeitsbedingungen verbessern. Allerdings müssen solche Angebote für unterschiedliche Altersgruppen und Lebenslagen zugänglich sein. Abschließend lässt sich sagen: Wirksame Prävention besteht aus vielen kleinen Schritten und braucht sowohl persönliche Entscheidungen als auch unterstützende Rahmenbedingungen.")}
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
archive=ROOT/"exam-009.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
