package com.sillytavern.app;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;

/** No Android stubs: exercise actual comparison and archive path code on a JVM. */
public class HostLogicTest {
    private static int assertions;
    private static void check(boolean ok, String message) {
        assertions++;
        if (!ok) throw new AssertionError(message);
    }
    private static void rejects(File root, String name) throws Exception {
        try { ArchivePaths.resolve(root, name); throw new AssertionError("Accepted " + name); }
        catch (IOException expected) { assertions++; }
    }
    public static void main(String[] args) throws Exception {
        check(!StableVersion.isNewer("v1.18.0", "1.18.0"), "v-prefix equality");
        check(StableVersion.isNewer("1.19.0", "1.18.0"), "minor update");
        check(StableVersion.isNewer("1.18.1", "1.18.0"), "patch update");
        check(!StableVersion.isNewer("1.9.0", "1.18.0"), "numeric order");
        check(!StableVersion.isNewer("1.19.0-beta", "1.18.0"), "reject prerelease");
        check(!StableVersion.isNewer(null, "1.18.0"), "network failure");
        check(!StableVersion.isNewer("1.19.0", "staging@abcd"), "unknown current");
        check(!StableVersion.isNewer("999999999999.1.0", "1.18.0"), "overflow");
        check(ServerReadiness.matches("SillyTavern is listening on IPv4: 127.0.0.1:18080", 18080), "own server ready");
        check(ServerReadiness.matches("SillyTavern is listening on IPv4: \u001B[32m127.0.0.1:18080\u001B[0m", 18080), "colored startup");
        check(!ServerReadiness.matches("SillyTavern is listening on IPv4: 127.0.0.1:8000", 18080), "Termux is not this server");
        check(!ServerReadiness.matches("SillyTavern is listening on IPv4: 127.0.0.1:180800", 18080), "exact port boundary");
        // server-main.js calls setWindowTitle() immediately before console.log(logListen).
        // On Android/Linux util.js writes OSC 2, terminated by ESC-backslash, without a newline.
        String startup = "SillyTavern is listening on IPv4: 127.0.0.1:18080";
        String title = "\u001B]2;SillyTavern WebServer\u001B\\";
        check(ServerReadiness.matches(title + startup, 18080), "real upstream OSC title prefix");
        check(ServerReadiness.matches(title + "SillyTavern is listening on\u001B[32m IPv4: 127.0.0.1:18080\u001B[39m", 18080), "OSC title and ANSI colors");
        check(ServerReadiness.matches("\u001B]0;SillyTavern\u0007" + startup, 18080), "BEL-terminated title");
        check(!ServerReadiness.matches(title + startup, 18081), "OSC prefix preserves exact port check");
        check(!ServerReadiness.matches("\u001B]2;" + startup + "\u001B\\unrelated output", 18080), "title text is not startup output");
        check(!ServerReadiness.matches("\u001B]2;" + startup, 18080), "unterminated title is not readiness");
        File temp = Files.createTempDirectory("st-archive-test").toFile();
        File root = new File(temp, "data"); root.mkdir();
        check(ArchivePaths.resolve(root, "default-user/characters/test.png").getParentFile()
                .equals(new File(root, "default-user/characters")), "nested card import");
        rejects(root, "../outside.txt");
        rejects(root, "../data-evil/settings.json");
        rejects(root, "/absolute.txt");
        rejects(root, "..\\escape.txt");
        rejects(root, "..");
        File outside = new File(temp, "outside"); outside.mkdir();
        File link = new File(root, "link");
        Files.createSymbolicLink(link.toPath(), outside.toPath());
        rejects(root, "link/file.txt");
        Files.delete(link.toPath()); root.delete(); outside.delete(); temp.delete();
        System.out.println("PASS: " + assertions + " host logic assertions");
    }
}
