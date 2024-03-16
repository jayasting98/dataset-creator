package com.jayasting98.codecovserver.utilities;

import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

public class BlockedExitSecurityManagerTest {
    @Test
    public void testCheckExit_blockedExitSecurityManagerHasBeenSet_throwsSecurityException() {
        SecurityManager originalSm = System.getSecurityManager();
        BlockedExitSecurityManager blockedExitSm = new BlockedExitSecurityManager(originalSm);
        System.setSecurityManager(blockedExitSm);
        assertThrows(SecurityException.class, () -> System.exit(0));
        System.setSecurityManager(originalSm);
    }
}
