package com.example.guessthenumber.ui;

import static org.junit.Assert.assertEquals;

import java.io.OutputStream;
import java.io.PrintStream;

import org.junit.Test;

public class CommandLineUiTest {
    @Test
    public void testInformUser() {
        OutputWriterMock outputWriter = new OutputWriterMock(System.out);
        CommandLineUi clui = new CommandLineUi(null, outputWriter, null);
        String expectedMessage = "Hello, World!";
        clui.informUser(expectedMessage);
        assertEquals(expectedMessage, outputWriter.getMessage());
    }

    private class OutputWriterMock extends PrintStream {
        private String message;

        public OutputWriterMock(OutputStream out) {
            super(out);
        }

        @Override
        public void println(String x) {
            message = x;
        }

        private String getMessage() {
            return message;
        }
    }
}
