import asyncio, subprocess, zipfile
from pathlib import Path
import edge_tts

ROOT=Path("output"); AUDIO=ROOT/"audio"; AUDIO.mkdir(parents=True,exist_ok=True)
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Der Wochenmarkt lädt am Freitag zu einer Informationsveranstaltung gegen Lebensmittelverschwendung ein. Sie beginnt um fünfzehn Uhr neben dem Haupteingang. Der Eintritt ist frei. Besucherinnen und Besucher erfahren, wie sie Lebensmittel länger nutzen können.")],
"teil1_02.mp3":[("de-DE-ConradNeural","Das Bürgerzentrum bietet am Samstag einen Kochkurs mit übrig gebliebenen Lebensmitteln an. Der Kurs beginnt um zehn Uhr. Bitte bringen Sie eine saubere, wiederverwendbare Dose mit. Die Teilnahme ist kostenlos, eine Anmeldung ist erforderlich.")],
"teil1_03.mp3":[("de-DE-AmalaNeural","Die Stadtbibliothek sammelt bis Mittwochmittag ungeöffnete und haltbare Lebensmittel. Die Spenden werden anschließend an eine lokale Hilfsorganisation weitergegeben. Frische Produkte und selbst zubereitete Speisen können leider nicht angenommen werden.")],
"teil1_04.mp3":[("de-DE-KatjaNeural","Restaurants und Bäckereien können ab sofort eine digitale Plattform nutzen, um überschüssige Speisen kurz vor Ladenschluss anzubieten. Interessierte Betriebe registrieren sich kostenlos. Kundinnen und Kunden reservieren die Angebote direkt über die Anwendung.")],
"teil1_05.mp3":[("de-DE-ConradNeural","Auf der Internetseite der Stadt gibt es neue Hinweise zur Lagerung von Obst, Gemüse und Milchprodukten. Außerdem erklärt ein kurzer Ratgeber den Unterschied zwischen Mindesthaltbarkeitsdatum und Verbrauchsdatum. Die Informationen können kostenlos heruntergeladen werden.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","In Deutschland werden noch immer große Mengen genießbarer Lebensmittel weggeworfen. Wo liegt das Problem besonders häufig?"),
("de-DE-AmalaNeural","Ein erheblicher Teil der vermeidbaren Abfälle entsteht in privaten Haushalten. Viele Menschen kaufen spontan ein, verlieren den Überblick über ihre Vorräte und planen Mahlzeiten nicht ausreichend."),
("de-DE-KatjaNeural","Viele werfen Produkte direkt nach dem Mindesthaltbarkeitsdatum weg. Ist das sinnvoll?"),
("de-DE-AmalaNeural","Nein. Das Mindesthaltbarkeitsdatum ist eine Qualitätsgarantie des Herstellers und kein automatisches Wegwerfdatum. Man sollte das Produkt ansehen, daran riechen und gegebenenfalls vorsichtig probieren. Das Verbrauchsdatum bei leicht verderblichen Lebensmitteln ist dagegen unbedingt zu beachten."),
("de-DE-KatjaNeural","Was kann man im Alltag konkret verändern?"),
("de-DE-AmalaNeural","Eine Einkaufsliste hilft, wenn man vorher Kühlschrank und Vorratsschrank kontrolliert. Außerdem sollte man Mahlzeiten für einige Tage planen und Reste kreativ weiterverwenden."),
("de-DE-KatjaNeural","Welche Verantwortung tragen Supermärkte?"),
("de-DE-AmalaNeural","Sie können Produkte kurz vor Ablauf günstiger anbieten, Mengen besser kalkulieren und genießbare Überschüsse an soziale Einrichtungen weitergeben. Dafür braucht es verlässliche Abläufe."),
("de-DE-KatjaNeural","Reichen digitale Apps aus, um das Problem zu lösen?"),
("de-DE-AmalaNeural","Sie sind nützlich, aber keine alleinige Lösung. Entscheidend ist die Zusammenarbeit von Landwirtschaft, Handel, Gastronomie, Politik und Verbrauchern.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Wir sprechen heute mit drei Gästen über Lebensmittelverschwendung. Mara, Jonas und Leonie vertreten unterschiedliche Perspektiven. Mara, was können Verbraucherinnen und Verbraucher tun?"),
("de-DE-AmalaNeural","Mara: Wir sollten zuerst bei unseren eigenen Gewohnheiten anfangen. Wenn wir vor dem Einkauf prüfen, was noch im Kühlschrank liegt, kaufen wir weniger doppelt. Außerdem müsste man die Menschen besser über das Mindesthaltbarkeitsdatum informieren. Viele verwechseln es mit dem Verbrauchsdatum."),
("de-DE-ConradNeural","Jonas: Das ist wichtig, aber meiner Meinung nach darf die Verantwortung nicht hauptsächlich auf Einzelpersonen abgeschoben werden. Große Handelsunternehmen sollten verbindliche Regeln bekommen, damit genießbare Ware nicht unnötig vernichtet wird. Apps können helfen, ersetzen jedoch keine strukturellen Veränderungen."),
("de-DE-AmalaNeural","Leonie: In unserem Viertel haben wir einen offenen Kühlschrank eingerichtet. Geschäfte und Privatpersonen stellen dort geeignete Lebensmittel hinein, die andere kostenlos mitnehmen können. Das funktioniert gut, weil sich Freiwillige um Kontrolle und Sauberkeit kümmern. So entsteht auch mehr Kontakt zwischen den Nachbarn."),
("de-DE-KatjaNeural","Mara: Bei der Information sehe ich ebenfalls großen Bedarf. Viele wissen nicht, wie man Gemüse richtig lagert oder Reste sicher aufbewahrt. Kleine Workshops in Schulen und Stadtteilzentren könnten viel bewirken."),
("de-DE-ConradNeural","Jonas: Ich möchte noch ergänzen, dass soziale Einrichtungen regelmäßig verlässliche Spenden benötigen. Es reicht nicht, gelegentlich große Mengen abzugeben. Die Weitergabe muss planbar sein und hygienische Standards erfüllen."),
("de-DE-AmalaNeural","Leonie: Genau. Wenn Handel, soziale Einrichtungen und Nachbarschaften zusammenarbeiten, können wir mehr erreichen. Wichtig ist, dass solche Projekte dauerhaft unterstützt werden und nicht nur von einzelnen engagierten Menschen abhängen.")
,
"teil4_01.mp3":[
("de-DE-AmalaNeural","Guten Abend. In meinem Vortrag geht es um Lebensmittelverschwendung und darum, wie sie entlang der gesamten Versorgungskette reduziert werden kann. Unter Lebensmittelverschwendung verstehen wir essbare Produkte, die nicht verzehrt werden, sondern verloren gehen oder entsorgt werden. Das betrifft Landwirtschaft, Verarbeitung, Transport, Handel, Gastronomie und private Haushalte."),
("de-DE-ConradNeural","Die Folgen sind erheblich. Für jedes Lebensmittel wurden Wasser, Energie, Arbeitskraft und Fläche eingesetzt. Wird es weggeworfen, waren diese Ressourcen teilweise umsonst. Zusätzlich entstehen Treibhausgasemissionen, etwa durch Produktion, Kühlung, Transport und die Entsorgung organischer Abfälle. Lebensmittelverschwendung ist deshalb nicht nur ein wirtschaftliches, sondern auch ein ökologisches und soziales Problem."),
("de-DE-AmalaNeural","Verluste können bereits bei der Ernte entstehen, wenn Produkte nicht den Handelsnormen entsprechen oder nicht rechtzeitig abgeholt werden. Während Lagerung und Transport können falsche Temperaturen oder beschädigte Verpackungen dazu führen, dass Waren verderben. Im Handel spielen Überbestände und eine ungenaue Nachfrageplanung eine Rolle."),
("de-DE-ConradNeural","Auch Kantinen und Restaurants können handeln. Sie sollten die Nachfrage besser einschätzen, Portionsgrößen flexibel anbieten und Speisepläne an saisonale Produkte anpassen. Gäste könnten außerdem die Möglichkeit erhalten, nicht verzehrte Speisen hygienisch verpackt mitzunehmen. Eine genaue Dokumentation der Reste hilft, wiederkehrende Ursachen zu erkennen."),
("de-DE-AmalaNeural","Spendenorganisationen übernehmen eine wichtige Vermittlungsfunktion. Sie sammeln geeignete Überschüsse und verteilen sie an soziale Einrichtungen oder Menschen in schwierigen Lebenslagen. Dabei müssen Kühlketten, Hygienevorschriften und eine nachvollziehbare Kennzeichnung eingehalten werden. Nicht jedes überschüssige Produkt ist automatisch für eine Weitergabe geeignet."),
("de-DE-ConradNeural","Auch politische Rahmenbedingungen können helfen. Denkbar sind steuerliche Anreize für die Weitergabe genießbarer Überschüsse, klare Leitlinien für Unternehmen und eine bessere Aufklärung. Gleichzeitig sollten unnötig strenge optische Anforderungen an Obst und Gemüse überprüft werden, denn ungewöhnlich geformte Produkte sind genauso essbar."),
("de-DE-AmalaNeural","Zusammenfassend lässt sich sagen: Lebensmittelverschwendung lässt sich weder durch Apps noch durch Appelle an einzelne Verbraucher allein beseitigen. Notwendig sind bessere Planung, passende Infrastruktur, sichere Weitergabe und eine Kultur der Wertschätzung. Wenn alle Beteiligten Verantwortung übernehmen, können Ressourcen geschont und Menschen unterstützt werden.")
]
}
async def make_track(name, segments):
    parts=[]
    for i,(voice,words) in enumerate(segments):
        p=AUDIO/f".{name}_{i}.mp3"
        await edge_tts.Communicate(words,voice).save(str(p))
        parts.append(p)
        if i<len(segments)-1:
            silence=AUDIO/f".silence_{name}_{i}.mp3"
            subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t","0.55","-codec:a","libmp3lame","-b:a","64k",str(silence)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
            parts.append(silence)
    listing=AUDIO/f".{name}.txt"
    listing.write_text("".join(f"file '{p.resolve()}'\n" for p in parts),encoding="utf-8")
    target=AUDIO/name
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(listing),"-codec:a","libmp3lame","-b:a","128k",str(target)],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,check=True)
    for p in parts+[listing]: p.unlink(missing_ok=True)
    if not target.exists() or target.stat().st_size<1024: raise RuntimeError(f"MP3 invalide: {name}")
    print(f"OK {name}: {target.stat().st_size} octets",flush=True)
async def main():
    for name,segments in tracks.items(): await make_track(name,segments)
asyncio.run(main())
expected=["teil1_01.mp3","teil1_02.mp3","teil1_03.mp3","teil1_04.mp3","teil1_05.mp3","teil2_01.mp3","teil3_01.mp3","teil4_01.mp3"]
archive=ROOT/"exam-029.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<10000 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
