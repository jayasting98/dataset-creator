package com.example.guessthenumber.ui;

import static org.junit.Assert.assertEquals;

import java.io.OutputStream;
import java.io.PrintStream;

import org.junit.Test;

import com.example.guessthenumber.logic.GameState;
import com.example.guessthenumber.logic.Logic;

public class CommandLineUiTest {
    @Test
    public void testHandleEnd_startState_informsUserOfDefeat() {
        OutputWriterMock outputWriter = new OutputWriterMock(System.out);
        Logic logic = new LogicStub(42);
        CommandLineUi clui = new CommandLineUi(null, outputWriter, logic);
        clui.handleEnd(GameState.START);
        String expectedMessage = "Sorry, you lose. The number was 42.";
        assertEquals(expectedMessage, outputWriter.getMessage());
    }

    @Test
    public void testHandleEnd_overestimate_informsUserOfDefeat() {
        OutputWriterMock outputWriter = new OutputWriterMock(System.out);
        Logic logic = new LogicStub(42);
        CommandLineUi clui = new CommandLineUi(null, outputWriter, logic);
        clui.handleEnd(GameState.OVERESTIMATE);
        String expectedMessage = "Sorry, you lose. The number was 42.";
        assertEquals(expectedMessage, outputWriter.getMessage());
    }

    @Test
    public void testHandleEnd_underestimate_informsUserOfDefeat() {
        OutputWriterMock outputWriter = new OutputWriterMock(System.out);
        Logic logic = new LogicStub(42);
        CommandLineUi clui = new CommandLineUi(null, outputWriter, logic);
        clui.handleEnd(GameState.UNDERESTIMATE);
        String expectedMessage = "Sorry, you lose. The number was 42.";
        assertEquals(expectedMessage, outputWriter.getMessage());
    }

    @Test
    public void testHandleEnd_correctGuess_informsUserOfDefeat() {
        OutputWriterMock outputWriter = new OutputWriterMock(System.out);
        Logic logic = new LogicStub(42);
        CommandLineUi clui = new CommandLineUi(null, outputWriter, logic);
        clui.handleEnd(GameState.CORRECT);
        String expectedMessage = "Good job! You guessed my number.";
        assertEquals(expectedMessage, outputWriter.getMessage());
    }

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

    private class LogicStub implements Logic {
        private int numberToGuess;

        private LogicStub(int numberToGuess) {
            this.numberToGuess = numberToGuess;
        }

        public int getNumberToGuess() {
            return numberToGuess;
        }
    }
}
