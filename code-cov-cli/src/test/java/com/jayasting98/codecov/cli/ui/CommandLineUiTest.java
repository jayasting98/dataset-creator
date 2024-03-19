package com.jayasting98.codecov.cli.ui;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.io.PrintStream;
import java.util.Arrays;
import java.util.List;
import java.util.function.Function;

import org.junit.jupiter.api.Test;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.jayasting98.codecov.data.coverages.Coverage;
import com.jayasting98.codecov.data.coverages.CreateCoverageRequestData;
import com.jayasting98.codecov.utilities.CoverageAnalyzer;

public class CommandLineUiTest {
    @Test
    private void testRun_noArguments_throwsIllegalArgumentException() {
        UserInterface ui = new CommandLineUi<>(null, null, null, null);
        String[] args = new String[] {};
        assertThrows(IllegalArgumentException.class, () -> ui.run(args),
            "There should be exactly one String argument.");
    }

    @Test
    private void testRun_moreThanOneArgument_throwsIllegalArgumentException() {
        UserInterface ui = new CommandLineUi<>(null, null, null, null);
        String[] args = new String[] {"Hello", "World!"};
        assertThrows(IllegalArgumentException.class, () -> ui.run(args),
            "There should be exactly one String argument.");
    }

    @Test
    private void testRun_typicalCase_runsSuccessfully() {
        Function<String, Integer> deserializer = Integer::parseInt;
        Function<Integer, Double> processor = x -> (double) x / 2;
        Function<Double, String> serializer = String::valueOf;
        PrintStream mockOutputWriter = mock(PrintStream.class);
        UserInterface ui =
            new CommandLineUi<>(deserializer, processor, serializer, mockOutputWriter);
        String[] args = new String[] {"1"};
        ui.run(args);
        verify(mockOutputWriter).println("0.5");
    }

    @Test
    private void testRun_jsonSerializationAndCoverageProcessing_runsSuccessfully() {
        ObjectMapper objectMapper = new ObjectMapper();
        Function<String, CreateCoverageRequestData> deserializer = jsonString -> {
            CreateCoverageRequestData requestData;
            try {
                requestData = objectMapper.readValue(jsonString, CreateCoverageRequestData.class);
            } catch (JsonProcessingException e) {
                throw new IllegalArgumentException(
                    "JSON string must represent valid instance of CreateCoverageRequestData.");
            }
            return requestData;
        };
        Function<CreateCoverageRequestData, Coverage> processor = requestData -> {
            CoverageAnalyzer mockCoverageAnalyzer = mock(CoverageAnalyzer.class);
            List<Integer> mockCoveredLineNumbers = Arrays.asList(1, 2, 3);
            List<Integer> coveredLineNumbers;
            try {
                when(mockCoverageAnalyzer.findCoveredLineNumbers())
                    .thenReturn(mockCoveredLineNumbers);
                coveredLineNumbers = mockCoverageAnalyzer.findCoveredLineNumbers();
            } catch (Exception e) {
                throw new IllegalArgumentException("Covered line numbers could not be found.");
            }
            Coverage coverage = new Coverage(coveredLineNumbers);
            return coverage;
        };
        Function<Coverage, String> serializer = coverage -> {
            String jsonString;
            try {
                jsonString = objectMapper.writeValueAsString(coverage);
            } catch (JsonProcessingException e) {
                throw new IllegalArgumentException("Coverage had the wrong format.");
            }
            return jsonString;
        };
        PrintStream mockOutputWriter = mock(PrintStream.class);
        UserInterface ui =
            new CommandLineUi<>(deserializer, processor, serializer, mockOutputWriter);
        String[] args = new String[] {"{\"Hello\": 0, \"World!\": 1}"};
        ui.run(args);
        verify(mockOutputWriter).println("{\"coveredLineNumbers\": [1, 2, 3]}");
    }
}
