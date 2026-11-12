import asyncio,subprocess,zipfile
from pathlib import Path
import edge_tts
ROOT=Path("output"); AUDIO=ROOT/"audio"; AUDIO.mkdir(parents=True,exist_ok=True)
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Mitteilung des Bürgerhauses: Der neue Rampenzugang an der Nordseite ist ab sofort geöffnet. Besucherinnen und Besucher können das Gebäude nun stufenlos erreichen. Der Haupteingang bleibt während der Bauarbeiten ebenfalls nutzbar.")],
"teil1_02.mp3":[("de-DE-ConradNeural","Die Beratungsstelle für barrierefreie Mobilität bietet am Donnerstag um fünfzehn Uhr eine offene Sprechstunde an. Fachleute informieren über Fahrdienste, öffentliche Verkehrsmittel und mögliche Zuschüsse. Eine Anmeldung ist nicht erforderlich.")],
"teil1_03.mp3":[("de-DE-AmalaNeural","Information des Rathauses: Der Aufzug im Hauptgebäude wird am Dienstagvormittag gewartet. Ab zwölf Uhr steht er wieder zur Verfügung. Wer vorher einen Termin hat, kann den barrierefreien Eingang am Innenhof benutzen.")],
"teil1_04.mp3":[("de-DE-KatjaNeural","Schäden und Hindernisse auf Gehwegen können beim Tiefbauamt gemeldet werden. Das ist telefonisch oder über das Onlineformular möglich. Bitte geben Sie möglichst die genaue Straße und eine kurze Beschreibung an.")],
"teil1_05.mp3":[("de-DE-ConradNeural","Das inklusive Kulturzentrum lädt am Samstag zu einer Führung ein. Dabei werden die barrierefreien Räume und Angebote vorgestellt. Die Teilnahme ist kostenlos, aber eine Anmeldung über die Website ist erforderlich, da die Gruppengröße begrenzt ist.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Barrierefreiheit wird häufig mit Rampen und Aufzügen verbunden. Unsere Gesprächspartnerin, die Stadtplanerin Dr. Hoffmann, erklärt heute, was noch dazugehört. Wie definieren Sie Barrierefreiheit?"),
("de-DE-AmalaNeural","Hoffmann: Es geht darum, dass Menschen möglichst selbstständig und gleichberechtigt am gesellschaftlichen Leben teilnehmen können. Dazu gehören Gebäude, Verkehrsmittel, Informationen und digitale Angebote. Eine Rampe allein macht einen Ort noch nicht für alle zugänglich."),
("de-DE-KatjaNeural","Moderatorin: Warum ist es wichtig, Betroffene an der Planung zu beteiligen?"),
("de-DE-AmalaNeural","Hoffmann: Weil sie Hindernisse aus dem Alltag kennen, die Fachleute am Schreibtisch manchmal übersehen. Eine Tür kann breit genug sein, aber wenn davor ein enger Weg liegt, bleibt der Zugang schwierig. Rückmeldungen helfen, konkrete Lösungen zu entwickeln."),
("de-DE-KatjaNeural","Moderatorin: Welche Rolle spielen digitale Informationen?"),
("de-DE-AmalaNeural","Hoffmann: Fahrpläne, Anträge und städtische Internetseiten müssen auch mit Hilfstechnologien nutzbar sein. Informationen sollten klar formuliert und bei Bedarf in verschiedenen Formaten angeboten werden. Sonst entstehen neue Barrieren, obwohl ein Angebot digital verfügbar ist."),
("de-DE-KatjaNeural","Moderatorin: Manche Kommunen befürchten hohe Kosten. Ist das berechtigt?"),
("de-DE-AmalaNeural","Hoffmann: Öffentliche Haushalte müssen sorgfältig planen. Allerdings kann es günstiger sein, Zugänglichkeit von Anfang an zu berücksichtigen, statt später aufwendig umzubauen. Zudem profitieren viele Menschen davon, etwa Eltern mit Kinderwagen oder Personen mit vorübergehenden Verletzungen."),
("de-DE-KatjaNeural","Moderatorin: Was würden Sie einer Stadt empfehlen, die ihre Infrastruktur modernisiert?"),
("de-DE-AmalaNeural","Hoffmann: Sie sollte Menschen mit unterschiedlichen Bedürfnissen früh einbeziehen, Hindernisse systematisch erfassen und Verbesserungen langfristig planen. Barrierefreiheit ist keine Zusatzleistung, sondern ein Qualitätsmerkmal öffentlicher Räume.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Wie kann unsere Stadt zugänglicher werden? Frau Stein arbeitet in einer Beratungsstelle, Herr Özdemir ist im Verkehrsbeirat. Frau Stein, womit sollten wir beginnen?"),
("de-DE-AmalaNeural","Stein: Betroffene müssen frühzeitig an Planungsentscheidungen beteiligt werden. Oft werden sie erst gefragt, wenn ein Bauprojekt fast fertig ist. Außerdem können kleine Hindernisse auf Gehwegen für Menschen mit Mobilitätseinschränkungen große Folgen haben."),
("de-DE-KatjaNeural","Moderatorin: Herr Özdemir, wo sehen Sie den größten Handlungsbedarf?"),
("de-DE-ConradNeural","Özdemir: Im öffentlichen Verkehr. Barrierefreie Haltestellen und gut zugängliche Fahrzeuge helfen nicht nur Menschen mit Behinderungen, sondern auch Eltern mit Kinderwagen und älteren Fahrgästen. Die Stadt sollte außerdem Informationen in leichter verständlicher Sprache anbieten."),
("de-DE-AmalaNeural","Stein: Bei Neubauten sollte Zugänglichkeit von Anfang an eingeplant werden. Nachträgliche Lösungen sind oft umständlich und teuer. Eine feste Ansprechstelle in der Verwaltung könnte Beschwerden sammeln und die Umsetzung verfolgen."),
("de-DE-ConradNeural","Özdemir: Eine zentrale Stelle wäre hilfreich. Wichtig ist aber auch, dass Beschäftigte im öffentlichen Dienst geschult werden. Technik allein löst nicht jedes Problem. Man muss wissen, wie man Menschen respektvoll unterstützt, ohne ihnen die Selbstständigkeit abzunehmen.")
],
"teil4_01.mp3":[("de-DE-ConradNeural","Guten Tag. In meinem Vortrag beschäftige ich mich mit Barrierefreiheit im öffentlichen Raum. Es geht darum, wie Städte so gestaltet werden können, dass möglichst alle Menschen selbstständig am gesellschaftlichen Leben teilnehmen.\nBarrierefreiheit betrifft nicht nur Menschen mit dauerhaften Behinderungen. Auch ältere Personen, Eltern mit Kinderwagen oder Menschen nach einem Unfall können auf Hindernisse stoßen. Deshalb ist Zugänglichkeit eine Aufgabe der gesamten Gesellschaft.\nEin wichtiger Bereich ist die bauliche Gestaltung. Gehwege sollten ausreichend breit und frei von Hindernissen sein. Öffentliche Gebäude benötigen geeignete Eingänge, Aufzüge und gut erkennbare Orientierungssysteme. In Parks sind feste Wege, Sitzmöglichkeiten und zugängliche Toiletten sinnvoll.\nEbenso wichtig ist der öffentliche Verkehr. Haltestellen müssen sicher erreichbar sein, Informationen sollten visuell und akustisch verfügbar sein, und Fahrzeuge brauchen geeignete Einstiege. Nur wenn die gesamte Reisekette funktioniert, können Menschen selbstständig unterwegs sein.\nBarrieren entstehen auch durch Kommunikation. Informationen in komplizierter Fachsprache schließen Menschen aus. Digitale Angebote sollten mit Hilfstechnologien funktionieren und verschiedene Darstellungsformen ermöglichen.\nBei der Planung ist die Beteiligung betroffener Menschen entscheidend. Sie können auf praktische Schwierigkeiten hinweisen. Beschäftigte in Behörden sollten ebenfalls geschult werden, damit sie angemessen unterstützen können.\nManche Kommunen betrachten barrierefreie Lösungen als zusätzliche Kosten. Langfristig kann es jedoch wirtschaftlicher sein, Zugänglichkeit von Anfang an einzuplanen, statt später Gebäude und Wege umzubauen. Eine gute Gestaltung verbessert die Nutzbarkeit für viele Menschen.\nZusammenfassend lässt sich sagen: Barrierefreiheit entsteht nicht durch eine einzelne Maßnahme. Sie erfordert vorausschauende Planung, verständliche Informationen und die Beteiligung unterschiedlicher Menschen. Eine zugängliche Stadt ermöglicht mehr Menschen ein unabhängiges und gleichberechtigtes Leben.")],
}
async def make_track(name,utterances):
 parts=[]
 for i,(voice,spoken) in enumerate(utterances):
  part=AUDIO/f".{name}.{i:02d}.mp3"; err=None
  for attempt in range(1,6):
   try:
    print(f"{name}: {i+1}/{len(utterances)} {voice} Versuch {attempt}/5",flush=True)
    await edge_tts.Communicate(spoken,voice,rate="-4%").save(str(part))
    if not part.exists() or part.stat().st_size<1000: raise RuntimeError("Audio fehlt oder zu klein")
    err=None; break
   except Exception as exc:
    err=exc; part.unlink(missing_ok=True); print(exc,flush=True)
    if attempt<5: await asyncio.sleep(attempt*2)
  if err: raise RuntimeError(name) from err
  parts.append(part); await asyncio.sleep(1)
  if i<len(utterances)-1:
   silence=AUDIO/f".silence_{name}_{i}.mp3"
   subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t","0.65","-codec:a","libmp3lame","-b:a","64k",str(silence)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True); parts.append(silence)
 listing=AUDIO/f".{name}.txt"; listing.write_text("".join(f"file '{p.resolve()}'\n" for p in parts),encoding="utf-8")
 target=AUDIO/name
 subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(listing),"-codec:a","libmp3lame","-b:a","128k",str(target)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
 for p in parts+[listing]: p.unlink(missing_ok=True)
 if not target.exists() or target.stat().st_size<1024: raise RuntimeError("MP3 ungültig "+name)
async def main():
 if len(tracks)!=8: raise RuntimeError("8 tracks required")
 for name,parts in tracks.items(): await make_track(name,parts)
asyncio.run(main())
expected=["teil1_01.mp3","teil1_02.mp3","teil1_03.mp3","teil1_04.mp3","teil1_05.mp3","teil2_01.mp3","teil3_01.mp3","teil4_01.mp3"]
archive=ROOT/"exam-023.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
 for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
 if sorted(z.namelist())!=sorted(expected) or any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("ZIP invalid")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
