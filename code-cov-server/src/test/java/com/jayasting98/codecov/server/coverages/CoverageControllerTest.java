package com.jayasting98.codecov.server.coverages;

import java.io.File;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

import com.fasterxml.jackson.databind.ObjectMapper;

@SpringBootTest
@AutoConfigureMockMvc
public class CoverageControllerTest {
    @Autowired
    private MockMvc mockMvc;

    @Test
    public void testCreateCoverage_typicalCase_createsCorrectly() throws Exception {
        String repositoryDirPathname = Paths.get("").toAbsolutePath().getParent().toString()
            + File.separator + "integration_tests/resources/repositories/maven/guess-the-number/";
        String junitJarPathname = Paths.get(System.getProperty("user.home"),
            ".m2/repository/junit/junit/4.11/junit-4.11.jar").toString();
        String focalClasspath = repositoryDirPathname + "target/classes/";
        String testClasspath = repositoryDirPathname + "target/test-classes/";
        List<String> classpathPathnames =
            Arrays.asList(junitJarPathname, focalClasspath, testClasspath);
        String focalClassName = "com.example.guessthenumber.ui.CommandLineUi";
        String testClassName = "com.example.guessthenumber.ui.CommandLineUiTest";
        String testMethodName = "testParseGuess";
        CreateCoverageRequestData requestData = new CreateCoverageRequestData(classpathPathnames,
            focalClasspath, focalClassName, testClassName, testMethodName);
        ObjectMapper mapper = new ObjectMapper();
        String requestDataJsonString = mapper.writeValueAsString(requestData);
        MockHttpServletRequestBuilder requestBuilder = MockMvcRequestBuilders.post("/coverages")
            .contentType(MediaType.APPLICATION_JSON)
            .content(requestDataJsonString);
        List<Integer> expectedCoveredLineNumbers = new ArrayList<>();
        expectedCoveredLineNumbers.add(24);
        expectedCoveredLineNumbers.add(25);
        expectedCoveredLineNumbers.add(26);
        expectedCoveredLineNumbers.add(27);
        expectedCoveredLineNumbers.add(28);
        expectedCoveredLineNumbers.add(67);
        expectedCoveredLineNumbers.add(68);
        expectedCoveredLineNumbers.add(69);
        expectedCoveredLineNumbers.add(70);
        expectedCoveredLineNumbers.add(71);
        expectedCoveredLineNumbers.add(72);
        expectedCoveredLineNumbers.add(73);
        expectedCoveredLineNumbers.add(88);
        expectedCoveredLineNumbers.add(89);
        Coverage expectedCoverage = new Coverage(expectedCoveredLineNumbers);
        String expectedResponseDataJsonString = mapper.writeValueAsString(expectedCoverage);
        mockMvc.perform(requestBuilder)
            .andExpect(MockMvcResultMatchers.status().isCreated())
            .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
            .andExpect(MockMvcResultMatchers.content().json(expectedResponseDataJsonString));
    }

    @Test
    public void testCreateCoverage_stackOverflowError_doesNotCrash() throws Exception {
        String repositoryDirPathname = Paths.get("").toAbsolutePath().getParent().toString();
        String testClasspath = new StringBuilder().append(repositoryDirPathname)
            .append(File.separator).append("app").append(File.separator).append("build")
            .append(File.separator).append("classes").append(File.separator).append("java")
            .append(File.separator).append("test").toString();
        String focalClasspath = testClasspath;
        List<String> classpathPathnames = Arrays.asList(focalClasspath, testClasspath);
        String testClassName = "com.jayasting98.codecovserver.coverages.CoverageControllerTest";
        String testMethodName = "recurseAsMuchAsPossible";
        String focalClassName = testClassName;
        CreateCoverageRequestData requestData = new CreateCoverageRequestData(classpathPathnames,
            focalClasspath, focalClassName, testClassName, testMethodName);
        ObjectMapper mapper = new ObjectMapper();
        String requestDataJsonString = mapper.writeValueAsString(requestData);
        MockHttpServletRequestBuilder requestBuilder = MockMvcRequestBuilders.post("/coverages")
            .contentType(MediaType.APPLICATION_JSON)
            .content(requestDataJsonString);
        mockMvc.perform(requestBuilder)
            .andExpect(MockMvcResultMatchers.status().isInternalServerError())
            .andExpect(MockMvcResultMatchers
                .content().string(CoverageControllerAdvice.UNEXPECTED_ERROR_MESSAGE));
    }

    public void recurseAsMuchAsPossible() {
        recurseAsMuchAsPossible();
    }
}
