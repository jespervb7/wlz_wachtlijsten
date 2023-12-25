# Introductie

## Wat is de WLZ en wat zijn de wachtlijsten?

De WLZ staat voor de Wet Langdurige Zorg en is het vervolg van de AWBZ. Mensen die recht hebben op WLZ hebben meerdere opties voor zorg, meestal gaat dit om een opname in een instelling. In de praktijk komt het voor dat de zorgaanbieder/instelling geen ruimte heeft om de cliënt op te nemen. Hierdoor komt de cliënt op een "wachtlijst". Grofweg onderscheiden we 4 soorten wachtstatussen:

| **Wachtlijst status** | **Beschrijving status**                                                                                                                               |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------|
| Urgent plaatsen       | Er is noodzaak om de cliënt z.s.m. op te nemen door een dringende zorgvraag. Mogelijk gebeurd dit bij een andere instelling.                          |
| Actief plaatsen       | Er is sprake van een dringende zorgvraag (binnen een half jaar), maar dit kan eventueel nog uitgesteld worden.                                        |
| Wacht op voorkeur     | Er is een opnamewens, maar er is geen sprake van dringende zorg.                                                                                      |
| Wacht uit voorzorg    | De cliënt woont thuis en wilt nog niet opgenomen worden. Voor de zekerheid wilt de cliënt toch in beeld blijven bij hun voorkeurs instelling          |

## Requirements - WIP
 - Inzicht in verloop van wachttijden
 - Dashboard is te filteren op:
    - Zorgverzekeraar
    - Huidige zorgverzekeraar (door fusies van bijvoorbeeld Agis. Dit is dan Zilveren Kruis ipv Agis)
    - 

## Vervolg

Het is jammer dat er geen openbare datasets zijn die op wat meer detail niveau opereren. Inhoudelijk zou je dan een veel mooier en bruikbarer dashboard krijgen. Je mist namelijk nu detail niveau (zorgaanbieder of wellicht cliënt niveau), je zou dan vervolg analyses kunnen doen op verschillende regios/zorgaanbieders/etc.

Met de komst van het bemiddelingsregister zou het eventueel mogelijk zijn om, i.p.v. de AW317, realtime gegevens uit het register te halen.

De Nza zou dit eventueel kunnen delen via Azure Entra (Azure Active Directory variant voor gast gebruikers). Via RLS en AD groepen is het namelijk mogelijk om de zorgverzekeraars alleen hun eigen data te tonen. Security technisch gezien kan er geen gebruik gemaakt worden van data van de andere zorgverzekeraars.

Zou ik overigens een leuk project vinden, dus mochten jullie dit zien? Ik hou me aanbevolen ;)!