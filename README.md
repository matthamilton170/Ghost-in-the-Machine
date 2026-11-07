# Ghost-in-the-Machine
A project to detect user stress and respond in the background
The keystrokes detected will record timestamps and event types, never which key.
Mouse movements track x and y coordinates and timestamp every 20ms - SUBJECT TO CHANGE
Single-Instance lock protects from multiple usage
Key Presses will always outnumber key releases as no way to find duplicate presses

## First results

![Key presses per minute over one day](docs/activity_overview.png)

*Key presses, mouse clicks, and mouse distance moved (in screen pixels, which depends on display resolution and scaling) per minute across a ~8-hour session (6 Nov 2026, Eastern time). Activity is bursty: most of the day containes little keyboard or mouse input, with typing especially having a concentrated burst in the evening. Counts include held-key auto-repeat for key presses, and this plot shows activity only, not stress.*
