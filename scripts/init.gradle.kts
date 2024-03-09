allprojects {
    tasks.register("listSubprojects") {
        for (subproject in rootProject.subprojects) {
            println(subproject.name)
        }
    }
    tasks.register("buildMainRuntimeClasspath") {
        println(project.the<SourceSetContainer>()["main"].runtimeClasspath.asPath)
    }
    tasks.register("buildTestRuntimeClasspath") {
        println(project.the<SourceSetContainer>()["test"].runtimeClasspath.asPath)
    }
}
