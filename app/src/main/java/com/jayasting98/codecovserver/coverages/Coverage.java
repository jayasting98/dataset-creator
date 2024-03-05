package com.jayasting98.codecovserver.coverages;

import java.util.List;

class Coverage {
    private List<Integer> coveredLineNumbers;

    Coverage(List<Integer> coveredLineNumbers) {
        this.coveredLineNumbers = coveredLineNumbers;
    }

    void setCoveredLineNumbers(List<Integer> coveredLineNumbers) {
        this.coveredLineNumbers = coveredLineNumbers;
    }

    public List<Integer> getCoveredLineNumbers() {
        return coveredLineNumbers;
    }
}
