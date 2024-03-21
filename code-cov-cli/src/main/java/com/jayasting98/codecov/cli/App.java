package com.jayasting98.codecov.cli;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.util.List;
import java.util.function.Function;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.jayasting98.codecov.cli.ui.CommandLineUi;
import com.jayasting98.codecov.cli.ui.UserInterface;
import com.jayasting98.codecov.data.coverages.Coverage;
import com.jayasting98.codecov.data.coverages.CreateCoverageRequestData;
import com.jayasting98.codecov.utilities.CoverageAnalyzer;

public class App {
    public static void main(String[] args) {
        BufferedReader inputReader = new BufferedReader(new InputStreamReader(System.in));
        ObjectMapper objectMapper = new ObjectMapper();
        Function<String, CreateCoverageRequestData> deserializer = jsonString -> {
            CreateCoverageRequestData requestData;
            try {
                requestData = objectMapper.readValue(jsonString, CreateCoverageRequestData.class);
            } catch (JsonProcessingException e) {
                throw new IllegalArgumentException(
                    "JSON string must represent valid instance of CreateCoverageRequestData.", e);
            }
            return requestData;
        };
        Function<CreateCoverageRequestData, Coverage> processor = requestData -> {
            CoverageAnalyzer coverageAnalyzer = new CoverageAnalyzer(
                requestData.getClasspathPathnames(), requestData.getFocalClasspath(),
                requestData.getFocalClassName(), requestData.getTestClassName(),
                requestData.getTestMethodName());
            List<Integer> coveredLineNumbers;
            try {
                coveredLineNumbers = coverageAnalyzer.findCoveredLineNumbers();
            } catch (Exception e) {
                throw new IllegalArgumentException("Covered line numbers could not be found.", e);
            }
            Coverage coverage = new Coverage(coveredLineNumbers);
            return coverage;
        };
        Function<Coverage, String> serializer = coverage -> {
            String jsonString;
            try {
                jsonString = objectMapper.writeValueAsString(coverage);
            } catch (JsonProcessingException e) {
                throw new IllegalArgumentException("Coverage had the wrong format.", e);
            }
            return jsonString;
        };
        PrintStream outputWriter = System.out;
        UserInterface ui =
            new CommandLineUi<>(inputReader, deserializer, processor, serializer, outputWriter);
        try {
            ui.run();
        } catch (IOException e) {
            throw new IllegalArgumentException("Input could not be read.", e);
        }
    }
}
