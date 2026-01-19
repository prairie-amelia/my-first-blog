from django.conf import settings
from django.db import models
from django.utils import timezone


class Player(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Board(models.Model):
    arrangement = models.JSONField(default=list, blank=True)
    link = models.CharField(unique=True)
    password = models.CharField(blank=True, null=True)

class Word(models.Model):
    word_string = models.CharField(max_length=200)
    valid = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.word_string

class Word_Board(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, blank=True, null=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE,blank=True, null=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, blank=True, null=True)
