# multimedia-learning-eye-tracker
Some python scripts for eye-tracking data analysis associated with my MSc thesis.
- [Other related repository!](https://github.com/K-Hun/multimedia-learning-hci)
- Data have been collected via [EyeLink 1000 Plus](https://www.sr-research.com/eyelink-1000-plus).
- I have used some scripts from [Edf2Mat© Matlab Toolbox](https://github.com/uzh/edf-converter) to convert raw eye-tracking files into mat files.
- I tried to minimal Matlab coding, so I have used [The MATLAB Engine API for Python](https://www.mathworks.com/help/matlab/matlab-engine-for-python.html) for running the required MatLab scripts in python.
- I have also used [heatmappy](https://github.com/Matheus-1095/Heatmap) as a heatmap generator for my simulations.

# Features

  - Extracting eye-tracking features at any time Intervals of the task:
    * Saccade length
    * Pupil dilation
    * Fixation duration
    * Fixation rate
    * Saccade length
    * Saccade velocity
    * Blink rate
    * Blink latency
    * Microsaccade amplitude
    * Microsaccade rate
  - Some minor preprocessing
  - Image and video heatmap generator based gaze locations or fixation locations




### Todos

 - SeekBar for the simulations

License
----

MIT
