package com.example.guessthenumber.logic;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.util.Random;

import org.junit.Test;

public class StandardLogicTest {
    @Test
    public void testIsAbleToGuess_correctGuess_returnsFalse() {
        Random random = mock(Random.class);
        when(random.nextInt(100)).thenReturn(41);
        StandardLogic logic = new StandardLogic(random);
        logic.process(42);
        assertEquals(false, logic.isAbleToGuess());
    }

    @Test
    public void testIsAbleToGuess_notCorrectYetAndHasGuessesLeft_returnsTrue() {
        Random random = mock(Random.class);
        when(random.nextInt(100)).thenReturn(41);
        StandardLogic logic = new StandardLogic(random);
        logic.process(41);
        assertEquals(true, logic.isAbleToGuess());
    }

    @Test
    public void testIsAbleToGuess_notCorrectYetAndHasNoGuessesLeft_returnsFalse() {
        Random random = mock(Random.class);
        when(random.nextInt(100)).thenReturn(41);
        StandardLogic logic = new StandardLogic(random);
        logic.process(41);
        logic.process(41);
        logic.process(41);
        logic.process(41);
        logic.process(41);
        assertEquals(true, logic.isAbleToGuess());
        logic.process(41);
        assertEquals(false, logic.isAbleToGuess());
    }

    @Test
    public void testProcess_overestimate_incrementsNumGuessesTakenAndTransitionsToOverestimateState() {
        Random random = mock(Random.class);
        when(random.nextInt(100)).thenReturn(41);
        StandardLogic logic = new StandardLogic(random);
        assertEquals(0, logic.getNumGuessesTaken());
        logic.process(43);
        assertEquals(1, logic.getNumGuessesTaken());
        assertEquals(GameState.OVERESTIMATE, logic.getState());
    }

    @Test
    public void testProcess_underestimate_incrementsNumGuessesTakenAndTransitionsToUnderestimateState() {
        Random random = mock(Random.class);
        when(random.nextInt(100)).thenReturn(41);
        StandardLogic logic = new StandardLogic(random);
        assertEquals(0, logic.getNumGuessesTaken());
        logic.process(41);
        assertEquals(1, logic.getNumGuessesTaken());
        assertEquals(GameState.UNDERESTIMATE, logic.getState());
    }

    @Test
    public void testProcess_correctGuess_incrementsNumGuessesTakenAndTransitionsToCorrectState() {
        Random random = mock(Random.class);
        when(random.nextInt(100)).thenReturn(41);
        StandardLogic logic = new StandardLogic(random);
        assertEquals(0, logic.getNumGuessesTaken());
        logic.process(42);
        assertEquals(1, logic.getNumGuessesTaken());
        assertEquals(GameState.CORRECT, logic.getState());
    }
}