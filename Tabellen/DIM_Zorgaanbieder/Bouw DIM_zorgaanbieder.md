# Beschrijving van bouw dimensie tabel: Zorgaanbieders



## Ophalen van AGB codes

Vanuit de [website van de Iwlz standaarden]("https://modules.istandaarden.nl/tabelbeheer/swagger-ui/index.html#/ZorgaanbiederController/getZorgaanbieders") kunnen wij een REST API bevragen voor data van alle zorgaanbieders. Deze API bevat meer gegevens dan wij nodig hebben. Namelijk mutaties - historie van records en inactieve AGB codes. Wij hallen de actuele records op en niet de historie. Historie is voor dit dashboard niet relevant en zullen we dus niet van de API ophalen.

Deze data hebben wij nodig om vervolgens data van Vektis op te halen met een webscraper. In [Verrijking van gegevens vanuit Vektis](#verrijking-van-gegevens-vanuit-vektis) zullen wij dit verder uitwerken. Deze gegevens zullen, zoals best practices, opslaan as **"Brons"** A.K.A **"Raw"** voordat we bewerkingen hierop uitvoeren.

#### Voorbeeld JSON Response
```json
[
  {
    "geldigVanaf": "2023-12-27",
    "geldigTot": "2023-12-27",
    "zorgkantoor": "string",
    "agb": "string",
    "agbVervanger": "string",
    "naamInstelling": "string",
    "erai": true,
    "adres": {
      "straat": "string",
      "huisnummer": 0,
      "huisnummerToevoeging": "string",
      "postcode": "string",
      "plaats": "string"
    },
    "mutaties": [
      {
        "publishDate": "2023-12-27T22:36:58.823Z",
        "type": "WIJZIGING"
      }
    ]
  }
]
```

## Verrijking van gegevens vanuit Vektis d.m.v. de AGB code

Op Vektis staat extra informatie m.b.t. de agb codes, deze informatie gaan wij ophalen.

https://www.vektis.nl/agb-register/onderneming-06290205 < voorbeeld url>
https://www.vektis.nl/agb-register/vestiging-47471602

## Zilver-Cleansed

- voeg zorgsoort toe (30 = verandelijk gehandicapt bijvoorbeeld)

## Problemen tijdens development

#### 1. Verschillende URL's om te scrapen bij Vektis
Dit was wel een irritant probleempje. Om code netjes te houden werd het script eigenlijk complexer, wellicht dat dit wel heel makkelijk op te lossen is met OOP programmeren, maar daar heb ik maar kleine kennis van. Niet genoeg om een creatief of juist idee bij te vormen. 

Voor nu heb ik de simpele oplossing genomen in het kader van een MVP maken. Het is niet de meest "nette" oplossing.

#### 2. Niet elke AGB Code heeft, bijvoorbeeld, een handelsnaam

Met gebruik van een beetje Chat GPT en Stackoverflow kwam ik erachter dat je ook een dict in een list of list mee kunt geven en daar later d.m.v. een pandas series naar kolommen kan converteren. 

#### 2. AGB codes bestaan niet altijd op Vektis