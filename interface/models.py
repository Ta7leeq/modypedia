from django.db import models

# Create your models here.

class Fach(models.Model):
    Name=models.CharField(null=True,blank=True,max_length=100)
    
    def __str__(self):
        return  f"{self.Name}, {self.pk}"


#from django.contrib.postgres.fields import JSONField

class Author(models.Model):
    author_name = models.CharField(max_length=50, unique=True, null=True,blank=True)

    def __str__(self):
        return self.author_name

class Platform(models.Model):
    platform_name = models.CharField(max_length=50, unique=True, null=True,blank=True)

    def __str__(self):
        return self.platform_name
    



    
class Domain(models.Model):
    domain_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.domain_name
    
class Field(models.Model):
    field_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.field_name
    
class Branch(models.Model):
    branch_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.branch_name
    
class Area(models.Model):
    area_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.area_name
    
class Topic(models.Model):
    topic_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.topic_name
    
class Section(models.Model):
    section_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.section_name

    
class Aspect(models.Model):
    aspect_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.aspect_name

    
    
class Item(models.Model):
    ITEM_TYPES = [
        ('Contact', 'Contact'),
        ('Article', 'Article'),
        ('Book', 'Book'),
        ('Quote', 'Quote'),
        ('Equation', 'Equation'),
        ('Code', 'Code'),
        ('Project', 'Project'),
        ('Task', 'Task'),
        ('Presentation', 'Presentation'),
        ('Research Paper', 'Research Paper'),
        ('Place', 'Place'),
        ('Post', 'Post'),
        ('Journal Entry', 'Journal Entry'),
        ('Report', 'Report'),
        ('Manual', 'Manual'),
        ('Guide', 'Guide'),
        ('Diagram', 'Diagram'),
        ('Image', 'Image'),
        ('Video', 'Video'),
        ('Audio', 'Audio'),
        ('Spreadsheet', 'Spreadsheet'),
        ('Dataset', 'Dataset'),
        ('Note', 'Note'),
        ('Email', 'Email'),
        ('Letter', 'Letter'),
        ('Survey', 'Survey'),
        ('Form', 'Form'),
        ('Resume', 'Resume'),
        ('Cover Letter', 'Cover Letter'),
        ('Policy Document', 'Policy Document'),
        ('Procedure', 'Procedure'),
        ('Contract', 'Contract'),
        ('Invoice', 'Invoice'),
        ('Receipt', 'Receipt'),
        ('Meeting Minutes', 'Meeting Minutes'),
        ('Agenda', 'Agenda'),
        ('Newsletter', 'Newsletter'),
        ('Brochure', 'Brochure'),
        ('Flyer', 'Flyer'),
        ('Press Release', 'Press Release'),
        ('Announcement', 'Announcement'),
        ('Memo', 'Memo'),
        ('White Paper', 'White Paper'),
        ('Case Study', 'Case Study'),
        ('Technical Specification', 'Technical Specification'),
        ('Blueprint', 'Blueprint'),
        ('Map', 'Map'),
        ('Flowchart', 'Flowchart'),
        ('Storyboard', 'Storyboard'),
        ('Mind Map', 'Mind Map'),
        ('Checklist', 'Checklist'),
        ('To-Do List', 'To-Do List'),
        ('Calendar Event', 'Calendar Event'),
        ('Log', 'Log'),
        ('Schedule', 'Schedule'),
        ('Plan', 'Plan'),
        ('Strategy', 'Strategy'),
        ('Proposal', 'Proposal'),
        ('Quote (Sales)', 'Quote (Sales)'),
        ('Order', 'Order'),
        ('Shipping Document', 'Shipping Document'),
        ('Warranty', 'Warranty'),
        ('User Feedback', 'User Feedback'),
        ('Bug Report', 'Bug Report'),
        ('Feature Request', 'Feature Request'),
        ('Interview', 'Interview'),
        ('Transcript', 'Transcript'),
        ('Speech', 'Speech'),
        ('Biography', 'Biography'),
        ('Autobiography', 'Autobiography'),
        ('Review', 'Review'),
        ('Critique', 'Critique'),
        ('Opinion', 'Opinion'),
        ('Editorial', 'Editorial'),
        ('Recipe', 'Recipe'),
        ('Menu', 'Menu'),
        ('Blog Post', 'Blog Post'),
        ('Web Page', 'Web Page'),
        ('Forum Post', 'Forum Post'),
        ('Social Media Post', 'Social Media Post'),
        ('Message', 'Message'),
        ('Comment', 'Comment'),
        ('Forum Thread', 'Forum Thread'),
        ('Webinar', 'Webinar'),
        ('Online Course', 'Online Course'),
        ('Training Material', 'Training Material'),
        ('Certification', 'Certification'),
        ('License', 'License'),
        ('Patents', 'Patents'),
        ('Trademark', 'Trademark'),
        ('Copyright', 'Copyright'),
        ('Legal Document', 'Legal Document'),
        ('Regulation', 'Regulation'),
        ('Standard', 'Standard'),
        ('Code of Conduct', 'Code of Conduct'),
        ('Guideline', 'Guideline'),
        ('FAQ', 'FAQ'),
        ('Help Document', 'Help Document'),
        ('Support Ticket', 'Support Ticket'),
        ('Troubleshooting Guide', 'Troubleshooting Guide'),
    ]


    item_type = models.CharField(max_length=50, choices=ITEM_TYPES)
    title = models.CharField(max_length=2000)
    content = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True,default="Mody")
    fPlatform = models.ForeignKey(Platform, on_delete=models.CASCADE, blank=True, null=True)
    
    platform = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    
    

    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, blank=True, null=True)
    field = models.ForeignKey(Field, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True) 
    area = models.ForeignKey(Area, on_delete=models.CASCADE, blank=True, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True, null=True)
    aspect = models.ForeignKey(Aspect, on_delete=models.CASCADE, blank=True, null=True)

    tags = models.CharField(max_length=255, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    init_time  =  models.DateField(null=True, blank=True)
    last_time  = models.DateField(null=True, blank=True)
    next_time  = models.DateField(null=True, blank=True)
    
    hide_time = models.CharField(max_length=255, blank=True, null=True)
    
    #additional_info = JSONField(blank=True, null=True)

    def __str__(self):
        return  f"{self.title} ({self.item_type}) by {self.author} last_time {self.last_time}"



  
class Tag(models.Model):
    tag_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag_name


class ItemTag(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('item', 'tag')

    def __str__(self):
        return f"{self.item.title} - {self.tag.tag_name}"


class Relationship(models.Model):
    RELATIONSHIP_TYPES = [
        ('related to', 'Related to'),
        ('cited by', 'Cited by'),
        ('part of', 'Part of'),
        # Add more types as needed
    ]

    item1 = models.ForeignKey(Item, related_name='relationship_item1', on_delete=models.CASCADE)
    item2 = models.ForeignKey(Item, related_name='relationship_item2', on_delete=models.CASCADE)
    relationship_type = models.CharField(max_length=50, choices=RELATIONSHIP_TYPES)

    def __str__(self):
        return f"{self.item1.title} {self.relationship_type} {self.item2.title}"