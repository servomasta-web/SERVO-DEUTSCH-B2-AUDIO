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
tracks={"teil1_01.mp3":[["de-DE-KatjaNeural","Mitteilung der Wohnungsbaugesellschaft: Für die Besichtigung der neuen geförderten Wohnungen ist eine vorherige Anmeldung nötig. Interessierte können sich bis zum 5. Februar online registrieren. Die Vergabe der Termine erfolgt anschließend per E-Mail."]],"teil1_02.mp3":[["de-DE-KatjaNeural","A: Wir suchen seit Monaten eine bezahlbare Wohnung. B: Habt ihr euch schon bei der kommunalen Wohnungsstelle beraten lassen? A: Noch nicht. B: Dort gibt es Informationen zu Wohnberechtigungsscheinen und geförderten Wohnungen. A: Dann vereinbare ich nächste Woche einen Termin."]],"teil1_03.mp3":[["de-DE-KatjaNeural","Hinweis der Stadt: Der neue Mietspiegel wird am 1. Juli veröffentlicht. Er dient als Orientierung für ortsübliche Vergleichsmieten, legt aber nicht automatisch die Miete jeder einzelnen Wohnung fest."]],"teil1_04.mp3":[["de-DE-AmalaNeural","Wir wohnen jetzt in einer kleineren Wohnung, dafür aber näher an der Schule und am Arbeitsplatz. Das spart uns täglich Wege. Wir mussten allerdings viele Möbel verkaufen, weil nicht alles in die neuen Räume passte."]],"teil1_05.mp3":[["de-DE-KatjaNeural","Durchsage im Bürgerzentrum: Die Beratung zu Wohngeldanträgen findet am Donnerstag ausnahmsweise im Raum 205 statt. Die Sprechzeit bleibt von 9 bis 12 Uhr. Bitte ziehen Sie am Eingang eine Wartemarke."]],"teil2_01.mp3":[["de-DE-KatjaNeural","Moderatorin: Bezahlbarer Wohnraum ist in vielen Städten knapp. Herr Kramer, Sie beraten Kommunen in der Wohnungspolitik. Welche Maßnahmen können kurzfristig helfen?\nKramer: Kommunen können vorhandene Wohnungen besser nutzen, leer stehende Gebäude erfassen und Beratungsangebote ausbauen. Kurzfristig ist auch wichtig, dass Menschen wissen, welche Unterstützung sie beantragen können.\nModeratorin: Reicht es, neue Wohnungen zu bauen?\nKramer: Neubau ist notwendig, aber er braucht Zeit und geeignete Flächen. Gleichzeitig müssen bestehende Gebäude modernisiert werden. Dabei sollte man darauf achten, dass die Mieten nach der Sanierung nicht so stark steigen, dass bisherige Bewohner wegziehen müssen.\nModeratorin: Welche Rolle spielt sozialer Wohnungsbau?\nKramer: Er schafft Wohnungen mit begrenzten Mieten für Haushalte, die auf dem freien Markt Schwierigkeiten haben. Entscheidend ist, dass die Bindungen lange genug gelten und die Wohnungen dort entstehen, wo Arbeitsplätze, Schulen und Verkehr erreichbar sind.\nModeratorin: Können private Anbieter beitragen?\nKramer: Ja, wenn klare Rahmenbedingungen bestehen. Kooperationen zwischen Stadt, Wohnungsunternehmen und Genossenschaften können unterschiedliche Modelle ermöglichen. Auch die Umwandlung leerer Büroflächen kann sinnvoll sein, sofern die Gebäude dafür geeignet sind.\nModeratorin: Was sollte bei der Planung nicht vergessen werden?\nKramer: Wohnraum ist mehr als eine Wohnung. Grünflächen, Kitas, Einkaufsmöglichkeiten und öffentliche Verkehrsmittel gehören zu einem lebenswerten Quartier."]],"teil3_01.mp3":[["de-DE-KatjaNeural","Moderator: Sollten Städte eine Mietobergrenze für alle Wohnungen einführen? Frau Hoffmann, Sie vertreten einen Eigentümerverband."],["de-DE-ConradNeural","Hoffmann: Eine pauschale Grenze kann Investitionen verhindern, wenn Eigentümer notwendige Reparaturen nicht mehr finanzieren können. Wir brauchen gezielte Unterstützung für Haushalte mit geringem Einkommen und klare Regeln, die auch Instandhaltung ermöglichen."],["de-DE-KatjaNeural","Moderator: Herr Yeboah, Sie engagieren sich in einer Mieterinitiative."],["de-DE-ConradNeural","Yeboah: Ohne wirksame Begrenzung können Menschen trotz Arbeit ihre Wohnung verlieren. Öffentliche Förderung allein reicht nicht, wenn die Preise weiter steigen. Es braucht Schutz vor übermäßigen Mieterhöhungen."],["de-DE-ConradNeural","Hoffmann: Schutz ist wichtig, aber eine Regel muss auch regionale Unterschiede berücksichtigen. In einer kleinen Gemeinde ist die Lage anders als im Zentrum einer Großstadt."],["de-DE-ConradNeural","Yeboah: Regionale Unterschiede kann man berücksichtigen. Entscheidend ist, dass Regeln verständlich sind und Mieter wissen, wie sie sich gegen unzulässige Forderungen wehren können."],["de-DE-KatjaNeural","Moderator: Beide Seiten wollen bezahlbares Wohnen sichern, unterscheiden sich aber bei der Frage, wie stark Mieten begrenzt werden sollen."]],"teil4_01.mp3":[["de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um bezahlbaren Wohnraum. Eine Wohnung ist eine Grundvoraussetzung für Sicherheit und gesellschaftliche Teilhabe. Wenn Mieten schneller steigen als Einkommen, müssen Haushalte oft an anderen wichtigen Ausgaben sparen oder ihre vertraute Umgebung verlassen.\nEine Maßnahme ist der soziale Wohnungsbau. Dabei werden Wohnungen mit begrenzten Mieten geschaffen, häufig mit öffentlicher Unterstützung. Die Bindung muss ausreichend lange gelten, damit der Wohnraum nicht nach kurzer Zeit wieder zu Marktpreisen angeboten wird.\nAuch die Nutzung vorhandener Gebäude ist wichtig. Leer stehende Büros oder ältere Immobilien können teilweise zu Wohnungen umgebaut werden. Vorher muss geprüft werden, ob Grundrisse, Licht, Schallschutz und Infrastruktur geeignet sind. Modernisierungen sollten außerdem sozial verträglich gestaltet werden.\nKommunen können durch eine aktive Bodenpolitik Einfluss nehmen. Sie können Grundstücke gezielt vergeben, Genossenschaften unterstützen und bei neuen Bauprojekten einen Anteil günstiger Wohnungen vereinbaren. Gleichzeitig müssen Schulen, Kitas, Einkaufsmöglichkeiten und Verkehr mitgeplant werden.\nSchließlich braucht es Beratung. Viele Haushalte kennen ihre Ansprüche auf Wohngeld oder einen Wohnberechtigungsschein nicht. Verständliche Informationen und Unterstützung bei Anträgen können helfen, vorhandene Angebote tatsächlich zu nutzen. Bezahlbares Wohnen entsteht durch Neubau, Bestandspolitik, soziale Förderung und eine gute Infrastruktur."]]}
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
archive=ROOT/"exam-024.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
