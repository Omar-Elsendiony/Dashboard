# Smart Home Database Wiki

## Overview

The Smart Home Database supports home management functionalities, user profiles, room assignments, device operations, automated routines, energy consumption tracking, emergency alerts, and user feedback. The database interacts exclusively through provided APIs, ensuring secure and structured data management.

## Database Schema

### Homes

Stores primary information about homes.

* **Fields:** home\_id, owner\_id, address\_id, home\_type, created\_at, updated\_at

### Users

Maintains user profiles.

* **Fields:** user\_id, first\_name, last\_name, phone\_number, role, parent\_id, email, primary\_address\_id, date\_of\_birth, status, created\_at, updated\_at

### Rooms

Details individual rooms within homes.

* **Fields:** room\_id, home\_id, room\_type, room\_owner\_id, status, width\_ft, length\_ft, created\_at, updated\_at

### Devices

Tracks smart home devices.

* **Fields:** device\_id, device\_type, room\_id, installed\_on, insurance\_expiry\_date, home\_id, status, width\_ft, length\_ft, price, scheduled\_maintainance\_date, last\_maintainance\_date, daily\_rated\_power\_consumption\_kWh, created\_at, updated\_at

### Historical Energy Consumption

Records historical energy usage.

* **Fields:** consumption\_id, device\_id, home\_id, room\_id, date, power\_used\_kWh, created\_at, updated\_at

### Automated Routines

Manages scheduled device operations.

* **Fields:** routine\_id, user\_id, home\_id, start\_action\_date, action\_time, action\_interval, created\_at, updated\_at

### Device Commands

Commands assigned to devices via routines.

* **Fields:** device\_command\_id, routine\_id, device\_id, status, created\_at, updated\_at

### Specialized Device Commands

* **Bulb Commands:** bulb\_command\_id, routine\_id, device\_id, brightness\_level, color, created\_at, updated\_at
* **Thermostat Commands:** thermostat\_command\_id, routine\_id, device\_id, current\_temperature, created\_at, updated\_at

### Specialized Devices

* **Security Cameras:** device\_id, resolution, last\_activity\_timestamp, created\_at, updated\_at
* **Smart Thermostats:** device\_id, current\_temperate, lowest\_rated\_temperature, highest\_rated\_temperature, last\_adjustment\_time, created\_at, updated\_at
* **Smart Bulbs:** device\_id, brightness\_level, color, created\_at, updated\_at

### User Feedbacks

Captures feedback on devices.

* **Fields:** user\_feedback\_id, user\_id, device\_id, rating, created\_at, updated\_at

### Addresses

Details address information.

* **Fields:** address\_id, house\_number, building\_name, street, city\_name, state, created\_at, updated\_at

### Emergency Alerts

Logs device-related emergencies.

* **Fields:** alert\_id, home\_id, device\_id, alert\_type, severity\_level, triggered\_at, acknowledged\_at, acknowledged\_by\_user, resolved\_at, resolved\_by\_user, created\_at

### Energy Tariffs

Defines energy billing rates.

* **Fields:** tariff\_id, home\_id, tariff\_name, rate\_per\_kWh, peak\_hours\_start, peak\_hours\_end, peak\_rate\_multiplier, effective\_from, effective\_until, created\_at, updated\_at

## API Interactions

APIs provided are the exclusive means for the agent to interact with the database, managing users, homes, rooms, devices, alerts, energy consumption, routines, commands, tariffs, and feedback.

### Key API Categories

* **User Management:** Create and update user profiles.
* **Home Management:** Add/update home details and addresses.
* **Room Management:** Manage room assignments and statuses.
* **Device Management:** Add/update devices and associated records.
* **Routine & Command Management:** Schedule and execute automated device actions.
* **Energy Management:** Log consumption and manage tariffs.
* **Emergency Management:** Handle creation and updates of alerts.
* **Feedback Management:** Collect and analyze device feedback.

## Smart Home Agent Policy

### General Guidelines

* Operate exclusively through APIs.
* Obtain explicit user-provided information for every database interaction.

### Authentication & Permissions

* Always authenticate user identity before performing actions.
* Verify user permissions through provided APIs.

### Home & Room Management

* Only home owners can create/update homes and rooms.
* Verify ownership explicitly before making changes.

### Device Management

* Only the home or room owner can add/update devices.
* Confirm device location and user permissions via API.
* Validate device details to avoid duplicates.

### Automated Routine Management

* Confirm user's association with home before creating routines.
* Verify no scheduling conflicts exist through APIs.

### Energy Management

* Always obtain explicit user confirmation before accessing historical consumption data.
* Retrieve accurate tariff information proactively for estimations.

### Emergency Alerts Management

* Confirm device association and user identity explicitly before alert creation or updates.
* Update alert status only after confirming active alerts.

### User Feedback

* Validate user's association with the device explicitly before feedback submission.

### Data Integrity & Security

* Validate data explicitly through APIs.
* Adhere strictly to privacy standards and user consent.

