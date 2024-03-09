package com.example.guessthenumber.logic;

public interface Logic {
    public boolean isAbleToGuess();
    public void process(int guessedNumber);
    public GameState getState();
    public int getNumberToGuess();
}
