
# Kandidat 29 - PGR301 DevOps Eksamen 2024 - Couch Explorers

---

## Oppgave 1 - AWS Lambda

### A: Implementer en Lambda-funksjon med SAM og API Gateway
Jeg har implementert en AWS Lambda-funksjon ved hjelp av AWS SAM som eksponerer et POST-endepunkt via API Gateway. Funksjonen genererer bilder basert på et "prompt" sendt i HTTP-body og lagrer bildene i S3-bucketen `pgr301-couch-explorers` under mappen `29/generated_images`.

#### Leveranse
- **HTTP Endepunkt for Lambda-funksjonen:**
  [https://7tppork5tf.execute-api.eu-west-1.amazonaws.com/Prod/generate](https://7tppork5tf.execute-api.eu-west-1.amazonaws.com/Prod/generate)

- ***Eksempel på bruk med curl:***
    ```bash
    curl -X POST https://7tppork5tf.execute-api.eu-west-1.amazonaws.com/Prod/generate \
    -H "Content-Type: application/json" \
    -d '{"prompt": "A beautiful sunset over the mountains with soft pink and orange hues."}'
    ```

---

### B: Opprett en GitHub Actions Workflow for SAM-deploy
Jeg har opprettet en GitHub Actions workflow som automatisk deployer Lambda-funksjonen hver gang det skjer en push til `main`-branchen.

#### Leveranse
- **Lenke til kjørt GitHub Actions workflow:**
  [Deploy SAM Application Workflow](https://github.com/prebenohre/PGR301-DevOps-Exam/actions/runs/11824291833/job/32945471053)

---

## Oppgave 2 - Infrastruktur med Terraform og SQS

### A: Infrastruktur som kode
Jeg har skrevet Terraform-kode for å konfigurere:
- Lambda-funksjonen med SQS-integrasjon (bruker koden i `lambda_sqs.py`)
- En egen SQS-kø og nødvendig integrasjon for AWS Lambda
- Nødvendige IAM-ressurser

Terraform state-filen er lagret i S3-bucketen `pgr301-2024-terraform-state` under `image-generator-lambda-29/terraform.tfstate`.

#### Leveranser
- **SQS Kø URL:** 
  [https://sqs.eu-west-1.amazonaws.com/244530008913/image-generation-queue-29](https://sqs.eu-west-1.amazonaws.com/244530008913/image-generation-queue-29)

- ***Test av SQS-køen med AWS CLI:***
    ```bash
    aws sqs send-message --queue-url "https://sqs.eu-west-1.amazonaws.com/244530008913/image-generation-queue-29" \
    --message-body "A beautiful mountain landscape at sunrise with mist." --output json
    ```

---

### B: Opprett en GitHub Actions Workflow for Terraform
Jeg har laget en GitHub Actions workflow som håndterer deploy av infrastrukturen til AWS ved å kjøre Terraform-koden. Workflowen kjører `terraform apply` ved push til `main` og `terraform plan` ved push til andre branches.

#### Leveranser
- **Lenke til kjørt GitHub Actions workflow på main:** 
  [Terraform Apply Workflow on Main](https://github.com/prebenohre/PGR301-DevOps-Exam/actions/runs/11852263979/job/33030123146)

- **Lenke til kjørt GitHub Actions workflow på annen branch:** 
  [Terraform Plan Workflow on Feature Branch](https://github.com/prebenohre/PGR301-DevOps-Exam/actions/runs/11852236051/job/33030042683)

---


## Oppgave 3 - Javaklient og Docker

### A: Skriv en Dockerfile
Jeg har skrevet en Dockerfile for Java-koden som bygger og kjører applikasjonen i et effektivt og kompakt image ved hjelp av multi-stage builds.

---

### B: Lag en GitHub Actions Workflow som publiserer container image til Docker Hub
Jeg har laget en GitHub Actions workflow som bygger og publiserer Docker-imaget til min konto på Docker Hub hver gang det gjøres en push til `main`.

#### Leveranser

- **Beskrivelse av taggestrategi:**
  - **latest tag:** 
    Hver gang vi gjør en push til `main`-branchen, bygger vi Docker-imaget og tagger det med `latest`. Dette gjør at teammedlemmer alltid kan hente ned den nyeste versjonen av applikasjonen uten å måtte kjenne til spesifikke versjoner.
  - **Commit SHA tag:** 
    Docker-imaget tagges også med den korte versjonen av commit SHA (`${{ github.sha }}`). Dette gir en unik tag for hver enkelt build basert på den spesifikke committen.

  **Begrunnelse av taggestrategien:**
  - **Enkel tilgang med `latest`:** 
    Ved å ha en `latest` tag kan teammedlemmer og automatiserte systemer alltid trekke ned den nyeste versjonen av applikasjonen uten å måtte vite den spesifikke versjonen. Dette forenkler distribusjon og testing, da man kan bruke samme tag hver gang for å få siste oppdatering.
  - **Sporbarhet med commit SHA:** 
    Ved å inkludere commit SHA som en tag, kan vi spore hvert Docker-image tilbake til den nøyaktige koden som ble brukt for å bygge det. Dette er nyttig for feilsøking og historikk, da vi kan identifisere nøyaktig hvilken kodeendring som forårsaket en eventuell feil eller endring i oppførsel. Det gir også mulighet til å rulle tilbake til en tidligere versjon ved å referere til en spesifikk commit.
  - **Best av begge verdener:** 
    Ved å kombinere begge taggene får vi både enkelhet og sporbarhet. `latest` gir oss rask tilgang til den nyeste stabile versjonen, mens commit SHA-taggen gir oss detaljert kontroll og oversikt over hver enkelt build.

- **Container image og SQS URL:**
  - **Docker Hub Image:** `prebenohre/sqs-client`
  - **SQS Kø URL:** 
    [https://sqs.eu-west-1.amazonaws.com/244530008913/image-generation-queue-29](https://sqs.eu-west-1.amazonaws.com/244530008913/image-generation-queue-29)

- ***Docker kommando for å teste Docker-imaget:***
    ```bash
    docker run --rm \
      -e AWS_ACCESS_KEY_ID=<din_egen_access_key> \
      -e AWS_SECRET_ACCESS_KEY=<din_egen_secret_key> \
      -e SQS_QUEUE_URL=https://sqs.eu-west-1.amazonaws.com/244530008913/image-generation-queue-29 \
      prebenohre/sqs-client:latest "me on top of a pyramid"
    ```

- ***Lenke til GitHub Actions workflow som pusher til Docker Hub:*** 
  [Docker Publish Workflow](https://github.com/prebenohre/PGR301-DevOps-Exam/actions/runs/11862805143/job/33062977331)

---


## Oppgave 4 - Metrics og overvåkning
Jeg har utvidet Terraform-koden fra Oppgave 2 med en CloudWatch-alarm som trigges når verdien for `ApproximateAgeOfOldestMessage` blir for høy. Alarmen sender en e-post til en adresse spesifisert som både en variabel i Terraform-koden, og en repository secret på GitHub. E-post ble mottatt under testing og det beskrftes dermed at alarmen fungerer som forventet.

#### Leveranser
- **Lenke til oppdatert GitHub Actions workflow:** 
  [Terraform Deploy with CloudWatch Alarm](https://github.com/prebenohre/PGR301-DevOps-Exam/actions/runs/11862805143/job/33062977331)

---

## Oppgave 5 - Drøfting: Serverless, Function as a Service vs Container-teknologi


### Automatisering og kontinuerlig levering (CI/CD)
- **Serverless Arkitektur:**
  - Med FaaS håndteres infrastrukturen av skyleverandøren, noe som reduserer kompleksiteten i deploy-prosessen. Funksjoner kan distribueres individuelt, noe som muliggjør hyppigere og mer granulære utrullinger.
  - Pipeline for serverless applikasjoner kan være enklere fordi man ikke trenger å bygge og distribuere containere eller håndtere infrastruktur. Automatiseringsverktøy som AWS SAM og Serverless Framework kan brukes for å definere og deploye funksjoner og tilhørende ressurser.

- **Mikrotjenestearkitektur:**
  - Mikrotjenester kjøres ofte i containere som krever orkestrering ved hjelp av verktøy som Kubernetes. Dette øker kompleksiteten i CI/CD-pipelines, da man må håndtere bygging, testing og distribusjon av containere.
  - Krever mer omfattende automatisering for å håndtere infrastruktur, nettverk og tjenesteavhengigheter. Pipelines må også sørge for versjonskontroll og kompatibilitet mellom tjenester.

- **Styrker og Svakheter:**
  - *Serverless:* Reduserer tiden til produksjon og forenkler deploy, men kan føre til utfordringer med versjonskontroll når antall funksjoner øker.
  - *Mikrotjenester:* Gir mer kontroll over infrastrukturen og kan være bedre egnet for komplekse systemer, men krever mer vedlikehold og avansert automatisering.



### Observability (Overvåkning)
- **Serverless Arkitektur:**
  - Funksjoner i FaaS er ofte kortvarige og kan skaleres automatisk, noe som gjør det vanskeligere å samle inn konsistente logger og metrikk.
  - Med mange små funksjoner kan det være utfordrende å spore gjennomgående transaksjoner og identifisere feil.
  - Avhengig av skyleverandørens overvåkningsverktøy som AWS CloudWatch, men kan kreve ekstra innsats for å implementere sammenhengende logging og sporing.

- **Mikrotjenestearkitektur:**
  - Tjenester kjører kontinuerlig, noe som gjør det enklere å samle inn data over tid.
  - Det finnes modne verktøy og mønstre for overvåkning av mikrotjenester, inkludert distribuert tracing og sentralisert logging.
  - Flere tjenester kan føre til kompleks overvåkning, men dette kan håndteres med riktig verktøysett.

- **Styrker og Svakheter:**
  - *Serverless:* Kan redusere synlighet og gjøre feilsøking vanskeligere, spesielt over tjenestegrenser.
  - *Mikrotjenester:* Tilbyr bedre muligheter for overvåkning, men kan bli komplekst uten riktig praksis.



### Skalerbarhet og kostnadskontroll
- **Serverless Arkitektur:**
  - FaaS-tjenester skalerer automatisk basert på etterspørsel, uten behov for manuell intervensjon.
  - Kostnader er basert på faktisk forbruk (antall kjøringer og varighet), noe som kan være kostnadseffektivt for ujevne arbeidsbelastninger.
  - Kan oppstå forsinkelser ved oppstart av funksjoner, noe som påvirker responstid.

- **Mikrotjenestearkitektur:**
  - Krever ofte manuell konfigurasjon eller komplisert auto-skalering ved hjelp av orkestreringsverktøy.
  - Kjører kontinuerlig, noe som kan føre til høyere faste kostnader, selv ved lav belastning.
  - Mulighet for bedre optimalisering av ressurser for tjenester med jevn belastning.

- **Styrker og Svakheter:**
  - *Serverless:* Utmerket for variable belastninger og kan redusere kostnader, men kan gi uforutsigbare responstider.
  - *Mikrotjenester:* Gir mer kontroll over ytelse og kan være mer kostnadseffektivt for tjenester med stabil høy belastning.



### Eierskap og ansvar
- **Serverless Arkitektur:**
  - Skyleverandøren håndterer infrastrukturen, noe som frigjør teamet til å fokusere på kode og forretningslogikk.
  - Flere små funksjoner kan føre til utfordringer med versjonskontroll, testing og distribusjon.
  - Teamet må utvikle nye ferdigheter for å overvåke og feilsøke i en serverless kontekst.

- **Mikrotjenestearkitektur:**
  - Teamet er ansvarlig for hele stacken, inkludert infrastruktur, noe som gir større fleksibilitet men også mer arbeid.
  - Risiko for at teamet deler seg etter tjenestegrenser, noe som kan hindre samarbeid.

- **Styrker og Svakheter:**
  - *Serverless:* Frigjør ressurser fra infrastrukturvedlikehold, men kan føre til tap av kontroll og krever tillit til skyleverandøren.
  - *Mikrotjenester:* Gir full kontroll, men øker ansvarsområdet og kan kreve større teamkompetanse.

---


## Oppsummering av Leveranser

| Oppgave | Leveranse                                                                                         |
|---------|-----------------------------------------------------------------------------------------------------|
| 1 A     | HTTP Endepunkt: [https://7tppork5tf.execute-api.eu-west-1.amazonaws.com/Prod/generate](https://7tppork5tf.execute-api.eu-west-1.amazonaws.com/Prod/generate)         |
| 1 B     | [Deploy SAM Application Workflow](https://github.com/prebenohre/PGR301-DevOps-Exam/actions/runs/11824291833/job/32945471053) |
| 2 A     | SQS-Kø URL: [https://sqs.eu-west-1.amazonaws.com/244530008913/image-generation-queue-29](https://sqs.eu-west-1.amazonaws.com/244530008913/image-generation-queue-29)            |
| 2 B     | [Terraform Apply Workflow on Main](https://github.com/prebenohre/PGR301-DevOps-Exam/actions/runs/11852263979/job/33030123146) |
| 2 B     | [Terraform Plan Workflow on Feature Branch](https://github.com/prebenohre/PGR301-DevOps-Exam/actions/runs/11852236051/job/33030042683) |
| 3       | Beskrivelse av taggstrategi i README.md under oppgave 3 B.                                                     |
| 3      | Docker Image: `prebenohre/sqs-client`                                                               |
| 3      | SQS-Kø URL: [https://sqs.eu-west-1.amazonaws.com/244530008913/image-generation-queue-29](https://sqs.eu-west-1.amazonaws.com/244530008913/image-generation-queue-29)|
| 4       | [Terraform Deploy with CloudWatch Alarm](https://github.com/prebenohre/PGR301-DevOps-Exam/actions/runs/11862805143/job/33062977331)                                               |
| 5       | Drøfting inkludert i README.md under oppgave 5.                                                     |

