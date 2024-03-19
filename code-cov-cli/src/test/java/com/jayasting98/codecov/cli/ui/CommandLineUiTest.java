package com.jayasting98.codecov.cli.ui;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;

import java.io.PrintStream;
import java.util.function.Function;

import org.junit.jupiter.api.Test;

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
}
