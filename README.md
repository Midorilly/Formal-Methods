# Process Mining with pm4py
DESCRIPTION OF PROCESS MINING

pm4py is an open source Python library that supports process mining algorithms.

## Dataset
The employed dataset is the result of the Human Activity Recognition for Intelligent Environments [study](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8423051) of Gorka Azkune and Aitor Almeida, University of Deusto. This paper presents a scalable and hybrid AR system called *HARS*, Hybrid Activity Recognition System, designed to work in dense sensing-based monitoring scenarios, where activities are inferred by monitoring human-object interactions through the usage of multiple sensors. This system is based on four core concepts
 - Sensor Activation: a sensor is activated when it changes its state from *no-interaction* state to *interaction* state and vice-versa; 
 - Action: actions constituite the primitives of activities; they are detected by sensors, thus sensor activations can be mapped to actions;
 - Activity: activities are a sequence of action executed with a common purpose in a specific location, at a given time and with a given duration.
 - *EAM*: Expert Activity Models are knowledge-based computational models able to recognise which activities are beign performed in a certain action pattern. These models encapsulate the prior knowledge of how an activity is performed in terms of 
    - Actions: the minimum number of actions typically executed to perform a given activity;
    - Duration: an estimate of the typical duration of a given activity;
    - Starting Time: approximate time ranges when a given activity is usually started;
    - Location: semantic tags for the places where a given activity is usually peformed.

EAM aims to represent a generic activity with minimum knowledge, instead of a detailed activity for a given person. This makes EAM flexible enough to be applied to several and diverse activity executions; furthermore, EAMs simplicity allows domain experts to easily design descriptive models without using complex techniques.

HARS is divided into two main modules:
 - *APD*: Action Pattern Discovery, which extracts frequent action sequences representig specific executions of activities. Its input data are (i) unlabelled dataset of sensor activation for a given users and (ii) sensor-action mappings. The pattern mining algorithm is iterated until no new pattern can be found. Finally, APD returns a dataset of actions tagged with the corresponding pattern;
 - *PMM*: Pattern-Model Matching algorithm, its purpose is to discover the activities for a given action pattern and a set of EAMs. PMM, taking in input the labelled dataset of actions previously discovered by APD and a set of EAMs for a given user, aims at matching the best set of EAMs to a certain action pattern, which may be composed by several activities, one activity or 'None', a lable used for idle or unknown activities. The algorithm returns a set of detected activities for each action pattern.

Our [initial dataset](https://github.com/aitoralmeida/c4a_activity_recognition/blob/master/experiments/kasterenC_dataset/pm_output.csv) inclueds six features: Timestamp, Sensor Activation, Action, Event, Pattern, Detected Activities
   