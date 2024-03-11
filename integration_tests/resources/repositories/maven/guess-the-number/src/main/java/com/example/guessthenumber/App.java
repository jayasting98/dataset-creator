package com.example.guessthenumber;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.util.Random;

import com.example.guessthenumber.logic.Logic;
import com.example.guessthenumber.logic.StandardLogic;
import com.example.guessthenumber.ui.CommandLineUi;
import com.example.guessthenumber.ui.UserInterface;

public class App {
    public static void main(String[] args) {
        UserInterface ui = constructUserInterface();
        ui.run();
    }

    private static UserInterface constructUserInterface() {
        Random random = new Random();
        int numberToGuess = random.nextInt(StandardLogic.UPPER_BOUND) + 1;
        Logic logic = new StandardLogic(numberToGuess);
        BufferedReader inputReader = new BufferedReader(new InputStreamReader(System.in));
        PrintStream outputWriter = System.out;
        UserInterface ui = new CommandLineUi(inputReader, outputWriter, logic);
        return ui;
    }
}
