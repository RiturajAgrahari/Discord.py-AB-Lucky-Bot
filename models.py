from tortoise.models import Model
from tortoise import fields
from datetime import datetime


class Profile(Model):
    id = fields.BigIntField(primary_key=True)
    discord_name = fields.CharField(max_length=225, null=True)
    discord_id = fields.CharField(max_length=225, null=True)
    bot_used = fields.IntField(null=True, default=0)


class BotUsage(Model):
    id = fields.BigIntField(primary_key=True)
    date = fields.DatetimeField(auto_now_add=True, default=datetime.utcnow())
    fandom_bot = fields.IntField(default=0)
    lucky_bot = fields.IntField(default=0)
    rpg_bot = fields.IntField(default=0)


class Review(Model):
    id = fields.BigIntField(primary_key=True)
    uid = fields.ForeignKeyField("models.Profile", related_name="reviews", on_delete=fields.CASCADE)
    review = fields.TextField(null=True)
    star_rating = fields.IntField(null=True)
    reviewed_on = fields.DatetimeField(auto_now_add=True)


class TodayLuck(Model):
    id = fields.IntField(primary_key=True)
    uid = fields.ForeignKeyField("models.Profile", related_name="luck", on_delete=fields.CASCADE)
    location = fields.CharField(max_length=225, null=True)
    container = fields.CharField(max_length=225, null=True)
    weapon = fields.CharField(max_length=225, null=True)
    item = fields.CharField(max_length=225, null=True)
    summary = fields.TextField(null=True)


if __name__ == "__main__":
    print(datetime.utcnow())