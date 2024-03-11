package com.example.guessthenumber.logic;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import org.junit.Test;

public class StandardLogicTest {
    @Test
    public void testIsAbleToGuess_correctGuess_returnsFalse() {
        StandardLogic logic = new StandardLogic(42);
        logic.process(42);
        assertEquals(false, logic.isAbleToGuess());
    }

    @Test
    public void testIsAbleToGuess_notCorrectYetAndHasGuessesLeft_returnsTrue() {
        StandardLogic logic = new StandardLogic(42);
        logic.process(41);
        assertEquals(true, logic.isAbleToGuess());
    }

    @Test
    public void testIsAbleToGuess_notCorrectYetAndHasNoGuessesLeft_returnsFalse() {
        StandardLogic logic = new StandardLogic(42);
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
        StandardLogic logic = new StandardLogic(42);
        assertEquals(0, logic.getNumGuessesTaken());
        logic.process(43);
        assertEquals(1, logic.getNumGuessesTaken());
        assertEquals(GameState.OVERESTIMATE, logic.getState());
    }

    @Test
    public void testProcess_underestimate_incrementsNumGuessesTakenAndTransitionsToUnderestimateState() {
        StandardLogic logic = new StandardLogic(42);
        assertEquals(0, logic.getNumGuessesTaken());
        logic.process(41);
        assertEquals(1, logic.getNumGuessesTaken());
        assertEquals(GameState.UNDERESTIMATE, logic.getState());
    }

    @Test
    public void testProcess_correctGuess_incrementsNumGuessesTakenAndTransitionsToCorrectState() {
        StandardLogic logic = new StandardLogic(42);
        assertEquals(0, logic.getNumGuessesTaken());
        logic.process(42);
        assertEquals(1, logic.getNumGuessesTaken());
        assertEquals(GameState.CORRECT, logic.getState());
    }
}
