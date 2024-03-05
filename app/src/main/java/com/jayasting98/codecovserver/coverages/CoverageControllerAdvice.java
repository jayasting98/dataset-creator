package com.jayasting98.codecovserver.coverages;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;

@ControllerAdvice
public class CoverageControllerAdvice {
    static final String UNEXPECTED_ERROR_MESSAGE = "An unexpected error has occurred.";

    @ResponseBody
    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    String handleException(Exception e) {
        return UNEXPECTED_ERROR_MESSAGE;
    }
}
