package com.example.guessthenumber.ui;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.inOrder;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.PrintStream;

import org.junit.Test;
import org.mockito.InOrder;

import com.example.guessthenumber.logic.GameState;
import com.example.guessthenumber.logic.Logic;

public class CommandLineUiTest {
    @Test
    public void testRun_ioExceptionThrown_exitsGracefully() throws IOException {
        BufferedReader mockBufferedReader = mock(BufferedReader.class);
        when(mockBufferedReader.readLine()).thenThrow(IOException.class);
        PrintStream mockOutputWriter = mock(PrintStream.class);
        InOrder inOrder = inOrder(mockOutputWriter);
        Logic mockLogic = mock(Logic.class);
        when(mockLogic.isAbleToGuess()).thenReturn(true);
        CommandLineUi clui = new CommandLineUi(mockBufferedReader, mockOutputWriter, mockLogic);
        clui.run();
        inOrder.verify(mockOutputWriter).println("Take a guess.");
        inOrder.verify(mockOutputWriter).println("Unexpected error faced. Exiting...");
    }

    @Test
    public void testRun_typicalWin_parsesProcessesAndInformsUserCorrectly() throws IOException {
        BufferedReader mockBufferedReader = mock(BufferedReader.class);
        when(mockBufferedReader.readLine()).thenReturn("42");
        PrintStream mockOutputWriter = mock(PrintStream.class);
        InOrder inOrder = inOrder(mockOutputWriter);
        Logic mockLogic = mock(Logic.class);
        when(mockLogic.isAbleToGuess()).thenReturn(true).thenReturn(false);
        when(mockLogic.getState()).thenReturn(GameState.CORRECT);
        CommandLineUi clui = new CommandLineUi(mockBufferedReader, mockOutputWriter, mockLogic);
        clui.run();
        inOrder.verify(mockOutputWriter).println("Take a guess.");
        inOrder.verify(mockOutputWriter).println("Good job! You guessed my number.");
    }

    @Test
    public void testParseGuess() throws IOException {
        BufferedReader mockBufferedReader = mock(BufferedReader.class);
        when(mockBufferedReader.readLine()).thenReturn("not an integer").thenReturn("42");
        PrintStream mockOutputWriter = mock(PrintStream.class);
        InOrder inOrder = inOrder(mockOutputWriter);
        CommandLineUi clui = new CommandLineUi(mockBufferedReader, mockOutputWriter, null);
        int expectedGuessedNumber = 42;
        int actualGuessedNumber = clui.parseGuess();
        assertEquals(expectedGuessedNumber, actualGuessedNumber);
        inOrder.verify(mockOutputWriter).println("Take a guess.");
        inOrder.verify(mockOutputWriter).println("I did not understand that.");
        inOrder.verify(mockOutputWriter).println("Take a guess.");
    }

    @Test
    public void testHandleState_startState_doesNotInformUser() {
        PrintStream mockOutputWriter = mock(PrintStream.class);
        CommandLineUi clui = new CommandLineUi(null, mockOutputWriter, null);
        clui.handleState(GameState.START);
        verifyNoInteractions(mockOutputWriter);
    }

    @Test
    public void testHandleState_overestimate_informsUser() {
        PrintStream mockOutputWriter = mock(PrintStream.class);
        CommandLineUi clui = new CommandLineUi(null, mockOutputWriter, null);
        clui.handleState(GameState.OVERESTIMATE);
        String expectedMessage = "Your guess was too high. :(";
        verify(mockOutputWriter).println(expectedMessage);
    }

    @Test
    public void testHandleState_underestimate_informsUser() {
        PrintStream mockOutputWriter = mock(PrintStream.class);
        CommandLineUi clui = new CommandLineUi(null, mockOutputWriter, null);
        clui.handleState(GameState.UNDERESTIMATE);
        String expectedMessage = "Your guess was too low. :(";
        verify(mockOutputWriter).println(expectedMessage);
    }

    @Test
    public void testHandleState_correctGuess_doesNotInformUser() {
        PrintStream mockOutputWriter = mock(PrintStream.class);
        CommandLineUi clui = new CommandLineUi(null, mockOutputWriter, null);
        clui.handleState(GameState.CORRECT);
        verifyNoInteractions(mockOutputWriter);
    }

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
    public void testHandleEnd_correctGuess_informsUserOfWin() {
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
