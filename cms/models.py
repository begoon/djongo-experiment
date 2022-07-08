from djongo import models


class Client(models.Model):
    class Meta:
        db_table = 'clients'
        managed = False

    id = models.fields.ObjectIdField(db_column='_id')
    platform = models.CharField(max_length=1024)
    manufacturer = models.CharField(max_length=1024)
    name = models.CharField(max_length=1024)
    model = models.CharField(max_length=1024)
    os_version = models.CharField(max_length=1024)
    app_version = models.CharField(max_length=1024)
    sdk_version = models.CharField(max_length=1024)
    client_id = models.CharField(max_length=1024)
    public_key = models.CharField(max_length=4096)
    app_id = models.CharField(max_length=1024)

    def __str__(self):
        return f'{self.client_id}/{self.name}'


class Bootstrap(models.Model):
    class Meta:
        db_table = 'bootstraps'
        managed = False

    id = models.fields.ObjectIdField(db_column='_id')
    camera = models.JSONField()
    matching = models.JSONField()
    tracking = models.JSONField()
    client_id = models.CharField(max_length=1024)

    def __str__(self):
        return self.client_id


class GroupKey(models.Model):
    class Meta:
        db_table = 'group_keys'
        managed = False

    id = models.fields.ObjectIdField(db_column='_id')
    group_id = models.CharField(max_length=1024)
    group_key = models.CharField(max_length=1024)

    def __str__(self):
        return f'{self.group_key}/{self.group_id}'


class Ticket(models.Model):
    class Meta:
        db_table = 'tickets'
        managed = False

    id = models.fields.ObjectIdField(db_column='_id')
    group_id = models.CharField(max_length=1024)
    user_id = models.CharField(max_length=1024)
    times_validated = models.JSONField()
    times_rejected = models.JSONField()
    biometric_data = models.CharField(max_length=1024 * 8)

    tag = models.CharField(max_length=1024)
    biometric_type = models.CharField(max_length=1024)
    display_data = models.JSONField()
    display_name = models.CharField(max_length=1024)

    objects = models.DjongoManager()

    def __str__(self):
        return f'{self.group_id}/{self.user_id}/{self.display_name}'
