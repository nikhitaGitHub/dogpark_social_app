from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from dogpark.constants import charLen256, charLen100
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

#Table to hold owner information
class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    num_dogs = models.IntegerField(default=0)
    checked_in = models.BooleanField(default=False)

#Table to hold dog information
class Dog(models.Model):
    GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    #dog breeds from keneel club
    BREED_CHOICES = (
            (1,'Barbet'),
            (2, 'Bracco Italiano'), 
            (28, 'Retriever (Curly Coated)'),
            (3, 'Braque D\'Auvergne'),
            (29, 'Retriever (Golden)'),
            (4, 'Brittany'),
            (30, 'Retriever (Flat Coated)'), 
            (5, 'English Setter'),
            (31, 'Retriever (Labrador)'),
            (6, 'German Longhaired Pointer'),
            (32, 'Retriever (Nova Scotia Duck Tolling)'),
            (7, 'German Shorthaired Pointer'),
            (33, 'Slovakian Rough Haired Pointer'),
            (8, 'German Wirehaired Pointer'),
            (34, 'Small Munsterlander'),
            (9, 'Gordon Setter'),
            (35,'Spaniel (American Cocker)'),
            (10, 'Hungarian Vizsla'),
            (36, 'Spaniel (American Water)'),
            (11, 'Hungarian Wire Haired Vizsla'),
            (37, 'Spaniel (Clumber)'),
            (12, 'Irish Red and White Setter'),
            (38, 'Spaniel (Cocker)'),
            (13, 'Irish Setter'),
            (39, 'Spaniel (English Springer)'),
            (14, 'Italian Spinone'),
            (40, 'Spaniel (Field)'),
            (15, 'Korthals Griffon'),
            (41, 'Spaniel (Irish Water)'),
            (16, 'Lagotto Romagnolo'),
            (42, 'Spaniel (Sussex)'),
            (17, 'Large Munsterlanderb'),
            (43, 'Spaniel (Welsh Springer)'),
            (18, 'Pointer'),
            (44, 'Spanish Water Dog'),
            (19, 'Portuguese Pointer'),
            (45, 'Weimaraner'),
            (20, 'Afghan Hound'),
            (46, 'Dachshund (Wire Haired)'),
            (21, 'Azawakh'),
            (47, 'Deerhound'),
            (22, 'Basenji'),
            (48, 'Finnish Spitz'),
            (23, 'Basset Bleu De Gascogne'),
            (24, 'Foxhound'),
            (25, 'Basset Fauve De Bretagne'),
            (26, 'Grand Bleu De Gascogne'),
            (27, 'Retriever (Chesapeake Bay)'),
            (49, 'Basset Griffon Vendeen (Grand)'),
            (50, 'Greyhound'),
            (51, 'Basset Griffon Vendeen (Petit)'),
            (52, 'Griffon Fauve De Bretagne'),
            (53, 'Basset Hound'),
            (54, 'Hamiltonstovare'),
            (55, 'Bavarian Mountain Hound'),
            (56, 'Ibizan Hound'),
            (57, 'Beagle'),
            (58, 'Irish Wolfhound'),
            (59, 'Black & Tan Coonhound'),
            (60, 'Norwegian Elkhound'),
            (61, 'Bloodhound'),
            (62, 'Otterhound'),
            (63, 'Borzoi'),
            (64, 'Pharaoh Hound'),
            (65, 'Cirneco Dell\'Etna'),
            (66, 'Portuguese Podengo'),
            (67, 'Dachshund (Long Haired)'),
            (68, 'Rhodesian Ridgeback'),
            (69, 'Sloughi'),
            (70, 'Dachshund (Miniature Wire Haired)'),
            (71, 'Whippet'),
            (72, 'Dachshund (Smooth Haired)'),	 
            (73, 'Anatolian Shepherd Dog'),
            (74, 'Hungarian Pumi'),
            (75, 'Australian Cattle Dog	Komondor'),
            (76, 'Australian Shepherd'),
            (77, 'Lancashire Heeler'),
            (78, 'Bearded Collie'),
            (79, 'Maremma Sheepdog'),
            (80, 'Beauceron'),
            (81, 'Norwegian Buhund'),
            (82, 'Belgian Shepherd Dog (Groenendael)'),
            (83, 'Old English Sheepdog'),
            (84, 'Belgian Shepherd Dog (Laekenois)'),
            (85, 'Picardy Sheepdog'),
            (86, 'Belgian Shepherd Dog (Malinois)'),
            (87, 'Polish Lowland Sheepdog'),
            (88, 'Belgian Shepherd Dog (Tervueren)'),
            (89, 'Pyrenean Mountain Dog'),
            (90, 'Bergamasco'),
            (91, 'Pyrenean Sheepdog (Long Haired)'),
            (92, 'Border Collie'),
            (93, 'Pyrenean Sheepdog (Smooth Faced)'),
            (94, 'Briard'),
            (95, 'Samoyed'),
            (96, 'Catalan Sheepdog'),
            (97, 'Shetland Sheepdog'),
            (98, 'Collie (Rough)'),
            (99, 'Swedish Lapphund'),
            (100, 'Collie (Smooth)'),
            (101, 'Swedish Vallhund'),
            (102, 'Estrela Mountain Dog'),
            (103, 'Turkish Kangal Dog'),
            (104, 'Finnish Lapphund'),
            (105, 'Welsh Corgi (Cardigan)'),
            (106, 'German Shepherd Dog'),
            (107, 'Welsh Corgi (Pembroke)'),
            (108, 'Hungarian Kuvasz'),
            (109, 'White Swiss Shepherd Dog'),
            (110, 'Hungarian Puli'),
            (111, 'Akita'), 
            (112, 'Korean Jindo'),
            (113, 'Boston Terrier'),
            (114, 'Lhasa Apso'),
            (115, 'Bulldog'),
            (116, 'Miniature Schnauzer'),
            (117, 'Canaan Dog'),
            (118, 'Poodle (Miniature)'),
            (119, 'Chow Chow'),
            (120, 'Poodle (Standard)'),
            (121, 'Dalmatian'),
            (122, 'Poodle (Toy)'),
            (123, 'Eurasier'),
            (124, 'Schipperke'),
            (125, 'French Bulldog'),
            (126, 'Schnauzer'),
            (127, 'German Spitz (Klein)'),
            (128, 'Shar Pei'),
            (129, 'German Spitz (Mittel)'),
            (130, 'Shih Tzu'),
            (131, 'Japanese Akita Inu'),
            (132, 'Tibetan Spaniel'),
            (133, 'Japanese Shiba Inu'),
            (134, 'Tibetan Terrier'),
            (135, 'Japanese Spitz'),
            (136, 'Xoloitzcuintle (Mex Hairless) Int'),
            (137, 'Keeshond'),
            (138, 'Xoloitzcuintle (Mex Hairless) Min'),
            (139, 'Kooikerhondje'),
            (140, 'Xoloitzcuintle (Mex Hairless) Std'),
            (141, 'Affenpinscher'),
            (142, 'Italian Greyhound'),
            (143, 'Australian Silky Terrier'),
            (144, 'Japanese Chin'),
            (145, 'Bichon Frise'),
            (146, 'King Charles Spaniel'),
            (147,'Bolognese'),
            (148, 'Lowchen (Little Lion Dog)'),
            (149, 'Cavalier King Charles Spaniel'),
            (150, 'Maltese'),
            (151, 'Chihuahua (Long Coat)'),
            (152, 'Miniature Pinscher'),
            (153, 'Chihuahua (Smooth Coat)'),
            (154, 'Papillon'),
            (155, 'Chinese Crested'),
            (156, 'Pekingese'),
            (157, 'Coton De Tulear'),
            (158, 'Pomeranian'),
            (159, 'English Toy Terrier (Black & Tan)'),
            (160, 'Pug'),
            (161, 'Griffon Bruxellois'),
            (162, 'Russian Toy'),
            (163, 'Havanese'),
            (164, 'Yorkshire Terrier'),
            (165, 'Airedale Terrier'),
            (166, 'Kerry Blue Terrier'),
            (167, 'Australian Terrier'),
            (168, 'Lakeland Terrier'),
            (169, 'Bedlington Terrier'),
            (170, 'Manchester Terrier'),
            (171, 'Border Terrier'),
            (172, 'Norfolk Terrier'),
            (173, 'Bull Terrier'),
            (174, 'Norwich Terrier'),
            (175, 'Bull Terrier (Miniature)'),
            (176, 'Parson Russell Terrier'),
            (177, 'Cairn Terrier'),
            (178, 'Scottish Terrier'),
            (179, 'Cesky Terrier'),
            (180, 'Sealyham Terrier'),
            (181, 'Dandie Dinmont Terrier'),
            (182, 'Skye Terrier'),
            (183, 'Fox Terrier (Smooth)'),
            (184, 'Soft Coated Wheaten Terrier'),
            (185, 'Fox Terrier (Wire)'),
            (186, 'Staffordshire Bull Terrier'),
            (186, 'Glen of Imaal Terrier'),
            (187, 'Welsh Terrier'),
            (188, 'Irish Terrier'),
            (189, 'West Highland White Terrier'),
            (190, 'Jack Russell Terrier'),	 
            (191, 'Working'),
            (192, 'Alaskan Malamute'),
            (193, 'Greenland Dog'),
            (194, 'Bernese Mountain Dog'),
            (195, 'Hovawart'),
            (196, 'Bouvier Des Flandres'),
            (197, 'Leonberger'),
            (198, 'Boxer'),
            (199, 'Mastiff'),
            (200, 'Bullmastiff'),
            (201, 'Neapolitan Mastiff'),
            (202, 'Canadian Eskimo Dog'),
            (203, 'Newfoundland'),
            (204, 'Dobermann'),
            (205, 'Portuguese Water Dog'),
            (206, 'Dogue de Bordeaux'),
            (207, 'Pyrenean Mastiff'),
            (208, 'Entlebucher Mountain Dog'),
            (209, 'Rottweiler'),
            (210, 'German Pinscher'),
            (211, 'Russian Black Terrier'),
            (212, 'Giant Schnauzer'),
            (213, 'Siberian Husky'),
            (214, 'Great Dane'),
            (215, 'St. Bernard'),
            (216, 'Great Swiss Mountain Dog'),
            (217, 'Tibetan Mastiff')
            )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    breed = models.IntegerField(choices=BREED_CHOICES, default=1) 
    breedname = models.CharField(max_length=charLen256)
    name = models.CharField(max_length = charLen100)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    picture = models.ImageField(upload_to="dog_profile_picture", blank=True)
    def __str__(self):
        if(self.gender == "M"):
            return self.name + " is a " + self.breedname + " Male and is " + str(self.age) + " years old."
        else:
            return self.name + " is a " + self.breedname + " Female and is " + str(self.age) + " years old."
#Table to hold Friend Request information
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='the_sender',on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='the_receiver', on_delete=models.CASCADE)
    def __str__(self):
        return "request sent"
    
    class Meta:
        unique_together = (('sender', 'receiver'),)
#Table to hold Friendship information
class Friendship(models.Model):
    from_friend = models.ForeignKey(User, related_name="from_friend", on_delete=models.CASCADE)
    to_friend= models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return "Friend request accepted"
    
    class Meta:
        unique_together = (('from_friend', 'to_friend'),)
#Table to hold Events information        
class Events(models.Model):
    name = models.CharField(max_length=charLen256)
    date = models.DateField(default=datetime.date.today, blank=True, null=True)
    time = models.TimeField(auto_now=False, auto_now_add=False)

#Table to hold Goals information
class Goals(models.Model):
    description = models.CharField(max_length=charLen256)
    points_earned = models.IntegerField(default=0)

#Table to add goal to my goal for a user
class MyGoal(models.Model):
    goal = models.ForeignKey(Goals, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

#Table to mark a goal complete and so achieve it
class Achievement(models.Model):
    goal = models.ForeignKey(Goals, on_delete=models.CASCADE)
    created = models.DateField(default=datetime.date.today)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

#Table to hold rating information
class Ratings(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, 
                                 validators=[
                                     MaxValueValidator(5),
                                     MinValueValidator(0),
                                ])
    created = models.DateField(default=datetime.date.today)

#Table to store events a user wants to attend
class MyEvents(models.Model):
    myevent = models.ForeignKey(Events, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)