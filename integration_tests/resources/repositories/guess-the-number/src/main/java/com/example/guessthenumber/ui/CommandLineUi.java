package com.example.guessthenumber.ui;

import java.io.BufferedReader;
import java.io.PrintStream;

import com.example.guessthenumber.logic.Logic;

public class CommandLineUi implements UserInterface {
    private BufferedReader inputReader;
    private PrintStream outputWriter;
    private Logic logic;

    public CommandLineUi(BufferedReader inputReader, PrintStream outputWriter, Logic logic) {
        this.inputReader = inputReader;
        this.outputWriter = outputWriter;
        this.logic = logic;
    }

    public void run() {}

    void informUser(String message) {
        outputWriter.println(message);
    }
}
