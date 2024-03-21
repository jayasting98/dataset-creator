package com.jayasting98.codecov.cli;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.io.PrintStream;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.jayasting98.codecov.data.coverages.CreateCoverageRequestData;

class AppTest {
    private InputStream originalIn;
    private PrintStream originalOut;

    @BeforeEach
    void setUp() {
        originalIn = System.in;
        originalOut = System.out;
    }

    @AfterEach
    void tearDown() {
        System.setIn(originalIn);
        System.setOut(originalOut);
    }

    @Test
    void testMain_typicalCase_printsCoverageJsonString() throws JsonProcessingException {
        String projectDirPathname = Paths.get("").toAbsolutePath().getParent().toString();
        String repositoryDirPathname = Paths.get(projectDirPathname, "integration_tests",
            "resources", "repositories", "maven", "guess-the-number", "").toString();
        String mavenDirPathname =
            Paths.get(System.getProperty("user.home"), ".m2", "repository").toString();
        String junitJarPathname =
            Paths.get(mavenDirPathname, "junit", "junit", "4.11", "junit-4.11.jar").toString();
        String hamcrestCoreJarPathname = Paths.get(mavenDirPathname, "org", "hamcrest",
            "hamcrest-core", "1.3", "hamcrest-core-1.3.jar").toString();
        String mockitoCoreJarPathname = Paths.get(mavenDirPathname, "org", "mockito",
            "mockito-core", "3.12.4", "mockito-core-3.12.4.jar").toString();
        String byteBuddyJarPathname = Paths.get(mavenDirPathname, "net", "bytebuddy", "byte-buddy",
            "1.11.13", "byte-buddy-1.11.13.jar").toString();
        String byteBuddyAgentJarPathname = Paths.get(mavenDirPathname, "net", "bytebuddy",
            "byte-buddy-agent", "1.11.13", "byte-buddy-agent-1.11.13.jar").toString();
        String objenesisJarPathname = Paths.get(mavenDirPathname, "org", "objenesis", "objenesis",
            "3.2", "objenesis-3.2.jar").toString();
        String focalClasspath =
            Paths.get(repositoryDirPathname, "target", "classes", "").toString();
        String testClasspath =
            Paths.get(repositoryDirPathname, "target", "test-classes", "").toString();
        List<String> classpathPathnames = Arrays.asList(focalClasspath, testClasspath,
            junitJarPathname, hamcrestCoreJarPathname, mockitoCoreJarPathname, byteBuddyJarPathname,
            byteBuddyAgentJarPathname, objenesisJarPathname);
            String focalClassName = "com.example.guessthenumber.ui.CommandLineUi";
            String testClassName = "com.example.guessthenumber.ui.CommandLineUiTest";
            String testMethodName = "testParseGuess";
        CreateCoverageRequestData requestData = new CreateCoverageRequestData(classpathPathnames,
            focalClasspath, focalClassName, testClassName, testMethodName);
        ObjectMapper mapper = new ObjectMapper();
        String requestDataJsonString = mapper.writeValueAsString(requestData);
        InputStream stubIn = new ByteArrayInputStream(requestDataJsonString.getBytes());
        System.setIn(stubIn);
        PrintStream mockOut = mock(PrintStream.class);
        System.setOut(mockOut);
        String[] args = new String[] {};
        App.main(args);
        verify(mockOut)
            .println("{\"coveredLineNumbers\":[24,25,26,27,28,67,68,69,70,71,72,73,88,89]}");
    }
}
