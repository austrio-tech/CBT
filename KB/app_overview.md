# App Overview — Travel KSA

## What is Travel KSA?

Travel KSA is an **AI-powered Android travel guide** for the Kingdom of Saudi Arabia. It helps users explore four major Saudi cities — Riyadh, Jeddah, Makkah, and Madinah — by providing real hotel listings, tourist attractions, activities, and an integrated AI chat assistant powered by OpenAI GPT-3.5.

The app has two distinct user types:
- **Regular users** — sign up/login via Firebase Auth to browse travel content
- **Admin** — logs in with local credentials to manage all content via a full CRUD dashboard

---

## Key Features

### For Users
1. **City Explorer** — Browse 4 Saudi cities from a card-based city selection screen
2. **City Details** — Each city shows a description (loaded from Firestore) and 3 section buttons: Attractions, Hotels, Activities
3. **Hotels** — Real hotel listings per city with name, rating, category, phone, description, and a Google Maps button
4. **Attractions** — Tourist attraction listings per city with category, rating, description, and a Google Maps button
5. **Activities** — Activity/event listings per city with open/close times, location, and a Google Maps button
6. **AI Chat** — Context-aware chat assistant per city (powered by OpenAI GPT-3.5-turbo). Chat history is persisted to Firestore
7. **FAQ / Help Desk** — Expandable FAQ loaded from Firestore
8. **User Authentication** — Firebase Email/Password sign up, login, and password reset
9. **Session Management** — Logged-in users skip the login screens; splash screen routes automatically
10. **Logout** — Available from the Cities screen (main user hub)

### For Admin
1. **Admin Dashboard** — Shows live counts for all 6 data collections in colored stat cards
2. **Navigation Drawer** — Access all manage sections + logout from a slide-in drawer
3. **Manage Users** — View all users, change their role (user/admin), delete Firestore records
4. **Manage Cities** — Full CRUD for city documents
5. **Manage Hotels** — Full CRUD for hotel documents
6. **Manage Attractions** — Full CRUD for attraction documents
7. **Manage Activities** — Full CRUD for activity documents
8. **Manage FAQs** — Full CRUD for FAQ documents including visibility toggle
9. **Seed Firebase Data** — One-tap seeder that populates all collections with real-world KSA data
10. **Admin Session Management** — Admin login state persisted via SharedPreferences; auto-routes if already logged in

---

## User Flow

```
App Launch (Splash, 3 seconds)
    │
    ├── [User logged in via Firebase Auth] ──► Cities screen
    │
    └── [Not logged in] ──► Home screen
            │
            ├── Login ──► Cities screen
            ├── Sign Up ──► Cities screen
            ├── FAQ ──► Help Desk
            └── Admin ──► Admin Login
                            │
                            └── [admin/admin123] ──► Admin Dashboard
```

---

## Cities Covered

| City | Region | Significance |
|---|---|---|
| Riyadh | Central | Capital city, political & financial hub |
| Jeddah | Western | Red Sea coast, UNESCO Al-Balad |
| Makkah | Hejaz | Holiest city in Islam (Muslims only) |
| Madinah | Hejaz | Second holiest city, Prophet's Mosque |

---

## Content Summary

| Collection | Count |
|---|---|
| Cities | 4 |
| Hotels | 21 (5–6 per city) |
| Attractions | 21 (5 per city) |
| Activities | 18 (3–6 per city) |
| FAQs | 6 |
| Users | Created on signup |
| Chat Sessions | Created on each AI chat |
