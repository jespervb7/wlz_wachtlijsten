# Beschrijving van bouw dimensie tabel: Zorgaanbieders



## Ophalen van AGB codes

Vanuit de [website van de Iwlz standaarden]("https://modules.istandaarden.nl/tabelbeheer/swagger-ui/index.html#/ZorgaanbiederController/getZorgaanbieders") kunnen wij een REST API bevragen voor data van alle zorgaanbieders. Deze API bevat meer gegevens dan wij nodig hebben. Namelijk mutaties - historie van records en inactieve AGB codes. Alleen actieve AGB codes zonder mutaties gaan wij ophalen.

Deze data hebben wij nodig om vervolgens data van Vektis op te halen met een webscraper. In [Verrijking van gegevens vanuit Vektis](#verrijking-van-gegevens-vanuit-vektis) zullen wij dit verder uitwerken. Deze gegevens zullen, zoals best practices, opslaan as **"Brons"** A.K.A **"Raw"** voordat we bewerkingen hierop uitvoeren.

#### Voorbeeld tabel

| **Mutatiedatum** | **Soort mutatie** | **Geldig vanaf** | **Geldig tot** | **vervangende iWlz-AGB code** | **iWlz-AGB** | **Naam instelling** | **Adres** | **Huisnummer** | **Huisnummertoevoeging** | **Postcode** | **Plaats**  | **Zorgkantoor** | **ERAI indicerend** |
|------------------|-------------------|------------------|----------------|-------------------------------|--------------|---------------------|-----------|----------------|--------------------------|--------------|-------------|-----------------|----------------------|
| 12102011         | NIEUW             | 17102010         |                |                               | 06010101     | Delfzicht           | JACHTLN   | 50             |                          | 9934JD       | DELFZYL     | 5501            |                      |
| 11102010         |                   | 01011900         | 04082010       |                               | 06010105     | REFAJA ZIEKENHUIS   | Postbus   | 109            |                          | 9500AC       | Stadskanaal | 5501            |                      |
| 12102011         | NIEUW             | 17102010         |                |                               | 06010107     | Martini             | POSTBUS   | 30033          |                          | 9700RM       | GRONINGEN   | 5501            |                     Ja |

## Verrijking van gegevens vanuit Vektis