package com.sillytavern.app;

/** Recognize the pinned upstream server's own startup message, not an HTTP stranger. */
final class ServerReadiness {
    static boolean matches(String line, int port) {
        if (line == null) return false;
        // Upstream writes an OSC window title without a newline before its ready message.
        String plain = line.replaceAll("\u001B\\][^\u0007\u001B]*(?:\u0007|\u001B\\\\)", "")
                .replaceAll("\u001B\\[[;\\d]*m", "");
        return plain.startsWith("SillyTavern is listening on")
                && plain.matches(".*127\\.0\\.0\\.1:" + port + "(?:\\D.*)?$");
    }
}
