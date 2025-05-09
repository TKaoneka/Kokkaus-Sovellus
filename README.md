# Kokkaus-Sovellus

Kurssiprojektia varten haluan tehdä sovellusta ruuantekoa varten. Tämä on ollut idea, joka minulla on ollut vuoden alusta lähtien ja olen innostunut tekemään kyseistä sovellusta! Toisin kuin muut ruokasovellukset, jossa reseptin tekijät ovat usein ammattikokkeja, haluamani sovellus kannustaa käyttäjien lisäämään omia reseptejä. Tässä on lyhyt kokoelma sovelluksen toiminnoista:

* Käyttäjä voi luoda käyttäjätunnuksen ja kirjautua sisään sekä ulos sovelluksesta
* Sovelluksessa on eri tapoja etsiä haluamasi ruokareseptejä, riippuen mitä ja miten haluat kokata. Sovelluksessa aikoa olla eri osa miten voi etsiä reseptejä esim. keittiön tyyppien perusteella, kuten välimeren, etelä-aasian, etelä-amerikan ja länsi-afrikan ruuat
* Sovelluksessa toinen tapa etsiä reseptejä on dietin mukaan, kuten urheilua, laihtumista tai painonnousua varten. Jos tekee mieli tiettyä proteinia tai hiilihydraattia, tai nopeita, helppoja reseptejä, voi sovelluksessa etsiä niitä myös
* Käyttäjä voi etsiä eri ruokareseptejä ja tallentaa/poistaa niitä halutessa. Käyttäjä voi tallentaessa editoida reseptiä lokaalisesti esim. lisätä/poistaa ainesosia tai editoida ainesosien määrää. Reseptien ainesosien määrä voi muuttaa keisarillisen ja metrijärjestelmän välissä.
* Halutessa käyttäjä voi muuttaa reseptin annoksien määrä
* Käyttäjä voi seurata muita käyttäjiä ja tehtyessä sekä halutessa käyttäjä voi saada seuratun reseptejä erilliseen sivuun
* Käyttäjä voi myös lisätä sovellukseen omia reseptejä, johon voi antaa kommentteja ja arvosanoja, sekä reddit-tyyppisiä postauksia johon voi esim. kysyä kokkaus- tai laihtumisvinkkejä tai yleisen keskustelun kokkaukseen liittyvä
* Käyttäjä voi lisätä kuvia reseptiin esim. tarvittavat tarvikkeet, reseptin eri vaiheet jne.
*Sovelluksessa on käyttäjäsivut, jossa näkyy käyttäjän ilmoitukset, muiden käyttäjien arvostetut ilmoitukset, käyttäjän kommentit ja käyttäjän seuratut sekä seuraajat.

(30.03.25.)
* Sovelluksessa on muutama uusi sivu, jossa on kaikki tarvittavat asiat tekemään uuden tilin, mutta tilinpoistoa ei ole. Nämä sivut ovat olemassa "templates" kansiossa
* Tietokanta on olemassa, mutta ei .db tiedoston muotona
* Sovelluksen suorituksen tekemä koodi app.py sivun muodostaman koodi ei ole valmiina
* Tapa tehdä kommentteja, arvosteluja ja blogeja, sekä niiden etsiminen eivät ole vielä olemassa

(13.04.25.)
* Sovelluksen perus piirteet pitäisi olla paikoillaan. Nämä ovat ne piirteet, jotka antavat ihmisen luoda tilin, reseptin ja blogin huolimatta sekä hakea niitä postauksen tunnuksen tai otsikon perusteella
* Sovellukseen on lisätty "kommentti" ja "arvostelu" ominaisuuksia, mutta niitä ei vielä ole toteutettu kunnolla 
* Sovelluksen edelliset muodostetut sivut pitäisi toimia kuin on tahdottu
* * Tietokannasta ei voi vielä lajitella tai soudata tietoa
* Tietoa ei voida muokata tai poistaa, vain lisätä
* Käyttäjä ei voi kirjautua ulos
* (Myös pitäisi lisätä, että tietokanta ei ole .db muotona. Se on vieläkin SQL-tiedosto)

(05.05.25.)
Viimeisen lopullisen palautuksen perusteella, sanoisin että olen tyytyväinen sovelluksen toimivuuteen. Voisi olla parempi, mutta kuitenkin sovellus tekee suurimmaksi osaksi oikein kaikki asiat, ja löytyi vähemmän bugeja kuin kelasin. Kerron sovelluksen tilanteesta:
* Sovellus voi luoda tilin ja hoitaa kaikki mahdolliset sivupyynnöt
* Sovellus lisää kaikki tarvittavat tiedot resepteistä, blogeista, kommenteista ja arvioinneista tietokantaan
* Sovellus antaa käyttäjän poistaa hänen tekemänsä reseptit, arvioinnit jne.
* Sovellus antaa käyttäjän lisätä profiilikuvan sekä pikkukuvan ruuasta reseptiin
* Sovelluksessa on kaikki tarvittavat turvamenetelmät (paitsi csrf-tokenin tarkastus, joka on lisätty jo viimeisimpään versioon)
* (En lisännyt reseptin editointia vaihtoehtona tahallaan. Reseptiä voidaan vain poistaa)
Seuraavaksi sovelluksessa ei ole:
* Tapaa soudata tai lajitella esim. reseptejä (halusin alunperin lisätä eri vaihtoehtoja esim. ruuan lajittelu alueittain, ruuan tarkoitus ja keittoaika jne)
* CSRF-token
* Testattu sovelluksen nopeutta suurella määrällä tietoa eikä sivu piirrettä (kuitenkin tärkeimmissä tietopyynnöissä on LIMIT 100)
* Tapa poistaa kommentteja/arviointeja, joka aiheuttaa bugin joka näyttää väärälle reseptille tai blogille kommentit poistaessa jonkin reseptin tai blogin
* CSS-tyyliä
* muita pieniä piirteitä, jotka auttavat toimivuudella ja käytettävyydellä
Sovelluksen koodi on myös kaikki samassa app-tiedostossa ja ei ole optimoitu. Sovelluksessa ei käytetty javascriptia paitsi reseptin tekemisessä, joka oli myös ainoa paikka projektissa jossa käytettiin CurreChattia avuksi

Viimeisessä versiossa suurin osa sovelluksen puutteista ovat jo korjattu.
Mikäli sovelluksessa on muita ongelmia, en niitä huomannut itse.

Toivottavasti sovellus toimii ja nautitte konseptista!

Thierry Kaoneka
