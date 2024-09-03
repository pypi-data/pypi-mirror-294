# Generated by Django 4.0.7 on 2022-11-06 16:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("eveonline", "0016_character_names_are_not_unique"),
        ("eveuniverse", "0007_evetype_description"),
        ("miningtaxes", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AdminCharacter",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "eve_character",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="miningtaxes_admin_character",
                        to="eveonline.evecharacter",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "default_permissions": (),
            },
        ),
        migrations.CreateModel(
            name="AdminMiningObservers",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("obs_id", models.BigIntegerField()),
                ("obs_type", models.CharField(max_length=32)),
                ("name", models.CharField(max_length=32)),
                ("sys_name", models.CharField(max_length=32)),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mining_obs",
                        to="miningtaxes.admincharacter",
                    ),
                ),
            ],
            options={
                "default_permissions": (),
            },
        ),
        migrations.CreateModel(
            name="Character",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "eve_character",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="miningtaxes_character",
                        to="eveonline.evecharacter",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "default_permissions": (),
            },
        ),
        migrations.CreateModel(
            name="Settings",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "phrase",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=10,
                        verbose_name="Keyword (case sensitive) that must be present in the donation reason to be counted. Leave blank/empty to count all donations regardless of reason.",
                    ),
                ),
                (
                    "tax_R64",
                    models.FloatField(
                        default=10.0, verbose_name="Tax for Moon R64 Ore as a percent"
                    ),
                ),
                (
                    "tax_R32",
                    models.FloatField(
                        default=10.0, verbose_name="Tax for Moon R32 Ore as a percent"
                    ),
                ),
                (
                    "tax_R16",
                    models.FloatField(
                        default=10.0, verbose_name="Tax for Moon R16 Ore as a percent"
                    ),
                ),
                (
                    "tax_R8",
                    models.FloatField(
                        default=10.0, verbose_name="Tax for Moon R8 Ore as a percent"
                    ),
                ),
                (
                    "tax_R4",
                    models.FloatField(
                        default=10.0, verbose_name="Tax for Moon R4 Ore as a percent"
                    ),
                ),
                (
                    "tax_Gasses",
                    models.FloatField(
                        default=10.0, verbose_name="Tax for Gasses as a percent"
                    ),
                ),
                (
                    "tax_Ice",
                    models.FloatField(
                        default=10.0, verbose_name="Tax for Ice as a percent"
                    ),
                ),
                (
                    "tax_Mercoxit",
                    models.FloatField(
                        default=10.0, verbose_name="Tax for Mercoxit Ore as a percent"
                    ),
                ),
                (
                    "tax_Ores",
                    models.FloatField(
                        default=10.0, verbose_name="Tax for Regular Ore as a percent"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrePrices",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("buy", models.FloatField()),
                ("sell", models.FloatField()),
                ("updated", models.DateTimeField()),
                (
                    "eve_type",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="eveuniverse.evetype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CharacterUpdateStatus",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_success",
                    models.BooleanField(db_index=True, default=None, null=True),
                ),
                ("content_hash_1", models.CharField(default="", max_length=32)),
                ("content_hash_2", models.CharField(default="", max_length=32)),
                ("content_hash_3", models.CharField(default="", max_length=32)),
                ("last_error_message", models.TextField()),
                (
                    "root_task_id",
                    models.CharField(
                        db_index=True,
                        default="",
                        help_text="ID of update_all_characters task that started this update",
                        max_length=36,
                    ),
                ),
                (
                    "parent_task_id",
                    models.CharField(
                        db_index=True,
                        default="",
                        help_text="ID of character_update task that started this update",
                        max_length=36,
                    ),
                ),
                (
                    "started_at",
                    models.DateTimeField(db_index=True, default=None, null=True),
                ),
                (
                    "finished_at",
                    models.DateTimeField(db_index=True, default=None, null=True),
                ),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="update_status_set",
                        to="miningtaxes.character",
                    ),
                ),
            ],
            options={
                "default_permissions": (),
            },
        ),
        migrations.CreateModel(
            name="CharacterTaxCredits",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField(db_index=True)),
                ("credit", models.FloatField(default=0.0)),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tax_credits",
                        to="miningtaxes.character",
                    ),
                ),
            ],
            options={
                "default_permissions": (),
            },
        ),
        migrations.CreateModel(
            name="CharacterMiningLedgerEntry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(db_index=True)),
                ("quantity", models.PositiveIntegerField()),
                ("raw_price", models.FloatField(default=0.0)),
                ("refined_price", models.FloatField(default=0.0)),
                ("taxed_value", models.FloatField(default=0.0)),
                ("taxes_owed", models.FloatField(default=0.0)),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mining_ledger",
                        to="miningtaxes.character",
                    ),
                ),
                (
                    "eve_solar_system",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="eveuniverse.evesolarsystem",
                    ),
                ),
                (
                    "eve_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="eveuniverse.evetype",
                    ),
                ),
            ],
            options={
                "default_permissions": (),
            },
        ),
        migrations.CreateModel(
            name="AdminMiningObsLog",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(db_index=True)),
                ("miner_id", models.BigIntegerField()),
                ("quantity", models.PositiveIntegerField()),
                ("observer_type", models.CharField(max_length=32)),
                (
                    "eve_solar_system",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="eveuniverse.evesolarsystem",
                    ),
                ),
                (
                    "eve_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="eveuniverse.evetype",
                    ),
                ),
                (
                    "observer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mining_log",
                        to="miningtaxes.adminminingobservers",
                    ),
                ),
            ],
            options={
                "default_permissions": (),
            },
        ),
        migrations.CreateModel(
            name="AdminMiningCorpLedgerEntry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField(db_index=True)),
                ("taxed_id", models.BigIntegerField()),
                ("amount", models.FloatField(default=0.0)),
                ("reason", models.CharField(max_length=32)),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="corp_ledger",
                        to="miningtaxes.admincharacter",
                    ),
                ),
            ],
            options={
                "default_permissions": (),
            },
        ),
        migrations.AddConstraint(
            model_name="characterupdatestatus",
            constraint=models.UniqueConstraint(
                fields=("character",),
                name="functional_pk_miningtaxes_charactersyncstatus",
            ),
        ),
        migrations.AddConstraint(
            model_name="charactertaxcredits",
            constraint=models.UniqueConstraint(
                fields=("character", "date", "credit"),
                name="functional_pk_miningtaxes_charactertaxes",
            ),
        ),
        migrations.AddConstraint(
            model_name="characterminingledgerentry",
            constraint=models.UniqueConstraint(
                fields=("character", "date", "eve_solar_system", "eve_type"),
                name="functional_pk_mt_characterminingledgerentry",
            ),
        ),
        migrations.AddConstraint(
            model_name="adminminingobslog",
            constraint=models.UniqueConstraint(
                fields=("observer", "date", "miner_id", "eve_type"),
                name="functional_pk_mt_adminMiningLog",
            ),
        ),
        migrations.AddConstraint(
            model_name="adminminingobservers",
            constraint=models.UniqueConstraint(
                fields=("obs_id",), name="functional_pk_mt_adminMiningObs"
            ),
        ),
        migrations.AddConstraint(
            model_name="adminminingcorpledgerentry",
            constraint=models.UniqueConstraint(
                fields=("character", "date", "taxed_id"),
                name="functional_pk_mt_admincorpledger",
            ),
        ),
    ]
