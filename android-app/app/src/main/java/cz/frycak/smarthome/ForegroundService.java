package cz.frycak.smarthome;
// https://www.tutorialspoint.com/how-to-run-an-android-service-always-in-background

import android.annotation.SuppressLint;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.net.wifi.WifiManager;
import android.os.Build;
import android.os.Handler;
import android.os.IBinder;
import android.preference.PreferenceManager;
import android.text.format.Formatter;
import android.util.Base64;
import android.util.Log;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.core.app.NotificationCompat;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.io.ByteArrayOutputStream;
import java.nio.charset.StandardCharsets;

public class ForegroundService extends Service {
    private DeviceControl device;
    private MqttAndroidClient client;
    private MediaPlayer mp_doorbell;
    private MediaPlayer mp_ring;
    private AudioManager mAudioManager;
    private SharedPreferences sharedPreferences;

    private static final String TAG = MainActivity.class.getSimpleName();

    @SuppressLint("StaticFieldLeak")
    private static ForegroundService instance;
    public static ForegroundService getInstance() {
        return instance;
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        throw new UnsupportedOperationException("Not yet implemented");
//        return null;
    }

    @Override
    public void onTaskRemoved(Intent rootIntent) {
        Intent restartServiceIntent = new Intent(getApplicationContext(),this.getClass());
        restartServiceIntent.setPackage(getPackageName());
        startService(restartServiceIntent);
        super.onTaskRemoved(rootIntent);
    }

    @Override
    public void onCreate() {
        sharedPreferences = PreferenceManager.getDefaultSharedPreferences(ForegroundService.this);
        mAudioManager = (AudioManager) getSystemService(AUDIO_SERVICE);
        mp_doorbell = MediaPlayer.create(ForegroundService.this, R.raw.doorbell);
        mp_doorbell.setAudioStreamType(AudioManager.STREAM_MUSIC);

        mp_ring = MediaPlayer.create(ForegroundService.this, R.raw.ring);
        mp_ring.setAudioStreamType(AudioManager.STREAM_MUSIC);

        instance = this;
        device = new DeviceControl(this);

        String clientId = MqttClient.generateClientId();
        final SharedPreferences sharedPreferences = PreferenceManager.getDefaultSharedPreferences(this);

        String ip = sharedPreferences.getString("server_ip", "");
        String port = sharedPreferences.getString("mqtt_port", "");
        client = new MqttAndroidClient(this.getApplicationContext(), "tcp://" + ip + ":" + port, clientId);

        MqttConnectOptions options = new MqttConnectOptions();
        options.setMqttVersion(MqttConnectOptions.MQTT_VERSION_3_1);
        options.setAutomaticReconnect(true);
        options.setCleanSession(false);
        options.setKeepAliveInterval(10);

        try {
            IMqttToken token = client.connect(options);
            token.setActionCallback(new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    setSubscription();
//                    Toast.makeText(ForegroundService.this,"MQTT connection success!",Toast.LENGTH_LONG).show();
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
//                    Toast.makeText(ForegroundService.this,"MQTT connection failed!",Toast.LENGTH_LONG).show();
                }
            });
        } catch (MqttException e) {
            e.printStackTrace();
        }


        client.setCallback(new MqttCallback() {
            @Override
            public void connectionLost(Throwable cause) {
//                Toast.makeText(ForegroundService.this,"MQTT connection lost!",Toast.LENGTH_LONG).show();
                Log.e(TAG, "MQTT connection lost!");
            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                Log.e(topic, message.toString());
                String[] ids = topic.split("/");
                switch (ids[0]) {
                    case "client":
                        String device_id = sharedPreferences.getString("device_id", "");
                        if (ids[1].equals(device_id) || ids[1].equals("android_broadcast")) {
                            switch (ids[2]) {
                                case "flashlight_back":
                                    device.flashlight(message.toString().equals("True"), 0);
                                    break;
                                case "flashlight_front":
                                    device.flashlight(message.toString().equals("True"), 1);
                                    break;
                                case "vibration":
                                    device.vibrator(Integer.parseInt(message.toString()));
                                    break;
                                case "ring_call":
                                    final int originalVolume = mAudioManager.getStreamVolume(AudioManager.STREAM_MUSIC);
                                    mAudioManager.setStreamVolume(AudioManager.STREAM_MUSIC, mAudioManager.getStreamMaxVolume(AudioManager.STREAM_MUSIC), 0);
                                    mp_ring.start();
                                    mp_ring.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
                                        @Override
                                        public void onCompletion(MediaPlayer mp) {
                                            mAudioManager.setStreamVolume(AudioManager.STREAM_MUSIC, originalVolume, 0);
                                        }
                                    });
                                    break;
                            }
                        }

                        break;
                    case "android_settings":
                        if (device.ip().equals(message.toString())) {
                            MainActivity.getInstance().showSettings();
                        }
                        break;
                    case "doorbird_client":
                        Log.e(TAG, message.toString());

                        // Define variables and constants
                        String channelID;
                        String messageText;
                        String titleText;
                        final int notifyID;
                        int priority;
                        boolean delayed;

                        // Set messages
                        if (ids[1].equals("doorbell")) {
                        final int originalVolume = mAudioManager.getStreamVolume(AudioManager.STREAM_MUSIC);
                            mAudioManager.setStreamVolume(AudioManager.STREAM_MUSIC, mAudioManager.getStreamMaxVolume(AudioManager.STREAM_MUSIC), 0);
                            mp_doorbell.start();
                            mp_doorbell.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
                                @Override
                                public void onCompletion(MediaPlayer mp) {
                                    mAudioManager.setStreamVolume(AudioManager.STREAM_MUSIC, originalVolume, 0);
                                }
                            });
                            titleText = (String) getText(R.string.doorbird_doorbell);
                            messageText = (String) getText(R.string.doorbird_doorbell_message);

                            priority = NotificationManager.IMPORTANCE_HIGH;

                            channelID = "doorbird_doorbell";
                            notifyID = 1;
                            delayed = true;
                        } else {
                            titleText = (String) getText(R.string.doorbird_motionsensor);
                            messageText = (String) getText(R.string.doorbird_motionsensor_message);

                            priority = NotificationManager.IMPORTANCE_DEFAULT;

                            channelID = "doorbird_motionsensor";
                            notifyID = 2;
                            delayed = false;
//                        device.vibrator(50);
                        }

                        // BitmapFactory.decodeStream(message.toString());

                        // General
                        final NotificationManager notificationManager = (NotificationManager) ForegroundService.this.getSystemService(Context.NOTIFICATION_SERVICE);

                        // Notification intents
                        Intent notificationIntent = new Intent(ForegroundService.this, MainActivity.class);
                        Intent unlockIntent = new Intent(ForegroundService.this, UnlockReceiver.class);
                        PendingIntent pendingNotificationIntent = PendingIntent.getActivity(ForegroundService.this, 0, notificationIntent, 0);
                        PendingIntent pendingUnlockIntent = PendingIntent.getBroadcast(ForegroundService.this, 0, unlockIntent, 0);

                        // Notification channel
                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                            NotificationChannel notificationChannel = new NotificationChannel(channelID, channelID, priority);
                            notificationManager.createNotificationChannel(notificationChannel);
                        }

                        byte[] imageBytes = Base64.decode(message.toString(), Base64.DEFAULT);
                        Bitmap decodedImage = BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.length);

                        // Bitmap bitmap = BitmapFactory.decodeResource(getResources(), R.drawable.example_appwidget_preview);

                        // Notification
                        final Notification notification = new NotificationCompat.Builder(ForegroundService.this, channelID)
                                .setAutoCancel(true)
                                .setPriority(priority)
                                .setContentText(messageText)
                                .setContentTitle(titleText)
                                .setContentIntent(pendingNotificationIntent)
                                .setAutoCancel(true)
                                .addAction(R.drawable.ic_notification_icon, getText(R.string.unlock), pendingUnlockIntent)
                                .setColor(Color.rgb(23, 162, 184))
                                .setSmallIcon(R.drawable.ic_notification_icon)
                                .setStyle(new NotificationCompat.BigPictureStyle()
                                        .bigPicture(decodedImage).setSummaryText(messageText))
                                .build();

//                        if (delayed) {
//                            final Handler handler = new Handler();
//                            handler.postDelayed(new Runnable() {
//                                @Override
//                                public void run() {
                                    notificationManager.notify(notifyID, notification);
//                                }
//                            }, 8000);
//                        } else {
//                            notificationManager.notify(notifyID, notification);
//                        }
                        break;
                }
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });

    }

    public void publish(String topic, String message){
        String[] ids = topic.split("/");
        if (ids[0].equals("doorbird_home") && ids[1].equals("open_door")) {
            device.toast(String.valueOf(getText(R.string.unlock_send)));
        }
        try {
            client.publish(topic, message.getBytes(),0,false);
        } catch ( MqttException e) {
            e.printStackTrace();
        }
    }

    private void setSubscription(){
        try {
            client.subscribe("client/#",0);
            client.subscribe("doorbird_client/#",0);
            client.subscribe("android_settings/#",0);
        } catch (MqttException e){
            e.printStackTrace();
        }
        Log.e(TAG, "finished loggin");
    }
    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        // Bitmap icon = BitmapFactory.decodeResource(getResources(), R.drawable.ic_notification_icon);

        // Constants and variables
        String channelID = "service";

//        onTaskRemoved(intent);
//        Toast.makeText(getApplicationContext(),"This is a Service running in Background",
//                Toast.LENGTH_SHORT).show();

        // Intent
        Intent notificationIntent = new Intent(this, MainActivity.class);
        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0, notificationIntent, 0);

        // Notification channel
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            NotificationChannel notificationChannel = new NotificationChannel(channelID, channelID, NotificationManager.IMPORTANCE_LOW);
            NotificationManager notificationManager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
            notificationManager.createNotificationChannel(notificationChannel);
        }

        // Notification
        Notification notification = new NotificationCompat.Builder(this, channelID)
                .setContentTitle(getText(R.string.app_name))
                .setContentText(getText(R.string.app_is_running))
                .setColor(Color.rgb(23, 162, 184))
                .setSmallIcon(R.drawable.ic_notification_icon)
//                    .setLargeIcon(icon)
//                    .setStyle(new NotificationCompat.BigPictureStyle()
//                            .bigPicture(icon))
                .setCategory(Notification.CATEGORY_SERVICE)
                .setContentIntent(pendingIntent)
                .setTicker("Ticker text")
                .build();

        // Notification ID cannot be 0.
        startForeground(1001, notification);
        

        // OS won't kill the service
        return START_STICKY;
    }


    @Override
    public void onDestroy() {
        Toast.makeText(this, "Service Stopped", Toast.LENGTH_LONG).show();
    }
}