package com.jayasting98.codecovserver.coverages;

import java.util.List;

class CreateCoverageRequestData {
    private List<String> jarPathnames;
    private String focalClasspath;
    private String testClasspath;
    private String focalClassName;
    private String testClassName;
    private String testMethodName;

    CreateCoverageRequestData(List<String> jarPathnames, String focalClasspath,
        String testClasspath, String focalClassName, String testClassName, String testMethodName) {
        this.jarPathnames = jarPathnames;
        this.focalClasspath = focalClasspath;
        this.testClasspath = testClasspath;
        this.focalClassName = focalClassName;
        this.testClassName = testClassName;
        this.testMethodName = testMethodName;
    }

    public List<String> getJarPathnames() {
        return jarPathnames;
    }

    public String getFocalClasspath() {
        return focalClasspath;
    }

    public String getTestClasspath() {
        return testClasspath;
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
