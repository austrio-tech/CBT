# Technical Stack — Travel KSA

## Platform
- **OS:** Android
- **Language:** Java 11
- **Min SDK:** 24 (Android 7.0 Nougat)
- **Target SDK:** 36
- **Compile SDK:** 36 (release)
- **Build system:** Gradle 8.13.2 (Kotlin DSL)
- **Package name:** `com.example.travelaks`

---

## Key Dependencies

| Library | Version | Purpose |
|---|---|---|
| Firebase BOM | 33.7.0 | Firebase SDK version management |
| Firebase Auth | (BOM-managed) | Email/Password user authentication |
| Cloud Firestore | (BOM-managed) | NoSQL database for all app content |
| OkHttp3 | 4.9.3 | HTTP client for OpenAI API calls |
| AndroidX AppCompat | 1.7.1 | Backward-compatible UI components |
| Material Components | 1.13.0 | Material Design UI widgets |
| AndroidX Activity | 1.12.4 | Activity result APIs |
| ConstraintLayout | 2.2.1 | Flexible layout system |
| Google Services plugin | 4.4.2 | Processes `google-services.json` |

---

## Architecture

```
app/
├── src/main/java/com/example/travelaks/
│   ├── data/model/          ← Firestore POJO classes
│   │   ├── User.java
│   │   ├── City.java
│   │   ├── Hotel.java
│   │   ├── Attraction.java
│   │   ├── ActivityItem.java
│   │   ├── ChatSession.java
│   │   ├── Faq.java
│   │   └── Message.java
│   │
│   ├── [Activities]         ← One Activity per screen
│   ├── [Adapters]           ← RecyclerView adapters
│   │   ├── HotelAdapter.java
│   │   ├── AttractionAdapter.java
│   │   ├── ActivityAdapter.java
│   │   └── ChatAdapter.java
│   │
│   └── FirebaseDataSeeder.java  ← Content seeder
│
├── src/main/res/
│   ├── layout/              ← XML layouts (one per screen + item layouts)
│   ├── drawable/            ← Background images, vector icons, button shapes
│   ├── values/              ← colors.xml, strings.xml, themes.xml
│   ├── values-night/        ← Overrides night theme to force light mode
│   └── menu/                ← admin_drawer_menu.xml
│
└── google-services.json     ← Firebase SDK configuration
```

---

## Build Configuration

**`app/build.gradle.kts`** key settings:
```kotlin
applicationId = "com.example.travelaks"
minSdk = 24
targetSdk = 36
versionCode = 1
versionName = "1.0"
buildConfigField("String", "OPENAI_API_KEY", "\"${project.findProperty("OPENAI_API_KEY")}\"")
```

**OpenAI API key** is stored in `gradle.properties` (not committed to version control):
```
OPENAI_API_KEY=sk-...
```

---

## Build Output Location

Due to OneDrive sync conflicts, the Gradle build directory is redirected via a **directory junction**:

```
app\build  →  C:\AndroidBuilds\TravelSKA\app\  (junction, physically outside OneDrive)
```

This means:
- Android Studio finds artifacts at `app\build\` as expected
- Actual files are written to `C:\AndroidBuilds\TravelSKA\app\` outside OneDrive
- APK location: `C:\AndroidBuilds\TravelSKA\app\outputs\apk\debug\app-debug.apk`

**To build from terminal:**
```powershell
$env:JAVA_HOME = "C:\Program Files\Android\Android Studio2\jbr"
# Stop OneDrive first to prevent file locks
Stop-Process -Name "OneDrive" -Force -ErrorAction SilentlyContinue
.\gradlew.bat assembleDebug
```

---

## Theme

- **Base theme:** `Theme.Material3.Light.NoActionBar` (forced light — no dark mode)
- **Night theme override:** `values-night/themes.xml` also uses Light to prevent dark mode inversions
- **Primary color (admin):** `#1A3C6E` (deep navy)
- **Tourist accent (user):** `#0077B6` (ocean blue)
- All user-facing toolbars and buttons use tourist blue
- All admin screens use admin navy

---

## Session Management

**User session (Firebase Auth):**
- Firebase Auth SDK persists the session automatically
- Splash screen checks `FirebaseAuth.getInstance().getCurrentUser()`
- Login and Sign Up check current user on start and skip if already signed in
- Logout calls `FirebaseAuth.getInstance().signOut()`

**Admin session (SharedPreferences):**
- Stored in `SharedPreferences` file named `admin_session`
- Key: `is_logged_in` (boolean)
- Set to `true` on successful admin login
- Set to `false` on logout
- Checked in `AdminLoginActivity.onCreate()` to auto-route to Dashboard

---

## Google Maps Integration

Hotels, attractions, and activities each have an **"Open in Google Maps"** button.

Implementation — opens a URL in the default browser or Maps app:
```java
String url = "https://www.google.com/maps/search/?api=1&query=" + lat + "," + lng;
context.startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url)));
```

No special Maps SDK or API key required — uses the web URL approach.
