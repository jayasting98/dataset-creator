package com.jayasting98.codecov.server.coverages;

import java.util.Collection;
import java.util.List;

import org.springframework.stereotype.Service;

import com.jayasting98.codecov.utilities.CoverageAnalyzer;

@Service
class JacocoCoverageService implements CoverageService {
    @Override
    public Coverage createCoverage(Collection<String> classpathPathnames, String focalClasspath,
        String focalClassName, String testClassName, String testMethodName) throws Exception {
        CoverageAnalyzer analyzer = new CoverageAnalyzer(classpathPathnames, focalClasspath,
            focalClassName, testClassName, testMethodName);
        List<Integer> coveredLineNumbers = analyzer.findCoveredLineNumbers();
        Coverage coverage = new Coverage(coveredLineNumbers);
        return coverage;
    }
}
