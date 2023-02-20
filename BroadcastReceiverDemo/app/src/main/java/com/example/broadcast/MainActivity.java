package com.example.broadcast;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import com.example.myapplication.R;

public class MainActivity extends AppCompatActivity {

    private Button static_button;
    private Button dynamic_button;
//    private DynamicBroadcastReceiver mReceiver;
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
                intent.setPackage("com.example.receiver");//8.0一下可以不用加这个也可以收到广播，但是8.0以后就需要加上这个不然收不到广播
                sendBroadcast(intent);
            }
        });

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
}