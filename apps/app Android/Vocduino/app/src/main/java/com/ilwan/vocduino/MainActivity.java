package com.ilwan.vocduino;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import java.util.Objects;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
    }
    public void openSettings(View v) {
        Intent i = new Intent(this, settingsSelectActivity.class);
        startActivity(i);
    }
    public void openAbout(View v) {
        Intent i = new Intent(this, aboutActivity.class);
        startActivity(i);
    }
    public static int levenshtein(String s1, String s2, int threshold) {
        if (Objects.equals(s1, s2)) {
            return 0;
        }
        if (s1 == null || s2 == null) {
            return threshold + 1;
        }
        int len1 = s1.length();
        int len2 = s2.length();
        // If the strings are of different lengths and the length difference is greater than the threshold,
        // the distance is definitely greater than the threshold
        if (Math.abs(len1 - len2) > threshold) {
            return threshold + 1;
        }
        // Swap the strings so that the first string is the shortest
        if (len1 > len2) {
            String tmp = s1;
            s1 = s2;
            s2 = tmp;
            int tmpLen = len1;
            len1 = len2;
            len2 = tmpLen;
        }

        // creating the matrix
        int[][] dp = new int[2][len2 + 1];
        int currentRow = 0;
        // Initialize the first row
        for (int j = 0; j <= len2; j++) {
            dp[currentRow][j] = j;
        }
        for (int i = 1; i <= len1; i++) {
            currentRow = 1 - currentRow; // Switch rows
            dp[currentRow][0] = i;
            for (int j = 1; j <= len2; j++) {
                int cost = (s1.charAt(i - 1) == s2.charAt(j - 1)) ? 0 : 1;
                dp[currentRow][j] = Math.min(
                        Math.min(dp[1 - currentRow][j] + 1, dp[currentRow][j - 1] + 1),
                        dp[1 - currentRow][j - 1] + cost);
                // Early exit if the distance exceeds the threshold
                if (dp[currentRow][j] > threshold) {
                    return threshold + 1;
                }
            }
        }
        return dp[currentRow][len2];
    }
    public static int levenshtein(String s1, String s2) {
        return levenshtein(s1, s2, Integer.MAX_VALUE);
    }
}