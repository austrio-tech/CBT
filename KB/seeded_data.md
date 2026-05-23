# Seeded Data — Travel KSA

All data below is pre-loaded into Firestore via `FirebaseDataSeeder.java`. Document IDs are the slug keys shown.

---

## Cities

| Doc ID | Name | Region | Lat | Lng |
|---|---|---|---|---|
| `riyadh` | Riyadh | Central | 24.7136 | 46.6753 |
| `jeddah` | Jeddah | Western | 21.5433 | 39.1728 |
| `makkah` | Makkah | Hejaz | 21.3891 | 39.8579 |
| `madinah` | Madinah | Hejaz | 24.5247 | 39.5692 |

---

## Hotels

### Riyadh
| Doc ID | Name | Rating | Phone |
|---|---|---|---|
| `riyadh_four_seasons` | Four Seasons Hotel Riyadh at Kingdom Centre | 4.8 | +966 11 211 5000 |
| `riyadh_ritz_carlton` | The Ritz-Carlton, Riyadh | 4.7 | +966 11 802 8020 |
| `riyadh_mandarin_oriental` | Mandarin Oriental Al Faisaliah, Riyadh | 4.7 | +966 11 273 2000 |
| `riyadh_fairmont` | Fairmont Riyadh | 4.6 | +966 11 249 1000 |
| `riyadh_jw_marriott` | JW Marriott Hotel Riyadh | 4.5 | +966 11 488 7777 |
| `riyadh_hyatt_regency` | Hyatt Regency Riyadh Olaya | 4.4 | +966 11 288 1234 |

### Jeddah
| Doc ID | Name | Rating | Phone |
|---|---|---|---|
| `jeddah_assila` | Assila Hotel, a Luxury Collection Hotel | 4.8 | +966 12 661 8000 |
| `jeddah_park_hyatt` | Park Hyatt Jeddah – Marina and Spa | 4.7 | +966 12 653 1234 |
| `jeddah_intercontinental` | InterContinental Jeddah | 4.6 | +966 12 229 5555 |
| `jeddah_sheraton` | Sheraton Jeddah Hotel | 4.5 | +966 12 699 2212 |
| `jeddah_hilton` | Hilton Jeddah | 4.4 | +966 12 696 9100 |

### Makkah
| Doc ID | Name | Rating | Phone |
|---|---|---|---|
| `makkah_fairmont` | Makkah Clock Royal Tower, A Fairmont Hotel | 4.9 | +966 12 571 7777 |
| `makkah_swissotel` | Swissotel Al Maqam Makkah | 4.7 | +966 12 540 9000 |
| `makkah_raffles` | Raffles Makkah Palace | 4.7 | +966 12 577 3333 |
| `makkah_conrad` | Conrad Makkah | 4.6 | +966 12 570 0555 |
| `makkah_pullman_zamzam` | Pullman ZamZam Makkah | 4.5 | +966 12 547 8000 |

### Madinah
| Doc ID | Name | Rating | Phone |
|---|---|---|---|
| `madinah_dar_al_taqwa` | Dar Al Taqwa Hotel | 4.7 | +966 14 817 7400 |
| `madinah_sofitel` | Sofitel Shahd Al Madinah | 4.6 | +966 14 820 7777 |
| `madinah_pullman_zamzam` | Pullman ZamZam Madinah | 4.6 | +966 14 825 8787 |
| `madinah_movenpick` | Anwar Al Madinah Movenpick Hotel | 4.5 | +966 14 828 5555 |
| `madinah_hilton` | Hilton Madinah | 4.5 | +966 14 835 5700 |

---

## Attractions

### Riyadh
| Doc ID | Name | Rating | Type |
|---|---|---|---|
| `riyadh_at_turaif` | At-Turaif District, Diriyah | 4.9 | historical |
| `riyadh_edge_of_world` | Edge of the World (Jebel Fihrayn) | 4.9 | natural |
| `riyadh_diriyah` | Diriyah Heritage and Culture District | 4.8 | historical |
| `riyadh_al_masmak` | Al Masmak Fortress | 4.7 | historical |
| `riyadh_national_museum` | National Museum of Saudi Arabia | 4.6 | cultural |
| `riyadh_kingdom_centre` | Kingdom Centre Tower Sky Bridge | 4.5 | modern |

### Jeddah
| Doc ID | Name | Rating | Type |
|---|---|---|---|
| `jeddah_al_balad` | Al-Balad Historic District | 4.8 | historical |
| `jeddah_king_fahd_fountain` | King Fahd Fountain | 4.7 | landmark |
| `jeddah_al_rahma_mosque` | Al-Rahma Floating Mosque | 4.7 | religious |
| `jeddah_corniche` | Jeddah Corniche | 4.5 | natural |
| `jeddah_nassif_house` | Nassif House Museum | 4.5 | historical |

### Makkah
| Doc ID | Name | Rating | Type |
|---|---|---|---|
| `makkah_masjid_al_haram` | Masjid Al-Haram (The Grand Mosque) | 5.0 | religious |
| `makkah_jabal_al_nour` | Jabal Al-Nour (Cave of Hira) | 4.8 | religious |
| `makkah_jabal_thawr` | Jabal Thawr (Cave of Thawr) | 4.7 | religious |
| `makkah_abraj_al_bait` | Abraj Al-Bait (Makkah Royal Clock Tower) | 4.6 | modern |
| `makkah_mina` | Mina — City of Tents | 4.5 | religious |

### Madinah
| Doc ID | Name | Rating | Type |
|---|---|---|---|
| `madinah_masjid_nabawi` | Al-Masjid an-Nabawi (Prophet's Mosque) | 5.0 | religious |
| `madinah_quba_mosque` | Quba Mosque | 4.8 | religious |
| `madinah_mount_uhud` | Mount Uhud | 4.7 | historical |
| `madinah_qiblatayn_mosque` | Al-Masjid al-Qiblatayn (Mosque of Two Qiblas) | 4.6 | religious |
| `madinah_al_baqi` | Al-Baqi Cemetery (Jannat Al-Baqi) | 4.5 | religious |

---

## Activities

### Riyadh
| Doc ID | Name | Rating | Hours |
|---|---|---|---|
| `riyadh_desert_safari` | Red Sand Dunes Desert Safari | 4.9 | 7 AM – 9 PM |
| `riyadh_boulevard_city` | Boulevard Riyadh City | 4.8 | 4 PM – 12 AM |
| `riyadh_diriyah_season` | Diriyah Season and Arts Festival | 4.7 | 4 PM – 12 AM |
| `riyadh_kingdom_sky_bridge` | Kingdom Centre Sky Bridge Experience | 4.5 | 9 AM – 12 AM |
| `riyadh_riyadh_zoo` | Riyadh Zoo | 4.2 | 8 AM – 4:30 PM |
| `riyadh_snow_city` | Snow City Riyadh | 4.0 | 10 AM – 12 AM |

### Jeddah
| Doc ID | Name | Rating | Hours |
|---|---|---|---|
| `jeddah_red_sea_diving` | Red Sea Scuba Diving and Snorkelling | 4.9 | 7 AM – 5 PM |
| `jeddah_al_balad_night_tour` | Al-Balad Night Walking Tour | 4.7 | 5 PM – 11 PM |
| `jeddah_al_shallal` | Al-Shallal Theme Park | 4.6 | 3 PM – 12 AM |
| `jeddah_fakieh_aquarium` | Fakieh Aquarium and Dolphin Show | 4.5 | 10 AM – 10 PM |
| `jeddah_corniche_walk` | Jeddah Corniche Sunset and Fountain Walk | 4.5 | 4 PM – 12 AM |

### Makkah
| Doc ID | Name | Rating | Hours |
|---|---|---|---|
| `makkah_kiswa_factory` | Kiswa Factory Tour | 4.6 | 8 AM – 12 PM |
| `makkah_observation_deck` | Abraj Al-Bait Observation Deck | 4.5 | 10 AM – 11 PM |
| `makkah_souq_al_zahed` | Souq Al-Zahed and Traditional Markets | 4.4 | 9 AM – 2 AM |

### Madinah
| Doc ID | Name | Rating | Hours |
|---|---|---|---|
| `madinah_quba_mosque_visit` | Quba Mosque Prayer Visit | 4.8 | 5 AM – 11 PM |
| `madinah_mount_uhud_tour` | Mount Uhud Guided Historical Tour | 4.7 | 7 AM – 6 PM |
| `madinah_date_market` | Madinah Date Market Tour | 4.7 | 8 AM – 10 PM |
| `madinah_hejaz_railway_museum` | Al-Hejaz Railway Museum | 4.5 | 9 AM – 5 PM |

---

## FAQs

| Doc ID | Order | Question |
|---|---|---|
| `faq_what_is` | 1 | What is Travel KSA? |
| `faq_cities` | 2 | Which cities are covered in the app? |
| `faq_ai_chat` | 3 | How does the AI Chat feature work? |
| `faq_makkah` | 4 | Can non-Muslims visit Makkah through the app? |
| `faq_reset` | 5 | How do I reset my password? |
| `faq_free` | 6 | Is Travel KSA free to use? |
