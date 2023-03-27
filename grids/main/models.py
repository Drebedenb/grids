from django.db import models


class PriceWinguardMain(models.Model):
    price_winguard_sketch_id = models.IntegerField()
    salary = models.IntegerField()
    price_b2c = models.IntegerField()
    price_b2b = models.IntegerField()
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'price_winguard_main'


class PriceWinguardFiles(models.Model):
    price_winguard_FilesType_id = models.IntegerField()
    price_winguard_sketch_id = models.IntegerField()
    path = models.CharField(max_length=255)

    class Meta:
        db_table = 'price_winguard_files'