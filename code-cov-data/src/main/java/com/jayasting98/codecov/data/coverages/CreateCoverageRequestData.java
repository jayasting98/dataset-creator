package com.jayasting98.codecov.data.coverages;

import java.util.List;

public class CreateCoverageRequestData {
    private List<String> classpathPathnames;
    private String focalClasspath;
    private String focalClassName;
    private String testClassName;
    private String testMethodName;

    public CreateCoverageRequestData(List<String> classpathPathnames, String focalClasspath,
        String focalClassName, String testClassName, String testMethodName) {
        this.classpathPathnames = classpathPathnames;
        this.focalClasspath = focalClasspath;
        this.focalClassName = focalClassName;
        this.testClassName = testClassName;
        this.testMethodName = testMethodName;
    }

    /**
     * Constructs CreateCoverageRequestData for Jackson.
     */
    private CreateCoverageRequestData() {}

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
