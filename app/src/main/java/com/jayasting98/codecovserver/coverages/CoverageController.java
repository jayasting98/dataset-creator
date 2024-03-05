package com.jayasting98.codecovserver.coverages;

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

    @PostMapping("/coverages")
    @ResponseStatus(HttpStatus.CREATED)
    Coverage createCoverage(@RequestBody CreateCoverageRequestData requestData) throws Exception {
        Coverage coverage = coverageService.createCoverage(requestData.getJarPathnames(),
            requestData.getFocalClasspath(), requestData.getTestClasspath(),
            requestData.getFocalClassName(), requestData.getTestClassName(),
            requestData.getTestMethodName());
        return coverage;
    }
}
