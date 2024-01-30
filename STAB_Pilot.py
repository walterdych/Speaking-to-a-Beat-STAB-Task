# -*- Endcoding: utf-8 -*-

#################### Speaking to a Beat (STAB) Task ####################
# This script presents a series of sentences to the participant. 
# Each sentence is presented in time with a metronome sound.
# The participant is asked to read each sentence aloud in time with the metronome.
# The script records the participant's voice while they are reading the sentences.
# The script also logs the participant's voice and the time at which each sentence was presented.

# @Author: Walter P. Dych 
# @Affiliation: State University of New York at Binghamton
# @Email: walterpdych@gmail.com

# @Last Modified by: Walter P. Dych
# @Last Modified time: 29-01-2024
########################################################################

from psychopy import visual, core, event, gui, data, sound, prefs, monitors
from psychopy import logging as psychoLog
from psychopy.hardware import keyboard
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import datetime
import time
prefs.hardware['audioLib'] = ['PTB', 'pygame', 'pyo', 'sounddevice']

###### Variables ######
# Define the BPM (beats per minute) set by the experimenter
bpm = 115
word_duration = 60 / bpm
today = datetime.datetime.now().strftime("%m-%d-%Y")
sample_rate = 44100  # Sample rate in Hz
recording_duration = 71  # Duration in seconds

###### Participant Dialog Box ######
# Add dialog fields
dlg = gui.Dlg(title='Participant Information')
dlg.addField('Participant #')
dlg.addField('Condition #')
dlg.show()
participant_number = dlg.data[0]
condition_number = dlg.data[1]
date = today
recording_filename = f"STAB_{participant_number}_COND{condition_number}_{date}.wav"

###### Create an experiment logger ######
psychoLog.console.setLevel(psychoLog.DATA) 
# Create logger file name based on participant information
psychoLog.data("Participant Number: {}".format(participant_number))
psychoLog.data("Condition Number: {}".format(condition_number))
psychoLog.data("Date: {}".format(date))
logger_filename = f"data/STAB_{participant_number}_COND{condition_number}_{date}.log"
psychoLog.setDefaultClock(core.Clock())
log_file = psychoLog.LogFile(logger_filename, level=psychoLog.DATA, filemode='w')  # Create a log file

###### Create a window ######
# Define the display monitor
mon = monitors.Monitor('testMonitor')
mon.setDistance(57)  # Distance from the monitor in cm
mon.setWidth(34)  # Width of the monitor in cm
mon.setSizePix([1920, 1080])  # Screen resolution
mon.save()

# Create a window
win = visual.Window(
    size=[1280, 1080], 
    units="pix", 
    fullscr=False, 
    color=[0, 0, 0],
    name="SPEAKING TO A BEAT Task"
)

###### Functions ######
def check_for_pause_or_quit(log_file=log_file, win=win):
    keys = event.getKeys()
    if 'p' in keys:
        pause_text = visual.TextStim(win, text="Paused. Press 'P' to resume.", height=30)
        pause_text.draw()
        win.flip()
        print("Participant paused the experiment.")
        psychoLog.data("Participant paused the experiment.")
        event.waitKeys(keyList=['p'])
        print("Participant resumed the experiment.")
        psychoLog.data("Participant resumed the experiment.")

    if 'q' in keys:
        psychoLog.data("Quitting the experiment...")
        psychoLog.data('Experiment ended at {}'.format(core.getTime()))
        core.quit()

###### Stimuli ######
# Define the sentences to be used in the experiment
sentences = [
    "Brightly colored birds swiftly fly across clear skies.",
    "Ancient forests house countless species unknown to science.",
    "Innovative designs often lead to unexpected, remarkable outcomes.",
    "Musical rhythms can influence emotions in profound ways.",
    "Starry nights inspire poets and scientists alike deeply.",
    "Complex algorithms decode patterns in vast data sets.",
    "Robust debates foster critical thinking and intellectual growth.",
    "Elegant equations often unveil truths about the universe.",
    "Cultural diversity enriches societies in numerous, vibrant ways.",
    "Effective communication bridges gaps between diverse communities globally."
]

# Metronome sound
metronome = sound.Sound('stimuli/metronome.wav')
sd.rec(int(recording_duration * sample_rate), samplerate=sample_rate, channels=1, blocking=False)


###### Istruction Screen######
# Create text stimulus for instructions
instruction_text = visual.TextStim(
    win=win,
    text="Welcome to the experiment! Please follow the instructions carefully. Press 'SPACE' to continue.",
    pos=(0, 0),
    color=[1, 1, 1],
    height=30
)
# Draw the instruction text on the window
instruction_text.draw()
win.flip()
event.waitKeys(keyList=["space"])

###### Entrainment Phase ######
# Play the metronome sound for 4 bars for entrainment phase
for _ in range(16):
    entrainment_text = visual.TextStim(
    win=win,
    text="In this phase, you will hear a metronome sound.",
    pos=(0, 0),
    color=[1, 1, 1],
    height=30
    )
    check_for_pause_or_quit()
    metronome.play()
    psychoLog.data("Tick!")
    entrainment_text.draw()
    win.flip()
    time.sleep(word_duration)

###### Sentence Presentation Phase ######  
# Assuming you have a window created named 'win'
pause_text = visual.TextStim(win, text="Paused. Press 'P' to resume.")
# Iterate through each sentence
for sentence in sentences:
    sentence_number = 0
    words = sentence.split()
    # Iterate through each word
    for word in words:
        check_for_pause_or_quit()
        # Metronome Stimulus
        metronome.play()
        # Log metroome stimulus
        psychoLog.data("Tick!")
        # Create text stimulus for the word
        word_text = visual.TextStim(
            win=win,
            text=word,
            pos=(0, 0),
            color=[1, 1, 1],
            height=30
        )
        
        # Draw the word on the window
        word_text.draw()
        # Log word
        psychoLog.data(word)
        win.flip()
        time.sleep(word_duration)
    
    # Rest phase
    for _ in range(8):
        check_for_pause_or_quit()
        metronome.play()
        psychoLog.data("Tick!")
        rest_text = visual.TextStim(
            win=win,
            text='Rest',
            pos=(0, 0),
            color=[1, 1, 1],
            height=30
        )
        rest_text.draw()
        psychoLog.data("Rest")
        win.flip()
        time.sleep(word_duration)
    sentence_number += 1  # Increment the sentence number
    # Log sentence number
    psychoLog.data("Sentence Number: {}".format(sentence_number))

##### CLEANUP #####
sd.stop()
win.close()
psychoLog.data('Experiment ended at {}'.format(core.getTime()))
core.quit()
