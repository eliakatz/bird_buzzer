# Smart Scarecrow (bird_buzzer)
Bird's classification using ML.

My first real-world ML project from the idea to a product.
The Smart scarecrow classifies the birds by the frequencies of their sounds, in order to decide whether to drive them away (dove, crow, myna) or not (sunbird).

It has two parts: The 'brain' and the 'body'.

The 'brain' (the algorithm):

Training stage: 

* The trainig of the models is done using audio samples from www.xeno-canto.org.
* Part of the sampls were processed with Audacity (reducing background noise, cutting silent parts, duplicating sounds in too short samples).

It converts mp3 files to wav for processing.



The next stage is to activate a buzzer through Arduino or Raspberry PI.

The mp3 files are located in the zipped folders.

21/12/22

https://app.pitch.com/app/presentation/f90d90a4-5e02-46ca-9dae-2801875257a9/d0150cbf-8d8a-4fbe-88be-f1a8729603fe
