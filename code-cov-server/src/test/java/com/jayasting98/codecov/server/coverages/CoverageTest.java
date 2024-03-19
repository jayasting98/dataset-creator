package com.jayasting98.codecov.server.coverages;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.Test;

public class CoverageTest {
    @Test
    public void testGetCoveredLineNumbers_typicalCase_getsCorrectly() {
        List<Integer> coveredLineNumbers = new ArrayList<>();
        coveredLineNumbers.add(42);
        Coverage coverage = new Coverage(coveredLineNumbers);
        assertEquals(coveredLineNumbers, coverage.getCoveredLineNumbers());
    }

    @Test
    public void testSetCoveredLineNumbers_typicalCase_setsCorrectly() {
        Coverage coverage = new Coverage(new ArrayList<>());
        List<Integer> coveredLineNumbers = new ArrayList<>();
        coveredLineNumbers.add(42);
        coverage.setCoveredLineNumbers(coveredLineNumbers);
        assertEquals(coveredLineNumbers, coverage.getCoveredLineNumbers());
    }
}
