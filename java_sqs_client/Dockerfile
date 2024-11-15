# Stage 1: Build stage
FROM maven:3.8.8-eclipse-temurin-17 AS build
WORKDIR /app

# Kopier prosjektets pom.xml og src/ mappe til Docker imaget
COPY pom.xml .
COPY src ./src

# Bygg applikasjonen
RUN mvn package

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

# Kopier den ferdige JAR-filen fra build-staget
COPY --from=build /app/target/imagegenerator-0.0.1-SNAPSHOT.jar app.jar

# Sett miljøvariabel for SQS_QUEUE_URL (kan overstyres ved runtime)
ENV SQS_QUEUE_URL=""

# Kjør applikasjonen
ENTRYPOINT ["java", "-jar", "app.jar"]
