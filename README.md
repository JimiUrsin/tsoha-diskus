# Diskus
Diskus on keskustelusovellus, jossa on useita alueita eri aiheen keskustelua varten. Alueilla on keskusteluketjuja, jotka muodostuvat viesteistä. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

### Sovelluksen testaus
Sovellusta pääsee kokeilemaan siirtymällä Herokuun https://tsoha-diskus.herokuapp.com/

### Projektin nykytilanne (välipalautus 3)
Kuten sovelluksen ominaisuuksista näkyy, sovellus on miltei valmis. Jäljellä on enää ketjujen ja viestien muokkauksen lisääminen ja tietenkin jo lisättyjen ominaisuuksien hiominen. Sovelluksen visuaalinen puoli kaipaa toki myös parannusta. Koodin uudelleenjärjestäminen viime välipalautuksessa mainittuun muotoon olisi myös tarkoitus tehdä ennen lopullista palautusta.

### Sovelluksen ominaisuuksia
✅ = lisätty, ❌ = ei vielä lisätty
- ✅ Itsensä voi tällä hetkellä (testaamista varten) muuttaa ylläpitäjäksi tai takaisin käyttäjäksi
- ✅ Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- ✅ Käyttäjä näkee sovelluksen etusivulla listan alueista
- ✅ Käyttäjä näkee jokaisen alueen ketjujen ja viestien määrän
- ✅ Käyttäjä näkee viimeksi lähetetyn viestin ajankohdan.
- ✅ Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
- ✅ Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
- ❌ Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä.
- ✅ Käyttäjä voi myös poistaa ketjun tai viestin.
- ✅ Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
- ✅ Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
- ✅ Ylläpitäjä voi luoda salaisen alueen jolle vain ylläpitäjillä on pääsy

### Tiedetyt ongelmat
- Ajat näkyvät UTC-ajassa eivätkä Suomen ajassa. En aio korjata tätä.