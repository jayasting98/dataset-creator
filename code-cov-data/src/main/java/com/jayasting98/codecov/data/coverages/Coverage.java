package com.jayasting98.codecov.data.coverages;

import java.util.List;

public class Coverage {
    private List<Integer> coveredLineNumbers;

    public Coverage(List<Integer> coveredLineNumbers) {
        this.coveredLineNumbers = coveredLineNumbers;
    }

    public void setCoveredLineNumbers(List<Integer> coveredLineNumbers) {
        this.coveredLineNumbers = coveredLineNumbers;
    }

    public List<Integer> getCoveredLineNumbers() {
        return coveredLineNumbers;
    }
}
