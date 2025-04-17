# Time Banking & Review System Specification

## Purpose
Let users trade hours of their life (not money), book appointments, and review experiences—ethically, transparently, and with geolocation.

## Features
* Users can offer/request services in exchange for hours
* Booking calendar and scheduling
* Geolocation for local offers/requests
* Review system for both workers and hirers
* Time ledger to track hours given/received
* No monetary exchange, no exploitative ranking
* All data is user-owned and exportable

## API & Data Model
* `User`, `Offer`, `Request`, `Booking`, `Review`, `TimeLedger`
* `/work/offers` (CRUD)
* `/work/requests` (CRUD)
* `/work/bookings` (create, update, cancel)
* `/work/reviews` (write, read, moderate)
* `/work/ledger` (track hours)

## UI/UX Notes
* Map view for geolocated offers/requests
* Booking calendar with availability
* Review UI with star rating, text, privacy controls
* Emphasis on constructive, ethical feedback

## Security/Ethics
* No monetary transactions
* Reviews are moderated for fairness and respect
* All participation is opt-in and privacy-respecting

## Example User Flow
1. User posts an offer (e.g., gardening for 2 hours)
2. Another user books the offer, selects a time slot
3. After completion, both users leave a review
4. Hours are logged in each user’s time ledger

---
*End of Time Banking & Review System Spec*