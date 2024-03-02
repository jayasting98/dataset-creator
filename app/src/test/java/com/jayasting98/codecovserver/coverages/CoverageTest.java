package com.jayasting98.codecovserver.coverages;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.HashSet;
import java.util.Set;

import org.junit.jupiter.api.Test;

public class CoverageTest {
    @Test
    public void testGetCoveredLineNumbers_typicalCase_getsCorrectly() {
        Set<Integer> coveredLineNumbers = new HashSet<>();
        coveredLineNumbers.add(42);
        Coverage coverage = new Coverage(coveredLineNumbers);
        assertEquals(coveredLineNumbers, coverage.getCoveredLineNumbers());
    }

    @Test
    public void testSetCoveredLineNumbers_typicalCase_setsCorrectly() {
        Coverage coverage = new Coverage(new HashSet<>());
        Set<Integer> coveredLineNumbers = new HashSet<>();
        coveredLineNumbers.add(42);
        coverage.setCoveredLineNumbers(coveredLineNumbers);
        assertEquals(coveredLineNumbers, coverage.getCoveredLineNumbers());
    }
}
