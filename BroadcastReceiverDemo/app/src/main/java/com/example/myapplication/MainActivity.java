package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebView;
import android.widget.Button;
import android.widget.Toast;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    private Button static_button;
    private Button dynamic_button;
    private DynamicBroadcastReceiver mReceiver;
    private static final String TAG = MainActivity.class.getSimpleName();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        init();

        static_button = (Button) findViewById(R.id.static_button);
        static_button.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                Intent intent = new Intent();
                intent.putExtra("msg", "你呢1");
                intent.setPackage(getPackageName());//8.0一下可以不用加这个也可以收到广播，但是8.0以后就需要加上这个不然收不到广播
                sendBroadcast(intent);
            }
        });

        mReceiver = new DynamicBroadcastReceiver();
        IntentFilter intentFilter = new IntentFilter();
        intentFilter.addAction("dynamic");
        registerReceiver(mReceiver, intentFilter);

        dynamic_button = (Button) findViewById(R.id.dynamic_button);
        dynamic_button.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                Intent intent = new Intent();
                intent.setAction("dynamic");
                sendBroadcast(intent);
            }
        });


    }

    public void init(){

    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        Log.d(TAG, "zwm, onDestroy");
        unregisterReceiver(mReceiver);
    }
}