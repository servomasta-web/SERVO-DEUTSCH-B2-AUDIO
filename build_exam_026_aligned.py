import asyncio, subprocess, zipfile
from pathlib import Path
import edge_tts
ROOT=Path("output"); AUDIO=ROOT/"audio"; AUDIO.mkdir(parents=True,exist_ok=True)
tracks={
"teil1_01.mp3":[("de-DE-KatjaNeural","Die offene Reparaturwerkstatt im Bürgerhaus ist ab sofort jeden Samstag von neun bis zwölf Uhr geöffnet. Ehrenamtliche helfen bei kleinen Reparaturen an Haushaltsgeräten und Fahrrädern. Die erste Diagnose ist kostenlos.")],
"teil1_02.mp3":[("de-DE-ConradNeural","Beim Reparaturtreff können Besucher defekte Geräte gemeinsam mit erfahrenen Helfern untersuchen. Bitte bringen Sie das Gerät und möglichst auch das passende Zubehör mit. Ersatzteile müssen bei Bedarf selbst besorgt werden. Eine Anmeldung ist nicht erforderlich.")],
"teil1_03.mp3":[("de-DE-AmalaNeural","Die Stadtbibliothek erweitert ihr Angebot: Ab Montag können registrierte Nutzer Werkzeugkoffer für kleinere Reparaturen ausleihen. Die Leihfrist beträgt sieben Tage. Eine Verlängerung ist möglich, sofern keine andere Person das Werkzeug vorgemerkt hat.")],
"teil1_04.mp3":[("de-DE-KatjaNeural","Das Umweltzentrum lädt zu einem kostenlosen Vortrag über die Lebensdauer von Elektrogeräten ein. Die Veranstaltung beginnt am Mittwoch um achtzehn Uhr. Interessierte müssen sich vorab über die Website des Umweltzentrums anmelden.")],
"teil1_05.mp3":[("de-DE-ConradNeural","Der städtische Wettbewerb für kreative Reparaturideen geht in die letzte Runde. Projekte können noch bis zum fünfundzwanzigsten September eingereicht werden. Die besten Vorschläge werden im Oktober ausgezeichnet und auf der Internetseite der Stadt vorgestellt.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Viele Menschen kaufen ein neues Gerät, sobald das alte nicht mehr funktioniert. Warum wird so selten repariert?"),
("de-DE-AmalaNeural","Experte: Häufig erscheint eine Reparatur teuer oder kompliziert. Manchmal fehlen Ersatzteile oder verständliche Informationen. Hinzu kommt, dass neue Geräte oft relativ günstig angeboten werden. Verbraucher vergleichen dann den Reparaturpreis mit dem Preis eines neuen Produkts."),
("de-DE-KatjaNeural","Moderatorin: Gibt es inzwischen politische Veränderungen?"),
("de-DE-AmalaNeural","Experte: Ja. Neue europäische Vorgaben sollen die Reparatur erleichtern. Für bestimmte Produktgruppen müssen Hersteller Ersatzteile länger verfügbar halten. Auch Informationen über Reparaturmöglichkeiten werden wichtiger. Das bedeutet allerdings nicht, dass jede Reparatur kostenlos sein muss."),
("de-DE-KatjaNeural","Moderatorin: Was brauchen unabhängige Werkstätten?"),
("de-DE-AmalaNeural","Experte: Sie benötigen Zugang zu Ersatzteilen, technischen Unterlagen und geeigneten Werkzeugen. Wenn Hersteller Informationen zurückhalten oder Teile nur zu hohen Preisen anbieten, wird eine Reparatur unnötig erschwert. Faire Bedingungen sind deshalb entscheidend."),
("de-DE-KatjaNeural","Moderatorin: Welche Bedeutung haben Reparaturcafés?"),
("de-DE-AmalaNeural","Experte: Sie bringen Menschen zusammen, die voneinander lernen. Ehrenamtliche helfen bei einfachen Problemen und zeigen, wie Geräte funktionieren. Solche Treffpunkte ersetzen keine Fachwerkstatt, fördern aber praktische Kenntnisse und einen bewussteren Umgang mit Gegenständen."),
("de-DE-KatjaNeural","Moderatorin: Worauf sollten Verbraucher schon beim Kauf achten?"),
("de-DE-AmalaNeural","Experte: Nicht nur auf den Anschaffungspreis. Wichtig sind auch die erwartete Lebensdauer, die Verfügbarkeit von Ersatzteilen und die Frage, ob sich das Produkt mit üblichen Werkzeugen öffnen lässt. Ein reparierbares Gerät kann langfristig wirtschaftlicher sein."),
("de-DE-KatjaNeural","Moderatorin: Was müsste sich gesellschaftlich noch ändern?"),
("de-DE-AmalaNeural","Experte: Reparieren sollte wieder als normale und sinnvolle Möglichkeit gelten. Dafür brauchen wir verständliche Informationen, gute Ausbildungsangebote und eine Zusammenarbeit zwischen Herstellern, Handel, Werkstätten und Kommunen.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Wie kann eine stärkere Reparaturkultur entstehen? Darüber sprechen Frau Roth von einer Umweltinitiative und Herr Seidel, der eine unabhängige Werkstatt betreibt. Frau Roth, welche Erfahrungen machen Sie?"),
("de-DE-AmalaNeural","Roth: In unseren Reparaturtreffs erleben wir, wie viel Wissen Menschen miteinander teilen können. Solche Angebote sollten stärker unterstützt werden. Außerdem halte ich es für sinnvoll, Reparatur und den Umgang mit Werkzeug schon in Schulen zu behandeln."),
("de-DE-ConradNeural","Seidel: Das begrüße ich. In meiner Werkstatt sehen wir jedoch oft, dass technische Unterlagen fehlen. Ohne Informationen über die Konstruktion lässt sich ein Gerät manchmal kaum öffnen. Hersteller sollten Reparaturanleitungen verständlich und zugänglich bereitstellen."),
("de-DE-AmalaNeural","Roth: Auch Verbraucher brauchen klare Informationen. Sie sollten bereits beim Kauf erkennen können, wie gut ein Gerät reparierbar ist. Transparente Angaben zu Ersatzteilpreisen helfen dabei, eine vernünftige Entscheidung zu treffen."),
("de-DE-ConradNeural","Seidel: Transparenz ist wichtig, aber Fachbetriebe brauchen ebenso faire wirtschaftliche Bedingungen. Ersatzteile müssen zu angemessenen Preisen erhältlich sein. Sonst kann eine Werkstatt ihre Arbeit nicht kostendeckend anbieten, selbst wenn die Reparatur technisch möglich wäre."),
("de-DE-AmalaNeural","Roth: Deshalb sollten Bildungseinrichtungen und Kommunen mit Betrieben zusammenarbeiten. Reparaturwissen ist eine gesellschaftliche Aufgabe. Gleichzeitig können lokale Treffpunkte Menschen ermutigen, zunächst eine Reparatur zu versuchen, statt ein Gerät sofort wegzuwerfen."),
("de-DE-ConradNeural","Seidel: Richtig. Wenn Hersteller technische Informationen bereitstellen und Ersatzteile zugänglich sind, profitieren Verbraucher und Werkstätten. Wichtig ist aber, dass Sicherheitsstandards eingehalten und Reparaturen fachgerecht dokumentiert werden."),
("de-DE-KatjaNeural","Moderatorin: Vielen Dank. Beide sehen also bessere Informationen und Zusammenarbeit als wichtige Voraussetzungen, setzen aber unterschiedliche Schwerpunkte.")
],
"teil4_01.mp3":[
("de-DE-ConradNeural","Guten Tag. In meinem Vortrag beschäftige ich mich mit der Frage, warum Reparieren wieder stärker in den Alltag integriert werden sollte. Viele Gegenstände werden heute ersetzt, obwohl eine Reparatur möglich wäre. Das hat Folgen für die Umwelt und für den Verbrauch wertvoller Rohstoffe. Eine nachhaltige Reparaturkultur kann dazu beitragen, Produkte länger zu nutzen und Abfälle zu vermeiden."),
("de-DE-ConradNeural","Zunächst geht es um die ökologischen Vorteile. Für die Herstellung von Elektrogeräten werden Metalle, Energie und Wasser benötigt. Wird ein Gerät frühzeitig weggeworfen, müssen häufig neue Rohstoffe gewonnen und neue Produkte hergestellt werden. Eine Reparatur kann diesen Bedarf verringern. Sie verhindert zwar nicht jeden Abfall, verlängert aber oft die Nutzungsdauer erheblich."),
("de-DE-ConradNeural","Eine wichtige Voraussetzung ist die Verfügbarkeit von Ersatzteilen. Selbst ein kleiner Defekt macht ein Gerät unbrauchbar, wenn ein passendes Bauteil nicht erhältlich ist. Hersteller sollten deshalb bestimmte Komponenten über einen angemessenen Zeitraum anbieten. Ebenso wichtig sind technische Unterlagen, damit Fachkräfte erkennen können, wie ein Produkt sicher geöffnet und repariert wird."),
("de-DE-ConradNeural","Auch das Produktdesign entscheidet darüber, ob eine Reparatur gelingt. Bei reparaturfreundlichen Geräten lassen sich einzelne Bauteile mit üblichen Werkzeugen austauschen. Stark verklebte Gehäuse oder untrennbar verbundene Komponenten erschweren dagegen die Arbeit. Verbraucher sollten deshalb beim Kauf nicht nur auf Preis und Ausstattung achten, sondern auch auf Reparierbarkeit und erwartete Lebensdauer."),
("de-DE-ConradNeural","Neben Herstellern und Werkstätten spielt die Bildung eine wichtige Rolle. Grundkenntnisse helfen Menschen, kleine Schäden früh zu erkennen und einfache Arbeiten selbst auszuführen. Schulen, Volkshochschulen und Reparaturtreffs können praktische Fähigkeiten vermitteln. Bei komplexen oder sicherheitsrelevanten Schäden bleibt allerdings die Unterstützung qualifizierter Fachkräfte notwendig."),
("de-DE-ConradNeural","Kommunen können diese Entwicklung fördern, indem sie Räume für Reparaturangebote bereitstellen, lokale Initiativen unterstützen und den Austausch zwischen Betrieben und Bürgern erleichtern. Gleichzeitig muss die Qualität der Arbeit stimmen. Eine nachvollziehbare Dokumentation hilft, Sicherheit und Funktionsfähigkeit nach der Reparatur zu beurteilen."),
("de-DE-ConradNeural","Zusammenfassend lässt sich sagen: Eine neue Reparaturkultur entsteht nicht allein durch guten Willen. Sie braucht reparierbare Produkte, zugängliche Ersatzteile, verständliche Informationen und wirtschaftlich tragfähige Werkstätten. Wenn Hersteller, Handel, Bildungseinrichtungen, Kommunen und Verbraucher zusammenarbeiten, wird Reparieren zu einer realistischen Alternative zum Wegwerfen. Vielen Dank für Ihre Aufmerksamkeit.")
]}
async def make(v,t,p): await edge_tts.Communicate(t,v).save(str(p))
async def main():
 for fn,segs in tracks.items():
  parts=[]
  for i,(v,t) in enumerate(segs):
   p=AUDIO/f"{fn[:-4]}_{i:02d}.mp3"; await make(v,t,p); parts.append(p)
  if len(parts)==1: parts[0].replace(AUDIO/fn)
  else:
   m=ROOT/f"{fn[:-4]}_concat.txt"; m.write_text("".join(f"file '{p.resolve()}'\n" for p in parts),encoding="utf-8")
   subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(m),"-c","copy",str(AUDIO/fn)],check=True)
   for p in parts:p.unlink()
   m.unlink()
 out=ROOT/"exam-026.zip"
 with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as z:
  for p in sorted(AUDIO.glob("*.mp3")):z.write(p,p.name)
 expected={f"teil1_0{i}.mp3" for i in range(1,6)}|{"teil2_01.mp3","teil3_01.mp3","teil4_01.mp3"}
 with zipfile.ZipFile(out) as z:
  actual={n for n in z.namelist() if n.endswith(".mp3")}
  assert actual==expected,(actual,expected)
  assert all(z.getinfo(n).file_size>10000 for n in expected)
 print(f"Created {out} ({out.stat().st_size} bytes), {len(expected)} tracks")
if __name__=="__main__":asyncio.run(main())
