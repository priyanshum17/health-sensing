# Assignment Details

## Objective

In this assignment, you will test and record the sensing limits of a person.  
The goal is to build a practical understanding of the capabilities and limitations of human sensory organs.

The focus is on:

- Sight
- Hearing

## Required Tests

### Sight

#### 1. Greyscale resolution

Compare two similar shades of gray by using one color for text and the other for the background.

- Start from high contrast (pure black and white reference).
- Reduce the contrast until the difference is no longer visible.
- Record the threshold as a percentage of greyscale range.
- Use this threshold to estimate bit resolution.

Example: 9-bit resolution gives 512 levels, roughly about 2% per distinguishable step.

#### 2. Angular field of view

With your head upright and fixed:

- Move a high-contrast marker toward visual field edges.
- Measure disappearance threshold in four directions: left, right, up, down.
- Eye movement is allowed; head tilt/turn is not.
- Report horizontal and vertical FOV in degrees.

#### 3. Smallest noticeable size

Display several lines with equal thickness and spacing (`t = d`).

- Increase distance between eyes and screen until exact line count is no longer distinguishable.
- Record that threshold distance.
- Use thickness and distance to calculate angular resolution.
- Report in arc minutes (`1 arcmin = 1/60 degree`).

Hint: Thickness can be measured physically or derived from screen dimensions and resolution.

Approximation: angular resolution is related to `t / distance`.

### Hearing

#### 4. Pitch frequency range

- Play a slow frequency sweep from 20 Hz to 20 kHz.
- Record the highest frequency that is still audible.
- Target at least 100 Hz precision.

#### 5. Sound gap detection

- Play a continuous sound with a silence gap inserted in the middle.
- Vary gap duration.
- Find and report the smallest noticeable gap.
- Report in milliseconds.

#### 6. Amplitude threshold

Use two tones of the same frequency (example: 440 Hz) separated by a short silence.

- First tone: baseline amplitude.
- Second tone: slightly louder or quieter.
- Reduce amplitude difference until louder/quieter judgment is no longer reliable.
- Record the smallest detectable amplitude change (dB).

Repeat at three baseline levels:

- Quiet
- Normal listening
- Moderately loud but comfortable

Control requirements:

- Keep device volume fixed.
- Adjust loudness only within the app.
- Use a relatively quiet environment.
- Do not increase volume to uncomfortable levels.
