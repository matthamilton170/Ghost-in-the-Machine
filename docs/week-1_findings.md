# Week 1: Building the logger and first look at the data

## Goal
To build a privacy-focused data collection pipeline.

## Design and privacy decisions
Only timing is measured, not the identity of keys pressed. All information is stored on the device. Cursor coordinates are recorded, though this will likely maintain privacy as what is on screen is not known and the information is required for mouse speed features.

## Data collected
Over the course of one day (around 7.7 hours), around 18,000 events, with 20ms mouse sampling.

## What I observed
Long idle gaps, particularly for key presses. There was an evening burst between 7pm and 9pm in which 654 of the 733 key presses occured. 

## Problems I hit and fixed
Over the first day of testing I found that the logger had run twice for the entire day, corrupting the data, so I implemented a lock system to prevent this in the future. This was diagnosed by a duplicate header.

## Limitations
The data collected this week is largely to show that this works. The data is from one person, on one day, with relatively little activity. Stress labels are not yet implemented and idle time can be ambiguous.

## Next steps
Self-report prompts, windowed features, baselines.