import asyncio, subprocess, zipfile
from pathlib import Path
import edge_tts
ROOT=Path("output"); AUDIO=ROOT/"audio"; AUDIO.mkdir(parents=True,exist_ok=True)
# Prüfung 022: Finanzielle Bildung im Alltag
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Mitteilung der Volkshochschule: Der kostenlose Informationsabend zum Thema Geld im Alltag findet am Montag um achtzehn Uhr im Raum 204 statt. Eine Anmeldung ist nicht nötig. Interessierte können Fragen zu Haushaltsplanung und sicheren Zahlungsmethoden stellen.")],
"teil1_02.mp3":[("de-DE-ConradNeural","Unser Workshop zum Haushaltsplan beginnt am Dienstag um achtzehn Uhr. Bitte bringen Sie, wenn möglich, eine Übersicht Ihrer regelmäßigen Einnahmen und Ausgaben mit. Die Teilnahmegebühr beträgt fünf Euro. Eine Kinderbetreuung wird leider nicht angeboten.")],
"teil1_03.mp3":[("de-DE-AmalaNeural","Hinweis zum Steuerkurs: Für den Kurs zur Steuererklärung stehen Computer in der Volkshochschule zur Verfügung. Sie müssen also keinen eigenen Laptop mitbringen. Bitte halten Sie jedoch Ihre Unterlagen bereit. Der Kurs beginnt nächste Woche.")],
"teil1_04.mp3":[("de-DE-KatjaNeural","Die kommunale Schuldnerberatung bietet vertrauliche Gespräche an. Termine können telefonisch beim Bürgerbüro oder über das Onlineformular vereinbart werden. Die Beratung ist kostenlos und richtet sich an Menschen in finanziellen Schwierigkeiten sowie an Angehörige.")],
"teil1_05.mp3":[("de-DE-ConradNeural","Im Jugendzentrum wird ab Freitag eine Ausstellung zum Thema Geld eröffnet. Jugendliche unter achtzehn Jahren haben freien Eintritt. Gezeigt werden Beispiele zu Taschengeld, Onlinekäufen und dem Umgang mit Werbung. Gruppen sollten sich vorher anmelden.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Viele Menschen haben Schwierigkeiten, ihre Finanzen langfristig zu planen. Dazu begrüße ich die Verbraucherberaterin Frau Dr. Lenz. Warum verlieren manche Menschen den Überblick über ihre Ausgaben?"),
("de-DE-AmalaNeural","Lenz: Häufig liegt es daran, dass kleine Beträge im Alltag kaum auffallen. Ein Kaffee hier, ein Abonnement dort: Am Monatsende kommt einiges zusammen. Hinzu kommt, dass viele Zahlungen automatisch abgebucht werden und man sie deshalb weniger bewusst wahrnimmt."),
("de-DE-KatjaNeural","Moderatorin: Was wäre ein sinnvoller erster Schritt?"),
("de-DE-AmalaNeural","Lenz: Ich empfehle, Einnahmen und Ausgaben zunächst einige Wochen lang aufzuschreiben. Dafür reicht eine einfache Tabelle oder ein Notizbuch. Erst wenn man weiß, wohin das Geld fließt, kann man realistische Veränderungen planen. Es geht nicht darum, sich alles zu verbieten."),
("de-DE-KatjaNeural","Moderatorin: Wie sehen Sie Ratenkäufe, die inzwischen überall angeboten werden?"),
("de-DE-AmalaNeural","Lenz: Sie wirken bequem, weil man nicht sofort den ganzen Preis bezahlen muss. Allerdings werden dadurch zukünftige Einkommensteile bereits verplant. Wer mehrere Ratenkäufe gleichzeitig abschließt, kann schnell den Überblick verlieren. Man sollte immer die Gesamtkosten betrachten."),
("de-DE-KatjaNeural","Moderatorin: Worauf sollte man achten, wenn man einen Kredit benötigt?"),
("de-DE-AmalaNeural","Lenz: Entscheidend sind nicht nur die monatlichen Raten. Man muss den effektiven Jahreszins, mögliche Zusatzgebühren und die gesamten Rückzahlungskosten vergleichen. Außerdem sollte man prüfen, ob die Rate auch bei unerwarteten Ausgaben tragbar bleibt."),
("de-DE-KatjaNeural","Moderatorin: Ist Sparen auch mit einem kleinen Einkommen möglich?"),
("de-DE-AmalaNeural","Lenz: Nicht für alle im gleichen Umfang, aber wenn es die Situation erlaubt, können kleine regelmäßige Beträge hilfreich sein. Wichtig ist ein erreichbares Ziel. Ein kleiner Notgroschen kann verhindern, dass jede unerwartete Rechnung zu neuen Schulden führt."),
("de-DE-KatjaNeural","Moderatorin: Was möchten Sie unseren Zuhörerinnen und Zuhörern mitgeben?"),
("de-DE-AmalaNeural","Lenz: Finanzielle Bildung bedeutet nicht, reich werden zu müssen. Sie hilft, Angebote kritisch zu prüfen, Risiken einzuschätzen und Entscheidungen zu treffen, die zur eigenen Lebenssituation passen.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Sollte finanzielle Bildung stärker gefördert werden? Frau Berger arbeitet in einer Verbraucherzentrale, Herr Yilmaz ist Lehrer. Frau Berger, was ist Ihnen besonders wichtig?"),
("de-DE-AmalaNeural","Berger: Viele Menschen führen kein Haushaltsbuch und bemerken deshalb erst spät, wenn sie regelmäßig mehr ausgeben, als sie einnehmen. Ein einfacher Überblick kann viel verändern. Werbung verleitet gerade junge Menschen oft zu spontanen Käufen."),
("de-DE-KatjaNeural","Moderatorin: Herr Yilmaz, welche Erfahrungen machen Sie in der Schule?"),
("de-DE-ConradNeural","Yilmaz: Finanzunterricht sollte früh und praktisch stattfinden. Jugendliche sollten lernen, Verträge zu lesen, Zinsen zu verstehen und ein Budget zu planen. Bei Geldanlagen darf man mögliche Verluste keinesfalls verschweigen."),
("de-DE-AmalaNeural","Berger: Ebenso wichtig ist ein Notgroschen. Bevor man über hohe Renditen nachdenkt, sollte man Geld für unvorhergesehene Ausgaben zurücklegen. Das ist nicht immer leicht, aber eine sichere Grundlage."),
("de-DE-ConradNeural","Yilmaz: Beratungsangebote müssen alle erreichen, auch Menschen mit geringem Einkommen. Finanzielle Bildung darf kein Luxus sein. Schulen und Beratungsstellen sollten zusammenarbeiten, damit niemand aus Scham auf Hilfe verzichtet."),
("de-DE-KatjaNeural","Moderatorin: Sie setzen unterschiedliche Schwerpunkte, sind sich aber einig, dass Wissen und zugängliche Beratung Menschen unabhängiger machen.")
],
"teil4_01.mp3":[("de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um finanzielle Bildung im Alltag. Finanzielle Kompetenz bedeutet, Einnahmen und Ausgaben zu verstehen, Angebote kritisch zu prüfen und verantwortungsvolle Entscheidungen zu treffen.\nEin erster Schritt ist die persönliche Übersicht. Wer regelmäßig notiert, wofür Geld ausgegeben wird, erkennt leichter unnötige Kosten. Besonders kleine, wiederkehrende Zahlungen werden häufig unterschätzt. Ein realistischer Haushaltsplan schafft Orientierung und sollte auch Raum für unerwartete Ausgaben lassen.\nVon großer Bedeutung ist der Umgang mit Schulden. Ratenzahlungen und Kauf-jetzt-zahl-später-Angebote erscheinen bequem. Werden mehrere Verpflichtungen gleichzeitig eingegangen, können sie sich jedoch summieren. Vor einem Kredit sollte man deshalb nicht nur die monatliche Rate, sondern auch den effektiven Jahreszins, Gebühren und die Gesamtkosten vergleichen.\nEin Notgroschen hilft, unvorhergesehene Rechnungen zu bezahlen, ohne sofort einen Kredit aufnehmen zu müssen. Wie hoch diese Rücklage sein kann, hängt von Einkommen und Lebenssituation ab. Auch kleine regelmäßige Beträge können einen Anfang bilden.\nBei Versicherungen sollte man zwischen wichtigen Risiken und zusätzlichen Angeboten unterscheiden. Nicht jede Versicherung ist für jede Person notwendig. Entscheidend ist, ob der Vertrag zum eigenen Bedarf passt.\nWer Geld anlegen möchte, sollte Renditeversprechen kritisch betrachten. Hohe mögliche Gewinne gehen häufig mit höheren Risiken einher. Anbieter, Gebühren, Laufzeit und persönliche Situation müssen geprüft werden. Eine Garantie auf hohe Erträge gibt es nicht.\nFinanzielle Bildung sollte bereits in der Schule beginnen und später durch unabhängige Beratungsangebote ergänzt werden. Praktische Übungen und verständliche Informationen können verhindern, dass Menschen aus Unsicherheit schlechte Entscheidungen treffen.\nZusammenfassend lässt sich sagen: Finanzielle Kompetenz stärkt Selbstständigkeit. Sie schützt nicht vor jeder wirtschaftlichen Schwierigkeit, hilft aber, Risiken besser einzuschätzen und den eigenen Handlungsspielraum zu erweitern.")],
}
async def make_track(name,utterances):
    parts=[]
    for i,(voice,spoken_text) in enumerate(utterances):
        part=AUDIO/f".{name}.{i:02d}.mp3"; error=None
        for attempt in range(1,6):
            try:
                print(f"{name}: {i+1}/{len(utterances)} {voice} Versuch {attempt}/5",flush=True)
                await edge_tts.Communicate(spoken_text,voice,rate="-4%").save(str(part))
                if not part.exists() or part.stat().st_size<1000: raise RuntimeError("Audio fehlt oder ist zu klein")
                error=None; break
            except Exception as exc:
                error=exc; part.unlink(missing_ok=True); print(f"Fehler: {exc}",flush=True)
                if attempt<5: await asyncio.sleep(2*attempt)
        if error: raise RuntimeError(f"Track fehlgeschlagen: {name}") from error
        parts.append(part); await asyncio.sleep(1)
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
    if len(tracks)!=8: raise RuntimeError("Il faut exactement huit pistes")
    for name,utterances in tracks.items(): await make_track(name,utterances)
asyncio.run(main())
expected=["teil1_01.mp3","teil1_02.mp3","teil1_03.mp3","teil1_04.mp3","teil1_05.mp3","teil2_01.mp3","teil3_01.mp3","teil4_01.mp3"]
archive=ROOT/"exam-022.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
