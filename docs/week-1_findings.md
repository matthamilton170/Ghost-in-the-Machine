# Week 1: Building the logger and first look at the data

## Goal
Goal is to build an application which uses multiple measurements to track stress, and acts on those measurements to make active background adjustements to calm the user.

## Design and privacy decisions
Only timing is measured, not the identity of keys pressed. All information is stored on the device. Cursor coordinates are recorded - this may need further exploration.

## Data collected
Over the course of one day (around 7.7 hours), around 18,000 events, with 20ms mouse sampling.

## What I observed
Long idle gaps, particularly for key presses. Also observed mouse movements without key presses during gaming with a controlpad.

## Problems I hit and fixed
Over the first day of testing I found that the logger had ran twice for the entire day, corrupting the data, so I implemented a lock system to prevent this in the future.

## Limitations
The data collected this week is largely to show that this works. The data is from one person, on one day, with relatively little activity.

## Next steps
Self-report prompts, windowed features, baselines.