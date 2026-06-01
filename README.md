# TerraTrack Off-Grid Scout

## Project Overview

TerraTrack is a solar-powered, fully offline environmental tracking device designed for use in remote areas without internet connectivity.

The system records:

* GPS location data
* Temperature
* Humidity
* Time-stamped journey logs

After a trip, the collected data can be converted into a map visualisation, allowing users to review both their route and the environmental conditions experienced along the way.

I was inspired to create TerraTrack because my father frequently hikes in remote mountainous regions where internet connectivity is unavailable. I wanted to better understand not only the routes he travelled but also the environmental conditions and physical challenges he encountered during these journeys.

The project combines embedded systems, environmental sensing, renewable energy, data processing and product design into a single integrated solution.

---

## Design Objectives

The project was designed to satisfy four key requirements:

* Operate entirely without internet access
* Record location and environmental data continuously
* Function using renewable energy
* Allow post-trip visualisation of collected data

Unlike smartphone tracking applications, TerraTrack remains functional in remote locations where mobile networks are unavailable.

---

## System Architecture

The device consists of several interconnected hardware and software subsystems.

### Core Processing Unit

The system is built around a Raspberry Pi Pico 2 microcontroller.

Responsibilities include:

* Reading sensor data
* Processing GPS information
* Managing user inputs
* Displaying information on screen
* Logging data to storage

The Pico was selected due to its low power consumption, reliability and compatibility with MicroPython.

---

## GPS Tracking System

### Neo-8M GPS Module

The GPS subsystem provides:

* Real-time location tracking
* Latitude and longitude coordinates
* Journey recording
* Route reconstruction

The GPS continuously receives satellite signals and transmits coordinate data to the microcontroller.

This allows TerraTrack to operate completely offline without relying on mobile networks or cloud services.

---

## Environmental Monitoring System

### BME280 Environmental Sensor

The environmental sensing subsystem records:

* Temperature
* Humidity
* Atmospheric pressure

Environmental data is captured alongside GPS coordinates, creating a detailed record of conditions experienced at specific locations throughout a journey.

This transforms TerraTrack from a simple GPS logger into an environmental data collection platform.

---

## User Interface System

### 20 × 4 LCD Display

The LCD display provides live feedback to the user.

Displayed information includes:

* GPS coordinates
* Temperature
* Humidity
* Device status
* Logging status

The display allows the device to operate independently without requiring a smartphone or computer connection.

### Physical Button Controls

Three dedicated buttons were implemented:

#### Live Data Button

Displays current sensor readings and GPS information.

#### Logging Button

Records the current location and environmental data into the onboard data log.

#### Reset Button

Allows recovery from unexpected software or hardware faults during operation.

This simple interface was intentionally designed for reliability in outdoor environments.

---

## Solar Power System

### Renewable Energy Design

TerraTrack is powered using a solar energy subsystem consisting of:

* Solar panels
* Solar charging module
* Power regulation circuitry

The solar subsystem provides energy for extended outdoor operation and reduces dependence on conventional charging methods.

### Engineering Challenge

One of the most difficult aspects of the project was ensuring stable power delivery from the solar panel.

Solar energy output varies based on:

* Sunlight intensity
* Weather conditions
* Panel orientation

Careful testing was required to ensure reliable operation despite these fluctuations.

---

## Embedded Software Development

### MicroPython Programming

The firmware was developed using MicroPython.

Key software functions include:

* GPS communication
* Environmental sensor interfacing
* LCD display control
* Button handling
* Data logging
* Error recovery routines

The program continuously coordinates data acquisition from multiple hardware systems while maintaining responsive user interaction.

### Data Logging System

Each recorded entry contains:

* Timestamp
* GPS coordinates
* Temperature
* Humidity
* Pressure readings

Data is stored in CSV format for later processing.

This required designing a structured logging format that could be interpreted by external software tools.

---

## Data Processing and Visualisation

### Python Data Pipeline

To make the collected data useful after a journey, I developed a separate Python application.

The software:

1. Reads the CSV log files.
2. Processes location and environmental data.
3. Converts the information into KML format.
4. Generates files compatible with mapping software.

### Map Visualisation

The KML files can be uploaded to Google Maps or Google Earth, allowing users to:

* View the complete route travelled
* Examine environmental conditions at specific points
* Analyse journey statistics

### Route Reconstruction

For journeys occurring on established roads or trails, I integrated mapping APIs to generate route visualisations that better represent the actual path travelled.

This required learning how to work with APIs and process geographic data programmatically.

---

## Product Design Process

### Iterative Prototyping

I followed an iterative engineering design process.

#### Phase 1 – Breadboard Prototype

All components were first tested on a breadboard to verify:

* Sensor communication
* Power requirements
* Software functionality
* System integration

This allowed problems to be identified before committing to permanent hardware.

#### Phase 2 – Perfboard Assembly

Once validated, the circuit was transferred to a perfboard.

Benefits included:

* Increased reliability
* Improved durability
* Reduced wiring complexity
* Better portability

---

## CAD Design and Manufacturing

### Fusion 360 Enclosure Design

To transform the electronics into a usable field device, I designed a custom enclosure using Fusion 360.

Design goals included:

* Compact size
* Structural durability
* Accessibility of controls
* Effective component organisation

### 3D Printing

The enclosure was manufactured using a 3D printer.

### Design Iterations

The enclosure underwent four complete redesigns before the final version was achieved.

Each iteration improved:

* Internal component fit
* Cable management
* Structural strength
* Ease of assembly

This process taught me the importance of iterative product development and user-centred design.

---

## Engineering Challenges

### Hardware Integration

Integrating multiple subsystems proved challenging.

The project required reliable communication between:

* GPS module
* Environmental sensor
* LCD display
* User inputs
* Power management circuitry

Debugging interactions between these systems required extensive testing.

### Soldering and Reliability

Many connections had to be rebuilt multiple times to achieve consistent operation.

The LCD display alone required five separate soldering attempts before a stable connection was achieved.

This taught me the importance of:

* Quality solder joints
* Systematic debugging
* Hardware reliability testing

### Power Management

Maintaining stable operation from solar power required careful testing and optimisation of the power delivery system.

---

## Future Improvements

Potential future developments include:

* Rechargeable battery energy storage system
* Improved power efficiency
* Enhanced graphical user interface
* Additional environmental sensors
* Altitude tracking
* Advanced route analytics
* Richer map-based visualisations

---

## Technical Skills Demonstrated

### Hardware Engineering

* Soldering and circuit assembly
* Microcontroller integration
* GPS systems
* Environmental sensing
* LCD interfacing
* Power management
* Solar energy systems

### Software Engineering

* MicroPython programming
* Embedded systems development
* Sensor communication protocols
* Data logging systems
* Python programming
* CSV data processing
* KML generation
* API integration

### Design and Manufacturing

* Engineering design process
* Rapid prototyping
* Fusion 360 CAD design
* 3D printing
* Product iteration
* Systems integration

### Problem-Solving

* Hardware debugging
* Reliability testing
* Power optimisation
* Mechanical packaging
* Multi-system integration

---

## Key Learning Outcomes

Through TerraTrack, I gained experience developing a complete engineering product from concept to deployment.

The project required me to integrate electronics, embedded software, renewable energy systems, CAD design and data visualisation into a single working device. Most importantly, it taught me the value of iterative design, persistence in troubleshooting and designing technology around a real-world user need.
