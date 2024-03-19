package com.jayasting98.codecovserver.utilities;

import java.security.Permission;

public class BlockedExitSecurityManager extends SecurityManager {
    private SecurityManager securityManager;

    public BlockedExitSecurityManager(SecurityManager securityManager) {
        this.securityManager = securityManager;
    }

    @Override
    public void checkExit(int status) {
        throw new SecurityException();
    }

    @Override
    public void checkPermission(Permission perm) {
        if (securityManager == null) {
            return;
        }
        securityManager.checkPermission(perm);
    }
}
