package com.jayasting98.codecov.server.coverages;

import java.util.List;

class CreateCoverageRequestData {
    private List<String> classpathPathnames;
    private String focalClasspath;
    private String focalClassName;
    private String testClassName;
    private String testMethodName;

    CreateCoverageRequestData(List<String> classpathPathnames, String focalClasspath,
        String focalClassName, String testClassName, String testMethodName) {
        this.classpathPathnames = classpathPathnames;
        this.focalClasspath = focalClasspath;
        this.focalClassName = focalClassName;
        this.testClassName = testClassName;
        this.testMethodName = testMethodName;
    }

    public List<String> getClasspathPathnames() {
        return classpathPathnames;
    }

    public String getFocalClasspath() {
        return focalClasspath;
    }

    public String getFocalClassName() {
        return focalClassName;
    }

    public String getTestClassName() {
        return testClassName;
    }

    public String getTestMethodName() {
        return testMethodName;
    }
}
