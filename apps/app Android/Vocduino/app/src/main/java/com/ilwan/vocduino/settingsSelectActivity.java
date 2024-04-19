package com.ilwan.vocduino;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class settingsSelectActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_settings_select);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
    }
    public void openGeneral(View v) {
        Intent i = new Intent(this, settingsGeneralActivity.class);
        startActivity(i);
    }
    public void openBluetooth(View v) {
        Intent i = new Intent(this, settingsBluetoothActivity.class);
        startActivity(i);
    }
    public void openRecognition(View v) {
        Intent i = new Intent(this, settingsRecognitionActivity.class);
        startActivity(i);
    }
}