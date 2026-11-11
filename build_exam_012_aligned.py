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
"teil1_01.mp3":[("de-DE-KatjaNeural","Hinweis der Stadtbibliothek: Ab nächster Woche können Besucherinnen und Besucher ihre Bibliothekskarte auch über das Online-Konto sperren lassen. Bei Verlust bleibt eine persönliche Meldung am Schalter weiterhin möglich. Die Sperre wird sofort wirksam.")],
"teil1_02.mp3":[("de-DE-KatjaNeural","Ich habe mein Profil auf einer Plattform auf öffentlich gestellt."),("de-DE-ConradNeural","Überleg dir das gut. Auch alte Fotos und Kommentare können später noch sichtbar sein."),("de-DE-KatjaNeural","Ich möchte aber, dass neue Leute meine Projekte finden."),("de-DE-ConradNeural","Dann könntest du nur berufliche Beiträge öffentlich zeigen und private Inhalte einschränken.")],
"teil1_03.mp3":[("de-DE-KatjaNeural","Mitteilung der Schule: Der Informationsabend zum sicheren Umgang mit sozialen Netzwerken beginnt am Mittwoch um 18.30 Uhr. Eltern und Jugendliche können gemeinsam teilnehmen. Eine Kinderbetreuung wird während der Veranstaltung nicht angeboten.")],
"teil1_04.mp3":[("de-DE-AmalaNeural","Ich verwende für jedes wichtige Konto ein eigenes Passwort und habe zusätzlich eine Zwei-Faktor-Bestätigung aktiviert. Das ist etwas umständlicher, aber wenn ein Passwort bekannt wird, sind nicht automatisch alle meine Konten gefährdet.")],
"teil1_05.mp3":[("de-DE-KatjaNeural","Durchsage im Medienzentrum: Die geplante Wartung des WLAN-Netzes findet nicht am Freitag, sondern am Sonntag zwischen sechs und acht Uhr morgens statt. Während dieser Zeit ist der Zugang zum Gastnetz nicht möglich.")],
"teil2_01.mp3":[
("de-DE-KatjaNeural","Moderator: Viele Menschen teilen täglich persönliche Informationen in sozialen Netzwerken. Frau Lenz, Sie arbeiten in einer Beratungsstelle für digitale Sicherheit. Welches Risiko wird häufig unterschätzt?"),
("de-DE-AmalaNeural","Lenz: Viele Nutzer denken, dass ein Beitrag verschwindet, sobald sie ihn löschen. Andere Personen können ihn jedoch vorher gespeichert oder weitergeleitet haben. Deshalb sollte man vor dem Veröffentlichen überlegen, wer die Information später sehen könnte."),
("de-DE-KatjaNeural","Moderator: Sind private Profile automatisch sicher?"),
("de-DE-AmalaNeural","Lenz: Nein. Einstellungen können sich ändern, und Kontakte können Inhalte weitergeben. Ein privates Profil reduziert die Sichtbarkeit, bietet aber keine absolute Kontrolle. Besonders vorsichtig sollte man mit Angaben zu Wohnort, Tagesablauf oder Kindern sein."),
("de-DE-KatjaNeural","Moderator: Was empfehlen Sie bei Passwörtern?"),
("de-DE-AmalaNeural","Lenz: Für jeden wichtigen Dienst ein eigenes, langes Passwort. Ein Passwortmanager kann helfen, solche Zugangsdaten sicher zu verwalten. Zusätzlich ist eine Zwei-Faktor-Authentifizierung sinnvoll, weil ein Passwort allein dann nicht genügt."),
("de-DE-KatjaNeural","Moderator: Wie erkennt man problematische Nachrichten?"),
("de-DE-AmalaNeural","Lenz: Misstrauen ist angebracht, wenn jemand starken Zeitdruck erzeugt, persönliche Daten verlangt oder auf eine unbekannte Seite verweist. Links sollte man nicht unüberlegt öffnen. Im Zweifel kontaktiert man die betreffende Organisation über einen bekannten offiziellen Weg."),
("de-DE-KatjaNeural","Moderator: Was ist Ihr wichtigster Rat?"),
("de-DE-AmalaNeural","Lenz: Datenschutz ist keine einmalige Einstellung. Man sollte regelmäßig prüfen, welche Apps Zugriff haben, welche Informationen öffentlich sind und ob die eigenen Gewohnheiten noch passen.")
],
"teil3_01.mp3":[
("de-DE-KatjaNeural","Moderatorin: Sollten soziale Netzwerke verpflichtet werden, die Identität aller Nutzer zu überprüfen? Herr Wolf, Sie vertreten eine Initiative für digitale Bürgerrechte."),
("de-DE-ConradNeural","Wolf: Eine allgemeine Identitätspflicht halte ich für problematisch. Menschen brauchen manchmal die Möglichkeit, unter einem Pseudonym zu sprechen, etwa wenn sie Missstände melden. Eine zentrale Sammlung echter Namen würde neue Datenschutzrisiken schaffen."),
("de-DE-KatjaNeural","Moderatorin: Frau Berger, Sie arbeiten im Bereich Medienbildung."),
("de-DE-AmalaNeural","Berger: Ich verstehe den Schutz anonymer Stimmen. Gleichzeitig erleben wir Beleidigungen und gezielte Täuschung. Plattformen müssen schneller auf glaubwürdige Meldungen reagieren und ihre Beschwerdewege verständlicher machen."),
("de-DE-ConradNeural","Wolf: Bei konkreten Straftaten sollen Behörden rechtmäßig ermitteln können. Das rechtfertigt aber nicht, dass jede Person vor dem Schreiben ihren Ausweis hochladen muss."),
("de-DE-AmalaNeural","Berger: Eine abgestufte Lösung wäre denkbar: freiwillige Verifizierung für bestimmte Funktionen, klare Regeln gegen Missbrauch und mehr Personal für die Moderation."),
("de-DE-KatjaNeural","Moderatorin: Beide Gesprächspartner wollen Missbrauch eindämmen, setzen aber unterschiedliche Schwerpunkte beim Schutz anonymer Kommunikation.")
],
"teil4_01.mp3":[("de-DE-ConradNeural","Guten Tag. In meinem Vortrag geht es um Datenschutz und die Verantwortung von Plattformen. Soziale Netzwerke ermöglichen Austausch, Information und berufliche Kontakte. Gleichzeitig sammeln sie Daten über Interessen, Aufenthaltsorte und Nutzungsverhalten. Diese Informationen können für personalisierte Angebote genutzt werden, aber auch unerwünschte Folgen haben. Ein erster Schutz besteht darin, nur notwendige Angaben zu veröffentlichen. Wer ein Profil erstellt, sollte prüfen, ob Geburtsdatum, Telefonnummer oder Wohnort wirklich sichtbar sein müssen. Besonders vorsichtig ist mit Informationen über Kinder und andere Personen umzugehen, die nicht selbst über eine Veröffentlichung entscheiden können. Ein zweiter Schritt betrifft technische Einstellungen. Nutzer sollten Zugriffsrechte von Apps kontrollieren, unbekannte Anwendungen entfernen und sichere Passwörter verwenden. Eine zusätzliche Bestätigung beim Einloggen bietet einen weiteren Schutz. Trotzdem kann keine einzelne Einstellung sämtliche Risiken ausschließen. Auch Plattformbetreiber tragen Verantwortung. Sie müssen verständlich erklären, welche Daten sie sammeln und zu welchem Zweck. Einstellungen sollten leicht auffindbar sein. Außerdem brauchen Nutzer wirksame Möglichkeiten, falsche Profile, Betrugsversuche und beleidigende Inhalte zu melden. Schulen und Erwachsenenbildung können digitale Urteilsfähigkeit stärken. Dazu gehört nicht nur die Bedienung einer Plattform, sondern auch die Frage, wie Informationen entstehen, wer davon profitiert und welche Spuren eine Veröffentlichung hinterlässt. Ein bewusster Umgang mit sozialen Netzwerken verbindet persönliche Vorsicht mit transparenten Regeln und verantwortlichen Anbietern.")]}
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
archive=ROOT/"exam-012.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    for name in expected: z.write(AUDIO/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    if sorted(z.namelist())!=sorted(expected): raise RuntimeError("Contenu ZIP incorrect")
    if any(x.file_size<1024 for x in z.infolist()): raise RuntimeError("Piste vide ou trop petite")
print(f"Archive validée: {archive} ({archive.stat().st_size} octets)",flush=True)
