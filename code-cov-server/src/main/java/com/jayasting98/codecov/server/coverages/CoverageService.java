package com.jayasting98.codecov.server.coverages;

import java.util.Collection;

interface CoverageService {
    public Coverage createCoverage(Collection<String> classpathPathnames, String focalClasspath,
        String focalClassName, String testClassName, String testMethodName) throws Exception;
}
