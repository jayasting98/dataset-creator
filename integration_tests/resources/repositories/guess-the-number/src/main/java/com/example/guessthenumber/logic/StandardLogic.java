package com.example.guessthenumber.logic;

import java.util.Random;

public class StandardLogic implements Logic {
    static final int LOWER_BOUND = 1;
    static final int UPPER_BOUND = 100;
    static final int MAX_NUM_GUESSES = 6;

    private GameState state;
    private int numGuessesTaken;
    private int numberToGuess;

    public StandardLogic(Random random) {
        state = GameState.START;
        numGuessesTaken = 0;
        numberToGuess = random.nextInt(UPPER_BOUND) + 1;
    }

    @Override
    public boolean isAbleToGuess() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'isAbleToGuess'");
    }

    @Override
    public void process(int guessedNumber) {
        numGuessesTaken++;
        if (guessedNumber > numberToGuess) {
            state = GameState.OVERESTIMATE;
        } else if (guessedNumber < numberToGuess) {
            state = GameState.UNDERESTIMATE;
        } else {
            state = GameState.CORRECT;
        }
    }

    @Override
    public GameState getState() {
        return state;
    }

    @Override
    public int getNumberToGuess() {
        return numberToGuess;
    }

    int getNumGuessesTaken() {
        return numGuessesTaken;
    }
}
