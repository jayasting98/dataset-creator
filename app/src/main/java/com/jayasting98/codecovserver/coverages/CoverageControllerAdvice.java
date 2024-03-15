package com.jayasting98.codecovserver.coverages;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;

@ControllerAdvice
public class CoverageControllerAdvice {
    static final String UNEXPECTED_ERROR_MESSAGE = "An unexpected error has occurred.";

    final Logger logger = LoggerFactory.getLogger(getClass());

    @ResponseBody
    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    String handleException(Exception e) {
        logger.error(UNEXPECTED_ERROR_MESSAGE, e);
        Throwable t = e.getCause();
        while (t != null) {
            logger.debug("Cause of " + e.toString(), t);
            t = t.getCause();
        }
        return UNEXPECTED_ERROR_MESSAGE;
    }
}
