package com.jayasting98.codecov.cli.ui;

import java.io.PrintStream;
import java.util.function.Function;

public class CommandLineUi<T, U> implements UserInterface {
    private Function<? super String, ? extends T> deserializer;
    private Function<? super T, ? extends U> processor;
    private Function<? super U, ? extends String> serializer;
    private PrintStream outputWriter;

    public CommandLineUi(Function<? super String, ? extends T> deserializer,
        Function<? super T, ? extends U> processor,
        Function<? super U, ? extends String> serializer, PrintStream outputWriter) {
        this.deserializer = deserializer;
        this.processor = processor;
        this.serializer = serializer;
        this.outputWriter = outputWriter;
    }

    @Override
    public void run(String[] args) {
        if (args.length != 1) {
            throw new IllegalArgumentException("There should be exactly one String argument.");
        }
        String encodedInput = args[0];
        T inputData = deserializer.apply(encodedInput);
        U outputData = processor.apply(inputData);
        String encodedOutput = serializer.apply(outputData);
        outputWriter.println(encodedOutput);
    }
}
