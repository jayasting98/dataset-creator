package com.jayasting98.codecovserver.coverages;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
class CoverageController {
    @Autowired
    private CoverageService coverageService;

    private final Logger logger = LoggerFactory.getLogger(getClass());

    @PostMapping("/coverages")
    @ResponseStatus(HttpStatus.CREATED)
    Coverage createCoverage(@RequestBody CreateCoverageRequestData requestData) throws Exception {
        logger.debug(String.format("/coverages POST (%s, %s, %s)",
            requestData.getFocalClassName(), requestData.getTestClassName(),
            requestData.getTestMethodName()));
        Coverage coverage = coverageService.createCoverage(requestData.getClasspathPathnames(),
            requestData.getFocalClasspath(), requestData.getFocalClassName(),
            requestData.getTestClassName(), requestData.getTestMethodName());
        return coverage;
    }
}
