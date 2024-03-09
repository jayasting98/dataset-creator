package com.jayasting98.codecovserver.coverages;

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
        List<String> jarPathnames = Arrays.asList(junitJarPathname);
        String focalClasspath = repositoryDirPathname + "target/classes/";
        String testClasspath = repositoryDirPathname + "target/test-classes/";
        String focalClassName = "com.example.guessthenumber.ui.CommandLineUi";
        String testClassName = "com.example.guessthenumber.ui.CommandLineUiTest";
        String testMethodName = "testParseGuess";
        CreateCoverageRequestData requestData = new CreateCoverageRequestData(jarPathnames,
            focalClasspath, testClasspath, focalClassName, testClassName, testMethodName);
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
}
