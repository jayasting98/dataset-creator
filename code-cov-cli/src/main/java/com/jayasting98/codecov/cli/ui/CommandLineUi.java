package com.jayasting98.codecov.cli.ui;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.PrintStream;
import java.util.function.Function;

public class CommandLineUi<T, U> implements UserInterface {
    private BufferedReader inputReader;
    private Function<? super String, ? extends T> deserializer;
    private Function<? super T, ? extends U> processor;
    private Function<? super U, ? extends String> serializer;
    private PrintStream outputWriter;

    public CommandLineUi(BufferedReader inputReader,
        Function<? super String, ? extends T> deserializer,
        Function<? super T, ? extends U> processor,
        Function<? super U, ? extends String> serializer, PrintStream outputWriter) {
        this.inputReader = inputReader;
        this.deserializer = deserializer;
        this.processor = processor;
        this.serializer = serializer;
        this.outputWriter = outputWriter;
    }

    @Override
    public void run() throws IOException {
        String encodedInput = inputReader.readLine();
        T inputData = deserializer.apply(encodedInput);
        U outputData = processor.apply(inputData);
        String encodedOutput = serializer.apply(outputData);
        outputWriter.println(encodedOutput);
    }
}
