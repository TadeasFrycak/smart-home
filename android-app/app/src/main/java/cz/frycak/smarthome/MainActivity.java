package cz.frycak.smarthome;

// TODO background process - MQTT, notifications
// TODO tile mobil - po MQTT bude moct být vyslán příkaz na zavolání, najití telefonu, vibrace, atd.
// TODO white background in whole app --> black
// TODO zkontrolovat, jestli nevyšla nová verze apk, potom ihned stáhnout
// TODO udělat nastavení, kde se nastaví na začátku IP adresa, port a poté i WiFi síť - pokud se poté zařízení připojí na špatnou WiFi síť, tak ukázat jinou chybu
// TODO only wifi, ne mobilní data
// TODO on preference change --> refresh page
// TODO optimalizovat HTML - udělat doplňování textu místo rozdílních HTML souborů (obsahují všechno stejné kromě textů)

import androidx.appcompat.app.AppCompatActivity;
import android.annotation.SuppressLint;
import android.app.ActivityManager;
import android.content.ActivityNotFoundException;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.Uri;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.judemanutd.autostarter.AutoStartPermissionHelper;


import java.net.URISyntaxException;
import com.github.nkzawa.socketio.client.IO;
import com.github.nkzawa.socketio.client.Socket;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class MainActivity extends AppCompatActivity {
    private WebView webview;
    private DeviceControl device;
    private Button refreshButton;
    private Button settingsButton;
    private boolean settingsShowed;
    private boolean settingsChanged;
    Intent mServiceIntent;
    private BackgroundService mYourService;
    private static final String TAG = MainActivity.class.getSimpleName();
//    MqttAndroidClient client;


//    private Socket mSocket;
//    {
//        try {
//            mSocket = IO.socket("http://192.168.88.25:5000/com");
//        } catch (URISyntaxException e) {
//            e.printStackTrace();
//        }
//    }
//
//    private void attemptSend() {
//        mSocket.emit("doorbird_open_door");
//    }

    @SuppressLint("StaticFieldLeak")
    private static MainActivity instance;

    public static MainActivity getInstance() {
        return instance;
    }

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
//        mSocket.connect();
//        attemptSend();
//        startMqtt();


        /*String clientId = MqttClient.generateClientId();
        client = new MqttAndroidClient(this.getApplicationContext(), "tcp://192.168.88.25:1883",clientId);
        //client = new MqttAndroidClient(this.getApplicationContext(), "tcp://192.168.43.41:1883",clientId);

        try {
            IMqttToken token = client.connect();
            token.setActionCallback(new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    Toast.makeText(MainActivity.this,"connected!!",Toast.LENGTH_LONG).show();
                    setSubscription();
                    published();
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    Toast.makeText(MainActivity.this,"connection failed!!",Toast.LENGTH_LONG).show();
                }
            });
        } catch (MqttException e) {
            e.printStackTrace();
        }

        client.setCallback(new MqttCallback() {
            @Override
            public void connectionLost(Throwable cause) {

            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                if (message.toString().equals("1")) {
                    device.flashlight(true, 0);
                    device.flashlight(true, 1);
                }
                else {
                    device.flashlight(false, 0);
                    device.flashlight(false, 1);
                }
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });*/


        device = new DeviceControl(this);

        updateUI();

        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);

        setContentView(R.layout.activity_main);
        refreshButton = findViewById(R.id.refresh);
        settingsButton = findViewById(R.id.settings);
        instance = this;

        AndroidBug5497Workaround.assistActivity(this);

        hideBars();

        // TODO on Pie with notch problem with status bar visibility after keyboard opens
//        KeyboardVisibilityEvent.setEventListener(
//                this,
//                new KeyboardVisibilityEventListener() {
//                    @Override
//                    public void onVisibilityChanged(boolean isOpen) {
//                        Log.e("puase", "halo pauza");
//                        View decorView = getWindow().getDecorView();
//                        // Show Status Bar.
//                        int uiOptions = View.SYSTEM_UI_FLAG_VISIBLE;
//                        decorView.setSystemUiVisibility(uiOptions);
//                    }
//                });

        webview = (WebView) findViewById(R.id.webView);
        webview.setBackgroundColor(Color.parseColor("#303030"));
        webview.getSettings().setJavaScriptEnabled(true);
        webview.getSettings().setDomStorageEnabled(true);
        webview.getSettings().setDatabaseEnabled(true);
        webview.getSettings().setMinimumFontSize(1);
        webview.getSettings().setMinimumLogicalFontSize(1);
        webview.getSettings().setLoadWithOverviewMode(true);
        webview.getSettings().setUseWideViewPort(true);
        webview.setOverScrollMode(View.OVER_SCROLL_NEVER);
        webview.setWebViewClient(new WebViewClient() {
            @Override
            public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
                showButtons();
                webview.loadUrl("file:///android_asset/html/" + getString(R.string.server_html));
                device.vibrator(200);
            }
        });

        mYourService = new BackgroundService();
        mServiceIntent = new Intent(this, mYourService.getClass());
        if (!isMyServiceRunning(mYourService.getClass())) {
            startService(mServiceIntent);
        }

        // TODO nefunguje v simulaci

        reloadPage();

//        try
//        {
//            //Open the specific App Info page:
//            Intent intent = new Intent(android.provider.Settings.ACTION_APPLICATION_DETAILS_SETTINGS);
//            intent.setData(Uri.parse("package:" + this.getPackageName()));
//            this.startActivity(intent);
//        }
//        catch ( ActivityNotFoundException e )
//        {
//            //Open the generic Apps page:
//            Intent intent = new Intent(android.provider.Settings.ACTION_MANAGE_APPLICATIONS_SETTINGS);
//            this.startActivity(intent);
//        }

//        AutoStartPermissionHelper.getInstance().getAutoStartPermission(this);

    }

    /*public void published(){

        String topic = "home/wl8915";
        String message = "1";
        try {
            client.publish(topic, message.getBytes(),0,false);
            Toast.makeText(this,"Published Message",Toast.LENGTH_SHORT).show();
        } catch ( MqttException e) {
            e.printStackTrace();
        }
    }

    private void setSubscription(){

        try{

            client.subscribe("#",0);


        }catch (MqttException e){
            e.printStackTrace();
        }
    }*/

    private boolean isMyServiceRunning(Class<?> serviceClass) {
        ActivityManager manager = (ActivityManager) getSystemService(Context.ACTIVITY_SERVICE);
        for (ActivityManager.RunningServiceInfo service : manager.getRunningServices(Integer.MAX_VALUE)) {
            if (serviceClass.getName().equals(service.service.getClassName())) {
                Log.i ("Service status", "Running");
                return true;
            }
        }
        Log.i ("Service status", "Not running");
        return false;
    }
//    @Override
//    protected void onDestroy() {
//        stopService(mServiceIntent);
//        super.onDestroy();
//    }
    @Override
    protected void onResume() {
        super.onResume();
        updateUI();
        if (settingsShowed && settingsChanged) {
            device.toast(getString(R.string.refreshing));
            reloadPage();
            settingsShowed = false;
            settingsChanged = false;
        }
    }



    private void reloadPage() {
        ConnectivityManager connManager = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo mWifi = connManager.getNetworkInfo(ConnectivityManager.TYPE_WIFI);

        if (mWifi != null && mWifi.isConnected()) {
            device.notification();
            SharedPreferences sharedPreferences = PreferenceManager.getDefaultSharedPreferences(this);

            String ip = sharedPreferences.getString("server_ip", "");
            String port = sharedPreferences.getString("server_port", "");

            if (port != null && ip != null && !ip.equals("")) {
                hideButtons();
                if (port.equals("443")) {
                    webview.loadUrl("https://" + ip + ":" + port);
                }

                else {
                    webview.loadUrl("http://" + ip + ":" + port);
                }

//                if (!(mqttIsConnected)) {
//                    mqttConnect();
//                }
            }

            else {
                showButtons();
                webview.loadUrl("file:///android_asset/html/" + getString(R.string.server_html));
                device.vibrator(200);
            }
        }

        else {
            showButtons();
            webview.loadUrl("file:///android_asset/html/" + getString(R.string.wifi_html));
            device.vibrator(200);
        }
    }



    private void updateUI() {
        final View decorView = getWindow().getDecorView();
        decorView.setOnSystemUiVisibilityChangeListener (new View.OnSystemUiVisibilityChangeListener() {
            @Override
            public void onSystemUiVisibilityChange(int visibility) {
                if ((visibility & View.SYSTEM_UI_FLAG_FULLSCREEN) == 0) {
                    hideBars();
                }
            }
        });
    }

    private void hideBars() {
        View decorView = getWindow().getDecorView();
        decorView.setSystemUiVisibility(View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION // hide nav bar
                | View.SYSTEM_UI_FLAG_FULLSCREEN // hide status bar
                | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY // hide status bar and nav bar after a short delay, or if the user interacts with the middle of the screen
        );
    }

    public void showSettings() {
        Intent intent = new Intent(this, SettingsActivity.class);
        startActivity(intent);
        settingsShowed = true;
    }

    private void showButtons() {
        refreshButton.setVisibility(View.VISIBLE);
        settingsButton.setVisibility(View.VISIBLE);
    }

    private void hideButtons() {
        refreshButton.setVisibility(View.GONE);
        settingsButton.setVisibility(View.GONE);
    }

    public void setSettingsChanged() {
        settingsChanged = true;
    }
    public void reload(View view) {
        reloadPage();
    }

    public void settings(View view) {
        showSettings();
    }
}