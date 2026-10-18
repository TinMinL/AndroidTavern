package com.sillytavern.app;

/** Compare only stable release tags; unknown/prerelease labels are not upgrades. */
final class StableVersion {
    static boolean isNewer(String latest, String current) {
        int[] a = parse(latest), b = parse(current);
        if (a == null || b == null) return false;
        for (int i = 0; i < 3; i++) {
            if (a[i] != b[i]) return a[i] > b[i];
        }
        return false;
    }

    private static int[] parse(String value) {
        if (value == null || !value.matches("v?[0-9]+\\.[0-9]+\\.[0-9]+")) return null;
        String[] parts = value.replaceFirst("^v", "").split("\\.");
        try {
            return new int[]{Integer.parseInt(parts[0]), Integer.parseInt(parts[1]), Integer.parseInt(parts[2])};
        } catch (NumberFormatException e) {
            return null;
        }
    }
}
