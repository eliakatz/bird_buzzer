# Smart Scarecrow (bird_buzzer)
Bird's classification using ML.

My first real-world ML project from the idea to a product.
The Smart scarecrow classifies the birds by the frequencies of their sounds, in order to decide whether to drive them away (dove, crow, myna) or not (sunbird).

It has two parts: The 'brain' and the 'body'.

The 'brain' (the algorithm):

Training stage: 

* The training of the models is done using audio samples from www.xeno-canto.org.
* Part of the samples were processed with Audacity (reducing background noise, cutting silent parts, duplicating sounds in too short samples).
* Converts mp3 files to wav for processing.
* Create spectrograms and extracts the loudest frequencies.
* Runs the models.

Real-life stage:
* Runs the selected model on the data captured by the Raspberry Pi.

The 'body' (Raspberry Pi with a microphone and LEDs simulating 'Activate a buzzer' (red LED) and 'Do nothing' (blue LED).

Real-life stage:
* Captures the sounds with the microphone.
* (The 'brain' runs the model).
* Activates the LED according to the result.




