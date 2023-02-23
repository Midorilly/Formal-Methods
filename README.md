# Process Mining with Pm4Py
Process mining is a set of techniques and tools to extract non-trivial and useful information from event logs. Specifically, information about processes is recorded by information systems, which include business processes, enterprise systems, automation and control systems, medical systems, daily activities, IoT devices, and social networks, among others.
One of the main aspects of process mining is control-flow discovery: given an event log containing a set of traces, it involves automatically discovering and visualising the actual process performed by constructing a suitable process model. Hence, a good example of a process model are Petri nets. 
Algorithms such as the α-algorithm construct a process model based on identifying characteristic patterns in the event log; an example of pattern is a situation in which one activity always follows another).

This case study aims to detect the weekly routine of a traked subject based on the event log obtained by sesnors. Specifically, this goal has been achieved using [pm4py](https://pm4py.fit.fraunhofer.de/), an open-source Python library for process mining. PM4Py involves tools used for data preparation, process discovery, conformance checking, as well as performance analysis.

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
As we can observe above, some ```detected_activities``` contain more than one activity in a single string. We decided to modify the dataset so that each row would contain only one activity. To this end, we first formatted the dataset on Microsoft Excel by removing the square brackets and the punctuation by employing a regular expression. We added three new columns to the dataset, ```activity_1```, ```activity_2``` and ```activity_3```, since we observed that ```detected_activities``` contained three activities at most; we then proceeded to split in the respective columns the eventual detected activities containing more than one activity. Below is the resulting new dataset, ```dataset/split_kasteren.csv```.
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
To further simplify the dataset we decided to keep only one activity per row. The code written for these accomodations can be found at ```src/pm.ipynb```. First and foremost, we read the ```split_kasteren.csv``` using the [pandas](https://pandas.pydata.org/) library. 
```
df = pd.read_csv("split_pm_output.csv", parse_dates=["timestamp"])
```
Since not every row contains more than one activity, their ```activity_2``` and ```activity_3``` fields were automatically set to **NaN** by Microsoft Excel. In order to work with strings only, NaN values have been replaced with the character ```e```, indicating that the corresponding field is empty. 

```
df = df.replace(np.nan, 'e')
```
Now that ```activity_1```, ```activity_2``` and ```activity_3``` fields contain strings only, we can further split the activities. We create a new dataframe with a different header: every row can have one corresponding ```activity``` only; additionally, we split ```timeframe``` in two more fields, ```date``` and ```time```, too.
```
split_df.to_csv('split_kasteren_activity.csv', header = ['timestamp', 'date', 'time', 'sensor', 'action', 'event', 'pattern', 'activity'])
```
The splitting algorithm is the following: 
- if a row in the initial dataframe ```df``` has non-empty ```activity_3```, we replicate it thrice so that the ```activity``` field of the new dataframe ```split_df``` contains the values of ```activity_1```, ```activity_2``` and ```activity_3``` respectively;
- if a row in ```df``` has non-empty ```activity_2``` and empty ```activity_3```, we add it to  ```split_df``` twice: the ```activity``` field contains the values of ```activity_1``` and ```activity_2```; similarly;
- finally, if a ```df``` row has non-empty ```activity_1``` field only, it is straightaway duplicated in ```split_df```.

We write this new dataframe to ```dataset/split_kasteren_activity.csv```. Below is an example of how a row having three activities has been split.

```
timestamp,date,time,sensor,action,event,pattern,activity_1,activity_2,activity_3
2008-12-07 01:03:30,2008-12-07,01:03:30,ToiletDoorDownstairs,ToiletDoorDownstairs,ON,Pat_154,Relax,UseToiletDownstairs,LeaveHouse
```

**split_df:**
```
timestamp,date,time,sensor,action,event,pattern,activity
2008-12-07 01:03:30,2008-12-07,01:03:30,ToiletDoorDownstairs,ToiletDoorDownstairs,ON,Pat_154,Relax
2008-12-07 01:03:30,2008-12-07,01:03:30,ToiletDoorDownstairs,ToiletDoorDownstairs,ON,Pat_154,UseToiletDownstairs
2008-12-07 01:03:30,2008-12-07,01:03:30,ToiletDoorDownstairs,ToiletDoorDownstairs,ON,Pat_154,LeaveHouse
```
Our dataset is now ready for one last step; since we aim to model a Petri Network for each day of the week, we extract from the entire dataset seven subsets, one for each day of the week. As we mentioned earlier, these data have been gathered between November 19th and December 8th, 2008, thus we have
- Mondays: 24-11, 01-12, 08-12
- Tuesdays: 25-11, 02-12
- Wednesdays: 19-11, 26-11, 03-12
- Thurdays: 20-11, 27-11, 04-12
- Fridays: 21-11, 28-11, 05-12
- Saturdays: 22-11, 29-11, 06-12
- Sundays: 23-11, 30-11, 07-12

We established that the daily routine starts at 7:00:00 of the day in question and ends at 6:59:59 of the next day. For example, here is how we extract the user's routine.
```
monday = pd.DataFrame(columns = ['timestamp', 'sensor', 'action', 'event', 'pattern', 'activity'], index=range(0,3695))
m24 = pd.Timestamp('2008-11-24 07:00:00')
m25 = pd.Timestamp('2008-11-25 06:59:59')
m01 = pd.Timestamp('2008-12-01 07:00:00')
m02 = pd.Timestamp('2008-12-02 06:59:59')
m08 = pd.Timestamp('2008-12-08 07:00:00')
m09 = pd.Timestamp('2008-12-09 06:59:59')
m = 0
for i in range(len(dataset)):
    if (dataset.loc[i, 'timestamp'] >= m24 and dataset.loc[i, 'timestamp'] <= m25) or (dataset.loc[i, 'timestamp'] >= m01 and dataset.loc[i, 'timestamp'] <= m02) or (dataset.loc[i, 'timestamp'] >= m08 and dataset.loc[i, 'timestamp'] <= m09):
        monday.iloc[m] = pd.Series({'timestamp': dataset.loc[i, 'timestamp'], 'sensor': dataset.loc[i, 'sensor'], 'action': dataset.loc[i, 'action'], 'event': dataset.loc[i, 'event'], 'pattern': dataset.loc[i, 'pattern'], 'activity': dataset.loc[i, 'activity']})
        m += 1
```
By observing the code we understand that the *Mondays routine* starts on Monday 24th at 07:00:00 and ends on Tuesday 25th at 06:59:59.

## Petri Nets Discovering
Petri nets are a graphical representation of a system that models the flow of data, events, or resources between different components or entities. Since the goal of this case study is detecting the weekly routine of a subject, Petri nets play a fundamental role to achieve it. 
Specifically, we expect seven Petri nets, one for each day of the week.

We can distinguish between two main phases:
    - training phase, during which we obtain seven Petri nets, each based on the respective train dataset;
    - testing phase, during which we check the predictive performances of the previously obtained Petri nets.

### Training Phase
In this phase, the pre-processed data is used to train Petri nets. This involves using algorithms to learn the structure and parameters of the model based on the observed behavior of the system.

In other words, for each day of the week, the respective dataset needs to be read into a pandas dataframe, which is an essential step in order to use the methods provided by PM4Py library. The following is a general exmaple of code.
```
day_df = pd.read_csv("day.csv", parse_dates=["timestamp"])

daydf = pd.DataFrame(monday_df, columns=['id', 'timestamp', 'date', 'time', 'sensor', 'action', 'event', 'pattern', 'activity'])

day_df = pm4py.format_dataframe(daydf, case_id='timestamp', activity_key='activity', timestamp_key='timestamp')
```

Then, this dataframe needs to be converted into an event log, which is then used by the alpha miner algorithm to discover the Petri net.
```
event_log = pm4py.convert_to_event_log(monday_df)

net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(event_log)

```

### Testing Phase
The testing phased involves to test the obtained Petri nets on the respective testing dataset in order to evalute their predictive performance. Hence, this involves using the model to make predictions about the behavior of the system based on new data, and comparing the predicted behavior to the actual behavior observed in the new data.

## Results


## Conclusions





