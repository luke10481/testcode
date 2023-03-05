package com.example.myapplication;

import android.Manifest;
import android.content.ContentResolver;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;

import com.google.android.material.snackbar.Snackbar;

import androidx.appcompat.app.AppCompatActivity;

import android.provider.ContactsContract;
import android.view.View;

import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;

import com.example.myapplication.databinding.ActivityMainBinding;

import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    private TextView et_contact; //显示查询的信息
    private EditText et_username; //用户名
    private EditText et_phone; //电话
    private Button btn_search; //搜索
    private Button btn_insert;//插入
    private Button btn_delete; //删除
    private Button btn_update; //更新
    private Button btn_search_all; //查询所有

    private String selections; //查询条件
    private String[] selection_args; //查询参数

    //要查询的字段
    String[] query_all = new String[]{
            ContactsContract.CommonDataKinds.Identity.RAW_CONTACT_ID, //用户id
            ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME, //联系人姓名
            ContactsContract.CommonDataKinds.Phone.NUMBER //联系人电话
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        et_contact = findViewById(R.id.et_contact);
        et_username = findViewById(R.id.et_username);
        et_phone = findViewById(R.id.et_phone);
        btn_search = findViewById(R.id.btn_search);
        btn_insert = findViewById(R.id.btn_insert);
        btn_delete = findViewById(R.id.btn_delete);
        btn_update = findViewById(R.id.btn_update);
        btn_search_all = findViewById(R.id.btn_search_all);

        btn_search_all.setOnClickListener(this);
        btn_insert.setOnClickListener(this);
        btn_delete.setOnClickListener(this);
        btn_search.setOnClickListener(this);
        btn_update.setOnClickListener(this);


        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_CONTACTS) != PackageManager.PERMISSION_GRANTED || ContextCompat.checkSelfPermission(this, Manifest.permission.READ_CONTACTS) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.WRITE_CONTACTS, Manifest.permission.READ_CONTACTS}, 1);
            }
        }
    }
    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.btn_insert:
                String name = et_username.getText().toString();
                String phone = et_phone.getText().toString();

                ContentValues values = new ContentValues();
                Uri uri = getContentResolver().insert(ContactsContract.RawContacts.CONTENT_URI, values);
                long rawContentID = ContentUris.parseId(uri);

                if (!name.equals("")) {
                    values.clear();
                    values.put(ContactsContract.Data.RAW_CONTACT_ID, rawContentID);
                    values.put(ContactsContract.Data.MIMETYPE, ContactsContract.CommonDataKinds.StructuredName.CONTENT_ITEM_TYPE);
                    values.put(ContactsContract.CommonDataKinds.StructuredName.GIVEN_NAME, name);
                    getContentResolver().insert(ContactsContract.Data.CONTENT_URI, values);
                }
                if (!phone.equals("")) {
                    values.clear();
                    values.put(ContactsContract.Data.RAW_CONTACT_ID, rawContentID);
                    values.put(ContactsContract.Data.MIMETYPE, ContactsContract.CommonDataKinds.Phone.CONTENT_ITEM_TYPE);
                    values.put(ContactsContract.CommonDataKinds.Phone.TYPE, ContactsContract.CommonDataKinds.Phone.TYPE_MOBILE);
                    values.put(ContactsContract.CommonDataKinds.Phone.NUMBER, phone);
                    getContentResolver().insert(ContactsContract.Data.CONTENT_URI, values);
                }
                Toast.makeText(this, "插入成功", Toast.LENGTH_SHORT).show();
                break;
            case R.id.btn_search_all:
                //参数二：表示要查询的字段，如果为null，表示查询所有的字段
                Cursor cursor1 = getContentResolver().query(ContactsContract.CommonDataKinds.Phone.CONTENT_URI, query_all, null, null, null);
                printQueryResult(cursor1);
                break;
            case R.id.btn_delete:
                String name1 = et_username.getText().toString();
                if (!name1.equals("")) {
                    getContentResolver().delete(ContactsContract.RawContacts.CONTENT_URI, ContactsContract.Contacts.DISPLAY_NAME + "=?", new String[]{name1});
                    Toast.makeText(this, "删除成功！", Toast.LENGTH_SHORT).show();
                }
                break;
            case R.id.btn_search:
                String name_search = et_username.getText().toString();
                Cursor cursor = getContentName(name_search);
                printQueryResult(cursor);
                break;
            case R.id.btn_update:
                String name_update = et_username.getText().toString();
                String phone_update = et_phone.getText().toString();
                Long rawContactId = 0L;
                ContentResolver resolver = getContentResolver();
                ContentValues values1 = new ContentValues();
                values1.put(ContactsContract.CommonDataKinds.Phone.NUMBER, phone_update);
                if (!name_update.equals("")) {
                    Cursor cursor2 = getContentName(name_update);
                    if (cursor2.moveToFirst()) {
                        rawContactId = cursor2.getLong(0);
                    }
                    resolver.update(ContactsContract.Data.CONTENT_URI, values1, "mimetype=? and raw_contact_id=?"
                            , new String[]{ContactsContract.CommonDataKinds.Phone.CONTENT_ITEM_TYPE, rawContactId + ""});
                    cursor2.close();
                    Toast.makeText(this, "更新成功！", Toast.LENGTH_SHORT).show();
                }
                break;
        }
    }
    private Cursor getContentName(String name_search) {
        selections = ContactsContract.Contacts.DISPLAY_NAME + "=?";
        selection_args = new String[]{name_search};
        Cursor cursor = getContentResolver().query(ContactsContract.CommonDataKinds.Phone.CONTENT_URI, query_all, selections, selection_args, null);
        return cursor;
    }

    private void printQueryResult(Cursor cursor) {
        if (cursor != null) {
            et_contact.setText("");
            while (cursor.moveToNext()) {
                String ID = cursor.getString(0);
                String stringName = cursor.getString(1);
                String phone = cursor.getString(2);
                et_contact.append("\n联系人ID:" + ID + "\n联系人姓名：" + stringName + "\n联系人电话:" + phone);
            }
        }
        cursor.close();
    }
}