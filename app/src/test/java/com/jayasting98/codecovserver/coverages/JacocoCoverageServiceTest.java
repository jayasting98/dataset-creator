package com.jayasting98.codecovserver.coverages;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.io.File;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
public class JacocoCoverageServiceTest {
    @Autowired
    private CoverageService coverageService;

    @Test
    public void testCreateCoverage_typicalCase_createsCorrectly() throws Exception {
        String repositoryDirPathname = Paths.get("").toAbsolutePath().getParent().toString()
            + File.separator + "integration_tests/resources/repositories/guess-the-number/";
        Collection<String> jarPathnames = Arrays.asList();
        String focalClasspath = repositoryDirPathname + "target/classes/";
        String testClasspath = repositoryDirPathname + "target/test-classes/";
        String focalClassName = "com.example.guessthenumber.ui.CommandLineUi";
        String testClassName = "com.example.guessthenumber.ui.CommandLineUiTest";
        String testMethodName = "testHandleState_overestimate_informsUser";
        Coverage coverage = coverageService.createCoverage(jarPathnames, focalClasspath,
            testClasspath, focalClassName, testClassName, testMethodName);
        List<Integer> expectedCoveredLineNumbers = new ArrayList<>();
        expectedCoveredLineNumbers.add(24);
        expectedCoveredLineNumbers.add(25);
        expectedCoveredLineNumbers.add(26);
        expectedCoveredLineNumbers.add(27);
        expectedCoveredLineNumbers.add(28);
        expectedCoveredLineNumbers.add(53);
        expectedCoveredLineNumbers.add(54);
        expectedCoveredLineNumbers.add(61);
        expectedCoveredLineNumbers.add(62);
        expectedCoveredLineNumbers.add(88);
        expectedCoveredLineNumbers.add(89);
        List<Integer> actualCoveredLineNumbers = coverage.getCoveredLineNumbers();
        assertEquals(expectedCoveredLineNumbers, actualCoveredLineNumbers);
    }
}
