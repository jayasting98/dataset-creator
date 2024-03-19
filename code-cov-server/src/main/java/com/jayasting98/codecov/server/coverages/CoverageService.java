package com.jayasting98.codecov.server.coverages;

import java.util.Collection;

import com.jayasting98.codecov.data.coverages.Coverage;

interface CoverageService {
    public Coverage createCoverage(Collection<String> classpathPathnames, String focalClasspath,
        String focalClassName, String testClassName, String testMethodName) throws Exception;
}
