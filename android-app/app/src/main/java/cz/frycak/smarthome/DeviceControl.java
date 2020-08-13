package cz.frycak.smarthome;


import android.app.Activity;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Intent;
import android.graphics.Color;
import android.os.Build;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.util.Log;
import android.content.Context;
import android.hardware.camera2.CameraAccessException;
import android.hardware.camera2.CameraManager;
import android.widget.Toast;

import androidx.core.app.NotificationCompat;


public class DeviceControl {
    private Context mainActivity;

    // Constructor
    public DeviceControl(Context context) {
        mainActivity = context;
    }

    // Flashlight
    public void flashlight(boolean state, int number) {
        CameraManager cameraManager = (CameraManager) mainActivity.getSystemService(Context.CAMERA_SERVICE);

        try {
            String cameraId = cameraManager.getCameraIdList()[number];
            cameraManager.setTorchMode(cameraId, state);
        }

        catch (CameraAccessException e) {
            Log.e("Flashlight", String.valueOf(e));
        }
    }

    // Vibrator
    public void vibrator(int time) {
        Vibrator vibrator = (Vibrator) mainActivity.getSystemService(Context.VIBRATOR_SERVICE);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            vibrator.vibrate(VibrationEffect.createOneShot(time, VibrationEffect.DEFAULT_AMPLITUDE));
        }

        else {
            // Deprecated in API 26
            vibrator.vibrate(time);
        }
    }

    // Toast notification
    public void toast(String text) {
        Toast.makeText(mainActivity.getApplicationContext(), text, Toast.LENGTH_SHORT).show();
    }

    // Normal notification
    public void notification() {
        Intent intent = new Intent(mainActivity.getApplicationContext(), MainActivity.class);
        PendingIntent pendingIntent = PendingIntent.getActivity(mainActivity.getApplicationContext(), 1, intent, 0);

        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            String CHANNEL_ID = "MYCHANNEL";
            NotificationChannel notificationChannel = null;
            notificationChannel = new NotificationChannel(CHANNEL_ID, "name", NotificationManager.IMPORTANCE_DEFAULT);

            Notification notification = new Notification.Builder(mainActivity.getApplicationContext(), CHANNEL_ID)
                    .setWhen(System.currentTimeMillis())
                    .setContentText("Filip je dežo. Nejnovějšími průzkumy to potvrdili američtí vědci.")
                    .setContentTitle("Novinky - Filip")
                    .setContentIntent(pendingIntent)
//                    .addAction(R.drawable.ic_notification_icon, "Zabít Filipa", pendingIntent)
                    .setChannelId(CHANNEL_ID)
                    .setColor(Color.rgb(23, 162, 184))
                    .setSmallIcon(R.drawable.ic_notification_icon)
                    .build();

            NotificationManager notificationManager = (NotificationManager) mainActivity.getSystemService(Context.NOTIFICATION_SERVICE);
            notificationManager.createNotificationChannel(notificationChannel);
            notificationManager.notify(1, notification);
        }

        else {
            NotificationCompat.Builder b = new NotificationCompat.Builder(mainActivity);
            b.setAutoCancel(true)
                    .setDefaults(NotificationCompat.DEFAULT_ALL)
                    .setWhen(System.currentTimeMillis())
                    .setContentText("Filip je dežo. Nejnovějšími průzkumy to potvrdili američtí vědci.")
                    .setContentTitle("Novinky - Filip")
                    .setContentIntent(pendingIntent)
//                    .addAction(R.drawable.ic_notification_icon, "Zabít Filipa", pendingIntent)
                    .setColor(Color.rgb(23, 162, 184))
                    .setSmallIcon(R.drawable.ic_notification_icon);

            NotificationManager notificationManager = (NotificationManager) mainActivity.getSystemService(Context.NOTIFICATION_SERVICE);
            notificationManager.notify(1, b.build());
        }
    }
}
