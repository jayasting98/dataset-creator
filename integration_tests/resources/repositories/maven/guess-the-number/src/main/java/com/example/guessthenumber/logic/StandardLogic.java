package com.example.guessthenumber.logic;

public class StandardLogic implements Logic {
    public static final int UPPER_BOUND = 100;

    static final int MAX_NUM_GUESSES = 6;

    private GameState state;
    private int numGuessesTaken;
    private int numberToGuess;

    public StandardLogic(int numberToGuess) {
        state = GameState.START;
        numGuessesTaken = 0;
        this.numberToGuess = numberToGuess;
    }

    @Override
    public boolean isAbleToGuess() {
        if (state == GameState.CORRECT) {
            return false;
        }
        boolean hasGuessesLeft = numGuessesTaken < MAX_NUM_GUESSES;
        return hasGuessesLeft;
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
