# Screens & Navigation — Travel KSA

## Screen List

### 1. Splash (`Splash.java`)
- **Layout:** `activity_splash.xml`
- **Shows:** Logo + progress indicator for 3 seconds
- **Routing:** If Firebase Auth user is signed in → Cities; else → Home

### 2. Home (`HomeActivity.java`)
- **Layout:** `activity_home.xml`
- **Shows:** Travel KSA logo (200dp), app name, 4 buttons
- **Buttons:** Login → LoginActivity | Sign Up → SignUpActivity | FAQ → HelpDeskActivity | Admin → AdminLoginActivity

### 3. Login (`LoginActivity.java`)
- **Layout:** `activity_login.xml`
- **Shows:** Logo (200dp), "Welcome Back", email + password fields, Forgot Password link, Continue button
- **Session guard:** If already logged in → skips to Cities
- **On success:** Navigates to Cities, updates `lastLoginAt` in Firestore

### 4. Sign Up (`SignUpActivity.java`)
- **Layout:** `activity_signup.xml`
- **Shows:** Logo (200dp), "Create Account", email + password fields
- **Session guard:** If already logged in → skips to Cities
- **On success:** Creates Firebase Auth account + writes `users/{uid}` doc in Firestore → navigates to Cities

### 5. Forgot Password (`Forgetpass.java`)
- **Layout:** `activity_forgetpass.xml`
- **Shows:** "Reset Password", email input, "Send Reset Link" button
- **Action:** Calls `FirebaseAuth.sendPasswordResetEmail(email)`

### 6. Cities / City Selection (`Cites.java`)
- **Layout:** `activity_cites.xml`
- **Shows:** Header with "Explore Saudi Arabia" + Logout button, SearchView, 4 city cards (Riyadh, Jeddah, Makkah, Madinah)
- **Search:** Live filter — typing hides non-matching city cards
- **Each card:** White card with city image, name, subtitle → tapping opens City Details

### 7. City Detail Pages (4 screens)
- `RiyadhDetailsActivity`, `JeddahDetailsActivity`, `MakkahDetailsActivity`, `MadinahDetailsActivity`
- **Layout:** `activity_riyadh_details.xml` (and equivalent for other cities)
- **Shows:** Tourist-blue toolbar with back arrow + city name, description card (from Firestore), 3 section buttons (Attractions ›, Hotels ›, Activities ›), Ask AI button
- **Description:** Loaded dynamically from `cities/{cityId}` in Firestore

### 8. Hotels (`activity_hotel_riyadh.java`)
- **Layout:** `activity_hotel_riyadh.xml`
- **Shows:** Toolbar with "Hotels in {City}", RecyclerView of hotel cards
- **Each card:** Hotel image, name, phone, rating/category, description, **"📍 Open in Google Maps"** button
- **Data:** Filtered from `hotels` collection by `city` field, sorted by `rating` descending client-side
- **Accepts:** `CITY_NAME` Intent extra — works for all 4 cities

### 9. Attractions (`Tourist_Attractions_Riyadh.java`)
- **Layout:** `activity_tourist_attractions_riyadh.xml`
- **Shows:** Toolbar with "Attractions in {City}", RecyclerView of attraction cards
- **Each card:** Image, name, category+rating, description, **"📍 Open in Google Maps"** button
- **Accepts:** `CITY_NAME` Intent extra

### 10. Activities (`activity_activitiess_riyadh.java`)
- **Layout:** `activity_activitiess_riyadh.xml`
- **Shows:** Toolbar with "Activities in {City}", RecyclerView of activity cards
- **Each card:** Image, name, rating/category, hours (🕐), description, location (📍), **"📍 Open in Google Maps"** button
- **Accepts:** `CITY_NAME` Intent extra

### 11. AI Chat (`AiChatActivity.java`)
- **Layout:** `chat_box_layout.xml`
- **Shows:** Tourist-blue title bar with back arrow + city name, chat message RecyclerView, text input + Send button
- **AI:** Calls OpenAI GPT-3.5-turbo API with city context
- **Persistence:** Creates a `chatSessions` document in Firestore; each message saved to `chatSessions/{id}/messages`
- **Accepts:** `city_name` Intent extra

### 12. Help Desk / FAQ (`HelpDeskActivity.java`)
- **Layout:** `activity_help_desk.xml`
- **Shows:** FAQ title bar, RecyclerView of expandable FAQ cards (tap to expand/collapse)
- **Data:** Loaded from `faqs` collection ordered by `order` field; hidden FAQs filtered client-side

---

## Admin Screens

### 13. Admin Login (`AdminLoginActivity.java`)
- **Layout:** `activity_admin_login.xml`
- **Credentials:** username `admin`, password `admin123` (local, NOT Firebase Auth)
- **Session guard:** If already logged in (SharedPreferences) → skips to Dashboard
- **On success:** Saves `is_logged_in=true` to SharedPreferences `admin_session` → goes to Dashboard

### 14. Admin Dashboard (`AdminDashboardActivity.java`)
- **Layout:** `activity_admin_dashboard.xml`
- **Shows:** Tourist-navy toolbar with hamburger menu, greeting banner, 6 stat cards (Users, Cities, Hotels, Attractions, Activities, FAQs), Logout button
- **Stat cards:** Each shows live count from Firestore, colored background, tappable to open manage screen
- **Drawer:** Navigation drawer with links to all manage screens + Logout

### 15–20. Admin Manage Screens (6 screens)
- `AdminManageUsersActivity` / `AdminManageCitiesActivity` / `AdminManageHotelsActivity`
- `AdminManageAttractionsActivity` / `AdminManageActivitiesActivity` / `AdminManageFaqsActivity`
- **Layout:** Shared `activity_admin_manage.xml` (Toolbar + RecyclerView + FAB)
- **Each row:** Title, subtitle, Edit (✏) button, Delete (🗑) button
- **FAB (+):** Opens Add dialog with all fields
- **Edit:** Opens pre-filled Edit dialog
- **Delete:** Confirmation dialog → deletes Firestore document

---

## Back Navigation Summary

| Screen type | Back button location |
|---|---|
| Hotels / Attractions / Activities | ← in toolbar (top-left) |
| City detail pages | ← in toolbar (top-left) |
| AI Chat | ← in title bar (top-left) |
| Login / Sign Up / Forgot Password | ← transparent button, top-left corner |
| Admin screens | ← in toolbar (top-left) via theme |
