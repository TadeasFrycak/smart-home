package cz.frycak.smarthome;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.widget.Toast;

public class UnlockReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        Toast.makeText(context,"recieved",Toast.LENGTH_SHORT).show();
        ForegroundService.getInstance().publish("doorbird_home/open_door", "1");

//        String action=intent.getStringExtra("action");
//        if(action.equals("action1")){
//            performAction1();
//        }
//        else if(action.equals("action2")){
//            performAction2();
//
//        }
        //This is used to close the notification tray
        Intent it = new Intent(Intent.ACTION_CLOSE_SYSTEM_DIALOGS);
        context.sendBroadcast(it);
    }
}