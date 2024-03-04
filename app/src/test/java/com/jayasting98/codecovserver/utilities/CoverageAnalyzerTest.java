package com.jayasting98.codecovserver.utilities;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.Arrays;
import java.util.Collection;
import java.util.HashSet;
import java.util.Set;

import org.junit.jupiter.api.Test;

public class CoverageAnalyzerTest {
    @Test
    public void testFindCoveredLineNumbers_typicalCase_findsCorrectly() throws Exception {
        String repositoryDirPathname = "/mnt/c/Users/Jasti/Documents/Work/NUS/AY2324 S1/"
            + "CP4101 B.Comp. Dissertation/repos/dataset-creator/integration_tests/resources/"
            + "repositories/guess-the-number/";
        Collection<String> jarPathnames = Arrays.asList();
        String focalClasspath = repositoryDirPathname + "target/classes/";
        String testClasspath = repositoryDirPathname + "target/test-classes/";
        String focalClassName = "com.example.guessthenumber.ui.CommandLineUi";
        String testClassName = "com.example.guessthenumber.ui.CommandLineUiTest";
        String testMethodName = "testHandleEnd_correctGuess_informsUserOfWin";
        CoverageAnalyzer analyzer = new CoverageAnalyzer(jarPathnames, focalClasspath,
            testClasspath, focalClassName, testClassName, testMethodName);
        Set<Integer> expectedCoveredLineNumbers = new HashSet<>();
        expectedCoveredLineNumbers.add(24);
        expectedCoveredLineNumbers.add(25);
        expectedCoveredLineNumbers.add(26);
        expectedCoveredLineNumbers.add(27);
        expectedCoveredLineNumbers.add(28);
        expectedCoveredLineNumbers.add(79);
        expectedCoveredLineNumbers.add(85);
        expectedCoveredLineNumbers.add(88);
        expectedCoveredLineNumbers.add(89);
        Set<Integer> actualCoveredLineNumbers = analyzer.findCoveredLineNumbers();
        assertEquals(expectedCoveredLineNumbers, actualCoveredLineNumbers);
    }
}
