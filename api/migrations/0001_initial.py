# Generated by Django 3.1.6 on 2021-03-18 14:01

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('color', models.CharField(max_length=10, null=True)),
                ('is_geo_transmitting_permitted', models.BooleanField(default=False)),
                ('is_notifying_permitted', models.BooleanField(default=False)),
                ('image_file_thumb', models.TextField(null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BudgetCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('color', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=5, null=True)),
                ('size', models.PositiveIntegerField()),
                ('upload_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('file_path', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('create_date', models.DateField(default=django.utils.timezone.now)),
                ('invite_id', models.CharField(max_length=75, null=True, unique=True)),
                ('image_file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='api.file')),
                ('user_creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user_member_list', models.ManyToManyField(related_name='group_list', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMapPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('description', models.TextField(null=True)),
                ('deadline_datetime', models.DateTimeField(null=True)),
                ('status', models.CharField(max_length=20, null=True)),
                ('create_date', models.DateField(default=django.utils.timezone.now)),
                ('is_task', models.BooleanField(default=False)),
                ('file_list', models.ManyToManyField(related_name='_task_file_list_+', to='api.File')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_list', to='api.group')),
                ('user_creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user_responsible_list', models.ManyToManyField(related_name='_task_user_responsible_list_+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subtask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('description', models.TextField(null=True)),
                ('deadline_datetime', models.DateTimeField(null=True)),
                ('status', models.CharField(max_length=20, null=True)),
                ('create_date', models.DateField(default=django.utils.timezone.now)),
                ('file_list', models.ManyToManyField(related_name='_subtask_file_list_+', to='api.File')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtask_list', to='api.task')),
                ('user_creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user_responsible_list', models.ManyToManyField(related_name='_subtask_user_responsible_list_+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MapPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(null=True)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('create_date', models.DateField(default=django.utils.timezone.now)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='map_point_list', to='api.group')),
                ('image_file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='api.file')),
                ('user_creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='file_list', to='api.group'),
        ),
        migrations.AddField(
            model_name='file',
            name='user_uploader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='file_list', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(null=True)),
                ('event_datetime', models.DateTimeField()),
                ('notify_datetime', models.DateTimeField(null=True)),
                ('create_date', models.DateField(default=django.utils.timezone.now)),
                ('file_list', models.ManyToManyField(related_name='_event_file_list_+', to='api.File')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_list', to='api.group')),
                ('map_point', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_list', to='api.mappoint')),
                ('user_creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChatUserSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_unread_messages', models.IntegerField(default=0)),
                ('is_notifying', models.BooleanField(default=True)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_user_settings', to='api.chat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_text', models.BooleanField()),
                ('text', models.TextField(null=True)),
                ('send_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_message_list', to='api.chat')),
                ('file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='api.file')),
                ('user_sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='chat',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_list', to='api.group'),
        ),
        migrations.AddField(
            model_name='chat',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='api.file'),
        ),
        migrations.AddField(
            model_name='chat',
            name='user_member_list',
            field=models.ManyToManyField(related_name='_chat_user_member_list_+', through='api.ChatUserSettings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='BudgetItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=16)),
                ('is_income', models.BooleanField()),
                ('payment_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('category_list', models.ManyToManyField(related_name='_budgetitem_category_list_+', to='api.BudgetCategory')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budget_item_list', to='api.group')),
                ('user_payer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='image_file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='api.file'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
