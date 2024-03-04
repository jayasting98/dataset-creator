package com.jayasting98.codecovserver.coverages;

import java.util.Collection;

interface CoverageService {
    public Coverage createCoverage(Collection<String> jarPathnames, String focalClasspath,
        String testClasspath, String focalClassName, String testClassName, String testMethodName)
        throws Exception;
}
