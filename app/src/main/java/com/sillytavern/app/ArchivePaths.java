package com.sillytavern.app;

import java.io.File;
import java.io.IOException;

/** Exact directory-boundary check, including sibling-prefix traversal. */
final class ArchivePaths {
    static File resolve(File root, String name) throws IOException {
        if (name.isEmpty() || name.startsWith("/") || name.contains("\\")) {
            throw new IOException("Invalid archive path: " + name);
        }
        File canonicalRoot = root.getCanonicalFile();
        File output = new File(canonicalRoot, name).getCanonicalFile();
        if (!output.getPath().startsWith(canonicalRoot.getPath() + File.separator)) {
            throw new IOException("Archive entry leaves destination: " + name);
        }
        return output;
    }
}
