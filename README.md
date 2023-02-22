# Smart Scarecrow (bird_buzzer)
Bird's classification using ML.

My first real-world ML project from the idea to a product. Winner in a project competition (data science category).

The Smart scarecrow classifies the birds by the frequencies of their sounds, in order to decide whether to drive them away (dove, crow, myna) or not (sunbird).

It has two parts: The 'brain' and the 'body'.

## The 'brain' (the algorithm):
The algorithm has two stages: Training (training the models), and real-life (processing the captured sounds with the chosen model).

### Training stage: 

* The training of the models is done using audio samples from www.xeno-canto.org.
* Part of the samples were processed with Audacity (reducing background noise, cutting silent parts, duplicating sounds in too short samples).
* Converts mp3 files to wav for processing.
* Create spectrograms and extracts the loudest frequencies.
* Runs the models.

### Real-life stage:
* Runs the selected model on the data captured by the Raspberry Pi.

## The 'body' 
Raspberry Pi (RPi) with a microphone and LEDs simulating 'Activate a buzzer' (red LED) and 'Do nothing' (blue LED).

### Real-life stage:
* Captures the sounds with the microphone.
* (The 'brain' runs the model).
* Activates the LED according to the result.


## Files:

* `bird_buzzer.ipynb`: The code for training the models.
* `bird_buzzer.pdf` contains the notebook code with the outputs (to see the output without running the Jupyter notebook).
* `scarecrow.py`: The code on the RPi to capture the sound, run the pre-trained model, and activate the LEDs.
