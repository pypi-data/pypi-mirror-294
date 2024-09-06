# Projectkiwi3 Client

This package adds a basic python interface for the projectkiwi api. 

### Installation
```
pip install projectkiwi3
```


### Getting Started

Retrieve your projectkiwi API key here: https://projectkiwi.io/developer
```python
import projectkiwi3

client = projectkiwi3.Client("YOUR_API_KEY")

# list all our projects
projects = client.getProjects()
```

<br />

---

<br />

#### Reading Annotations
```python
project = projects[0]

# get current annotations
annotations = client.getAnnotations(project.id)
```

#### Adding Annotations
```python
# get labels
newLabel = client.addLabel(project.id, "demo label", "rgb(3, 186, 252)")

# create new annotation
newAnnotation = client.addAnnotation(
    project.id, 
    coordinates=[[-123.4, 56.789012]], 
    shape="Point", 
    labelId=newLabel.id
    confidence=1.0
)

print(newAnnotation)
# id=553971 sub='google-oauth2|115859123295676188590' shape='Point' createdAt='2024-09-05T18:47:17.529Z' confidence=1.0 labelId=3 label=Label(id=3, name='demo label', color='rgb(3, 186, 252)', active=True, modifiedAt='2024-07-15T20:29:59.697Z') coordinates=[[-123.4, 56.789012]]
```

<br />

---

<br />

#### Working with labeling Queues
Labeling Queues allow us to break up larger labeling tasks in to bite size portions, easily digestible for both humans and GPUs.
```python
import matplotlib.pyplot as plt

# list out all labeling queues in the project
labelingQueues = client.getLabelingQueues(project.id)

# let's just pick out the latest one
labelingQueue = labelingQueues[-1]

# find imagery layer to use - every geotiff you upload creates an imagery layer
imageryLayer = client.getImagery(project.id)[-1]

# Preview an image for a single task within the labeling queue
task = labelingQueue.labelingTasks[-1]
img = client.getImageForTask(imageryLayer, task.coordinates)
plt.imshow(img)
plt.show()
```

![preview image](imgs/imgPreview.png "Preview Image")
