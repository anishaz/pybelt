from __future__ import unicode_literals

from django.db import models

import re
import bcrypt

# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[a-zA-Z]')


class UserManager(models.Manager):
    def login(self, data):
        errors = []

        try:
            user = self.get(username=data['username'])
            if bcrypt.hashpw(data['password'].encode('utf8'), user.password.encode('utf8')) == user.password.encode('utf8'):
                return {'user' : user}
            errors.append("Incorrect password")

        except:
            errors.append("Username not registered")
        return {'errors': errors}

    def registration(self, data):
        errors = []

        for field in data:
            if len(data[field]) == 0:
                errors.append(field + " cannot be blank. Please check and re-submit.")

        if len(data['first_name']) < 3:
            errors.append("First name cannot be less than 3 characters.")

        if len(data['last_name']) < 3:
            errors.append("Last name cannot be less than 3 characters.")

        if len(data['first_name']) > 3 and not NAME_REGEX.match(data['first_name']):
            errors.append("Invalid First Name. Name must only contain letters.")

        if len(data['last_name']) > 3 and not NAME_REGEX.match(data['last_name']):
            errors.append("Invalid Last Name. Name must only contain letters.")

        try:
            self.get(username=data['username'])
            errors.append("Username already registered")
        except:
            pass

        if not NAME_REGEX.match(data['username']):
                errors.append("Invalid Username. Please try again.")

        if len(data['password']) < 8:
                errors.append("Password cannot be less than 8 characters in length.")

        if not data['password'] == data['confirmPassword']:
                errors.append("Passwords must match.")

        if len(errors) != 0:
            return {'errors' : errors}

        data['password'] = bcrypt.hashpw(data['password'].encode('utf8'), bcrypt.gensalt())
        user = User.objects.create(first_name = data['first_name'], last_name = data['last_name'], username = data['username'], password = data['password'])
        return {'user' : user}

class User(models.Model):
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    username = models.CharField(max_length = 30)
    password = models.CharField(max_length = 255)
    date_hired = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
