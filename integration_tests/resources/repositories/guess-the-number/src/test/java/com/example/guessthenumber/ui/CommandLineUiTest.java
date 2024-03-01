package com.example.guessthenumber.ui;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.io.PrintStream;

import org.junit.Test;

import com.example.guessthenumber.logic.GameState;
import com.example.guessthenumber.logic.Logic;

public class CommandLineUiTest {
    @Test
    public void testHandleEnd_startState_informsUserOfDefeat() {
        PrintStream mockOutputWriter = mock(PrintStream.class);
        Logic mockLogic = mock(Logic.class);
        when(mockLogic.getNumberToGuess()).thenReturn(42);
        CommandLineUi clui = new CommandLineUi(null, mockOutputWriter, mockLogic);
        clui.handleEnd(GameState.START);
        String expectedMessage = "Sorry, you lose. The number was 42.";
        verify(mockOutputWriter).println(expectedMessage);
    }

    @Test
    public void testHandleEnd_overestimate_informsUserOfDefeat() {
        PrintStream mockOutputWriter = mock(PrintStream.class);
        Logic mockLogic = mock(Logic.class);
        when(mockLogic.getNumberToGuess()).thenReturn(42);
        CommandLineUi clui = new CommandLineUi(null, mockOutputWriter, mockLogic);
        clui.handleEnd(GameState.OVERESTIMATE);
        String expectedMessage = "Sorry, you lose. The number was 42.";
        verify(mockOutputWriter).println(expectedMessage);
    }

    @Test
    public void testHandleEnd_underestimate_informsUserOfDefeat() {
        PrintStream mockOutputWriter = mock(PrintStream.class);
        Logic mockLogic = mock(Logic.class);
        when(mockLogic.getNumberToGuess()).thenReturn(42);
        CommandLineUi clui = new CommandLineUi(null, mockOutputWriter, mockLogic);
        clui.handleEnd(GameState.UNDERESTIMATE);
        String expectedMessage = "Sorry, you lose. The number was 42.";
        verify(mockOutputWriter).println(expectedMessage);
    }

    @Test
    public void testHandleEnd_correctGuess_informsUserOfDefeat() {
        PrintStream mockOutputWriter = mock(PrintStream.class);
        CommandLineUi clui = new CommandLineUi(null, mockOutputWriter, null);
        clui.handleEnd(GameState.CORRECT);
        String expectedMessage = "Good job! You guessed my number.";
        verify(mockOutputWriter).println(expectedMessage);
    }

    @Test
    public void testInformUser() {
        PrintStream mockOutputWriter = mock(PrintStream.class);
        CommandLineUi clui = new CommandLineUi(null, mockOutputWriter, null);
        String expectedMessage = "Hello, World!";
        clui.informUser(expectedMessage);
        verify(mockOutputWriter).println(expectedMessage);
    }
}
