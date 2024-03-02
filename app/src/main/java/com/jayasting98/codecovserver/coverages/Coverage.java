package com.jayasting98.codecovserver.coverages;

import java.util.Set;

class Coverage {
    private Set<Integer> coveredLineNumbers;

    Coverage(Set<Integer> coveredLineNumbers) {
        this.coveredLineNumbers = coveredLineNumbers;
    }

    void setCoveredLineNumbers(Set<Integer> coveredLineNumbers) {
        this.coveredLineNumbers = coveredLineNumbers;
    }

    Set<Integer> getCoveredLineNumbers() {
        return coveredLineNumbers;
    }
}
