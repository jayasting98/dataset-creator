package com.jayasting98.codecov.utilities;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.io.File;
import java.lang.reflect.InvocationTargetException;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;

import org.junit.jupiter.api.Test;

public class CoverageAnalyzerTest {
    @Test
    public void testFindCoveredLineNumbers_typicalCase_findsCorrectly() throws Exception {
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
        Collection<String> classpathPathnames = Arrays.asList(focalClasspath, testClasspath,
            junitJarPathname, hamcrestCoreJarPathname, mockitoCoreJarPathname, byteBuddyJarPathname,
            byteBuddyAgentJarPathname, objenesisJarPathname);
        String focalClassName = "com.example.guessthenumber.ui.CommandLineUi";
        String testClassName = "com.example.guessthenumber.ui.CommandLineUiTest";
        String testMethodName = "testHandleEnd_correctGuess_informsUserOfWin";
        CoverageAnalyzer analyzer = new CoverageAnalyzer(classpathPathnames, focalClasspath,
            focalClassName, testClassName, testMethodName);
        List<Integer> expectedCoveredLineNumbers = new ArrayList<>();
        expectedCoveredLineNumbers.add(24);
        expectedCoveredLineNumbers.add(25);
        expectedCoveredLineNumbers.add(26);
        expectedCoveredLineNumbers.add(27);
        expectedCoveredLineNumbers.add(28);
        expectedCoveredLineNumbers.add(79);
        expectedCoveredLineNumbers.add(85);
        expectedCoveredLineNumbers.add(88);
        expectedCoveredLineNumbers.add(89);
        List<Integer> actualCoveredLineNumbers = analyzer.findCoveredLineNumbers();
        assertEquals(expectedCoveredLineNumbers, actualCoveredLineNumbers);
    }

    @Test
    public void testFindCoveredLineNumbers_systemExit_doesNotExit() throws Exception {
        String repositoryDirPathname = Paths.get("").toAbsolutePath().getParent().toString();
        String focalClasspath = Paths.get(repositoryDirPathname, "code-cov-utilities", "build",
            "classes", "java", "test").toString();
        String testClasspath = focalClasspath;
        Collection<String> classpathPathnames = Arrays.asList(focalClasspath, testClasspath);
        String focalClassName = "com.jayasting98.codecov.utilities.CoverageAnalyzerTest";
        String testClassName = "com.jayasting98.codecov.utilities.CoverageAnalyzerTest";
        String testMethodName = "doSystemExit";
        CoverageAnalyzer analyzer = new CoverageAnalyzer(classpathPathnames, focalClasspath,
            focalClassName, testClassName, testMethodName);
        assertThrows(InvocationTargetException.class, analyzer::findCoveredLineNumbers);
    }

    public void doSystemExit() {
        System.exit(2);
    }
}
