package com.example.guessthenumber.ui;

import java.io.BufferedReader;
import java.io.PrintStream;

import com.example.guessthenumber.logic.GameState;
import com.example.guessthenumber.logic.Logic;

public class CommandLineUi implements UserInterface {
    private BufferedReader inputReader;
    private PrintStream outputWriter;
    private Logic logic;

    static final String WIN_MESSAGE = "Good job! You guessed my number.";
    static final String DEFEAT_TEMPLATE = "Sorry, you lose. The number was %d.";

    public CommandLineUi(BufferedReader inputReader, PrintStream outputWriter, Logic logic) {
        this.inputReader = inputReader;
        this.outputWriter = outputWriter;
        this.logic = logic;
    }

    public void run() {}

    void handleEnd(GameState state) {
        if (state == GameState.CORRECT) {
            informUser(WIN_MESSAGE);
        } else {
            int numberToGuess = logic.getNumberToGuess();
            String defeatMessage = String.format(DEFEAT_TEMPLATE, numberToGuess);
            informUser(defeatMessage);
        }
    }

    void informUser(String message) {
        outputWriter.println(message);
    }
}
