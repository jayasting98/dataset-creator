plugins {
    application
}

repositories {
    mavenCentral()
}

dependencies {
    testImplementation(libs.junit.jupiter)
    testImplementation("org.mockito:mockito-core:5.11.0")

    testRuntimeOnly("org.junit.platform:junit-platform-launcher")

    implementation("com.fasterxml.jackson.core:jackson-databind:2.17.0")
    implementation(project(":code-cov-data"))
    implementation(project(":code-cov-utilities"))
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(17)
    }
}

application {
    mainClass = "com.jayasting98.codecov.cli.App"
}

tasks.named<Test>("test") {
    useJUnitPlatform()
}
