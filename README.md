# Process Mining with Pm4Py
Process mining is a set of techniques and tools to extract non-trivial and useful information from event logs. Specifically, information about processes is recorded by information systems, which include business processes, enterprise systems, automation and control systems, medical systems, daily activities, IoT devices, and social networks, among others.

One of the main aspects of process mining is control-flow discovery: given an event log containing a set of traces, it involves automatically discovering and visualising the actual process performed by constructing a suitable process model. A process model describes the behaviour seen in the log; a good example is a Petri net. 
Algorithms such as the α-algorithm construct a process model based on identifying characteristic patterns in the event log; an example of a pattern is a situation in which one activity always follows another).

[pm4py](https://pm4py.fit.fraunhofer.de/) is an open source Python library for process mining. PM4Py involves tools used for data preparation, process discovery, conformance checking, as well as performance analysis.
It can be installed using pip, a package installer for Python:
```
pip install pm4py
```

## Hybrid Activity Recognition System: an overview
The employed dataset is the result of the Human Activity Recognition for Intelligent Environments [study](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8423051) of Gorka Azkune and Aitor Almeida, University of Deusto. The paper presents a scalable and hybrid AR system called *HARS*, Hybrid Activity Recognition System, designed to work in dense sensing-based monitoring scenarios, where activities are inferred by monitoring human-object interactions through the usage of multiple sensors. This system is based on four core concepts
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

## Dataset manipulation
Our [initial dataset](https://github.com/aitoralmeida/c4a_activity_recognition/blob/master/experiments/kasterenC_dataset/pm_output.csv) inclueds six features: ```timestamp```, ```sensor```, ```action```, ```event```, ```pattern```, ```detected_activities```. It contains 22,700 observations gathered in the timeframe going from November 19th to December 8th, 2008. The frame below shows the first ten rows of our dataset. 
```
timestamp,sensor,action,event,pattern,detected_activities
2008-11-19 22:47:46,Frontdoor,Frontdoor,ON,Pat_15,[u'LeaveHouse']
2008-11-19 22:49:20,Frontdoor,Frontdoor,ON,Pat_15,[u'LeaveHouse']
2008-11-19 22:49:24,Frontdoor,Frontdoor,ON,Pat_15,[u'LeaveHouse']
2008-11-19 22:50:18,Frontdoor,Frontdoor,ON,Pat_15,[u'LeaveHouse']
2008-11-19 22:51:02,ToiletDoorDownstairs,ToiletDoorDownstairs,ON,Pat_158,"[u'UseToiletDownstairs', u'GetSnack']"
2008-11-19 22:51:04,ToiletDoorDownstairs,ToiletDoorDownstairs,ON,Pat_158,"[u'UseToiletDownstairs', u'GetSnack']"
2008-11-19 22:51:49,ToiletDoorDownstairs,ToiletDoorDownstairs,ON,Pat_158,"[u'UseToiletDownstairs', u'GetSnack']"
2008-11-19 22:52:17,ToiletFlushDownstairs,ToiletFlushDownstairs,ON,Pat_158,"[u'UseToiletDownstairs', u'GetSnack']"
2008-11-19 22:59:12,PlatesCupboard,PlatesCupboard,ON,Pat_158,"[u'UseToiletDownstairs', u'GetSnack']"
2008-11-19 22:59:53,Fridge,Fridge,ON,Pat_38,[u'GetSnack']
```
As we can observe above, some ```detected_activities``` contain more than one activity in a single string. We decided to modify the dataset so that each row would contain only one activity. To this end, we first formatted the dataset on Microsoft Excel by removing the square brackets and the punctuation by employing a regular expression. We added three new columns to the dataset, ```activity_1```, ```activity_2``` and ```activity_3```, since we observed that ```detected_activities``` contained three activities at most; we then proceeded to split in the respective columns the eventual detected activities containing more than one activity. Below is the resulting new dataset, ```dataset/split_pm_output.csv```.
```
timestamp,date,time,sensor,action,event,pattern,activity_1,activity_2,activity_3
2008-11-19 22:47:46,2008-11-19,22:47:46,Frontdoor,Frontdoor,ON,Pat_15,LeaveHouse,,
2008-11-19 22:49:20,2008-11-19,22:49:20,Frontdoor,Frontdoor,ON,Pat_15,LeaveHouse,,
2008-11-19 22:49:24,2008-11-19,22:49:24,Frontdoor,Frontdoor,ON,Pat_15,LeaveHouse,,
2008-11-19 22:50:18,2008-11-19,22:50:18,Frontdoor,Frontdoor,ON,Pat_15,LeaveHouse,,
2008-11-19 22:51:02,2008-11-19,22:51:02,ToiletDoorDownstairs,ToiletDoorDownstairs,ON,Pat_158,UseToiletDownstairs,GetSnack,
2008-11-19 22:51:04,2008-11-19,22:51:04,ToiletDoorDownstairs,ToiletDoorDownstairs,ON,Pat_158,UseToiletDownstairs,GetSnack,
2008-11-19 22:51:49,2008-11-19,22:51:49,ToiletDoorDownstairs,ToiletDoorDownstairs,ON,Pat_158,UseToiletDownstairs,GetSnack,
2008-11-19 22:52:17,2008-11-19,22:52:17,ToiletFlushDownstairs,ToiletFlushDownstairs,ON,Pat_158,UseToiletDownstairs,GetSnack,
2008-11-19 22:59:12,2008-11-19,22:59:12,PlatesCupboard,PlatesCupboard,ON,Pat_158,UseToiletDownstairs,GetSnack,
2008-11-19 22:59:53,2008-11-19,22:59:53,Fridge,Fridge,ON,Pat_38,GetSnack,,
```
To further simplify the dataset we decided to keep only one activity per row. The code written for these accomodations can be found at ```src/pm.ipynb```. First and foremost, we read the ```split_pm_output.csv``` using the [pandas](https://pandas.pydata.org/) library. 
```
df = pd.read_csv("split_pm_output.csv", parse_dates=["timestamp"])
```
Since not every row contains more than one activity, their ```activity_2``` and ```activity_3``` fields were automatically set to **NaN** by Microsoft Excel. In order to work with strings only, NaN values have been replaced with the character ```e```, indicating that the corresponding field is empty. 

```
df = df.replace(np.nan, 'e')
```
Now that ```activity_1```, ```activity_2``` and ```activity_3``` fields contain strings only, we can further split the activities. We create a new dataframe with a different header: every row can have one corresponding ```activity``` only; additionally, we split ```timeframe``` in two more fields, ```date``` and ```time```, too.
```
split_df.to_csv('out.csv', header = ['timestamp', 'date', 'time', 'sensor', 'action', 'event', 'pattern', 'activity'])
```


- ```activity_3 != 'e'``` means that the pattern consists of three activities; we duplicate the corresponding row two times, one containing the value of 

## Petri Nets
The employed dataset is the result of the Human Activity Recognition for Intelligent Environments [study](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8423051) of Gorka Azkune and Aitor Almeida, University of Deusto. The paper presents a scalable and hybrid AR system called *HARS*, Hybrid Activity Recognition System, designed to work in dense sensing-based monitoring scenarios, where activities are inferred by monitoring human-object interactions through the usage of multiple sensors. This system is based on four core concepts
 - Sensor Activation: a sensor is activated when it changes its state from *no-interaction* state to *interaction* state and vice-versa; 
 - Action: actions constitui