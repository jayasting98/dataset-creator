package com.jayasting98.codecovserver.utilities;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.lang.reflect.Constructor;
import java.lang.reflect.Method;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.jacoco.core.analysis.Analyzer;
import org.jacoco.core.analysis.CoverageBuilder;
import org.jacoco.core.analysis.IClassCoverage;
import org.jacoco.core.analysis.ICounter;
import org.jacoco.core.analysis.ILine;
import org.jacoco.core.data.ExecutionDataStore;
import org.jacoco.core.data.SessionInfoStore;
import org.jacoco.core.instr.Instrumenter;
import org.jacoco.core.runtime.IRuntime;
import org.jacoco.core.runtime.LoggerRuntime;
import org.jacoco.core.runtime.RuntimeData;

public class CoverageAnalyzer {
    private List<String> classpathPathnames;
    private String focalClasspath;
    private String focalClassName;
    private String testClassName;
    private String testMethodName;
    private SecurityManager originalSm;
    private SecurityManager blockedExitSm;

    public CoverageAnalyzer(Collection<String> classpathPathnames, String focalClasspath,
        String focalClassName, String testClassName, String testMethodName) {
        this.classpathPathnames = new ArrayList<>(classpathPathnames);
        this.focalClasspath = focalClasspath;
        this.focalClassName = focalClassName;
        this.testClassName = testClassName;
        this.testMethodName = testMethodName;
        originalSm = System.getSecurityManager();
        blockedExitSm = new BlockedExitSecurityManager(originalSm);
    }

    public List<Integer> findCoveredLineNumbers() throws Exception {
        IRuntime runtime = new LoggerRuntime();
        Instrumenter instrumenter = new Instrumenter(runtime);
        byte[] instrumentedDefinition;
        try (InputStream focalClassDefinition =
            findClassDefinition(focalClasspath, focalClassName)) {
            instrumentedDefinition = instrumenter.instrument(focalClassDefinition, focalClassName);
        }
        RuntimeData runtimeData = new RuntimeData();
        runtime.startup(runtimeData);
        URL[] urls = generateUrls(classpathPathnames);
        Class<?> testClass;
        try (MemoryClassLoader classLoader = new MemoryClassLoader(urls)) {
            classLoader.put(focalClassName, instrumentedDefinition);
            testClass = classLoader.loadClass(testClassName);
            Constructor<?> testConstructor = testClass.getConstructor();
            System.setSecurityManager(blockedExitSm);
            Object testObject = testConstructor.newInstance();
            Method testMethod = testClass.getMethod(testMethodName);
            testMethod.invoke(testObject);
            System.setSecurityManager(originalSm);
        }
        ExecutionDataStore executionDataStore = new ExecutionDataStore();
        SessionInfoStore sessionInfoStore = new SessionInfoStore();
        runtimeData.collect(executionDataStore, sessionInfoStore, false);
        runtime.shutdown();
        CoverageBuilder coverageBuilder = new CoverageBuilder();
        Analyzer analyzer = new Analyzer(executionDataStore, coverageBuilder);
        try (InputStream focalClassDefinition =
            findClassDefinition(focalClasspath, focalClassName)) {
            analyzer.analyzeClass(focalClassDefinition, focalClassName);
        }
        List<Integer> coveredLineNumbers = new ArrayList<>();
        for (IClassCoverage classCoverage : coverageBuilder.getClasses()) {
            for (int i = classCoverage.getFirstLine(); i <= classCoverage.getLastLine(); i++) {
                ILine line = classCoverage.getLine(i);
                if (line.getStatus() != ICounter.FULLY_COVERED) {
                    continue;
                }
                coveredLineNumbers.add(i);
            }
        }
        return coveredLineNumbers;
    }

    InputStream findClassDefinition(String classpath, String className)
        throws FileNotFoundException {
        String filePathname = Paths
            .get(classpath, className.replace(".", File.separator)).toString() + ".class";
        File file = new File(filePathname);
        InputStream classDefinition = new FileInputStream(file);
        return classDefinition;
    }

    URL[] generateUrls(Collection<String> classpathPathnames) throws MalformedURLException {
        Set<String> urlStrings = new HashSet<>(classpathPathnames);
        Set<URL> uniqueUrls = new HashSet<>();
        for (String urlString : urlStrings) {
            URL url = new File(urlString).toURI().toURL();
            uniqueUrls.add(url);
        }
        URL[] urls = uniqueUrls.toArray(new URL[0]);
        return urls;
    }

    static class MemoryClassLoader extends URLClassLoader {
        private Map<String, byte[]> nameDefinitions;

        MemoryClassLoader(URL[] urls) {
            super(urls);
            nameDefinitions = new HashMap<>();
        }

        void put(String className, byte[] definition) {
            nameDefinitions.put(className, definition);
        }

        @Override
        public Class<?> loadClass(String name) throws ClassNotFoundException {
            byte[] definition = nameDefinitions.get(name);
            if (definition == null) {
                return super.loadClass(name);
            }
            Class<?> clazz = defineClass(name, definition, 0, definition.length);
            return clazz;
        }
    }
}
