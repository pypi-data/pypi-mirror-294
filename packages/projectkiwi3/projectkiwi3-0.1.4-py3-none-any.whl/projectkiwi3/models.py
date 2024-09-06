from pydantic import BaseModel
from typing import List, Optional



# model Imagery {
#   id             Int                    @id @default(autoincrement())
#   sub            String
#   name           String
#   projectId      Int
#   createdAt      DateTime               @default(now())
#   ready          Boolean                @default(false)
#   error          Boolean                @default(false)
#   project        Project                @relation(fields: [projectId], references: [id], onDelete: Cascade)
#   storageSizeKB  Int?
#   labelingQueues LabelingQueueImagery[]
#   modifiedAt DateTime @default(now())
#   reconstruction ReconstructionEntry?
# }

class Imagery(BaseModel):
    id: int
    sub: str
    name: str
    createdAt: str
    ready: bool
    error: bool
    storageSizeKB: Optional[int]
    modifiedAt: str
    downloadUrl: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):

        return cls(
            id = data['id'],
            sub = data['sub'],
            name = data['name'],
            createdAt = data['createdAt'],
            ready = data['ready'],
            error = data['error'],
            storageSizeKB = data['storageSizeKB'],
            modifiedAt = data['modifiedAt'],
        )
    

# model LabelingTask {
#   id              Int              @id @default(autoincrement())
#   labelingQueueId Int
#   complete        Boolean          @default(false)
#   completedBy     String?
#   labelingQueue   LabelingQueue    @relation(fields: [labelingQueueId], references: [id], onDelete: Cascade)
#   taskCoordinates TaskCoordinate[]
# }
class LabelingTask(BaseModel):

    id: int
    complete: bool
    completedBy: Optional[str]
    coordinates: List[List[float]] # [[lng, lat], [lng,lat]]

    @classmethod
    def from_dict(cls, data: dict):
        coords = []
        for coord in data['taskCoordinates']:
            coords.append([coord['lng'], coord['lat']])
        return cls(
            id = data['id'],
            complete = data['complete'],
            completedBy = data['completedBy'],
            coordinates = coords
        )
    
    
    

# model LabelingQueue {
#   id                   Int                    @id @default(autoincrement())
#   name                 String?
#   projectId            Int
#   createdBy            String
#   project              Project                @relation(fields: [projectId], references: [id], onDelete: Cascade)
#   labelingQueueImagery LabelingQueueImagery[]
#   labelingTasks        LabelingTask[]
#   modifiedAt DateTime @default(now())
# }
class LabelingQueue(BaseModel):

    id: int
    name: Optional[str] = None
    createdBy: str
    modifiedAt: str
    labelingTasks: List[LabelingTask]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id = data['id'],
            name = data['name'],
            createdBy = data['createdBy'],
            modifiedAt = data['modifiedAt'],
            labelingTasks = [LabelingTask.from_dict(dict) for dict in data['labelingTasks']]
        )
    






# model Label {
#   id          Int          @id @default(autoincrement())
#   name        String
#   color       String
#   projectId   Int
#   active      Boolean      @default(true)
#   annotations Annotation[]
#   project     Project      @relation(fields: [projectId], references: [id], onDelete: Cascade)
#   modifiedAt DateTime @default(now())
# }
class Label(BaseModel):

    id: int
    name: str
    color: str
    active: bool
    modifiedAt: str
    

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id = data['id'],
            name = data['name'],
            color = data['color'],
            active = data['active'],
            modifiedAt = data['modifiedAt']
        )


# model Annotation {
#   id          Int          @id @default(autoincrement())
#   sub         String
#   projectId   Int
#   shape       String
#   createdAt   DateTime     @default(now())
#   confidence  Float        @default(1)
#   labelId     Int
#   label       Label        @relation(fields: [labelId], references: [id], onDelete: Cascade)
#   project     Project      @relation(fields: [projectId], references: [id], onDelete: Cascade)
#   coordinates Coordinate[]
#   modifiedAt DateTime @default(now())
# }
class Annotation(BaseModel):

    id: int
    sub: str
    shape: str
    createdAt: str
    confidence: float
    labelId: int
    label: Label
    coordinates: List[List[float]] # [[lng, lat], [lng,lat]]


    @classmethod
    def from_dict(cls, data: dict):
        coords = []
        for coord in data['coordinates']:
            coords.append([coord['lng'], coord['lat']])
        return cls(
            id = data['id'],
            sub = data['sub'],
            shape = data['shape'],
            createdAt = data['createdAt'],
            confidence = data['confidence'],
            labelId = data['labelId'],
            label = Label.from_dict(data['label']),
            coordinates = coords
        )
    
# model Project {
#   id              Int              @id @default(autoincrement())
#   name            String
#   createdAt       DateTime         @default(now())
#   owner           String
#   annotations     Annotation[]
#   deletedAnnotations DeletedAnnotation[]
#   images          Image[]
#   deletedImages DeletedImage[]
#   imagery         Imagery[]
#   deletedImagery DeletedImagery[]
#   labels          Label[]
#   labelingQueues  LabelingQueue[]
#   previousProject MigratedProject?
#   members         ProjectMember[]
#   projectShares   ProjectShare[]
#   modifiedAt DateTime @default(now())
# }
class Project(BaseModel):

    id: int
    name: str
    createdAt: str
    modifiedAt: str
    owner: str
    labels: List[Label]
    

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id = data['id'],
            name = data['name'],
            createdAt = data['createdAt'],
            modifiedAt = data['modifiedAt'],
            owner = data['owner'],
            labels = [Label.from_dict(labelDict) for labelDict in data['labels']]
        )

    





# class Annotation(BaseModel):  
#     shape: str
#     label_id: int
#     coordinates: List[List[float]]
#     url: Optional[str]
#     imagery_id: Optional[str]
#     confidence: Optional[float]
#     id: Optional[int]
#     label_name: Optional[str]
#     label_color: Optional[str]

#     @classmethod
#     def from_dict(cls, data: dict, annotation_id: int = None):
#         coordinates = []
#         for point in data['coordinates']:
#             coordinates.append([float(point[0]), float(point[1])])

        
#         imagery_id = data['imagery_id']
#         if imagery_id == "NULL":
#             imagery_id = None

#         confidence = data['confidence']
#         if confidence == "NULL":
#             confidence = None
        
#         if annotation_id is None:
#             annotation_id = int(data['id'])

        
#         return cls(
#             id = annotation_id,
#             shape = data['shape'],
#             label_id = data['label_id'],
#             label_name = data['label_name'],
#             label_color = data['label_color'],
#             coordinates = coordinates,
#             url = data['url'],
#             imagery_id = data['imagery_id'],
#             confidence=confidence
#         )
    
#     def geoJSON(self) -> str:
#         """Convert the annotation to a geoJSON string

#         Returns:
#             str: geoJSON representation

#         Example:

#             >>>
#         """

#         geojson = {
#             "type": "Feature",
#             "geometry": {
#                 "type": self.shape,
#                 "coordinates": self.coordinates
#             },
#             "properties": {
#                 "label_id": self.label_id
#             }
#         }

#         if self.confidence is not None:
#             geojson['properties']['confidence'] = self.confidence
        
#         if self.label_name is not None:
#             geojson['properties']['name'] = self.label_name

#         return json.dumps(geojson)






# class Project(BaseModel):
#     name: str
#     id: str
#     user_login: str

#     @classmethod
#     def from_dict(cls, data: dict):

#         return cls(
#             name = data['name'],
#             id = data['project_id'],
#             user_login = data['user_login']
#         )

# class ImageryLayer(BaseModel):
#     id: str
#     project: str
#     name: str
#     url: str
#     attribution: str
#     size_mb: Optional[float]
#     bounds: Optional[List[float]]
#     min_zoom: Optional[int]
#     max_zoom: Optional[int]
#     status: Optional[str]

# class Tile(BaseModel):
#     zxy: str
#     imagery_id: str
#     url: str
#     z: int
#     x: int
#     y: int


#     @classmethod
#     def from_zxy(cls, 
#             zxy: str, 
#             imagery_id: str, 
#             url: str):
#         z = int(zxy.split("/")[0])
#         x = int(zxy.split("/")[1])
#         y = int(zxy.split("/")[2])

#         return cls(
#             zxy=zxy,
#             imagery_id=imagery_id,
#             url=url,
#             z=z,
#             x=x,
#             y=y
#         )



# class Task(BaseModel):
#     complete: bool
#     id: int
#     imagery_id: str
#     queue: int
#     submitter_login: Optional[str]
#     zxy: str


# class Label(BaseModel):
#     id: Optional[int]
#     project_id: str
#     color: str
#     name: str
#     status: str

