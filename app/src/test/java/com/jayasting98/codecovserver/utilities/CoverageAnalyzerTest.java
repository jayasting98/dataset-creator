package com.jayasting98.codecovserver.utilities;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.io.File;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;

import org.junit.jupiter.api.Test;

public class CoverageAnalyzerTest {
    @Test
    public void testFindCoveredLineNumbers_typicalCase_findsCorrectly() throws Exception {
        String repositoryDirPathname = Paths.get("").toAbsolutePath().getParent().toString()
            + File.separator + "integration_tests/resources/repositories/maven/guess-the-number/";
        String focalClasspath = repositoryDirPathname + "target/classes/";
        String testClasspath = repositoryDirPathname + "target/test-classes/";
        Collection<String> classpathPathnames = Arrays.asList(focalClasspath, testClasspath);
        String focalClassName = "com.example.guessthenumber.ui.CommandLineUi";
        String testClassName = "com.example.guessthenumber.ui.CommandLineUiTest";
        String testMethodName = "testHandleEnd_correctGuess_informsUserOfWin";
        CoverageAnalyzer analyzer = new CoverageAnalyzer(classpathPathnames, focalClasspath,
            testClasspath, focalClassName, testClassName, testMethodName);
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
}
