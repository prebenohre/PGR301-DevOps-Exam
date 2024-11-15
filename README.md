# PGR301 DevOps Eksamen 2024 - Couch Explorers

## Oppgave 1 - AWS Lambda

### A: Lambda-funksjon med SAM og API Gateway

#### Beskrivelse
Lambda-funksjonen er implementert med SAM og eksponert gjennom et API Gateway POST-endepunkt. Når en forespørsel med et bildeprompt sendes til API-et, genereres bildet og lagres i S3.

#### Leveranser
- **API Endepunkt:** `https://7tppork5tf.execute-api.eu-west-1.amazonaws.com/Prod/generate`
- **Eksempel CURL-kommando:**
    ```bash
    curl -X POST https://7tppork5tf.execute-api.eu-west-1.amazonaws.com/Prod/generate \
    -H "Content-Type: application/json" \
    -d '{"prompt": "A beautiful sunset over the mountains with soft pink and orange hues."}'
    ```
- **Bildelagring i S3:** Amazon S3 > Buckets > `pgr301-couch-explorers/29/generated_images`

### B: GitHub Actions Workflow for SAM Deploy

#### Beskrivelse
En GitHub Actions workflow som automatisk deployer Lambda-funksjonen ved push til `main`-branchen.

#### Leveranser
- **Workflow-kjøring:** [GitHub Actions SAM Deploy](https://github.com/prebenohre/PGR301-DevOps-Exam/actions/runs/11824291833/job/32945471053)

---

## Oppgave 2 - Infrastruktur med Terraform og SQS

### A: Infrastruktur med Terraform

#### Beskrivelse
Terraform-kode for opprettelse av en SQS-kø og integrasjon med en Lambda-funksjon, inkludert IAM-roller og -policyer.

#### Leveranser
- **S3-bucket for Terraform state:** `Amazon S3 > pgr301-2024-terraform-state > image-generator-lambda-29`
- **SQS-kø URL:** `https://sqs.eu-west-1.amazonaws.com/244530008913/image-generation-queue-29`
- **Testkommando for SQS-kø:**
    ```bash
    aws sqs send-message --queue-url "https://sqs.eu-west-1.amazonaws.com/244530008913/image-generation-queue-29" \
    --message-body "A beautiful mountain landscape at sunrise with mist." --output json
    ```
- **Bildelagring i S3:** Amazon S3 > Buckets > `pgr301-couch-explorers/29/sqs_generated_images`

### B: GitHub Actions Workflow for Terraform

#### Beskrivelse
En GitHub Actions workflow som kjører `terraform apply` ved push til `main`-branchen og `terraform plan` ved push til andre brancher.

#### Leveranser
- **Workflow-kjøring (terraform apply på main):** [GitHub Actions Terraform Apply](https://github.com/prebenohre/PGR301-DevOps-Exam/actions/runs/11852263979/job/33030123146)
- **Workflow-kjøring (terraform plan på feature/test-workflow):** [GitHub Actions Terraform Plan](https://github.com/prebenohre/PGR301-DevOps-Exam/actions/runs/11852236051/job/33030042683)

---

## Oppgave 3 - Javaklient og Docker

### Forberedelse: Testing av Java-koden

#### Kommandoer
- **Kompiler JAR-fil:**
    ```bash
    mvn package
    ```
- **Kjør JAR med testprompt:**
    ```bash
    export SQS_QUEUE_URL=https://sqs.eu-west-1.amazonaws.com/244530008913/image-generation-queue-29
    java -jar target/imagegenerator-0.0.1-SNAPSHOT.jar "Me on top of K2"
    ```

### A: Dockerfile for Java-klient

#### Beskrivelse
En Dockerfile som bruker multi-stage build for å kompilere Java-koden og kjøre applikasjonen i et minimalt runtime-miljø.

### B: GitHub Actions Workflow for Docker Hub Deploy

#### Beskrivelse
GitHub Actions workflow for å bygge og publisere Docker-imaget til Docker Hub ved push til `main`-branchen.

#### Leveranser
- **Workflow-kjøring:** [GitHub Actions Docker Publish](https://github.com/prebenohre/PGR301-DevOps-Exam/actions/runs/11862805143/job/33062977331)
- **Container image:** `prebenohre/sqs-client`
- **Test Docker-imaget med kommando:**
    ```bash
    docker run --rm \
    -e AWS_ACCESS_KEY_ID=<din_egen_access_key> \
    -e AWS_SECRET_ACCESS_KEY=<din_egen_secret_key> \
    -e SQS_QUEUE_URL=<din_egen_sqs_queue_url> \
    prebenohre/sqs-client:latest "me on top of a pyramid"
    ```

#### Taggestrategi
- **latest tag:** Gir alltid tilgang til siste versjon.
- **Commit SHA tag:** Unik tag for hver build basert på commit SHA for sporbarhet og feilsøking.

---

## Oppgave 4 - Metrics og overvåkning

### A: CloudWatch Alarm for ApproximateAgeOfOldestMessage

#### Beskrivelse
Terraform-kode som oppretter en CloudWatch-alarm basert på SQS-metrikken `ApproximateAgeOfOldestMessage`. Alarmen sender e-post når meldingsalderen overskrider en definert terskel.

#### Leveranser
- **CloudWatch Alarm:** Opprettet og kan verifiseres ved å sende en melding til køen som skaper ventetid.
- **Alarm e-postadresse:** Definert i `terraform.tfvars` som `alarm_email`.

---

## Oppgave 5 - Drøfting: Serverless vs Container-teknologi

### Besvarelse
Drøfting av fordeler og ulemper ved bruk av serverless arkitektur (FaaS og SQS) vs. mikrotjenestearkitektur med hensyn til DevOps-prinsipper som CI/CD, observability, skalerbarhet, kostnadskontroll, eierskap og ansvar.

---

## Leveranseoversikt

| Oppgave    | Leveranse                                          | Beskrivelse                                                                                         |
|------------|----------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| Oppgave 1  | Lambda API Endpoint                                | [API Endpoint](https://7tppork5tf.execute-api.eu-west-1.amazonaws.com/Prod/generate)                |
| Oppgave 1  | GitHub Actions SAM Deploy                          | [Workflow](https://github.com/prebenohre/PGR301-DevOps-Exam/actions/runs/11824291833/job/32945471053) |
| Oppgave 2  | Terraform SQS URL                                  | `https://sqs.eu-west-1.amazonaws.com/244530008913/image-generation-queue-29`                        |
| Oppgave 2  | GitHub Actions Terraform Apply                     | [Terraform Apply](https://github.com/prebenohre/PGR301-DevOps-Exam/actions/runs/11852263979/job/33030123146) |
| Oppgave 2  | GitHub Actions Terraform Plan                      | [Terraform Plan](https://github.com/prebenohre/PGR301-DevOps-Exam/actions/runs/11852236051/job/33030042683) |
| Oppgave 3  | Docker Image                                       | `prebenohre/sqs-client`                                                                             |
| Oppgave 3  | GitHub Actions Docker Publish                      | [Docker Publish Workflow](https://github.com/prebenohre/PGR301-DevOps-Exam/actions/runs/11862805143/job/33062977331) |
| Oppgave 4  | CloudWatch Alarm                                   | Alarm for `ApproximateAgeOfOldestMessage`                                                           |
| Oppgave 5  | Drøfting                                           | Drøfting av serverless vs container-teknologi (se over)                                             |

---
