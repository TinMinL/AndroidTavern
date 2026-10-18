package com.sillytavern.app;

import android.content.Context;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

/** Read-only upstream release lookup. Core updates require a future rollback design. */
public class StUpdater {

    private static final String UPSTREAM = "https://github.com/SillyTavern/SillyTavern.git";
    private static final String API_LATEST =
            "https://api.github.com/repos/SillyTavern/SillyTavern/releases/latest";

    public enum Mode {ST_LATEST, ST_STAGING, PACKAGES, REPAIR}

    public interface Logger {
        void log(String line);
    }

    /** Queries GitHub for the latest upstream release tag; null on failure. */
    public static String fetchLatestReleaseTag() {
        HttpURLConnection conn = null;
        try {
            conn = (HttpURLConnection) new URL(API_LATEST).openConnection();
            conn.setConnectTimeout(8000);
            conn.setReadTimeout(8000);
            conn.setRequestProperty("User-Agent", "ST-Manager-Android");
            conn.setRequestProperty("Accept", "application/vnd.github+json");
            if (conn.getResponseCode() != 200) {
                return null;
            }
            StringBuilder sb = new StringBuilder();
            try (BufferedReader reader = new BufferedReader(
                    new InputStreamReader(conn.getInputStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    sb.append(line);
                }
            }
            return new JSONObject(sb.toString()).optString("tag_name", null);
        } catch (Exception e) {
            return null;
        } finally {
            if (conn != null) {
                conn.disconnect();
            }
        }
    }

    /** Preview deliberately provides checks only until rollback is implemented. */
    public static void run(Context context, Mode mode, Logger log) throws Exception {
        throw new Exception("试用版只检查更新，尚未启用程序替换与回退。现有数据未改动。");
    }
}
