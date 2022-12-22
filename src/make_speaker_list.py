import os 
import json
import random
# Path to the directory containing the speaker files
speark_path = 'VAS Experimental Stimuli'
reliability_path = 'Reliability VAS'
reliability_files = [f for f in os.listdir(reliability_path) if f.endswith('.wav')]
speakers = list(set(range(1,18)) - set([2,13]))
expiriment_cycle = ['X1','X2','Y2']
num_listeners = 30

data = []
for l in range(1,num_listeners+1):
    random.shuffle(speakers)
   
    listener_data = []
    for speaker in speakers:
        random.shuffle(expiriment_cycle)
        filenames_1 =[f'{expiriment_cycle[0]}_P{speaker}_{counter}.wav' for counter in range(1,4)]
        filenames_2 =[ f"{expiriment_cycle[1]}_P{speaker}_{counter}.wav" for counter in range(1,4)]
        filenames_3 =[ f"{expiriment_cycle[2]}_P{speaker}_{counter}.wav" for counter in range(1,4)]
        listener_data.append({'speaker':speaker, 'expiriment_cycle': str(expiriment_cycle), 'filenames_1': filenames_1, 'filenames_2': filenames_2, 'filenames_3': filenames_3})
    data.append({'listener':l,'speakers': str(speakers), 'data':listener_data, 'reliability':reliability_files})
    


json.dump(data, open('speaker_list.json','w'),indent=4)
