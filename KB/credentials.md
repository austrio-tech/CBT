# Credentials & Configuration — Travel KSA

> ⚠️ This file contains sensitive configuration. Keep it private and do not commit to public repositories.

---

## Admin Panel

| Field | Value |
|---|---|
| Username | `admin` |
| Password | `admin123` |
| Auth method | Local (SharedPreferences — NOT Firebase Auth) |
| Session storage | `SharedPreferences` → key: `is_logged_in` in pref file `admin_session` |

The admin account has no Firebase Auth entry. Credentials are hardcoded in `AdminLoginActivity.java`.

---

## Firebase Project

| Field | Value |
|---|---|
| Project name | `travel-ksa-meta` |
| Project ID | `travel-ksa-meta` |
| Project number | `990685645822` |
| Firebase App ID (Android) | `1:990685645822:android:632f11bcfcf171ab130eaf` |
| Android package | `com.example.travelaks` |
| Web API Key | `AIzaSyB_VWvxChPfcz4DAY-TAL7Ocj7jKDj5OVs` |
| Firestore region | `europe-west1` |
| Config file | `app/google-services.json` |

---

## Firebase Authentication

- **Provider enabled:** Email/Password
- **Regular user accounts:** Created via Sign Up screen using Firebase Auth
- **Admin account:** Does NOT use Firebase Auth (local credentials only)

### How to create an admin Firebase account (optional)
If you want to give admin role to a regular Firebase Auth user:
1. That user signs up normally via the app
2. Go to Firebase Console → Firestore → `users` collection → find their UID document
3. Edit the `role` field from `"user"` to `"admin"`

---

## OpenAI API

| Field | Value |
|---|---|
| API Key | Stored in `gradle.properties` as `OPENAI_API_KEY` |
| Model used | `gpt-3.5-turbo` |
| Endpoint | `https://api.openai.com/v1/chat/completions` |
| Usage | AI Chat feature — one call per user message |

> The API key is injected at build time via `buildConfigField` in `app/build.gradle.kts` and accessed at runtime as `BuildConfig.OPENAI_API_KEY`.

---

## google-services.json (Location)

File path: `app/google-services.json`

This file was generated from the Firebase Console and contains the Firebase SDK configuration. It links the Android app to the `travel-ksa-meta` Firebase project. Do not modify manually.

---

## Data Seeder

The `FirebaseDataSeeder.java` class seeds all content (cities, hotels, attractions, activities, FAQs) into Firestore. It is triggered from the Admin Dashboard via the **"Seed Firebase Data"** button.

- Uses named document IDs → **idempotent** (safe to re-run, overwrites existing data without duplicates)
- Does NOT seed the `users` collection (users are created on signup)
- Does NOT require any special permissions beyond normal Firestore write access
