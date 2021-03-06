# Welcome to droid (Re, 635p, 24 solved)

[PL](#pl-version)

In the task we get [android application](droid.apk) to work with.
Once we reverse the sources, it seems we need to pass some checks to reach the flag.
However one of the checks is:

```java
public String m4832k() {
	char[] cArr = new char[]{'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};
	StringBuffer stringBuffer = new StringBuffer();
	Random random = new Random();
	for (int i = 0; i < 20; i++) {
		stringBuffer.append(cArr[random.nextInt(cArr.length)]);
	}
	return stringBuffer.toString();
}
```

And sice it's using random values, it's very unlikely we can pass it.
We could try to patch the code, but it's a lot of fuss.
If we could pass all the checks the code that shows the flag is:

```java
this.f3092l = (EditText) findViewById(R.id.editText);
this.f3092l.setText(stringFromJNI());
```

So it calls a single function from the native library shipped with the app.
The function is pretty much unreversable, way to complex, but we don't need that.
We can simply load this library and call the function, without all silly checks!

In order to do that we create a new android project (we actually used NDK example) with Android Studio, create a new Activity, but keeping all the names and packages the same, and write code:

```java
package com.example.puing.a2018codegate;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

import java.util.logging.Logger;

public class Main4Activity extends AppCompatActivity {
    static {
        System.loadLibrary("hello-libs");
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        TextView tv = new TextView(this);
        String flagString = stringFromJNI();
        tv.setText(flagString);
        setContentView(tv);
        Logger.getLogger("flagLogger").info(flagString);
    }

    public native String stringFromJNI();
}
```

We modify the build.gradle for libs to include our .so files:

```
sourceSets {
	main {
		// let gradle pack the shared library into apk
		jniLibs.srcDirs = ['../distribution/gperf/lib', '../distribution/droid/lib']
	}
}
```

And we're good to go.
We can just run the app and get:

![](flag.png)

So the flag is: `FLAG{W3_w3r3_Back_70_$3v3n7een!!!}`

### PL version

W zadaniu dostajemy [aplikacj?? androidow??](droid.apk).
Po zdekompilowaniu i analizie ??r??de?? wida??, ??e musimy przej???? kilka test??w ??eby dosta?? flag??.
Niestety jeden z nich to:

```java
public String m4832k() {
	char[] cArr = new char[]{'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};
	StringBuffer stringBuffer = new StringBuffer();
	Random random = new Random();
	for (int i = 0; i < 20; i++) {
		stringBuffer.append(cArr[random.nextInt(cArr.length)]);
	}
	return stringBuffer.toString();
}
```

A skoro u??ywa losowych warto??ci to jest ma??a szansa ??e uda si?? go przej????.
Mogliby??my spr??bowa?? patchowa?? ten kod, ale to du??o roboty.
Gdyby??my przeszli testy to za wy??wietlenie flagi odpowiada:

```java
this.f3092l = (EditText) findViewById(R.id.editText);
this.f3092l.setText(stringFromJNI());
```

Wi??c wo??ana jest jedna funkcja z natywnej biblioteki dostarczonej z aplikacj??.
Sama funkcja jest praktycznie nie do zreversowania, zbyt skomplikowana, ale nie musimy tego robi??.
Mo??emy po prostu za??adowa?? sobie t?? bibliotek?? i wywo??a?? funkcje, bez ??adnych test??w!

??eby to zrobi?? stworzyli??my nowy projekt androidowy (u??yli??my jako szablonu przyk??adowego kodu z NDK) w Android Studio, stworzyli??my w??asne Activity, pozostawiaj??c takie same nazwy klas i pakiet??w i napisali??my kod:

```java
package com.example.puing.a2018codegate;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

import java.util.logging.Logger;

public class Main4Activity extends AppCompatActivity {
    static {
        System.loadLibrary("hello-libs");
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        TextView tv = new TextView(this);
        String flagString = stringFromJNI();
        tv.setText(flagString);
        setContentView(tv);
        Logger.getLogger("flagLogger").info(flagString);
    }

    public native String stringFromJNI();
}
```

Musieli??my te?? zmodyfikowa?? build.gradle dla bibliotek, ??eby uwzgl??dni?? nasze pliki .so:

```
sourceSets {
	main {
		// let gradle pack the shared library into apk
		jniLibs.srcDirs = ['../distribution/gperf/lib', '../distribution/droid/lib']
	}
}
```

I pozosta??o ju?? tylko uruchomi?? aplikacj?? i dosta??:

![](flag.png)

Wi??c flaga to `FLAG{W3_w3r3_Back_70_$3v3n7een!!!}`
