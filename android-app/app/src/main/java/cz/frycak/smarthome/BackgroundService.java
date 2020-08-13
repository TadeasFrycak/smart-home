package cz.frycak.smarthome;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.net.wifi.WifiManager;
import android.os.Build;
import android.os.CountDownTimer;
import android.os.IBinder;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.preference.PreferenceManager;
import android.text.format.Formatter;
import android.util.Log;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.core.app.NotificationCompat;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;


public class BackgroundService extends Service implements MqttCallback {

    private static final int NOTIF_ID = 1;
    private static final String NOTIF_CHANNEL_ID = "Channel_Id";
    private DeviceControl device;

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId){
        device = new DeviceControl(this);
        mqttConnect();
        startForeground();

        return super.onStartCommand(intent, flags, startId);
    }

    @Override
    public void connectionLost(Throwable cause) {
        Log.d("MQTT", "connection lost");
        device.toast("MQTT connection lost");
        mqttConnect();
    }

    @Override
    public void messageArrived(String topic, MqttMessage message) throws Exception {
        String payload = new String(message.getPayload());
        Log.d("MQTT", topic + " - " + payload);

        switch (topic) {
            case "android_settings":
                WifiManager wm = (WifiManager) getSystemService(WIFI_SERVICE);
                String ip = Formatter.formatIpAddress(wm.getConnectionInfo().getIpAddress());
                if (ip.equals(payload)) {
                    MainActivity.getInstance().showSettings();
                    device.vibrator(100);
                }
                break;
            case "client/android/flashlight-back":
                if (String.valueOf(message).equals("0")) {
                    device.flashlight(false, 0);
                } else {
                    device.flashlight(true, 0);
                }
                break;
            case "client/android/flashlight-front":
                if (String.valueOf(message).equals("0")) {
                    device.flashlight(false, 1);
                } else {
                    device.flashlight(true, 1);
                }
                break;
            case "client/android/vibrator":
                device.vibrator(Integer.parseInt(payload));

                break;
        }
    }

    private void mqttConnect() {
//        device.toast("test");
        SharedPreferences sharedPreferences = PreferenceManager.getDefaultSharedPreferences(this);
        String ip = sharedPreferences.getString("server_ip", "");
        String mqtt_port = sharedPreferences.getString("mqtt_port", "");


        try {
            MqttClient client = new MqttClient("tcp://" + ip + ":" + mqtt_port, "AndroidThingSub", new MemoryPersistence());
            client.setCallback(this);
            client.connect();
            client.subscribe("client/android/#");
            client.subscribe("android_settings/#");
            device.toast("ok");
        }

        catch (MqttException e) {
            e.printStackTrace();
            device.toast("err");
        }
    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken token) {
        Log.d("MQTT", "deliveryComplete");
    }
    private void startForeground() {
        Intent notificationIntent = new Intent(this, MainActivity.class);

        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0,
                notificationIntent, 0);
        NotificationChannel notificationChannel = null;
        notificationChannel = new NotificationChannel(NOTIF_CHANNEL_ID, "name", NotificationManager.IMPORTANCE_DEFAULT);

        startForeground(NOTIF_ID, new NotificationCompat.Builder(this,
                NOTIF_CHANNEL_ID) // don't forget create a notification channel first
                .setOngoing(true)
                .setSmallIcon(R.drawable.ic_notification_icon)
                .setContentTitle(getString(R.string.app_name))
                .setContentText("Service is running background")
                .setColor(Color.rgb(23, 162, 184))
                .setContentIntent(pendingIntent)
                .build());
    }
}
