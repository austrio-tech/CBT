# Database Structure — Travel KSA

**Database:** Google Cloud Firestore (Firebase)
**Project ID:** `travel-ksa-meta`
**Mode:** Production (custom security rules — see below)

---

## Collections Overview

| Collection | Documents | Purpose |
|---|---|---|
| `users` | One per registered user | User profiles and roles |
| `cities` | 4 | City descriptions and coordinates |
| `hotels` | 21 | Hotel listings per city |
| `attractions` | 21 | Tourist attractions per city |
| `activities` | 18 | Activities/events per city |
| `faqs` | 6 | Help desk FAQ entries |
| `chatSessions` | One per AI chat session | AI chat history per user per city |

---

## Collection: `users`

Created automatically when a user signs up via the app.
Document ID = Firebase Auth UID.

```
users/
  {uid}/
    email:        string     — user's email address
    createdAt:    timestamp  — when the account was created
    lastLoginAt:  timestamp  — updated on every login
    role:         string     — "user" | "admin"
```

**Notes:**
- Passwords are NEVER stored here — handled entirely by Firebase Auth
- Admin role must be set manually in Firestore Console or via Admin manage screen
- `role = "admin"` grants access to the Admin Dashboard

---

## Collection: `cities`

Document IDs are fixed: `riyadh`, `jeddah`, `makkah`, `madinah`

```
cities/
  {cityId}/
    name:         string   — "Riyadh" | "Jeddah" | "Makkah" | "Madinah"
    description:  string   — full city description (shown on city detail screen)
    imageUrl:     string   — drawable resource name (e.g. "riyadh", "jeddh", "makkah", "almadina")
    country:      string   — "Saudi Arabia"
    region:       string   — "Central" | "Western" | "Hejaz"
    latitude:     number   — city center GPS latitude
    longitude:    number   — city center GPS longitude
```

**City coordinates:**
| City | Latitude | Longitude |
|---|---|---|
| Riyadh | 24.7136 | 46.6753 |
| Jeddah | 21.5433 | 39.1728 |
| Makkah | 21.3891 | 39.8579 |
| Madinah | 24.5247 | 39.5692 |

---

## Collection: `hotels`

Document IDs are named slugs (e.g. `riyadh_four_seasons`, `jeddah_assila`).

```
hotels/
  {hotelId}/
    name:          string   — hotel full name
    cityId:        string   — parent city ID (e.g. "riyadh")
    city:          string   — city name used for filtering (e.g. "Riyadh")
    rating:        number   — rating out of 5 (e.g. 4.8)
    category:      string   — hotel tier (e.g. "5-Star Luxury")
    phone:         string   — international phone number
    description:   string   — full hotel description
    imageUrl:      string   — drawable resource name (e.g. "ritz_carlton", "four_seasons")
    pricePerNight: number   — approximate price in SAR
    latitude:      number   — hotel GPS latitude
    longitude:     number   — hotel GPS longitude
```

**Query used in app:** `.whereEqualTo("city", cityName)` → sorted by `rating` descending client-side

---

## Collection: `attractions`

Document IDs are named slugs (e.g. `riyadh_at_turaif`, `jeddah_al_balad`).

```
attractions/
  {attractionId}/
    name:         string   — attraction full name
    cityId:       string   — parent city ID
    city:         string   — city name for filtering
    rating:       number   — rating out of 5
    category:     string   — e.g. "UNESCO World Heritage Site", "Historic Fortress"
    description:  string   — full description
    imageUrl:     string   — drawable resource name
    type:         string   — "historical" | "cultural" | "natural" | "religious" | "modern" | "landmark"
    latitude:     number   — GPS latitude
    longitude:    number   — GPS longitude
```

**Query used in app:** `.whereEqualTo("city", cityName)` → sorted by `rating` descending client-side

---

## Collection: `activities`

Document IDs are named slugs (e.g. `riyadh_boulevard_city`, `jeddah_red_sea_diving`).

```
activities/
  {activityId}/
    name:         string   — activity name
    cityId:       string   — parent city ID
    city:         string   — city name for filtering
    rating:       number   — rating out of 5
    category:     string   — e.g. "Outdoor Adventure", "Theme Park"
    description:  string   — full description
    imageUrl:     string   — drawable resource name
    openTime:     string   — opening time (e.g. "4 PM")
    closeTime:    string   — closing time (e.g. "12 AM")
    location:     string   — human-readable address/area
    latitude:     number   — GPS latitude
    longitude:    number   — GPS longitude
```

**Query used in app:** `.whereEqualTo("city", cityName)` → sorted by `rating` descending client-side

---

## Collection: `faqs`

Document IDs are named slugs (e.g. `faq_what_is`, `faq_cities`).

```
faqs/
  {faqId}/
    question:   string    — the FAQ question
    answer:     string    — the full answer
    order:      number    — display order (1 = first)
    isVisible:  boolean   — true = shown to users, false = hidden
```

**Query used in app:** `.orderBy("order")` → hidden FAQs filtered client-side (`isVisible == false` skipped)

---

## Collection: `chatSessions`

Auto-generated document IDs.

```
chatSessions/
  {sessionId}/
    userId:     string      — Firebase Auth UID of the user
    city:       string      — city context (e.g. "Riyadh")
    startedAt:  timestamp   — when the session started

    messages/               ← sub-collection
      {messageId}/
        text:       string      — message content
        isUser:     boolean     — true = sent by user, false = AI response
        timestamp:  timestamp   — when the message was sent
```

---

## Firestore Security Rules

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // Content — open read/write (admin manages without Firebase Auth)
    match /cities/{id}      { allow read, write: if true; }
    match /hotels/{id}      { allow read, write: if true; }
    match /attractions/{id} { allow read, write: if true; }
    match /activities/{id}  { allow read, write: if true; }
    match /faqs/{id}        { allow read, write: if true; }

    // Users — open read (admin dashboard counts), write restricted to owner
    match /users/{userId} {
      allow read: if true;
      allow write: if request.auth != null && request.auth.uid == userId;
    }

    // Chat sessions — authenticated users only
    match /chatSessions/{sessionId} {
      allow read, write: if request.auth != null;
      match /messages/{msgId} {
        allow read, write: if request.auth != null;
      }
    }
  }
}
```

---

## Data Relationships

```
cities (4 docs)
  └── hotels    — linked via hotel.cityId + hotel.city
  └── attractions — linked via attraction.cityId + attraction.city
  └── activities  — linked via activity.cityId + activity.city

users (N docs)
  └── chatSessions — linked via chatSession.userId
        └── messages (sub-collection)
```
